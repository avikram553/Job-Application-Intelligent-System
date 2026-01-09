# MCP Job Application Intelligence System

**Version:** 1.0.0
**Author:** Aditya Vikram
**Status:** Production Ready

---

## Overview

An intelligent, privacy-preserving job application automation system that leverages local AI (Ollama/Llama 3.1) and the Model Context Protocol (MCP) to generate personalized, ATS-optimized resumes for each job opportunity.

### Key Features

- **AI-Powered Personalization:** Each resume uniquely tailored to specific job descriptions
- **Privacy-First:** 100% local processing using Ollama (no cloud AI services)
- **ATS-Optimized:** Resumes formatted for Applicant Tracking System compatibility
- **Time-Saving:** Automates 90% of job application preparation
- **Cost-Free:** No API costs for AI (unlike ChatGPT/Claude)
- **Hallucination Prevention:** Strict validation to prevent AI from fabricating information

---

## Quick Start

### 1. Installation

```bash
# Clone or download the repository
cd "Job Application Intelligence System"

# Run installation script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source .venv/bin/activate
```

### 2. Configuration

**Set Apify API Token:**
```bash
# Edit .env file
nano .env

# Add your token:
APIFY_API_TOKEN=your_actual_token_here
```

**Configure Job Preferences:**
```bash
python cli_set_preferences.py
```

### 3. Initialize Profile

Ensure your profile data is in `data/profiles/profile.json`. The system already has Aditya's profile loaded.

### 4. Run Workflow

```bash
python orchestrator.py --workflow
```

---

## System Architecture

### 6 MCP Servers

1. **Profile Server** (`src/models/profile_server.py`)
   - Manages user profile data
   - Tools: `get_profile_json`, `update_profile`
   - Resources: `profile://me`, `profile://me/{section}`

2. **Job Scraper Server** (`src/scraper/job_scraper_server.py`)
   - Scrapes job postings from LinkedIn and Indeed
   - Tools: `scrape_jobs`, `get_job_details`, `list_jobs`
   - API: Apify

3. **Analysis Server** (`src/analysis/analysis_server.py`)
   - Analyzes job descriptions using Ollama
   - Tools: `analyze_jd`, `list_analyzed_jobs`
   - AI: Llama 3.1 8B (local)

4. **Matcher Server** (`src/matcher/matcher_server.py`)
   - Matches profile to job requirements
   - Tools: `match_profile`, `list_matches`
   - Scoring: Weighted algorithm (skills 40%, experience 30%, domain 30%)

5. **Document Generator Server** (`src/generator/document_generator_server.py`)
   - Generates personalized LaTeX resumes
   - Tools: `generate_resume`
   - Validation: Prevents AI hallucinations

6. **Tracker Server** (`src/tracker/tracker_server.py`)
   - Tracks application status
   - Tools: `create_application`, `update_status`, `list_applications`, `get_stats`

---

## Workflow

### Complete Job Search Process

1. **Set Preferences** (one-time)
   ```bash
   python cli_set_preferences.py
   ```

2. **Scrape Jobs** (daily)
   ```bash
   python src/scraper/job_scraper_server.py
   # Via MCP client: scrape_jobs(keywords="ML Engineer", location="Munich")
   ```

3. **Analyze Jobs** (automated)
   ```bash
   python src/analysis/analysis_server.py
   # For each job: analyze_jd(job_id="<id>")
   ```

4. **Match Profile** (automated)
   ```bash
   python src/matcher/matcher_server.py
   # For each job: match_profile(job_id="<id>")
   ```

5. **Generate Resumes** (for matches ≥70%)
   ```bash
   python src/generator/document_generator_server.py
   # For high matches: generate_resume(job_id="<id>")
   ```

6. **Review & Apply** (MANDATORY HUMAN REVIEW)
   - Open generated .tex files in Overleaf
   - Compile to PDF and review
   - Verify accuracy (no fabricated info)
   - Apply to jobs manually

7. **Track Applications**
   ```bash
   python src/tracker/tracker_server.py
   # After applying: create_application(job_id, resume_file, match_score, variant)
   ```

---

## Usage Examples

### Using MCP Servers

Each MCP server runs independently using stdio transport. You can interact with them using:

1. **Claude Desktop App** (recommended)
2. **MCP CLI Client**
3. **Custom scripts**

### Example: Scrape Jobs

```python
# In an MCP client connected to job_scraper_server.py
scrape_jobs({
    "keywords": "Machine Learning Engineer",
    "location": "Munich, Germany",
    "job_type": "Full-time",
    "max_results": 50
})
```

### Example: Match Profile

