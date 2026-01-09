# User Guide - MCP Job Application Intelligence System

**For:** Aditya Vikram & Future Users
**Version:** 1.0.0
**Last Updated:** January 9, 2026

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Using MCP Servers with Claude Desktop](#using-mcp-servers-with-claude-desktop)
3. [Daily Workflow](#daily-workflow)
4. [Advanced Features](#advanced-features)
5. [Tips & Best Practices](#tips--best-practices)
6. [FAQ](#faq)

---

## Getting Started

### First-Time Setup

**1. Install Dependencies**

```bash
cd "Job Application Intelligence System"
chmod +x setup.sh
./setup.sh
```

**2. Configure API Token**

Get your free Apify token:
- Visit https://apify.com
- Sign up (free tier gives $5/month credit)
- Go to Settings → API Tokens
- Copy your token

Add to `.env`:
```bash
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxx
```

**3. Install & Start Ollama**

```bash
# Download from https://ollama.ai
# After installation:
ollama serve  # Start in background
ollama pull llama3.1:8b  # Download AI model
```

**4. Set Job Preferences**

```bash
python cli_set_preferences.py
```

Configure:
- **Roles:** e.g., "Machine Learning Engineer", "AI Engineer"
- **Locations:** e.g., "Munich", "Berlin", "Stuttgart"
- **Salary:** Minimum acceptable (e.g., 70000 EUR)
- **Keywords:** Must-have skills (e.g., "Python", "TensorFlow")

**5. Verify Setup**

```bash
python tests/test_system.py
```

All tests should pass ✓

---

## Using MCP Servers with Claude Desktop

### Option 1: Claude Desktop Integration (Recommended)

**Setup:**

1. Install Claude Desktop App (if not already)

2. Add MCP servers to Claude's config:
   ```bash
   # macOS
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Copy contents from claude_desktop_config.json in project root
   ```

3. Restart Claude Desktop

4. Verify servers are loaded:
   - Open Claude Desktop
   - Look for MCP server indicators
   - Try: "List available MCP tools"

**Usage in Claude:**

```
User: "Scrape Machine Learning Engineer jobs in Munich"

Claude: [Uses job_scraper server]
        scrape_jobs(keywords="Machine Learning Engineer", location="Munich")
        ✓ Scraped 48 jobs (35 unique) from LinkedIn and Indeed
```

### Option 2: Command Line (Manual)

Run each server individually in separate terminals:

```bash
# Terminal 1 - Profile Server
python src/models/profile_server.py

# Terminal 2 - Job Scraper
python src/scraper/job_scraper_server.py

# Terminal 3 - Analysis Server
python src/analysis/analysis_server.py

# ... and so on
```

Then interact using MCP client or API calls.

---

## Daily Workflow

### Morning Routine (15-20 minutes)

**1. Scrape New Jobs (2-3 min)**

Via Claude Desktop:
```
"Scrape Machine Learning Engineer jobs in Munich, full-time, max 50 results"
```

Or manually:
```bash
python src/scraper/job_scraper_server.py
# Then call: scrape_jobs(...)
```

**2. Analyze Jobs (5-10 min)**

```
"Analyze all new jobs that were just scraped"
```

This runs AI analysis on each job description to extract:
- Required skills
- Nice-to-have skills
- ATS keywords
- Role category
- Experience level

**3. Match Your Profile (1-2 min)**

```
"Match my profile to all analyzed jobs"
```

This calculates match scores (0-100%) based on:
- Skills overlap (40% weight)
- Experience level (30% weight)
- Domain expertise (30% weight)

**4. Generate Resumes for High Matches (5-10 min)**

```
"Generate resumes for all jobs with match score >= 75%"
```

Resumes are saved to `./generated_resumes/`

**5. Review & Apply (Manual)**

For each generated resume:

1. **Open in Overleaf:**
   - Upload .tex file to https://overleaf.com
   - Click "Compile" to generate PDF

2. **Review for Accuracy:**
   - ✓ No fabricated information
   - ✓ All experience is real
   - ✓ Skills are accurate
   - ✓ Dates are correct

3. **Check ATS Compatibility:**
   - Use https://resumeworded.com/ats-resume-scanner
   - Or https://www.jobscan.co/

4. **Make Edits if Needed:**
   - Adjust wording
   - Reorder sections
   - Fine-tune for specific company

5. **Download PDF and Apply:**
   - Apply through company website or LinkedIn
   - Save application confirmation

**6. Track Application**

After applying:
```
"Create application for job ID abc123, resume file resume_Bosch_abc123.tex, match score 87.5, variant ml_focused"
```

---

## Advanced Features

### Custom Resume Variants

You can create different resume versions for different roles:

**Edit profile.json:**
```json
"latex_variants": {
  "ml_focused": "Developed ML models using TensorFlow...",
  "backend_focused": "Built scalable APIs with FastAPI...",
  "automotive_focused": "Applied automotive sensors (ADC, PWM)..."
}
```

The matcher automatically selects the best variant for each job.

### Filtering Jobs

**By Status:**
```
"List all jobs with status 'analyzed'"
```

**By Match Score:**
```
"List all matches with score >= 80%"
```

### Updating Application Status

As you hear back from companies:
```
"Update application abc123 status to 'interview', add note 'First round scheduled for Jan 15'"
```

Valid statuses:
- `submitted`
- `under_review`
- `interview`
- `offer`
- `rejected`
- `withdrawn`

### Statistics & Analytics

View your job search performance:
```
"Get application statistics"
```

Returns:
- Total applications
- Applications by status
- Average match score
- Interview rate
- Offer rate
- Total jobs scraped

---

## Tips & Best Practices

### Job Scraping

**DO:**
- Scrape once daily (morning is best)
- Use specific keywords ("Machine Learning Engineer" vs "Engineer")
- Target 2-3 cities to start
- Monitor Apify usage to stay within free tier

**DON'T:**
- Scrape multiple times per day (wastes API credits)
- Use overly broad keywords
- Exceed 100 jobs per day (API limits)

### AI Analysis

**DO:**
- Let Ollama warm up first (first query may be slow)
- Review AI analysis for accuracy
- Trust the ATS keyword extraction

**DON'T:**
- Analyze jobs with incomplete descriptions
- Skip validation of AI output

### Resume Generation

**DO:**
- Review EVERY resume before applying (MANDATORY)
- Use AI customization for better personalization
- Check ATS compatibility online
- Keep original highlights if AI changes meaning

**DON'T:**
- Auto-apply without review
- Trust AI blindly
- Submit without proofreading
- Ignore ATS warnings

### Application Tracking

**DO:**
- Log applications immediately after submitting
- Update status promptly
- Add notes about key details
- Review stats weekly to optimize

**DON'T:**
- Forget to track applications
- Skip notes (you'll forget details)

---

## FAQ

### Q: How much does this cost?

**A:** Essentially free:
- Apify: Free tier ($5/month credit) sufficient for daily use
- Ollama: 100% free (runs locally)
- All other components: Free and open source

### Q: Is my data private?

**A:** Yes, 100%:
- Profile data: Stored locally only
- AI processing: Runs on your machine (Ollama)
- No cloud AI services used
- Only Apify accesses internet (for job scraping only)

### Q: How long does the complete workflow take?

**A:** Breakdown:
- Job scraping: 2-3 minutes
- AI analysis: 5-10 minutes (depends on number of jobs)
- Matching: 1-2 minutes
- Resume generation: 5-10 minutes
- **Total: 15-25 minutes**

### Q: Can I use this without Ollama?

**A:** Yes, partially:
- Job scraping: Works without Ollama
- Analysis: Requires Ollama OR you can skip (won't auto-analyze)
- Matching: Works without Ollama (uses rule-based scoring)
- Resume generation: Has `use_ai_customization=false` option

### Q: What if AI generates incorrect information?

**A:** Multiple safeguards:
1. Strict validation prevents structural changes
2. Bullet point count must match original
3. Human review is MANDATORY
4. You can disable AI customization entirely

If AI output seems wrong, regenerate with `use_ai_customization=false`.

### Q: How do I update my profile?

**A:** Two options:

1. **Edit JSON directly:**
   ```bash
   nano data/profiles/profile.json
   ```

2. **Use Profile MCP Server:**
   ```
   "Update my profile personal section with email: new.email@example.com"
   ```

### Q: Can I customize the LaTeX template?

**A:** Yes! Edit `templates/resume_template.tex`

**Important:** Keep the Jinja2 placeholders ({{ }}) intact.

### Q: Jobs aren't being scraped. Why?

**Possible causes:**
1. Apify token not set or invalid
2. API rate limits exceeded
3. Network issues
4. No jobs match your criteria

**Debug:**
- Check .env file
- Verify Apify dashboard for usage
- Try broader search terms

### Q: Ollama is slow. Can I speed it up?

**A:** Yes:
1. Use GPU if available (NVIDIA with CUDA)
2. Close other applications
3. Use smaller model (llama3.1:8b is already smallest)
4. Upgrade RAM to 16GB+

### Q: Can I run this on Windows?

**A:** Yes, with some adjustments:
- Use PowerShell or WSL2
- Install Ollama for Windows
- Update file paths in config

### Q: How do I backup my data?

**A:** Backup these directories:
```bash
# Essential
data/profiles/
data/databases/

# Optional
generated_resumes/
data/preferences.json
```

Recommended: Use Git for version control.

---

## Troubleshooting

See `docs/README.md` for detailed troubleshooting guide.

**Common Issues:**
1. Ollama not running → `ollama serve`
2. Apify token not set → Edit `.env`
3. LaTeX errors → Use Overleaf
4. No jobs found → Adjust search criteria

---

## Support

**Contact:** vkrm.aditya553@gmail.com

**Documentation:**
- README: `docs/README.md`
- API Reference: `docs/API_REFERENCE.md`
- Quick Start: `QUICKSTART.md`
- Product Requirements: `PRD.md`

---

**Happy Job Hunting! 🎯**

