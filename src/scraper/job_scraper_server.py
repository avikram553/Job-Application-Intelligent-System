"""
Job Scraper MCP Server
Scrapes job postings from LinkedIn and Indeed via Apify
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
import hashlib
import os
import json

# Initialize MCP server
mcp = FastMCP("job_scraper_mcp")

# Database setup
DB_PATH = "./data/databases/jobs.db"

def _init_database() -> None:
    """Initialize SQLite database with jobs table"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT,
            requirements TEXT,
            posted_date TEXT,
            source TEXT,
            url TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'new'
        )
    """)

    conn.commit()
    conn.close()


class ScrapeJobsInput(BaseModel):
    """Input for scraping jobs"""
    model_config = ConfigDict(extra='forbid')

    keywords: str = Field(..., description="Job search keywords (e.g., 'Machine Learning Engineer')")
    location: str = Field(..., description="Job location (e.g., 'Munich, Germany')")
    job_type: str = Field(default="Full-time", description="Job type")
    max_results: int = Field(default=50, description="Maximum jobs to scrape")


@mcp.tool(
    name="scrape_jobs",
    annotations={
        "title": "Scrape Job Postings",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def scrape_jobs(params: ScrapeJobsInput) -> str:
    """
    Scrape job postings from LinkedIn and Indeed using Apify

    Returns summary of jobs found and stored
    """
    try:
        # Check if Apify API token is set
        apify_token = os.getenv("APIFY_API_TOKEN")
        if not apify_token:
            return "Error: APIFY_API_TOKEN environment variable not set. Please set your Apify API key."

        # Import apify_client only when needed
        try:
            from apify_client import ApifyClient
        except ImportError:
            return "Error: apify-client not installed. Run: pip install apify-client"

        # Initialize Apify client
        apify = ApifyClient(apify_token)

        jobs_found = []

        # 1. Scrape LinkedIn
        try:
            print(f"Scraping LinkedIn for '{params.keywords}' in '{params.location}'...")
            linkedin_run = apify.actor("apify/linkedin-jobs-scraper").call(
                run_input={
                    "keywords": params.keywords,
                    "location": params.location,
                    "posted_at": "past-24h",
                    "job_type": params.job_type,
                    "max_results": params.max_results // 2
                }
            )

            linkedin_jobs = apify.dataset(linkedin_run["defaultDatasetId"]).list_items().items
            jobs_found.extend(_process_jobs(linkedin_jobs, "linkedin"))
            print(f"✓ Found {len(linkedin_jobs)} LinkedIn jobs")

        except Exception as e:
            print(f"Warning: LinkedIn scraping failed: {str(e)}")

        # 2. Scrape Indeed
        try:
            print(f"Scraping Indeed for '{params.keywords}' in '{params.location}'...")
            indeed_run = apify.actor("apify/indeed-scraper").call(
                run_input={
                    "queries": f"{params.keywords} in {params.location}",
                    "maxItems": params.max_results // 2
                }
            )

            indeed_jobs = apify.dataset(indeed_run["defaultDatasetId"]).list_items().items
            jobs_found.extend(_process_jobs(indeed_jobs, "indeed"))
            print(f"✓ Found {len(indeed_jobs)} Indeed jobs")

        except Exception as e:
            print(f"Warning: Indeed scraping failed: {str(e)}")

        # 3. Deduplicate and store
        if not jobs_found:
            return "No jobs found. This could be due to API limits, network issues, or no matches for your criteria."

        unique_jobs = _deduplicate_jobs(jobs_found)
        stored_count = _store_jobs(unique_jobs)

        return f"✓ Scraped {len(jobs_found)} jobs ({stored_count} unique) from LinkedIn and Indeed\nStored in database: {DB_PATH}"

    except Exception as e:
        return f"Error scraping jobs: {str(e)}"


def _process_jobs(raw_jobs: List[Dict], source: str) -> List[Dict]:
    """Normalize job data from different sources"""
    processed = []

    for job in raw_jobs:
        # Generate unique job ID
        job_id = hashlib.md5(
            f"{job.get('company', 'Unknown')}_{job.get('title', 'Unknown')}_{job.get('location', 'Unknown')}".encode()
        ).hexdigest()

        # Extract description (may vary by source)
        description = job.get("description") or job.get("jobDescription") or ""

        processed.append({
            "job_id": job_id,
            "title": job.get("title") or job.get("position"),
            "company": job.get("company") or job.get("employer"),
            "location": job.get("location"),
            "description": description,
            "requirements": job.get("requirements", ""),
            "posted_date": job.get("posted_date") or job.get("postedAt") or datetime.now().isoformat(),
            "source": source,
            "url": job.get("url") or job.get("link") or "",
            "status": "new"
        })

    return processed


def _deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Remove duplicate jobs based on job_id"""
    seen = set()
    unique = []

    for job in jobs:
        if job["job_id"] not in seen:
            seen.add(job["job_id"])
            unique.append(job)

    return unique


def _store_jobs(jobs: List[Dict]) -> int:
    """Store jobs in SQLite, return count of new jobs"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    stored = 0
    for job in jobs:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO jobs
                (job_id, title, company, location, description, requirements,
                 posted_date, source, url, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job["job_id"], job["title"], job["company"], job["location"],
                job["description"], job["requirements"], job["posted_date"],
                job["source"], job["url"], job["status"]
            ))
            if cursor.rowcount > 0:
                stored += 1
        except Exception as e:
            print(f"Error storing job {job['job_id']}: {e}")

    conn.commit()
    conn.close()

    return stored


class GetJobDetailsInput(BaseModel):
    """Input for getting job details"""
    model_config = ConfigDict(extra='forbid')
    job_id: str = Field(..., description="Job ID to retrieve")


@mcp.tool(
    name="get_job_details",
    annotations={
        "title": "Get Job Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_job_details(params: GetJobDetailsInput) -> str:
    """
    Get details for a specific job
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (params.job_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return f"Error: Job {params.job_id} not found"

        job = dict(row)
        return json.dumps(job, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error retrieving job: {str(e)}"


class ListJobsInput(BaseModel):
    """Input for listing jobs"""
    model_config = ConfigDict(extra='forbid')
    status: Optional[str] = Field(default=None, description="Filter by status (new, analyzed, applied, skipped)")
    limit: int = Field(default=50, description="Maximum number of jobs to return")


@mcp.tool(
    name="list_jobs",
    annotations={
        "title": "List Jobs",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_jobs(params: ListJobsInput) -> str:
    """
    List jobs from database with optional filtering
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if params.status:
            cursor.execute(
                "SELECT * FROM jobs WHERE status = ? ORDER BY scraped_at DESC LIMIT ?",
                (params.status, params.limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM jobs ORDER BY scraped_at DESC LIMIT ?",
                (params.limit,)
            )

        rows = cursor.fetchall()
        conn.close()

        jobs = [dict(row) for row in rows]

        return json.dumps({
            "count": len(jobs),
            "jobs": jobs
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error listing jobs: {str(e)}"


# Initialize database on server start
_init_database()


def main():
    """Run the Job Scraper MCP server using stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
