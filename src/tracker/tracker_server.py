"""
Tracker MCP Server
Tracks application status and provides statistics
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
import os

mcp = FastMCP("tracker_mcp")

DB_PATH = "./data/databases/jobs.db"


def _init_applications_table():
    """Initialize applications table"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            application_id TEXT PRIMARY KEY,
            job_id TEXT,
            resume_file TEXT,
            match_score FLOAT,
            variant_used TEXT,
            applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'submitted',
            notes TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        )
    """)

    conn.commit()
    conn.close()


class CreateApplicationInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    job_id: str = Field(..., description="Job ID")
    resume_file: str = Field(..., description="Path to resume file used")
    match_score: float = Field(..., description="Match score for this application")
    variant_used: str = Field(..., description="Profile variant used")
    notes: Optional[str] = Field(default="", description="Optional notes")


@mcp.tool(
    name="create_application",
    annotations={
        "title": "Log New Application",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def create_application(params: CreateApplicationInput) -> str:
    """
    Log a new job application
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Generate application ID
        app_id = f"{params.job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Get job details
        cursor.execute("SELECT title, company FROM jobs WHERE job_id = ?", (params.job_id,))
        job_row = cursor.fetchone()

        if not job_row:
            conn.close()
            return f"Error: Job {params.job_id} not found"

        job_title, company = job_row

        # Insert application
        cursor.execute("""
            INSERT INTO applications
            (application_id, job_id, resume_file, match_score, variant_used, status, notes)
            VALUES (?, ?, ?, ?, ?, 'submitted', ?)
        """, (app_id, params.job_id, params.resume_file, params.match_score, params.variant_used, params.notes))

        # Update job status
        cursor.execute("""
            UPDATE jobs
            SET status = 'applied'
            WHERE job_id = ?
        """, (params.job_id,))

        conn.commit()
        conn.close()

        return f"✓ Application logged: {app_id}\nJob: {job_title} at {company}\nMatch Score: {params.match_score:.2f}%"

    except Exception as e:
        return f"Error creating application: {str(e)}"


class UpdateStatusInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    application_id: str = Field(..., description="Application ID")
    new_status: str = Field(..., description="New status (submitted, under_review, interview, offer, rejected)")
    notes: Optional[str] = Field(default="", description="Optional notes")


@mcp.tool(
    name="update_status",
    annotations={
        "title": "Update Application Status",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def update_status(params: UpdateStatusInput) -> str:
    """
    Update application status
    """
    try:
        valid_statuses = ["submitted", "under_review", "interview", "offer", "rejected", "withdrawn"]

        if params.new_status not in valid_statuses:
            return f"Error: Invalid status. Must be one of: {', '.join(valid_statuses)}"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Update status and notes
        cursor.execute("""
            UPDATE applications
            SET status = ?,
                notes = CASE
                    WHEN ? != '' THEN notes || '\n[' || datetime('now') || '] ' || ?
                    ELSE notes
                END,
                last_updated = CURRENT_TIMESTAMP
            WHERE application_id = ?
        """, (params.new_status, params.notes, params.notes, params.application_id))

        if cursor.rowcount == 0:
            conn.close()
            return f"Error: Application {params.application_id} not found"

        conn.commit()
        conn.close()

        return f"✓ Updated application {params.application_id} to status: {params.new_status}"

    except Exception as e:
        return f"Error updating status: {str(e)}"


class ListApplicationsInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: Optional[str] = Field(default=None, description="Filter by status")
    limit: int = Field(default=50, description="Maximum number of results")


@mcp.tool(
    name="list_applications",
    annotations={
        "title": "List Applications",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_applications(params: ListApplicationsInput) -> str:
    """
    List all applications with optional filtering
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if params.status:
            cursor.execute("""
                SELECT a.*, j.title, j.company, j.location
                FROM applications a
                JOIN jobs j ON a.job_id = j.job_id
                WHERE a.status = ?
                ORDER BY a.applied_date DESC
                LIMIT ?
            """, (params.status, params.limit))
        else:
            cursor.execute("""
                SELECT a.*, j.title, j.company, j.location
                FROM applications a
                JOIN jobs j ON a.job_id = j.job_id
                ORDER BY a.applied_date DESC
                LIMIT ?
            """, (params.limit,))

        rows = cursor.fetchall()
        conn.close()

        applications = [dict(row) for row in rows]

        return json.dumps({
            "count": len(applications),
            "applications": applications
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error listing applications: {str(e)}"


@mcp.tool(
    name="get_stats",
    annotations={
        "title": "Get Application Statistics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_stats() -> str:
    """
    Get application statistics
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Total applications
        cursor.execute("SELECT COUNT(*) FROM applications")
        total = cursor.fetchone()[0]

        # By status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM applications
            GROUP BY status
        """)
        by_status = dict(cursor.fetchall())

        # Average match score
        cursor.execute("SELECT AVG(match_score) FROM applications")
        avg_score = cursor.fetchone()[0] or 0

        # Total jobs scraped
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cursor.fetchone()[0]

        # Jobs by status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM jobs
            GROUP BY status
        """)
        jobs_by_status = dict(cursor.fetchall())

        # Application rate (applications / scraped jobs)
        application_rate = (total / total_jobs * 100) if total_jobs > 0 else 0

        # Interview rate (interviews / applications)
        interview_count = by_status.get("interview", 0)
        interview_rate = (interview_count / total * 100) if total > 0 else 0

        # Offer rate
        offer_count = by_status.get("offer", 0)
        offer_rate = (offer_count / total * 100) if total > 0 else 0

        conn.close()

        stats = {
            "application_summary": {
                "total_applications": total,
                "by_status": by_status,
                "average_match_score": round(avg_score, 2)
            },
            "job_summary": {
                "total_jobs_scraped": total_jobs,
                "jobs_by_status": jobs_by_status
            },
            "conversion_rates": {
                "application_rate": round(application_rate, 2),
                "interview_rate": round(interview_rate, 2),
                "offer_rate": round(offer_rate, 2)
            },
            "top_performers": {
                "interviews": interview_count,
                "offers": offer_count
            }
        }

        return json.dumps(stats, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error getting stats: {str(e)}"


# Initialize table on server start
_init_applications_table()


def main():
    """Run the Tracker MCP server using stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