```python
# In an MCP client connected to matcher_server.py
match_profile({
    "job_id": "abc123def456",
    "profile_path": "./data/profiles/profile.json"
})
```

### Example: Generate Resume

```python
# In an MCP client connected to document_generator_server.py
generate_resume({
    "job_id": "abc123def456",
    "use_ai_customization": true
})
```

---

## Configuration

### Preferences (`data/preferences.json`)

```json
{
  "roles": ["Machine Learning Engineer", "AI Engineer"],
  "locations": ["Munich", "Berlin", "Stuttgart"],
  "job_type": "Full-time",
  "experience_level": "Senior",
  "must_have_keywords": ["Python", "TensorFlow", "PyTorch"],
  "exclude_keywords": ["PhD required"],
  "salary_min": 70000,
  "match_threshold": 70.0
}
```

### Environment Variables (`.env`)

```bash
APIFY_API_TOKEN=your_api_token_here
OLLAMA_URL=http://localhost:11434/api/generate
```

---

## Database Schema

### SQLite Database: `data/databases/jobs.db`

**Tables:**
- `jobs` - Scraped job listings
- `job_analysis` - AI analysis results
- `match_scores` - Profile-to-job match scores
- `applications` - Tracked applications

See `docs/API_REFERENCE.md` for complete schemas.

---

## AI Hallucination Prevention

### Critical Safeguards

1. **Fixed LaTeX Template**
   - AI customizes content, NOT structure
   - Template is locked and validated

2. **Section-by-Section Generation**
   - Limits AI scope to prevent drift
   - Each section validated independently

3. **Structure Validation**
   - Checks that AI didn't add/remove sections
   - Validates bullet point counts match original
   - Rejects any structural changes

4. **Pydantic Validation**
   - Blocks unauthorized fields
   - Type checking on all inputs/outputs

5. **Mandatory Human Review**
   - System never auto-applies
   - User MUST review before submitting

---

## Privacy & Security

### Data Privacy

- **100% Local Processing:** All AI runs on your machine via Ollama
- **No Cloud AI:** Never sends data to ChatGPT, Claude, or similar
- **Local Storage:** SQLite database stored locally
- **Exception:** Apify API (only for job scraping - public data)

### API Keys

- Apify API token stored in `.env` (never committed to git)
- Free tier: $5 credit/month (sufficient for daily use)

---

## Troubleshooting

### Common Issues

#### 1. "Ollama is not running"

**Solution:**
```bash
# Start Ollama
ollama serve

# In another terminal, pull model
ollama pull llama3.1:8b
```

#### 2. "APIFY_API_TOKEN not set"

**Solution:**
```bash
# Edit .env file
nano .env

# Add token:
APIFY_API_TOKEN=your_token_here
```

#### 3. "Job scraping returns no results"

**Possible causes:**
- API rate limits exceeded
- Network issues
- Invalid search criteria

**Solution:**
- Check Apify dashboard for usage
- Verify internet connection
- Adjust search keywords/location

#### 4. "LaTeX compilation errors"

**Solution:**
- Review generated .tex file for special characters
- Ensure LaTeX is installed: `pdflatex --version`
- Use Overleaf for easier debugging

---

## Performance

### Expected Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| Job Scraping (50 jobs) | ~2 min | Depends on Apify |
| JD Analysis (1 job) | ~10 sec | Depends on hardware |
| Resume Generation | ~30 sec | With AI customization |
| Database Queries | <100ms | SQLite |

### Hardware Recommendations

**Minimum:**
- CPU: 4 cores, 2.0 GHz
- RAM: 8 GB
- Storage: 10 GB

**Recommended:**
- CPU: 8 cores, 3.0 GHz
- RAM: 16 GB
- GPU: NVIDIA GPU with 6GB+ VRAM (for faster Ollama)

---

## Roadmap

### Future Enhancements

- **Phase 9:** Web UI with Flask/FastAPI
- **Phase 10:** Cover letter generation
- **Phase 11:** LinkedIn auto-apply automation
- **Phase 12:** Advanced analytics and insights

See `PRD.md` for complete roadmap.

---

## Contributing

This is a personal project for Aditya Vikram's job search. However, feedback and suggestions are welcome!

**Contact:** vkrm.aditya553@gmail.com

---

## License

Personal Use License - Not for redistribution without permission.

---

## Acknowledgments

- **MCP Framework:** Anthropic's Model Context Protocol
- **AI Model:** Meta's Llama 3.1 via Ollama
- **Job Scraping:** Apify platform

---

**Last Updated:** January 9, 2026
**Version:** 1.0.0
