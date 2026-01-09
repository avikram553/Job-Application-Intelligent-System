# Quick Start Guide

**Get up and running in 10 minutes!**

---

## Prerequisites

- Python 3.10+
- Internet connection
- Terminal/Command line access

---

## Step 1: Installation (3 minutes)

```bash
# Navigate to project directory
cd "Job Application Intelligence System"

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate  # On Windows
```

---

## Step 2: Get Apify API Token (2 minutes)

1. Go to https://apify.com
2. Sign up for free account
3. Get API token from Account Settings
4. Add to `.env` file:
   ```bash
   APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxx
   ```

---

## Step 3: Install Ollama (3 minutes)

```bash
# macOS/Linux
# Download from https://ollama.ai
# OR use curl:
curl https://ollama.ai/install.sh | sh

# After installation:
ollama serve &  # Start Ollama service
ollama pull llama3.1:8b  # Download AI model (~4GB)
```

---

## Step 4: Configure Preferences (2 minutes)

```bash
python cli_set_preferences.py
```

Set:
- Target roles (e.g., "Machine Learning Engineer")
- Locations (e.g., "Munich, Germany")
- Minimum salary
- Must-have keywords

---

## Step 5: Test the System (Optional)

```bash
# View current profile
python src/models/profile_server.py
# (In another terminal with MCP client, call get_profile_json())

# Test job scraping (requires Apify token)
python src/scraper/job_scraper_server.py
# (Call scrape_jobs via MCP client)
```

---

## Step 6: Run Complete Workflow

```bash
python orchestrator.py --workflow
```

Follow the prompts to:
1. Scrape jobs
2. Analyze with AI
3. Match your profile
4. Generate personalized resumes
5. Review and apply

---

## Daily Usage

### Morning Routine (5 minutes)

```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Run workflow
python orchestrator.py --workflow

# 3. Review generated resumes in ./generated_resumes/

# 4. Apply to jobs manually

# 5. Track applications
python src/tracker/tracker_server.py
# (Call create_application via MCP client)
```

---

## Troubleshooting

### "Ollama not found"
```bash
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### "No jobs found"
- Check Apify token is correct
- Verify search criteria in preferences
- Check Apify dashboard for API usage

### "LaTeX errors"
- Use Overleaf (https://overleaf.com) for easier editing
- Compile .tex files there instead of locally

---

## Next Steps

- Read full documentation: `docs/README.md`
- View API reference: `docs/API_REFERENCE.md`
- Check project roadmap: `PRD.md`

---

**Need Help?** Contact: vkrm.aditya553@gmail.com

