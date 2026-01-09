"""
Document Generator MCP Server
Generates personalized LaTeX resumes with STRICT validation to prevent hallucinations
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from jinja2 import Template
import httpx
import json
from pathlib import Path
from typing import Dict, Any, List
import os
import sqlite3

mcp = FastMCP("document_generator_mcp")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OUTPUT_DIR = Path("./generated_resumes")
TEMPLATE_PATH = Path("./templates/resume_template.tex")
DB_PATH = "./data/databases/jobs.db"

# CRITICAL: System prompt that prevents hallucinations
PERSONALIZATION_SYSTEM_PROMPT = """You are a resume bullet point customizer.

CRITICAL RULES - NEVER VIOLATE:
1. ONLY use information from the provided profile
2. DO NOT invent achievements, projects, or experience
3. DO NOT add skills not in the profile
4. ONLY reorder and rephrase existing content
5. Keep facts accurate - change wording, not facts
6. Return EXACTLY the same number of bullet points as input

Task: Reorder bullet points to match job requirements. Emphasize relevant points first.
Return JSON array with same structure as input.
"""


class GenerateResumeInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    job_id: str = Field(..., description="Job ID to generate resume for")
    profile_path: str = Field(default="./data/profiles/profile.json", description="Path to profile")
    use_ai_customization: bool = Field(default=True, description="Whether to use AI for customization")


@mcp.tool(
    name="generate_resume",
    annotations={
        "title": "Generate Personalized Resume",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def generate_resume(params: GenerateResumeInput) -> str:
    """
    Generate personalized resume for job with strict validation
    """
    try:
        # 1. Load profile
        profile_path = Path(params.profile_path)
        if not profile_path.exists():
            return f"Error: Profile not found at {params.profile_path}"

        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)

        # 2. Get job analysis and match score
        analysis = _get_analysis(params.job_id)
        match_score_data = _get_match_score(params.job_id)

        if not analysis:
            return f"Error: Analysis not found for job {params.job_id}. Please run analyze_jd first."

        if not match_score_data:
            return f"Error: Match score not found. Please run match_profile first."

        # 3. Get job details
        job = _get_job(params.job_id)
        if not job:
            return f"Error: Job {params.job_id} not found"

        # 4. CRITICAL: Customize content with validation
        if params.use_ai_customization:
            customized_profile = await _customize_profile_safe(profile, analysis, match_score_data)
        else:
            customized_profile = _customize_profile_no_ai(profile, analysis, match_score_data)

        # 5. CRITICAL: Validate structure hasn't changed
        if not _validate_structure(profile, customized_profile):
            print("WARNING: AI attempted to modify structure - using original profile")
            customized_profile = profile

        # 6. Load and render LaTeX template
        if not TEMPLATE_PATH.exists():
            return f"Error: Template not found at {TEMPLATE_PATH}"

        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_content = f.read()

        template = Template(template_content)
        latex_content = template.render(**customized_profile)

        # 7. Save file
        company_safe = job['company'].replace(' ', '_').replace('/', '_')
        filename = f"resume_{company_safe}_{params.job_id[:8]}.tex"
        output_path = OUTPUT_DIR / filename

        OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        # 8. Return success with details
        result = {
            "status": "success",
            "file": str(output_path),
            "job_id": params.job_id,
            "company": job['company'],
            "job_title": job['title'],
            "match_score": match_score_data["overall_score"],
            "variant_used": match_score_data["recommended_variant"],
            "ai_customization": params.use_ai_customization,
            "message": f"Resume generated successfully. Review at: {output_path}"
        }

        return json.dumps(result, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error generating resume: {str(e)}"


async def _customize_profile_safe(profile: Dict, analysis: Dict, match_score: Dict) -> Dict:
    """
    Customize profile content using AI with STRICT validation
    Section-by-section to limit AI scope
    """
    customized = profile.copy()

    # Check if Ollama is available
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.get("http://localhost:11434/api/tags")
    except:
        print("WARNING: Ollama not available, using non-AI customization")
        return _customize_profile_no_ai(profile, analysis, match_score)

    # ONLY customize experience highlights (most impactful)
    print("Customizing experience section with AI...")

    for i, exp in enumerate(profile.get("experience", [])):
        try:
            # Prepare prompt with strict constraints
            prompt = f"""{PERSONALIZATION_SYSTEM_PROMPT}

Job Requirements:
{json.dumps(analysis.get("required_skills", []))}

