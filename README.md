# MCP Job Application Intelligence System

**AI-Powered Job Application Automation with Privacy & Safety**

[![Status](https://img.shields.io/badge/status-production%20ready-success)](PROJECT_SUMMARY.md)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple)](https://modelcontextprotocol.io)
[![Privacy](https://img.shields.io/badge/privacy-100%25%20local-green)](#privacy-first)

---

## 🚀 Quick Start (10 Minutes)

```bash
# 1. Install dependencies
chmod +x setup.sh
./setup.sh

# 2. Activate environment
source .venv/bin/activate

# 3. Configure API token (get from https://apify.com)
echo "APIFY_API_TOKEN=your_token_here" >> .env

# 4. Install Ollama and AI model
# Download from https://ollama.ai
ollama serve &
ollama pull llama3.1:8b

# 5. Set job preferences
python cli_set_preferences.py

# 6. Test system
python tests/test_system.py

# 7. Run workflow
python orchestrator.py --workflow
```

**Full guide:** [QUICKSTART.md](QUICKSTART.md)

---

## 📖 What Is This?

An intelligent system that automates 90% of job application preparation while maintaining complete privacy and preventing AI from fabricating information.

### Key Features

- ✅ **Automated Job Discovery:** Scrapes LinkedIn & Indeed daily
- ✅ **AI Analysis:** Analyzes job descriptions using local AI (Ollama)
- ✅ **Smart Matching:** Calculates profile-to-job fit scores
- ✅ **Personalized Resumes:** Generates ATS-optimized LaTeX resumes
- ✅ **Application Tracking:** Monitors status and provides statistics
- ✅ **100% Privacy:** All processing happens locally (no cloud AI)
- ✅ **Hallucination Prevention:** Strict validation prevents AI from inventing information

---

## 🏗️ Architecture

**6 Independent MCP Servers:**

```
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│   Profile   │  │ Job Scraper  │  │   Analysis   │
│   Server    │  │    Server    │  │    Server    │
└─────────────┘  └──────────────┘  └──────────────┘
       ↓                ↓                  ↓
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│   Matcher   │  │   Document   │  │   Tracker    │
│   Server    │  │  Generator   │  │    Server    │
└─────────────┘  └──────────────┘  └──────────────┘
```

**Each server is independent and can be used standalone or together.**

---

## 💼 Use Case: Daily Job Search

**Morning (15 min):**
1. Scrape new jobs matching your criteria
2. AI analyzes each job description
3. System matches your profile and scores fit
4. Generates personalized resumes for top matches (≥70%)

**Review (30 min):**
5. You review generated resumes (MANDATORY)
6. Apply to jobs manually
7. Track applications in the system

**Result:** Apply to 50+ targeted jobs per week with minimal effort.

---

## 🛡️ Privacy & Safety

### Privacy-First Design

- **100% Local AI:** Uses Ollama (Llama 3.1) - no cloud AI services
- **Local Storage:** All data in SQLite on your machine
- **No Data Sharing:** Profile never sent to external services
- **Exception:** Apify API (only for scraping public job postings)

### Hallucination Prevention

**5 Layers of Protection:**
1. Fixed LaTeX templates (AI can't modify structure)
2. Constrained prompts (strict rules)
3. Structure validation (rejects unauthorized changes)
4. Pydantic validation (type checking)
5. **Mandatory human review** before applying

**You are always in control. The system never auto-applies.**

---

## 📚 Documentation

**Essential Guides:**
- [QUICKSTART.md](QUICKSTART.md) - Get started in 10 minutes
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - Complete usage guide
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API documentation
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Implementation details
- [PRD.md](PRD.md) - Product requirements

**For Developers:**
- Architecture documentation in `docs/README.md`
- Code comments in each MCP server
- Test suite in `tests/test_system.py`

---

## 🔧 Requirements

### Software
- Python 3.10 or higher
- Ollama (for local AI)
- LaTeX distribution (optional, for local PDF generation)

### Services
- Apify account (free tier - $5/month credit)

### Hardware
**Minimum:**
- CPU: 4 cores, 2.0 GHz
- RAM: 8 GB
- Storage: 10 GB

**Recommended:**
- CPU: 8 cores, 3.0 GHz
- RAM: 16 GB
- GPU: NVIDIA with 6GB+ VRAM (optional, for faster AI)

---

## 🎯 System Components

### 1. Profile Server
Manages your profile data with multiple variants for different roles.

**Usage:**
```python
# Via Claude Desktop or MCP client
get_profile_json()
update_profile(section="personal", data={...})
```

### 2. Job Scraper Server
Scrapes LinkedIn and Indeed for relevant jobs.

**Usage:**
```python
scrape_jobs(
    keywords="Machine Learning Engineer",
    location="Munich, Germany",
    max_results=50
)
```

### 3. Analysis Server
Analyzes job descriptions using local AI to extract requirements.

**Usage:**
```python
analyze_jd(job_id="abc123")
```

### 4. Matcher Server
Matches your profile to jobs with intelligent scoring.

**Usage:**
```python
match_profile(job_id="abc123")
# Returns: { "overall_score": 87.5, ... }
```

### 5. Document Generator Server
Generates personalized, ATS-optimized LaTeX resumes.

**Usage:**
```python
generate_resume(
    job_id="abc123",
    use_ai_customization=true
)
```

### 6. Tracker Server
Tracks application status and provides analytics.

**Usage:**
```python
create_application(job_id="abc123", ...)
update_status(application_id="...", new_status="interview")
get_stats()
```

---

## 📊 Expected Results

### Time Savings
- **Before:** 30 min per application = 25 hours for 50 applications
- **After:** 5 min per application = 4 hours for 50 applications
- **Savings:** 21 hours/week

### Quality Improvements
- Every resume personalized to job requirements
- ATS-optimized format (higher pass rate)
- Consistent quality across all applications
- No missed opportunities

---

## 🔍 How It Works

### Complete Workflow

```
1. Set Preferences → What roles/locations you want

2. Scrape Jobs → System finds relevant postings daily
           ↓
3. AI Analysis → Ollama extracts job requirements
           ↓
4. Match Profile → Calculates fit score (0-100%)
           ↓
5. Generate Resume → Creates personalized LaTeX for high matches
           ↓
6. Human Review → YOU review and approve (MANDATORY)
           ↓
7. Apply → You apply manually (system doesn't auto-apply)
           ↓
8. Track → System tracks status and statistics
```

---

## ⚙️ Configuration

### Job Preferences

```bash
python cli_set_preferences.py
```

Set:
- Target roles (e.g., "ML Engineer", "AI Engineer")
- Locations (e.g., "Munich", "Berlin")
- Salary requirements
- Must-have keywords
- Exclude keywords
- Match threshold (default: 70%)

### Environment Variables

```bash
# .env file
APIFY_API_TOKEN=your_token_here
OLLAMA_URL=http://localhost:11434/api/generate
```

---

## 🧪 Testing

```bash
# Run validation suite
python tests/test_system.py

# Expected output:
# ✓ Imports OK
# ✓ Directories OK
# ✓ Profile OK
# ✓ Preferences OK
# ✓ LaTeX Template OK
# ✓ Ollama connection OK
# ✓ Database OK
# Tests Passed: 8/8
```

---

## 📈 Monitoring Progress

```bash
# View statistics
python orchestrator.py --stats

# Or via Tracker Server:
get_stats()

# Returns:
# - Total applications
# - Applications by status
# - Average match score
# - Interview rate
# - Offer rate
```

---

## 🤝 Integration with Claude Desktop

**1. Copy server configuration:**
```bash
# Copy claude_desktop_config.json to Claude's config directory
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/
```

**2. Restart Claude Desktop**

**3. Use in conversations:**
```
"Scrape Machine Learning Engineer jobs in Munich"
"Analyze all new jobs"
"Match my profile to analyzed jobs"
"Generate resumes for matches above 80%"
```

---

## 🚨 Important Notes

### What This System Does

✅ Automates job discovery and resume customization
✅ Saves you 20+ hours per week
✅ Maintains complete privacy
✅ Ensures ATS compatibility
✅ Tracks applications systematically

### What This System Does NOT Do

❌ Auto-apply to jobs (requires your manual review & submission)
❌ Guarantee job offers (improves your chances)
❌ Fabricate experience or skills (strict validation)
❌ Replace human judgment (you review everything)

---

## 💡 Tips for Success

1. **Run daily:** Scrape jobs every morning for fresh postings
2. **Review thoroughly:** Always verify AI-generated content
3. **Track everything:** Log all applications immediately
4. **Adjust preferences:** Fine-tune based on results
5. **Monitor stats:** Review weekly to optimize approach

---

## 🐛 Troubleshooting

### Common Issues

**"Ollama not running"**
```bash
ollama serve
ollama pull llama3.1:8b
```

**"No jobs found"**
- Check Apify token in `.env`
- Verify search criteria
- Check Apify dashboard for usage

**"LaTeX errors"**
- Use Overleaf (https://overleaf.com) for easier editing
- Check for special characters in profile data

**Full troubleshooting guide:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md#troubleshooting)

---

## 📦 Project Structure

```
Job Application Intelligence System/
├── src/                      # MCP Servers
│   ├── models/               # Profile server
│   ├── scraper/              # Job scraper
│   ├── analysis/             # AI analysis
│   ├── matcher/              # Profile matching
│   ├── generator/            # Resume generation
│   └── tracker/              # Application tracking
├── templates/                # LaTeX templates
├── docs/                     # Documentation
├── data/                     # Database & profiles
├── generated_resumes/        # Output directory
├── tests/                    # Test suite
├── orchestrator.py           # Workflow coordinator
├── cli_set_preferences.py    # Preferences CLI
├── setup.sh                  # Installation script
└── README.md                 # This file
```

---

## 🎓 Learn More

**Video Tutorials:** (Coming soon)
**Blog Posts:** (Coming soon)

**Contact:** vkrm.aditya553@gmail.com

---

## 📜 License

Personal Use License - Created for Aditya Vikram's job search.
Not for redistribution without permission.

---

## 🙏 Acknowledgments

- **MCP Framework:** Anthropic's Model Context Protocol
- **AI Model:** Meta's Llama 3.1 via Ollama
- **Job Scraping:** Apify platform
- **Development:** Claude Sonnet 4.5 (AI Assistant)

---

## 🚀 Status

**Version:** 1.0.0
**Status:** Production Ready ✅
**Last Updated:** January 9, 2026

**Ready to transform your job search? Get started with [QUICKSTART.md](QUICKSTART.md)**

---

**Made with 🤖 for 🎯 by Aditya Vikram**

