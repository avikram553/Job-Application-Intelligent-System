"""
Matcher MCP Server
Matches user profile to job requirements with intelligent scoring
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
import sqlite3
import json
from typing import Dict, Any, Set
from pathlib import Path

mcp = FastMCP("matcher_mcp")

DB_PATH = "./data/databases/jobs.db"


class MatchProfileInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    job_id: str = Field(..., description="Job ID to match against")
    profile_path: str = Field(default="./data/profiles/profile.json", description="Path to profile")


@mcp.tool(
    name="match_profile",
    annotations={
        "title": "Match Profile to Job",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def match_profile(params: MatchProfileInput) -> str:
    """
    Match user profile to job requirements
    Returns match score and recommendations
    """
    try:
        # 1. Load profile
        profile_path = Path(params.profile_path)
        if not profile_path.exists():
            return f"Error: Profile not found at {params.profile_path}"

        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)

        # 2. Get job analysis
        analysis = _get_analysis(params.job_id)
        if not analysis:
            return f"Error: Analysis not found for job {params.job_id}. Please run analyze_jd first."

        # 3. Get job details
        job = _get_job(params.job_id)
        if not job:
            return f"Error: Job {params.job_id} not found"

        # 4. Calculate match scores
        skills_score = _calculate_skills_match(profile, analysis)
        experience_score = _calculate_experience_match(profile, analysis)
        domain_score = _calculate_domain_match(profile, analysis)

        # 5. Weighted overall score
        overall_score = (
            skills_score * 0.4 +
            experience_score * 0.3 +
            domain_score * 0.3
        )

        # 6. Recommend variant
        variant = _recommend_variant(analysis["role_category"])

        # 7. Identify skills to emphasize
        skills_to_emphasize = _identify_skills_to_emphasize(profile, analysis)

        # 8. Store match score
        _store_match_score(params.job_id, {
            "overall_score": overall_score,
            "skills_score": skills_score,
            "experience_score": experience_score,
            "domain_score": domain_score,
            "recommended_variant": variant,
            "skills_to_emphasize": skills_to_emphasize
        })

        # 9. Format response
        result = {
            "job_id": params.job_id,
            "job_title": job["title"],
            "company": job["company"],
            "overall_score": round(overall_score, 2),
            "recommended_variant": variant,
            "skills_to_emphasize": skills_to_emphasize[:5],  # Top 5
            "breakdown": {
                "skills": round(skills_score, 2),
                "experience": round(experience_score, 2),
                "domain": round(domain_score, 2)
            },
            "recommendation": _get_recommendation(overall_score)
        }

        return json.dumps(result, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error matching profile: {str(e)}"


def _calculate_skills_match(profile: Dict, analysis: Dict) -> float:
    """Calculate skills overlap percentage"""
    # Get all user skills
    user_skills = set()
    for category in profile.get("skills", {}).values():
        if isinstance(category, list):
            user_skills.update([s.lower().strip() for s in category])

    # Get required skills from analysis
    required = set([s.lower().strip() for s in analysis.get("required_skills", [])])

    # Calculate overlap
    if not required:
        return 100.0

    overlap = user_skills.intersection(required)
    match_percentage = (len(overlap) / len(required)) * 100

    # Bonus points for nice-to-have skills
    nice_to_have = set([s.lower().strip() for s in analysis.get("nice_to_have_skills", [])])
    bonus_overlap = user_skills.intersection(nice_to_have)

    if nice_to_have:
        bonus = (len(bonus_overlap) / len(nice_to_have)) * 10  # Up to 10% bonus
        match_percentage = min(100, match_percentage + bonus)

    return match_percentage


def _calculate_experience_match(profile: Dict, analysis: Dict) -> float:
    """Match experience level"""
    level_map = {
        "entry": 0,
        "junior": 0,
        "mid": 1,
        "mid-level": 1,
        "senior": 2,
        "lead": 3,
        "staff": 3,
        "principal": 4
    }

    # Calculate user's experience level from years
    years_exp = float(profile.get("metadata", {}).get("years_of_experience", "3.5"))
    if years_exp < 2:
        user_level = 0  # Entry
    elif years_exp < 5:
        user_level = 1  # Mid
    elif years_exp < 8:
        user_level = 2  # Senior
    else:
        user_level = 3  # Lead/Staff

    # Get required level
    required_level_str = analysis.get("experience_level", "Mid").lower()
    required_level = level_map.get(required_level_str, 1)

    # Calculate score
    # Perfect match = 100, one level off = 80, two levels = 60, etc.
    diff = abs(user_level - required_level)

    if diff == 0:
        return 100.0
    elif diff == 1:
        return 80.0
    elif diff == 2:
        return 60.0
    else:
        return 40.0


def _calculate_domain_match(profile: Dict, analysis: Dict) -> float:
    """Calculate domain expertise match"""
    role_category = analysis.get("role_category", "").lower()

    # Extract user's domain experience from profile
    has_ml = False
    has_automotive = False
    has_backend = False

    # Check from experience
    for exp in profile.get("experience", []):
        highlights = " ".join(exp.get("highlights", [])).lower()
        techs = " ".join(exp.get("technologies", [])).lower()

        if any(term in highlights or term in techs for term in ["machine learning", "ml", "tensorflow", "pytorch", "ai"]):
            has_ml = True
        if any(term in highlights or term in techs for term in ["automotive", "bosch", "car", "vehicle"]):
            has_automotive = True
        if any(term in highlights or term in techs for term in ["backend", "api", "fastapi", "flask", "django"]):
            has_backend = True

    # Score based on role category
    if "ml" in role_category or "machine learning" in role_category or "ai" in role_category:
        if has_ml and has_automotive:
            return 100.0  # Perfect match for ML + Automotive
        elif has_ml:
            return 90.0
        else:
            return 50.0

    elif "backend" in role_category or "software engineer" in role_category:
        if has_backend:
            return 90.0
        else:
            return 70.0

    elif "data" in role_category:
        if has_ml:
            return 85.0
        else:
            return 60.0

    else:
        return 75.0  # Neutral score for unknown categories


def _recommend_variant(role_category: str) -> str:
    """Recommend best profile variant for role"""
    category_lower = role_category.lower()

    if "ml" in category_lower or "machine learning" in category_lower or "ai" in category_lower:
        if "automotive" in category_lower:
            return "ml_focused+automotive_focused"
        return "ml_focused"
    elif "backend" in category_lower or "software" in category_lower:
        return "backend_focused"
    elif "lead" in category_lower or "senior" in category_lower:
        return "leadership_focused"
    else:
        return "ml_focused"  # Default to ML for Aditya


def _identify_skills_to_emphasize(profile: Dict, analysis: Dict) -> list:
    """Identify which skills to emphasize based on job requirements"""
    # Get all user skills
    user_skills = {}
    for category, skills_list in profile.get("skills", {}).items():
        if isinstance(skills_list, list):
            for skill in skills_list:
                user_skills[skill.lower().strip()] = skill  # Preserve original casing

    # Get required skills
    required = [s.lower().strip() for s in analysis.get("required_skills", [])]

    # Find matches
    matched_skills = []
    for req_skill in required:
        if req_skill in user_skills:
            matched_skills.append(user_skills[req_skill])

    return matched_skills


def _get_recommendation(score: float) -> str:
    """Get recommendation based on score"""
    if score >= 85:
        return "Excellent match! Highly recommend applying."
    elif score >= 70:
        return "Good match. Recommend generating customized resume."
    elif score >= 55:
        return "Moderate match. Consider applying if interested."
    else:
        return "Low match. May not be the best fit."


def _get_analysis(job_id: str) -> Dict:
    """Retrieve job analysis from database"""
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


def _get_job(job_id: str) -> Dict:
    """Retrieve job from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def _store_match_score(job_id: str, scores: Dict) -> None:
    """Store match score in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_scores (
            match_id TEXT PRIMARY KEY,
            job_id TEXT,
            overall_score FLOAT,
            skills_score FLOAT,
            experience_score FLOAT,
            domain_score FLOAT,
            recommended_variant TEXT,
            skills_to_emphasize TEXT,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        )
    """)

    # Insert or update
    cursor.execute("""
        INSERT OR REPLACE INTO match_scores
        (match_id, job_id, overall_score, skills_score, experience_score,
         domain_score, recommended_variant, skills_to_emphasize)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job_id,
        job_id,
        scores["overall_score"],
        scores["skills_score"],
        scores["experience_score"],
        scores["domain_score"],
        scores["recommended_variant"],
        json.dumps(scores["skills_to_emphasize"])
    ))

    # Update job status
    cursor.execute("""
        UPDATE jobs
        SET status = 'matched'
        WHERE job_id = ?
    """, (job_id,))

    conn.commit()
    conn.close()


class ListMatchesInput(BaseModel):
    """Input for listing matches"""
    model_config = ConfigDict(extra='forbid')
    min_score: float = Field(default=70.0, description="Minimum match score")
    limit: int = Field(default=20, description="Maximum number of results")


@mcp.tool(
    name="list_matches",
    annotations={
        "title": "List Job Matches",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_matches(params: ListMatchesInput) -> str:
    """
    List all matched jobs above a certain score threshold
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT j.job_id, j.title, j.company, j.location,
                   m.overall_score, m.recommended_variant
            FROM jobs j
            INNER JOIN match_scores m ON j.job_id = m.job_id
            WHERE m.overall_score >= ?
            ORDER BY m.overall_score DESC
            LIMIT ?
        """, (params.min_score, params.limit))

        rows = cursor.fetchall()
        conn.close()

        results = [dict(row) for row in rows]

        return json.dumps({
            "count": len(results),
            "matches": results,
            "min_score": params.min_score
        }, indent=2)

    except Exception as e:
        return f"Error listing matches: {str(e)}"


def main():
    """Run the Matcher MCP server using stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