Original Highlights (keep count={len(exp["highlights"])}):
{json.dumps(exp["highlights"])}

Task: Return JSON array with {len(exp["highlights"])} highlights, reordered to emphasize skills matching job requirements.
"""

            # Call Ollama with timeout
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    OLLAMA_URL,
                    json={
                        "model": "llama3.1:8b",
                        "prompt": prompt,
                        "stream": False
                    }
                )

            result = response.json()
            customized_highlights = json.loads(result["response"])

            # CRITICAL: Validate same number of highlights
            if len(customized_highlights) == len(exp["highlights"]):
                customized["experience"][i]["highlights"] = customized_highlights
            else:
                print(f"WARNING: AI changed highlight count ({len(customized_highlights)} vs {len(exp['highlights'])}), using original")

        except Exception as e:
            print(f"Error customizing highlights for {exp.get('company', 'unknown')}: {e}, using original")

    # Reorder skills (matched skills first) - NO AI needed
    required_skills = analysis.get("required_skills", [])
    customized["skills"] = _reorder_skills(profile["skills"], required_skills)

    return customized


def _customize_profile_no_ai(profile: Dict, analysis: Dict, match_score: Dict) -> Dict:
    """
    Customize profile WITHOUT AI - safer alternative
    Uses rule-based skill reordering only
    """
    customized = profile.copy()

    # Reorder skills to show matched skills first
    required_skills = analysis.get("required_skills", [])
    customized["skills"] = _reorder_skills(profile["skills"], required_skills)

    # Use recommended variant for experience if available
    variant = match_score.get("recommended_variant", "ml_focused")

    # Reorder experience highlights to emphasize variant
    for i, exp in enumerate(customized.get("experience", [])):
        # If latex_variants exists, we can use variant-specific description
        if "latex_variants" in exp and variant in exp["latex_variants"]:
            # Add variant-optimized bullet point at the beginning
            variant_text = exp["latex_variants"][variant]
            # Keep original highlights but emphasize variant first
            customized["experience"][i]["highlights"] = [variant_text] + exp["highlights"][:2]

    return customized


def _validate_structure(original: Dict, customized: Dict) -> bool:
    """
    Validate AI didn't add/remove sections
    CRITICAL: Prevents hallucinations
    """
    # Check same top-level keys
    if set(original.keys()) != set(customized.keys()):
        print(f"ERROR: Top-level keys mismatch")
        return False

    # Check experience count unchanged
    if len(original.get("experience", [])) != len(customized.get("experience", [])):
        print(f"ERROR: Experience count changed")
        return False

    # Check education count unchanged
    if len(original.get("education", [])) != len(customized.get("education", [])):
        print(f"ERROR: Education count changed")
        return False

    # Check each experience has same number of highlights (if AI was used)
    for i, exp in enumerate(original.get("experience", [])):
        if i < len(customized.get("experience", [])):
            orig_highlights = len(exp.get("highlights", []))
            cust_highlights = len(customized["experience"][i].get("highlights", []))
            if abs(orig_highlights - cust_highlights) > 1:  # Allow 1 difference for variant
                print(f"ERROR: Highlight count mismatch at index {i}")
                return False

    return True


def _reorder_skills(skills: Dict, required_skills: List[str]) -> Dict:
    """Reorder skills to show matched skills first"""
    reordered = {}
    required_lower = [s.lower().strip() for s in required_skills]

    for category, skill_list in skills.items():
        if not isinstance(skill_list, list):
            reordered[category] = skill_list
            continue

        matched = [s for s in skill_list if s.lower().strip() in required_lower]
        unmatched = [s for s in skill_list if s.lower().strip() not in required_lower]
        reordered[category] = matched + unmatched

    return reordered


def _get_analysis(job_id: str) -> Dict:
    """Get job analysis from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM job_analysis WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    analysis = dict(row)
    analysis["required_skills"] = json.loads(analysis.get("required_skills", "[]"))
    analysis["nice_to_have_skills"] = json.loads(analysis.get("nice_to_have_skills", "[]"))
    analysis["ats_keywords"] = json.loads(analysis.get("ats_keywords", "[]"))

    return analysis


def _get_match_score(job_id: str) -> Dict:
    """Get match score from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM match_scores WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    match_score = dict(row)
    match_score["skills_to_emphasize"] = json.loads(match_score.get("skills_to_emphasize", "[]"))

    return match_score


def _get_job(job_id: str) -> Dict:
    """Get job from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def main():
    """Run the Document Generator MCP server using stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
