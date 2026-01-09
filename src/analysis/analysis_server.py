"""
Analysis MCP Server
Analyzes job descriptions using Ollama (Llama 3.1 8B)
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
import httpx
import json
import sqlite3
from typing import Dict, Any, List
import os

mcp = FastMCP("analysis_mcp")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
DB_PATH = "./data/databases/jobs.db"

# CRITICAL: Constrained system prompt to prevent hallucinations
ANALYSIS_SYSTEM_PROMPT = """You are a job description analyzer. Your task is to extract structured information.

CRITICAL RULES - NEVER VIOLATE:
1. ONLY extract information present in the job description
2. DO NOT invent or assume information
3. DO NOT add sections not requested
4. Return ONLY valid JSON

Extract the following from the job description:
- required_skills: List of required technical skills (e.g., ["Python", "TensorFlow", "AWS"])
- nice_to_have_skills: List of preferred/optional skills
- ats_keywords: Important keywords for ATS systems (unique terms that appear in JD)
- role_category: Type of role (e.g., "ML Engineer", "Backend Engineer", "Data Scientist")
- experience_level: Required experience (e.g., "Entry", "Mid", "Senior", "Lead")

Return as JSON only, no markdown, no explanations.
"""


class AnalyzeJDInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    job_id: str = Field(..., description="Job ID to analyze")


@mcp.tool(
    name="analyze_jd",
    annotations={
        "title": "Analyze Job Description",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def analyze_jd(params: AnalyzeJDInput) -> str:
    """
    Analyze job description using Ollama
    Returns structured analysis as JSON
    """
    try:
        # 1. Get job from database
        job = _get_job(params.job_id)
        if not job:
            return f"Error: Job {params.job_id} not found"

        # 2. Check if already analyzed
        existing_analysis = _get_analysis(params.job_id)
        if existing_analysis:
            return f"✓ Job already analyzed. Analysis: {json.dumps(existing_analysis, indent=2)}"

        # 3. Check if Ollama is accessible
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code != 200:
                    return "Error: Ollama is not running. Please start Ollama first: ollama serve"
        except Exception as e:
            return f"Error: Cannot connect to Ollama. Make sure it's running: {str(e)}"

        # 4. Prepare prompt
        prompt = f"{ANALYSIS_SYSTEM_PROMPT}\n\nJob Title: {job['title']}\nCompany: {job['company']}\n\nJob Description:\n{job['description']}"

        # 5. Call Ollama for analysis
        print(f"Analyzing job: {job['title']} at {job['company']}...")

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"  # Force JSON output
                }
            )

        # 6. Parse response
        ollama_result = response.json()
        analysis = json.loads(ollama_result["response"])

        # 7. Validate structure (prevent hallucinations)
        required_keys = ["required_skills", "nice_to_have_skills", "ats_keywords",
                        "role_category", "experience_level"]

        if not all(key in analysis for key in required_keys):
            return f"Error: Invalid analysis structure from AI. Missing required fields."

        # 8. Store analysis
        _store_analysis(params.job_id, analysis)

        return f"✓ Analysis complete for job {params.job_id}\n\n{json.dumps(analysis, indent=2)}"

    except httpx.TimeoutException:
        return "Error: Ollama request timed out. The model might be too slow or not loaded. Try: ollama run llama3.1:8b"
    except json.JSONDecodeError as e:
        return f"Error: Failed to parse AI response as JSON: {str(e)}"
    except Exception as e:
        return f"Error analyzing job: {str(e)}"


def _get_job(job_id: str) -> Dict:
    """Retrieve job from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def _get_analysis(job_id: str) -> Dict:
    """Check if job is already analyzed"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM job_analysis WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    analysis = dict(row)
    # Parse JSON fields
    analysis["required_skills"] = json.loads(analysis.get("required_skills", "[]"))
    analysis["nice_to_have_skills"] = json.loads(analysis.get("nice_to_have_skills", "[]"))
    analysis["ats_keywords"] = json.loads(analysis.get("ats_keywords", "[]"))

    return analysis


def _store_analysis(job_id: str, analysis: Dict) -> None:
    """Store analysis in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create analysis table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_analysis (
            analysis_id TEXT PRIMARY KEY,
            job_id TEXT,
            required_skills TEXT,
            nice_to_have_skills TEXT,
            ats_keywords TEXT,
            role_category TEXT,
            experience_level TEXT,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        )
    """)

    # Insert analysis
    cursor.execute("""
        INSERT OR REPLACE INTO job_analysis
        (analysis_id, job_id, required_skills, nice_to_have_skills,
         ats_keywords, role_category, experience_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        job_id,  # Use job_id as analysis_id
        job_id,
        json.dumps(analysis["required_skills"]),
        json.dumps(analysis["nice_to_have_skills"]),
        json.dumps(analysis["ats_keywords"]),
        analysis["role_category"],
        analysis["experience_level"]
    ))

    # Update job status
    cursor.execute("""
        UPDATE jobs
        SET status = 'analyzed'
        WHERE job_id = ?
    """, (job_id,))

    conn.commit()
    conn.close()


class ListAnalyzedJobsInput(BaseModel):
    """Input for listing analyzed jobs"""
    model_config = ConfigDict(extra='forbid')
    limit: int = Field(default=20, description="Maximum number of results")


@mcp.tool(
    name="list_analyzed_jobs",
    annotations={
        "title": "List Analyzed Jobs",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_analyzed_jobs(params: ListAnalyzedJobsInput) -> str:
    """
    List all analyzed jobs with their analysis
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT j.job_id, j.title, j.company, j.location,
                   ja.role_category, ja.experience_level
            FROM jobs j
            INNER JOIN job_analysis ja ON j.job_id = ja.job_id
            ORDER BY ja.analyzed_at DESC
            LIMIT ?
        """, (params.limit,))

        rows = cursor.fetchall()
        conn.close()

        results = [dict(row) for row in rows]

        return json.dumps({
            "count": len(results),
            "analyzed_jobs": results
        }, indent=2)

    except Exception as e:
        return f"Error listing analyzed jobs: {str(e)}"


def main():
    """Run the Analysis MCP server using stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
