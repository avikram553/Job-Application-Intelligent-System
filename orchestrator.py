#!/usr/bin/env python3
"""
Master Orchestrator for MCP Job Application Intelligence System
Coordinates all MCP servers to automate job search workflow
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preferences import load_preferences, display_preferences


async def main_workflow():
    """
    Execute complete job search workflow
    """
    print("\n" + "=" * 70)
    print(" MCP JOB APPLICATION INTELLIGENCE SYSTEM")
    print(" Automated Job Search & Resume Generation")
    print("=" * 70 + "\n")

    # Load preferences
    prefs = load_preferences()

    print("Step 1/7: Loading Preferences")
    print("-" * 70)
    print(display_preferences())

    confirm = input("\nProceed with these preferences? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("\nWorkflow cancelled. Update preferences using: python cli_set_preferences.py")
        return

    # Step 2: Job Scraping
    print("\n\nStep 2/7: Scraping Jobs")
    print("-" * 70)
    print(f"Searching for roles: {', '.join(prefs['roles'])}")
    print(f"Locations: {', '.join(prefs['locations'])}")

    # Note: In production, this would call the actual MCP servers via subprocess
    # For now, we'll provide instructions for manual execution

    print("\nTo scrape jobs, run the job scraper server:")
    print("  python src/scraper/job_scraper_server.py")
    print("\nThen use an MCP client to call:")
    print(f"  scrape_jobs(keywords='{prefs['roles'][0]}', location='{prefs['locations'][0]}')")

    input("\nPress Enter after you've scraped jobs...")

    # Step 3: Analyze Jobs
    print("\n\nStep 3/7: Analyzing Jobs with AI")
    print("-" * 70)
    print("Analyzing job descriptions using Ollama (Llama 3.1)...")

    print("\nTo analyze jobs, run the analysis server:")
    print("  python src/analysis/analysis_server.py")
    print("\nThen for each job_id, call:")
    print("  analyze_jd(job_id='<job_id>')")

    input("\nPress Enter after you've analyzed jobs...")

    # Step 4: Match Profile
    print("\n\nStep 4/7: Matching Profile to Jobs")
    print("-" * 70)
    print(f"Calculating match scores (threshold: {prefs['match_threshold']}%)...")

    print("\nTo match profile, run the matcher server:")
    print("  python src/matcher/matcher_server.py")
    print("\nThen for each analyzed job, call:")
    print("  match_profile(job_id='<job_id>')")

    input("\nPress Enter after you've matched jobs...")

    # Step 5: Generate Resumes
    print("\n\nStep 5/7: Generating Personalized Resumes")
    print("-" * 70)
    print(f"Generating resumes for jobs with score >= {prefs['match_threshold']}%...")

    print("\nTo generate resumes, run the document generator server:")
    print("  python src/generator/document_generator_server.py")
    print("\nThen for each high-match job, call:")
    print("  generate_resume(job_id='<job_id>', use_ai_customization=true)")

    input("\nPress Enter after you've generated resumes...")

    # Step 6: Review Resumes
    print("\n\nStep 6/7: Review Generated Resumes")
    print("-" * 70)
    print("IMPORTANT: Human review is MANDATORY before applying!")
    print("\nReview generated resumes in: ./generated_resumes/")
    print("\nFor each resume:")
    print("  1. Open the .tex file in Overleaf or local LaTeX editor")
    print("  2. Compile to PDF and review")
    print("  3. Check for accuracy (no fabricated information)")
    print("  4. Verify ATS compatibility")
    print("  5. Make any necessary edits")

    input("\nPress Enter after you've reviewed resumes...")

    # Step 7: Track Applications
    print("\n\nStep 7/7: Track Applications")
    print("-" * 70)
    print("Log applications as you submit them...")

    print("\nTo track applications, run the tracker server:")
    print("  python src/tracker/tracker_server.py")
    print("\nAfter applying to a job, call:")
    print("  create_application(job_id='<job_id>', resume_file='<path>', match_score=<score>, variant_used='<variant>')")

    print("\n\nTo view statistics:")
    print("  get_stats()")

    print("\n\n" + "=" * 70)
    print(" WORKFLOW COMPLETE!")
    print("=" * 70)
    print("\nNext Steps:")
    print("  1. Review and apply to jobs manually")
    print("  2. Update application status as you receive responses")
    print("  3. Run this workflow daily for new jobs")
    print("\n")


async def quick_stats():
    """Quick statistics view"""
    print("\n" + "=" * 70)
    print(" APPLICATION STATISTICS")
    print("=" * 70 + "\n")

    print("To view statistics, run the tracker server:")
    print("  python src/tracker/tracker_server.py")
    print("\nThen call:")
    print("  get_stats()")
    print("\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="MCP Job Application Intelligence System Orchestrator")
    parser.add_argument("--workflow", action="store_true", help="Run complete workflow")
    parser.add_argument("--stats", action="store_true", help="View statistics")
    parser.add_argument("--help-servers", action="store_true", help="Show how to start MCP servers")

    args = parser.parse_args()

    if args.workflow:
        asyncio.run(main_workflow())
    elif args.stats:
        asyncio.run(quick_stats())
    elif args.help_servers:
        print("\n" + "=" * 70)
        print(" MCP SERVER STARTUP GUIDE")
        print("=" * 70 + "\n")

        servers = [
            ("Profile Server", "src/models/profile_server.py", "Manage user profile"),
            ("Job Scraper Server", "src/scraper/job_scraper_server.py", "Scrape job postings"),
            ("Analysis Server", "src/analysis/analysis_server.py", "Analyze job descriptions"),
            ("Matcher Server", "src/matcher/matcher_server.py", "Match profile to jobs"),
            ("Document Generator", "src/generator/document_generator_server.py", "Generate resumes"),
            ("Tracker Server", "src/tracker/tracker_server.py", "Track applications")
        ]

        for name, path, description in servers:
            print(f"{name}:")
            print(f"  Description: {description}")
            print(f"  Command: python {path}")
            print()

        print("Note: Each server runs independently using stdio transport.")
        print("Use an MCP client (like Claude Desktop) to interact with servers.")
        print("\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
