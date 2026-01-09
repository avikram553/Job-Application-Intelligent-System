# Product Requirements Document (PRD)
## MCP Job Application Intelligence System

---

**Document Version:** 1.0  
**Last Updated:** January 9, 2026  
**Product Owner:** Aditya Vikram  
**Status:** Planning Phase

---

## 📋 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [Problem Statement](#3-problem-statement)
4. [Goals & Objectives](#4-goals--objectives)
5. [Target Users](#5-target-users)
6. [User Stories](#6-user-stories)
7. [Product Features](#7-product-features)
8. [Technical Architecture](#8-technical-architecture)
9. [System Requirements](#9-system-requirements)
10. [Non-Functional Requirements](#10-non-functional-requirements)
11. [Development Phases](#11-development-phases)
12. [Success Metrics](#12-success-metrics)
13. [Risks & Mitigation](#13-risks--mitigation)
14. [Future Enhancements](#14-future-enhancements)
15. [Appendix](#15-appendix)

---

## 1. Executive Summary

### 1.1 Product Vision

An intelligent, privacy-preserving job application automation system that leverages local AI (Ollama/Llama 3.1) and the Model Context Protocol (MCP) to generate personalized, ATS-optimized resumes for each job opportunity, reducing manual effort while maximizing application quality.

### 1.2 Key Value Propositions

- **AI-Powered Personalization:** Each resume is uniquely tailored to the specific job description
- **Privacy-First:** All processing happens locally using Ollama (no cloud AI services)
- **ATS-Optimized:** Resumes are formatted for Applicant Tracking System compatibility
- **Time-Saving:** Automates 90% of the job application preparation process
- **Cost-Free:** No API costs (unlike ChatGPT/Claude API-based solutions)

### 1.3 High-Level Overview

```
User Upload Resume → Parse & Store Profile → Set Job Preferences
    ↓
Automated Daily Job Scraping (Apify)
    ↓
AI Analysis (Ollama) → Profile Matching → Quality Filtering (≥70% match)
    ↓
Personalized LaTeX Resume Generation → ATS Optimization
    ↓
Review & Apply → Application Tracking
```

---

## 2. Product Overview

### 2.1 Product Name
**MCP Job Application Intelligence System**

### 2.2 Product Type
Desktop application with CLI interface, built on MCP (Model Context Protocol) architecture

### 2.3 Core Functionality

1. **Profile Management:** Parse and store user resume data
2. **Job Discovery:** Automated scraping of job boards (LinkedIn, Indeed, etc.)
3. **AI Analysis:** Intelligent job description analysis using local LLM
4. **Smart Matching:** Profile-to-job matching with scoring
5. **Resume Generation:** Personalized LaTeX resume creation
6. **Application Tracking:** Monitor application status and outcomes

### 2.4 Technology Stack

- **Framework:** Model Context Protocol (MCP)
- **Language:** Python 3.10+
- **AI/LLM:** Ollama (Llama 3.1 8B)
- **Job Scraping:** Apify API
- **Database:** SQLite
- **Document Generation:** LaTeX (Overleaf-compatible)
- **Transport:** stdio (local execution)

---

## 3. Problem Statement

### 3.1 Current Pain Points

**Problem 1: Manual Resume Customization is Time-Consuming**
- Job seekers spend 30-60 minutes customizing each resume
- Applying to 50 jobs = 25-50 hours of manual work
- Leads to application fatigue and reduced quality

**Problem 2: Generic Resumes Have Low Success Rates**
- One-size-fits-all resumes poorly match specific job requirements
- ATS systems filter out non-optimized resumes (75% rejection rate)
- Keywords and skills not aligned with job descriptions

**Problem 3: Job Discovery is Inefficient**
- Manually checking multiple job boards daily
- Missing time-sensitive opportunities (jobs posted in last 24 hours)
- No systematic approach to tracking applications

**Problem 4: Privacy Concerns with Cloud AI**
- Sending resume data to ChatGPT/Claude costs $20-50/month
- Privacy risks with sensitive personal information
- Dependence on third-party services

### 3.2 User Impact

**For Aditya (Primary User):**
- Currently in Germany (Chemnitz) seeking ML Engineer roles
- Needs to apply to 50-100 jobs for visa sponsorship/job security
- Limited time due to Master's thesis and coursework
- Requires German job board integration (LinkedIn DE, Indeed DE)
- Strong preference for local AI (privacy + no costs)

---

## 4. Goals & Objectives

### 4.1 Primary Goals

**Goal 1: Reduce Application Preparation Time**
- **Target:** From 30 minutes per application to 2 minutes (review only)
- **Impact:** Save 23+ hours per 50 applications

**Goal 2: Increase Application Quality**
- **Target:** Achieve 85%+ match scores for submitted applications
- **Impact:** Higher interview callback rate

**Goal 3: Maximize Application Volume**
- **Target:** Enable applying to 50+ jobs per week
- **Impact:** Increase job opportunities 5x

**Goal 4: Ensure Privacy**
- **Target:** 100% local processing (zero cloud AI)
- **Impact:** Complete data privacy

### 4.2 Success Criteria

| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| Time per application | 30 min | <5 min | Phase 5 complete |
| Applications per week | 10 | 50+ | Phase 5 complete |
| Match score average | N/A | 85%+ | Phase 4 complete |
| Interview rate | Unknown | Track & improve | Post-launch |
| System uptime | N/A | 99%+ | Post-launch |

---

## 5. Target Users

### 5.1 Primary User Persona

**Name:** Aditya Vikram (also the product builder)

**Demographics:**
- Age: 26
- Location: Chemnitz, Germany
- Current: Master's student (Web Engineering, TU Chemnitz)
- Background: 3.7 years as Senior Software Engineer (Bosch)

**Goals:**
- Secure ML Engineer / AI Engineer role in Germany
- Maximize applications while maintaining quality
- Leverage automotive + ML background
- Stay in Germany (visa requirements)

**Pain Points:**
- Time-constrained (thesis + coursework)
- Need to apply to many jobs (visa/security)
- Generic resumes don't highlight automotive + ML combo
- Manual customization is exhausting

**Technical Proficiency:**
- Expert: Python, ML frameworks, LLMs
- Comfortable: Command-line tools, LaTeX, Git
- Familiar: MCP protocol, Ollama

### 5.2 Secondary User Personas (Future)

**Persona 2: ML/AI Job Seekers**
- Background: Technical degree + 2-5 years experience
- Goal: Career advancement in AI/ML field
- Pain: Generic resumes don't show specialization

**Persona 3: Career Changers**
- Background: Traditional engineering → ML/AI
- Goal: Pivot to AI roles
- Pain: Need to emphasize transferable skills

---

## 6. User Stories

### 6.1 Epic 1: Profile Management

**Story 1.1: Upload Resume**
```
As a user
I want to upload my existing resume (PDF/DOCX)
So that the system can parse and store my profile data

Acceptance Criteria:
- Support PDF and DOCX formats
- Extract personal info, experience, skills, education, projects
- Store in structured JSON format
- Display parsed data for verification
- Allow manual corrections if needed
```

**Story 1.2: Verify Profile**
```
As a user
I want to review parsed profile data
So that I can ensure accuracy before using it

Acceptance Criteria:
- Show all extracted sections clearly
- Allow editing of any field
- Highlight potentially incorrect extractions
- Save verified profile to database
```

**Story 1.3: Manage Profile Variants**
```
As a user
I want to create different resume variants (ML-focused, Backend-focused, etc.)
So that the system can choose the best one for each job

Acceptance Criteria:
- Create multiple variants from base profile
- Each variant emphasizes different skills/experience
- System automatically selects best variant per job
- Manual override option available
```

### 6.2 Epic 2: Job Discovery

**Story 2.1: Set Job Preferences**
```
As a user
I want to define my job search criteria
So that the system only finds relevant opportunities

Acceptance Criteria:
- Specify job titles/roles (e.g., "Machine Learning Engineer")
- Set locations (e.g., "Munich, Berlin, Stuttgart")
- Define job type (Full-time, Part-time, Remote)
- Set experience level (Entry, Mid, Senior)
- Specify must-have and exclude keywords
- Set minimum salary expectations
```

**Story 2.2: Automated Job Scraping**
```
As a user
I want the system to automatically find new jobs daily
So that I don't miss time-sensitive opportunities

Acceptance Criteria:
- Scrape LinkedIn, Indeed, Glassdoor (via Apify)
- Filter by: posted in last 24 hours
- Apply user-defined preferences
- Deduplicate job listings
- Store job details in database
- Run daily at specified time
```

### 6.3 Epic 3: Intelligent Matching

**Story 3.1: AI Job Analysis**
```
As a user
I want each job description analyzed by AI
So that the system understands what the job requires

Acceptance Criteria:
- Extract required skills from JD
- Extract nice-to-have skills
- Identify ATS keywords
- Determine role focus (ML/Backend/Full-stack)
- Extract company culture indicators
- Store analysis results
```

**Story 3.2: Profile-Job Matching**
```
As a user
I want my profile matched against each job
So that I only apply to jobs where I'm competitive

Acceptance Criteria:
- Calculate match score (0-100%)
- Compare required skills vs. my skills
- Factor in experience level
- Consider domain expertise (automotive, ML, etc.)
- Recommend best profile variant to use
- Filter out jobs below 70% match
```

### 6.4 Epic 4: Resume Generation

**Story 4.1: Personalized Resume Creation**
```
As a user
I want a customized resume generated for each high-match job
So that I maximize my chances of getting interviews

Acceptance Criteria:
- Use appropriate profile variant
- Reorder skills (matched skills first)
- Emphasize relevant experience
- Customize bullet points for the role
- Integrate ATS keywords naturally
- Generate Overleaf-compatible LaTeX
- Include metadata (job ID, match score, variant used)
```

**Story 4.2: ATS Optimization**
```
As a user
I want my resumes to pass ATS systems
So that human recruiters actually see them

Acceptance Criteria:
- Use ATS-friendly formatting (no tables, columns)
- Include relevant keywords from JD
- Standard section headers
- Proper font and spacing
- Machine-readable text
- Test with ATS checkers
```

**Story 4.3: Review Before Applying**
```
As a user
I want to review each generated resume
So that I can approve or make edits before applying

Acceptance Criteria:
- Preview generated LaTeX/PDF
- Show match score and customizations applied
- Highlight what was emphasized
- Allow manual edits in Overleaf
- Option to regenerate with different variant
- Approve to apply or skip
```

### 6.5 Epic 5: Application Tracking

**Story 5.1: Track Applications**
```
As a user
I want to track all my applications in one place
So that I can follow up appropriately

Acceptance Criteria:
- Store: Company, role, date applied, resume used
- Track status: Submitted, Under Review, Interview, Offer, Rejected
- Link to original job posting
- Notes field for follow-up reminders
- View statistics (total, pending, interviews, offers)
```

**Story 5.2: Analytics Dashboard**
```
As a user
I want to see statistics about my job search
So that I can optimize my approach

Acceptance Criteria:
- Jobs scraped per day/week
- Match rate (% of jobs above 70%)
- Applications submitted
- Interview rate
- Top matched companies
- Most requested skills
- Response time trends
```

---

## 7. Product Features

### 7.1 Core Features (Must-Have)

#### Feature 1: Profile Management System
**Description:** Parse, store, and manage user profile data

**Components:**
- Resume parser (PDF/DOCX support)
- Structured profile storage (JSON/SQLite)
- Profile verification interface
- Multiple variant support

**Technical Implementation:**
- MCP Server: Profile Server
- Tools: `parse_resume`, `get_profile_json`, `update_profile`
- Resources: `profile://me`, `profile://me/{section}`
- Storage: SQLite database

**Priority:** P0 (Must-have for MVP)

---

#### Feature 2: Automated Job Discovery
**Description:** Scrape job boards daily for new opportunities

**Components:**
- Apify integration (LinkedIn, Indeed scrapers)
- Job filtering by preferences
- Deduplication logic
- Scheduling system (daily runs)

**Technical Implementation:**
- MCP Server: Job Scraper Server
- Tools: `scrape_jobs`, `filter_jobs`, `get_job_details`
- API: Apify Client SDK
- Storage: SQLite jobs table

**Priority:** P0 (Must-have for MVP)

---

#### Feature 3: AI-Powered Job Analysis
**Description:** Analyze job descriptions using local LLM

**Components:**
- Ollama integration (Llama 3.1 8B)
- JD parsing and extraction
- Skill identification
- ATS keyword detection

**Technical Implementation:**
- MCP Server: Analysis Server
- Tools: `analyze_jd`, `extract_keywords`, `identify_ats_terms`
- LLM: Ollama (local)
- Storage: SQLite analysis table

**Priority:** P0 (Must-have for MVP)

---

#### Feature 4: Smart Profile Matching
**Description:** Match user profile against job requirements

**Components:**
- Skill overlap calculation
- Experience level matching
- Domain expertise matching (automotive, ML, etc.)
- Scoring algorithm (0-100%)

**Technical Implementation:**
- MCP Server: Matcher Server
- Tools: `match_profile`, `score_fit`, `recommend_variant`
- Algorithm: Weighted scoring (skills 40%, experience 30%, domain 30%)
- Storage: SQLite match_scores table

**Priority:** P0 (Must-have for MVP)

---

#### Feature 5: Personalized Resume Generation
**Description:** Generate customized LaTeX resumes per job

**Components:**
- LaTeX template system
- Content personalization (via Ollama)
- ATS optimization
- Overleaf compatibility

**Technical Implementation:**
- MCP Server: Document Generator Server
- Tools: `generate_resume`, `optimize_ats`, `compile_pdf`
- Template: Jinja2 + LaTeX
- Output: .tex files (Overleaf-compatible)

**Priority:** P0 (Must-have for MVP)

---

#### Feature 6: Application Tracking
**Description:** Track application status and outcomes

**Components:**
- Application database
- Status management
- Notes and follow-ups
- Basic analytics

**Technical Implementation:**
- MCP Server: Tracker Server
- Tools: `create_application`, `update_status`, `get_stats`
- Storage: SQLite applications table
- Dashboard: CLI-based statistics

**Priority:** P0 (Must-have for MVP)

---

### 7.2 Secondary Features (Should-Have)

#### Feature 7: Advanced Analytics
**Description:** Detailed insights into job search performance

**Components:**
- Visual dashboards
- Trend analysis
- Skill gap identification
- Success rate by company/role

**Priority:** P1 (Post-MVP)

---

#### Feature 8: Cover Letter Generation
**Description:** Generate personalized cover letters

**Components:**
- Cover letter templates
- AI-powered personalization
- Company research integration

**Priority:** P1 (Post-MVP)

---

#### Feature 9: Interview Preparation
**Description:** Generate interview prep materials

**Components:**
- Common questions for role
- Company research summary
- Technical topic review

**Priority:** P2 (Future enhancement)

---

#### Feature 10: Email Integration
**Description:** Auto-send applications via email

**Components:**
- Email template system
- Attachment handling
- Follow-up scheduling

**Priority:** P2 (Future enhancement)

---

### 7.3 Feature Priority Matrix

| Feature | Priority | Phase | Complexity | Impact |
|---------|----------|-------|------------|--------|
| Profile Management | P0 | 1 | Low | Critical |
| Job Discovery | P0 | 2-3 | Medium | Critical |
| AI Analysis | P0 | 4 | Medium | Critical |
| Profile Matching | P0 | 4 | Medium | Critical |
| Resume Generation | P0 | 5 | High | Critical |
| Application Tracking | P0 | 6 | Low | High |
| Advanced Analytics | P1 | 7 | Medium | Medium |
| Cover Letters | P1 | 8 | Medium | Medium |
| Interview Prep | P2 | 9 | Low | Low |
| Email Integration | P2 | 10 | High | Low |

---

## 8. Technical Architecture

### 8.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER (User)                      │
│              CLI Interface / Claude.ai Integration          │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol (stdio)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  MCP ORCHESTRATION LAYER                    │
│                   (Workflow Coordinator)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┬──────────────┐
        │                │                │              │
        ▼                ▼                ▼              ▼
┌──────────────┐  ┌─────────────┐  ┌──────────┐  ┌──────────┐
│   PROFILE    │  │     JOB     │  │ ANALYSIS │  │ DOCUMENT │
│  MCP SERVER  │  │  SCRAPER    │  │  SERVER  │  │   GEN    │
│              │  │  SERVER     │  │          │  │  SERVER  │
└──────┬───────┘  └──────┬──────┘  └────┬─────┘  └────┬─────┘
       │                 │               │             │
       │                 │               ▼             │
       │                 │         ┌──────────┐        │
       │                 │         │  OLLAMA  │        │
       │                 │         │ (Llama   │        │
       │                 │         │  3.1 8B) │        │
       │                 │         └──────────┘        │
       │                 │               │             │
       │                 ▼               │             │
       │           ┌──────────┐          │             │
       │           │  APIFY   │          │             │
       │           │   API    │          │             │
       │           └──────────┘          │             │
       │                                 │             │
       └─────────────────┬───────────────┴─────────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │   PERSISTENCE LAYER   │
             │                       │
             │  ┌─────────────────┐  │
             │  │ SQLite Database │  │
             │  │ - profiles      │  │
             │  │ - jobs          │  │
             │  │ - applications  │  │
             │  │ - match_scores  │  │
             │  └─────────────────┘  │
             │                       │
             │  ┌─────────────────┐  │
             │  │ File Storage    │  │
             │  │ - Generated     │  │
             │  │   resumes (.tex)│  │
             │  └─────────────────┘  │
             └───────────────────────┘
```

### 8.2 MCP Server Specifications

#### 8.2.1 Profile MCP Server

**Responsibility:** Manage user profile data

**Tools:**
- `get_profile_json() -> str` - Retrieve complete profile as JSON
- `update_profile(section, data, merge) -> str` - Update profile section

**Resources:**
- `profile://me` - Complete profile
- `profile://me/{section}` - Individual sections

**Storage:** SQLite table `profiles`

**Technology:** Python + FastMCP + Pydantic

---

#### 8.2.2 Job Scraper MCP Server

**Responsibility:** Discover and collect job listings

**Tools:**
- `scrape_jobs(keywords, location, job_type) -> str` - Scrape job boards
- `filter_jobs(criteria) -> str` - Filter jobs by preferences
- `get_job_details(job_id) -> str` - Retrieve specific job

**External APIs:**
- Apify LinkedIn Jobs Scraper
- Apify Indeed Jobs Scraper

**Storage:** SQLite table `jobs`

**Technology:** Python + FastMCP + Apify Client SDK

---

#### 8.2.3 Analysis MCP Server

**Responsibility:** Analyze job descriptions with AI

**Tools:**
- `analyze_jd(job_description) -> str` - Extract requirements
- `extract_keywords(text) -> str` - Identify ATS keywords
- `identify_role_type(job_description) -> str` - Classify role

**External Services:**
- Ollama API (local Llama 3.1 8B)

**Storage:** SQLite table `job_analysis`

**Technology:** Python + FastMCP + Ollama Client

---

#### 8.2.4 Matcher MCP Server

**Responsibility:** Match profile to jobs

**Tools:**
- `match_profile(profile, job_analysis) -> str` - Calculate fit
- `score_fit(profile, requirements) -> str` - Generate score (0-100)
- `recommend_variant(profile, job_analysis) -> str` - Select best variant

**Algorithm:**
```python
score = (
    skills_overlap * 0.4 +
    experience_match * 0.3 +
    domain_expertise * 0.3
)
```

**Storage:** SQLite table `match_scores`

**Technology:** Python + FastMCP + Ollama Client

---

#### 8.2.5 Document Generator MCP Server

**Responsibility:** Generate personalized resumes

**Tools:**
- `generate_resume(profile, job_analysis, variant) -> str` - Create LaTeX
- `optimize_ats(resume_content) -> str` - Optimize for ATS
- `compile_pdf(latex_file) -> str` - Generate PDF (optional)

**Template Engine:** Jinja2 + LaTeX

**Output Format:** .tex (Overleaf-compatible)

**Storage:** File system (`/generated_resumes/`)

**Technology:** Python + FastMCP + Jinja2 + LaTeX

---

#### 8.2.6 Tracker MCP Server

**Responsibility:** Track application status

**Tools:**
- `create_application(job_id, resume_file, status) -> str` - Log application
- `update_status(application_id, new_status) -> str` - Update status
- `list_applications(filters) -> str` - Query applications
- `get_stats() -> str` - Retrieve statistics

**Storage:** SQLite table `applications`

**Technology:** Python + FastMCP

---

### 8.3 Data Models

#### 8.3.1 Profile Schema

```json
{
  "personal": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "linkedin": "string",
    "github": "string"
  },
  "experience": [
    {
      "company": "string",
      "role": "string",
      "duration": "string",
      "highlights": ["string"],
      "technologies": ["string"],
      "latex_variants": {
        "ml_focused": "string",
        "backend_focused": "string",
        "automotive_focused": "string"
      }
    }
  ],
  "skills": {
    "programming_languages": ["string"],
    "ml_frameworks": ["string"],
    "backend_frameworks": ["string"],
    "cloud_platforms": ["string"],
    "automotive": ["string"],
    "languages_spoken": ["string"]
  },
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "year": "string",
      "gpa": "float"
    }
  ],
  "projects": [
    {
      "title": "string",
      "description": "string",
      "technologies": ["string"],
      "url": "string"
    }
  ],
  "metadata": {
    "created_at": "timestamp",
    "last_updated": "timestamp",
    "version": "string"
  }
}
```

#### 8.3.2 Job Schema

```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    description TEXT,
    requirements TEXT,
    posted_date TIMESTAMP,
    source TEXT,  -- "linkedin", "indeed", etc.
    url TEXT,
    scraped_at TIMESTAMP,
    status TEXT DEFAULT 'new'  -- new, analyzed, applied, skipped
);
```

#### 8.3.3 Job Analysis Schema

```sql
CREATE TABLE job_analysis (
    analysis_id TEXT PRIMARY KEY,
    job_id TEXT,
    required_skills TEXT,  -- JSON array
    nice_to_have_skills TEXT,  -- JSON array
    ats_keywords TEXT,  -- JSON array
    role_category TEXT,  -- "ML Engineer", "Backend", etc.
    experience_level TEXT,  -- "Entry", "Mid", "Senior"
    analyzed_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);
```

#### 8.3.4 Match Score Schema

```sql
CREATE TABLE match_scores (
    match_id TEXT PRIMARY KEY,
    job_id TEXT,
    profile_version TEXT,
    overall_score FLOAT,  -- 0-100
    skills_score FLOAT,
    experience_score FLOAT,
    domain_score FLOAT,
    recommended_variant TEXT,
    skills_to_emphasize TEXT,  -- JSON array
    calculated_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);
```

#### 8.3.5 Application Schema

```sql
CREATE TABLE applications (
    application_id TEXT PRIMARY KEY,
    job_id TEXT,
    resume_file TEXT,
    match_score FLOAT,
    variant_used TEXT,
    applied_date TIMESTAMP,
    status TEXT,  -- submitted, under_review, interview, offer, rejected
    notes TEXT,
    last_updated TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);
```

### 8.4 Communication Flow

#### 8.4.1 Complete Workflow Sequence

```
1. User uploads resume
   ↓
2. Profile Server: parse_resume()
   → Stores in SQLite
   ↓
3. User sets job preferences
   → Stores in config
   ↓
4. Daily trigger at 9:00 AM
   ↓
5. Job Scraper: scrape_jobs(preferences)
   → Calls Apify API
   → Stores jobs in SQLite
   ↓
6. FOR EACH scraped job:
   ↓
7. Analysis Server: analyze_jd(job.description)
   → Calls Ollama
   → Stores analysis in SQLite
   ↓
8. Matcher Server: match_profile(profile, analysis)
   → Calculates score
   → Stores match_score in SQLite
   ↓
9. IF score >= 70%:
   ↓
10. Document Generator: generate_resume(profile, analysis, variant)
    → Calls Ollama for personalization
    → Generates LaTeX file
    → Saves to file system
    ↓
11. Tracker Server: create_application(job_id, resume_file, score)
    → Stores in applications table
    ↓
12. User reviews generated resumes
    → Approves or edits
    ↓
13. User applies to job
    ↓
14. Tracker Server: update_status(application_id, "applied")
```

### 8.5 Technology Stack Details

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Framework** | MCP (Model Context Protocol) | Latest | Server communication |
| **Language** | Python | 3.10+ | Core development |
| **MCP Library** | FastMCP | Latest | MCP server implementation |
| **Validation** | Pydantic | 2.x | Input validation |
| **LLM** | Ollama (Llama 3.1) | 8B model | AI analysis & generation |
| **Job Scraping** | Apify | API v2 | Job board scraping |
| **Database** | SQLite | 3.x | Data persistence |
| **Template Engine** | Jinja2 | 3.x | LaTeX generation |
| **Document Format** | LaTeX | - | Resume format |
| **PDF Library** | PyPDF2 | Latest | Resume parsing |
| **DOCX Library** | python-docx | Latest | Resume parsing |
| **HTTP Client** | httpx | Latest | Async API calls |

---

## 9. System Requirements

### 9.1 Hardware Requirements

**Minimum:**
- CPU: 4 cores, 2.0 GHz
- RAM: 8 GB
- Storage: 10 GB free space
- GPU: Not required (CPU inference acceptable)

**Recommended:**
- CPU: 8 cores, 3.0 GHz
- RAM: 16 GB
- Storage: 20 GB free space
- GPU: NVIDIA GPU with 6GB+ VRAM (for faster Ollama inference)

### 9.2 Software Requirements

**Operating System:**
- Linux (Ubuntu 22.04+, Debian, Fedora)
- macOS (12.0+)
- Windows 10/11 with WSL2

**Dependencies:**
- Python 3.10 or higher
- Ollama installed and running
- LaTeX distribution (TeX Live or MiKTeX)
- Git

**Optional:**
- Docker (for containerized deployment)
- Overleaf account (for cloud editing)

### 9.3 Network Requirements

- Internet connection for:
  - Apify API access (job scraping)
  - Downloading Llama 3.1 model (one-time, ~4GB)
- Local network for:
  - Ollama API (localhost:11434)
  - MCP server communication (stdio, no network needed)

### 9.4 External Service Requirements

**Required:**
- Apify account (Free tier: $5 credit/month)
  - LinkedIn Jobs Scraper actor
  - Indeed Jobs Scraper actor

**Optional:**
- Overleaf account (for online LaTeX editing)

---

## 10. Non-Functional Requirements

### 10.1 Performance

**Response Times:**
- Profile parsing: < 5 seconds
- Job scraping (50 jobs): < 2 minutes
- JD analysis (single job): < 10 seconds
- Resume generation: < 30 seconds
- Database queries: < 100ms

**Throughput:**
- Process 50 jobs per run
- Generate 15-20 resumes per run (assuming 30% match rate)
- Handle daily batch operations

**Scalability:**
- Support up to 1000 jobs in database
- Support up to 500 applications tracking
- No performance degradation with growing data

### 10.2 Reliability

**Uptime:**
- Target: 99%+ for scheduled daily runs
- Graceful failure handling for API outages

**Data Integrity:**
- SQLite ACID compliance
- Automatic backups before updates
- Transaction rollback on errors

**Error Recovery:**
- Retry logic for API calls (3 attempts)
- Continue processing remaining jobs if one fails
- Log all errors for debugging

### 10.3 Security

**Data Privacy:**
- All data stored locally (no cloud storage)
- SQLite database encrypted at rest (optional)
- No personal data sent to external services (except Apify for job scraping)

**API Security:**
- Apify API key stored in environment variables
- No hardcoded credentials
- Secure key management

**Input Validation:**
- Pydantic validation for all MCP tool inputs
- SQL injection prevention (parameterized queries)
- File path validation

### 10.4 Usability

**User Interface:**
- CLI-based for Phase 1
- Clear error messages
- Progress indicators for long operations
- Color-coded output (success/warning/error)

**Documentation:**
- Installation guide
- Usage guide
- API documentation (MCP tools)
- Troubleshooting guide

**Learning Curve:**
- Technical users: < 1 hour to set up and run
- Configuration: Simple YAML/JSON files

### 10.5 Maintainability

**Code Quality:**
- Type hints throughout (Python 3.10+)
- Comprehensive docstrings
- Unit tests for critical functions
- Integration tests for MCP servers

**Modularity:**
- Each MCP server is independent
- Clear separation of concerns
- Pluggable architecture (easy to add new servers)

**Logging:**
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Separate log files per MCP server

### 10.6 Compatibility

**Python Version:**
- Minimum: Python 3.10
- Tested on: Python 3.10, 3.11, 3.12

**LaTeX Compatibility:**
- Output: Overleaf-compatible .tex files
- No custom packages required
- Standard article class

**Database:**
- SQLite 3.x (cross-platform)
- No external database server needed

---

## 11. Development Phases

### Phase 1: Profile Management (Week 1)

**Duration:** 5-7 days

**Objective:** Build profile storage and management system

**Deliverables:**
- ✅ Profile MCP Server (completed)
- ✅ Tools: `get_profile_json`, `update_profile`
- ✅ Resources: `profile://me`, `profile://me/{section}`
- ✅ JSON file-based persistence
- ✅ Pydantic input validation
- ✅ Test client
- ⚠️ API documentation (partially complete)
- ❌ Code review and refactoring (pending)

**Success Criteria:**
- Profile data can be loaded, updated, and retrieved
- All tools work correctly
- Test coverage: 80%+

**Status:** ~90% complete (Tasks 1.9, 1.10 remaining)

---

### Phase 2: Job Scraping Infrastructure (Week 2)

**Duration:** 5-7 days

**Objective:** Implement job discovery via Apify

**Deliverables:**
- Job Scraper MCP Server
- Apify integration (LinkedIn, Indeed)
- Job filtering logic
- SQLite jobs table
- Deduplication algorithm
- Scheduling system

**Tasks:**
1. Set up Apify account and API key
2. Test LinkedIn Jobs Scraper actor
3. Test Indeed Jobs Scraper actor
4. Create Job Scraper MCP Server structure
5. Implement `scrape_jobs` tool
6. Implement `filter_jobs` tool
7. Create SQLite jobs schema
8. Add deduplication logic
9. Implement daily scheduling
10. Test with real job searches

**Success Criteria:**
- Scrape 50+ jobs from LinkedIn and Indeed
- Filter jobs by user preferences
- Store jobs in database
- No duplicate entries
- Daily automation works

---

### Phase 3: User Preferences & Configuration (Week 2-3)

**Duration:** 3-4 days

**Objective:** Allow users to set job search criteria

**Deliverables:**
- Preferences configuration system
- CLI interface for setting preferences
- Preferences storage (JSON/SQLite)
- Integration with Job Scraper

**Tasks:**
1. Design preferences schema
2. Create preferences configuration CLI
3. Implement preferences storage
4. Update Job Scraper to use preferences
5. Add preference validation
6. Test preference filtering

**Success Criteria:**
- Users can set job roles, locations, keywords
- Scraping respects user preferences
- Preferences persist between runs

---

### Phase 4: AI Analysis & Matching (Week 3-4)

**Duration:** 7-10 days

**Objective:** Implement intelligent job analysis and matching

**Deliverables:**
- Analysis MCP Server
- Matcher MCP Server
- Ollama integration
- Matching algorithm
- SQLite analysis and match_scores tables

**Tasks:**
1. Install and configure Ollama
2. Download Llama 3.1 8B model
3. Create Analysis MCP Server
4. Implement `analyze_jd` tool
5. Create prompts for JD analysis
6. Test analysis accuracy
7. Create Matcher MCP Server
8. Implement matching algorithm
9. Implement `match_profile` tool
10. Test matching with real jobs
11. Tune matching thresholds

**Success Criteria:**
- Ollama analyzes JDs accurately (manual review)
- Matching algorithm achieves 85%+ accuracy
- Match scores correlate with manual assessment
- Filter threshold (70%) works effectively

---

### Phase 5: Resume Generation (Week 5-6)

**Duration:** 10-14 days

**Objective:** Generate personalized, ATS-optimized resumes

**Deliverables:**
- Document Generator MCP Server
- LaTeX templates
- Resume personalization logic
- ATS optimization
- File output system

**Tasks:**
1. Research ATS-friendly LaTeX templates
2. Create base LaTeX template (Overleaf-compatible)
3. Create Document Generator MCP Server
4. Implement `generate_resume` tool
5. Create prompts for content personalization
6. Implement skill reordering logic
7. Implement keyword integration
8. Test with sample jobs
9. ATS compatibility testing (online checkers)
10. Create validation layer (prevent AI hallucinations)
11. Implement section-by-section generation
12. Test with Aditya's real profile
13. Generate resumes for 10 sample jobs
14. Manual quality review

**Success Criteria:**
- Generated resumes are ATS-friendly (pass checkers)
- Content is personalized per job
- No fabricated information
- LaTeX compiles successfully
- Output is Overleaf-compatible
- 90%+ user satisfaction with quality

---

### Phase 6: Application Tracking (Week 6-7)

**Duration:** 5-7 days

**Objective:** Track application status and outcomes

**Deliverables:**
- Tracker MCP Server
- SQLite applications table
- Status management system
- Basic analytics/statistics

**Tasks:**
1. Create Tracker MCP Server
2. Design applications schema
3. Implement `create_application` tool
4. Implement `update_status` tool
5. Implement `list_applications` tool
6. Implement `get_stats` tool
7. Create CLI for tracking management
8. Test tracking workflow

**Success Criteria:**
- Applications are logged correctly
- Status updates work
- Statistics are accurate
- Users can query their applications

---

### Phase 7: Integration & Testing (Week 7-8)

**Duration:** 7-10 days

**Objective:** Integrate all components and test end-to-end

**Deliverables:**
- Orchestration layer
- Integration tests
- End-to-end workflow
- Bug fixes
- Documentation

**Tasks:**
1. Create orchestration script (master workflow)
2. Integrate all MCP servers
3. Test complete workflow (upload → scrape → analyze → match → generate → track)
4. Write integration tests
5. Identify and fix bugs
6. Performance optimization
7. Create user documentation
8. Create developer documentation
9. Conduct user acceptance testing (Aditya tests system)

**Success Criteria:**
- Complete workflow runs without errors
- All integration tests pass
- Performance meets requirements
- Documentation is complete
- User can run system independently

---

### Phase 8: Deployment & Monitoring (Week 8)

**Duration:** 3-5 days

**Objective:** Deploy system for daily use

**Deliverables:**
- Installation script
- Configuration guide
- Monitoring system
- Backup strategy

**Tasks:**
1. Create installation script
2. Set up daily cron job / scheduler
3. Configure logging
4. Implement backup system
5. Create monitoring dashboard (CLI-based)
6. Deploy to production (Aditya's local machine)
7. Test daily automation

**Success Criteria:**
- System runs automatically daily
- Logs are accessible and useful
- Backups are created
- Monitoring alerts work

---

### Development Timeline Summary

```
Week 1:   [████████████████████] Phase 1: Profile Management (90% done)
Week 2:   [░░░░░░░░░░░░░░░░░░░░] Phase 2: Job Scraping
Week 2-3: [░░░░░░░░░░░░░░░░░░░░] Phase 3: Preferences
Week 3-4: [░░░░░░░░░░░░░░░░░░░░] Phase 4: AI Analysis & Matching
Week 5-6: [░░░░░░░░░░░░░░░░░░░░] Phase 5: Resume Generation
Week 6-7: [░░░░░░░░░░░░░░░░░░░░] Phase 6: Application Tracking
Week 7-8: [░░░░░░░░░░░░░░░░░░░░] Phase 7: Integration & Testing
Week 8:   [░░░░░░░░░░░░░░░░░░░░] Phase 8: Deployment

Total: 8 weeks (2 months)
```

---

## 12. Success Metrics

### 12.1 Development Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Phase Completion** | 8/8 phases | Deliverables checklist |
| **Code Coverage** | 80%+ | pytest coverage report |
| **Bug Count** | < 10 critical bugs | GitHub Issues tracker |
| **Documentation** | 100% API coverage | Manual review |

### 12.2 Product Metrics

| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| **Time per Application** | 30 min | < 5 min | Phase 8 |
| **Applications per Week** | 10 | 50+ | Phase 8 |
| **Match Score Average** | N/A | 85%+ | Phase 5 |
| **Resume Quality (User Rating)** | N/A | 4.5/5 | Phase 5 |

### 12.3 System Performance Metrics

| Metric | Target | Actual (Track Post-Launch) |
|--------|--------|---------------------------|
| **Job Scraping Speed** | < 2 min for 50 jobs | TBD |
| **Analysis Speed** | < 10 sec per job | TBD |
| **Resume Generation Speed** | < 30 sec | TBD |
| **Daily Uptime** | 99%+ | TBD |
| **Error Rate** | < 1% | TBD |

### 12.4 Job Search Outcome Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Interview Rate** | Track & improve | % of applications → interviews |
| **Response Rate** | Track & improve | % of applications with response |
| **Time to Interview** | Track | Days from application to interview |
| **Offer Rate** | Track | % of interviews → offers |

**Note:** Outcome metrics will be tracked post-launch to optimize the system over time.

---

## 13. Risks & Mitigation

### 13.1 Technical Risks

#### Risk 1: Apify API Rate Limits or Downtime
**Probability:** Medium  
**Impact:** High  
**Mitigation:**
- Stay within free tier limits ($5 credit/month)
- Implement retry logic with exponential backoff
- Cache job listings to reduce API calls
- Consider scraping only once per day (not multiple times)
- Fallback: Manual job entry if Apify fails

---

#### Risk 2: Ollama Performance Issues (Slow Inference)
**Probability:** Medium  
**Impact:** Medium  
**Mitigation:**
- Use Llama 3.1 8B (lighter model)
- Optimize prompts to reduce token count
- Consider GPU acceleration if available
- Batch processing to amortize overhead
- Fallback: Use simpler rule-based analysis

---

#### Risk 3: LaTeX Compilation Errors
**Probability:** Low  
**Impact:** Medium  
**Mitigation:**
- Use well-tested, standard LaTeX templates
- Validate all dynamic content before insertion
- Escape special LaTeX characters
- Provide clear error messages
- Fallback: Output raw .tex file for manual fixing

---

#### Risk 4: ATS Compatibility Issues
**Probability:** Medium  
**Impact:** High (resumes not read by ATS)  
**Mitigation:**
- Research ATS best practices
- Use ATS checker tools during development
- Avoid tables, columns, fancy formatting
- Test with real job applications
- Iterate based on feedback

---

#### Risk 5: AI Hallucinations (Fabricated Information)
**Probability:** High  
**Impact:** Critical (career damage)  
**Mitigation:**
- Use strict LaTeX templates (fixed structure)
- Validate all AI output against original profile
- Section-by-section generation (limit AI scope)
- Pydantic validation (block unauthorized sections)
- Human review before every application (mandatory)

---

### 13.2 Product Risks

#### Risk 6: Low Match Rate (< 30%)
**Probability:** Medium  
**Impact:** High (few resumes generated)  
**Mitigation:**
- Tune matching algorithm thresholds
- Expand job search criteria
- Improve skill matching logic
- Consider lowering threshold to 65% (with user approval)

---

#### Risk 7: Poor Resume Quality
**Probability:** Medium  
**Impact:** High (low interview rate)  
**Mitigation:**
- Iterate on LaTeX templates
- Refine AI personalization prompts
- A/B test different templates
- Get feedback from recruiters/HR professionals
- Continuous improvement based on outcomes

---

#### Risk 8: User Doesn't Review Resumes (Auto-Apply)
**Probability:** Low  
**Impact:** Critical (mistakes in applications)  
**Mitigation:**
- Make review mandatory (no auto-apply feature)
- Show clear summary of customizations made
- Highlight match score and reasoning
- Provide easy editing in Overleaf

---

### 13.3 Business/Legal Risks

#### Risk 9: Apify API Costs Exceed Budget
**Probability:** Low  
**Impact:** Low (can pause system)  
**Mitigation:**
- Monitor API usage closely
- Stay within free tier ($5/month)
- Optimize scraping (scrape once daily, not more)
- Fallback: Manual job search

---

#### Risk 10: Web Scraping Legal Issues
**Probability:** Low  
**Impact:** Medium  
**Mitigation:**
- Use Apify (compliant scraping service)
- Respect robots.txt and rate limits
- Only scrape public job postings
- Do not scrape personal data
- Review Apify's terms of service

---

#### Risk 11: Resume Data Privacy Concerns
**Probability:** Low  
**Impact:** High (if data leaked)  
**Mitigation:**
- All processing is local (no cloud)
- SQLite database on local machine only
- No external services except Apify (for job listings)
- Encrypt database at rest (optional)
- User controls all data

---

### Risk Matrix

```
Impact →
        Low         Medium      High        Critical
High    Risk 5      Risk 9      Risk 1      Risk 5
        (Apify)     (Costs)     (Apify)     (AI Halluc)
        
Medium  -           Risk 2      Risk 4      Risk 7
                    (Ollama)    (ATS)       (Quality)
                    Risk 6
                    (Match Rate)
        
Low     -           Risk 3      Risk 8      -
                    (LaTeX)     (No Review)
```

**Priority Mitigation Order:**
1. Risk 5 (AI Hallucinations) - Critical
2. Risk 8 (No Review) - Critical
3. Risk 7 (Resume Quality) - High
4. Risk 4 (ATS Compatibility) - High
5. Risk 1 (Apify Downtime) - High

---

## 14. Future Enhancements

### 14.1 Phase 9: Advanced Features (Post-MVP)

**Feature 1: Web Interface**
- Replace CLI with web UI (Flask/FastAPI)
- Drag-and-drop resume upload
- Visual resume preview
- Dashboard with charts

**Feature 2: Cover Letter Generation**
- Generate personalized cover letters
- Company research integration
- Multi-language support (German cover letters)

**Feature 3: LinkedIn Auto-Apply**
- Browser automation (Playwright)
- Auto-fill application forms
- Easy Apply integration

**Feature 4: Email Integration**
- Send applications via email
- Auto-follow-up after 1-2 weeks
- Track email opens/responses

**Feature 5: Interview Prep**
- Generate common interview questions for role
- Company research summaries
- Technical topic review guides

### 14.2 Phase 10: Multi-User Support

**Feature 6: User Accounts**
- Support multiple users on same machine
- Separate profiles and applications
- User authentication

**Feature 7: Cloud Sync (Optional)**
- Sync data across devices (encrypted)
- Mobile app for tracking on-the-go
- Browser extension

### 14.3 Phase 11: Advanced Analytics

**Feature 8: ML-Powered Insights**
- Predict interview likelihood
- Identify skill gaps
- Recommend skill development
- Salary insights

**Feature 9: A/B Testing**
- Test different resume variants
- Track which templates get more callbacks
- Optimize based on data

### 14.4 Phase 12: Community Features

**Feature 10: Template Marketplace**
- Share LaTeX templates with community
- Download templates from others
- Rate and review templates

**Feature 11: Success Stories**
- Track job offers
- Share success strategies
- Community support forum

---

## 15. Appendix

### 15.1 Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - Framework for AI agent communication |
| **ATS** | Applicant Tracking System - Software used by companies to filter resumes |
| **Ollama** | Local LLM runtime for running models like Llama |
| **Apify** | Web scraping platform with pre-built scrapers |
| **LaTeX** | Document preparation system for high-quality typesetting |
| **Overleaf** | Online LaTeX editor (cloud-based) |
| **JD** | Job Description |
| **LLM** | Large Language Model (e.g., Llama 3.1, GPT-4) |
| **stdio** | Standard input/output (MCP transport method) |
| **Profile Variant** | Different versions of resume emphasizing different skills |

### 15.2 References

**MCP Documentation:**
- https://modelcontextprotocol.io/

**Ollama Documentation:**
- https://ollama.ai/

**Apify Documentation:**
- https://docs.apify.com/

**LaTeX Resources:**
- https://www.overleaf.com/learn
- https://www.latex-project.org/

**ATS Optimization:**
- https://www.jobscan.co/ats-resume-guide
- https://resumeworded.com/ats-resume-scanner

### 15.3 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-09 | Aditya Vikram | Initial PRD creation |

### 15.4 Approval

**Product Owner:** Aditya Vikram  
**Status:** Draft - Pending Final Review

---

**END OF DOCUMENT**

---

## Quick Reference

### Key Metrics to Track
- Time per application: Target < 5 min
- Applications per week: Target 50+
- Match score average: Target 85%+
- Interview rate: Track & optimize

### Critical Success Factors
1. ✅ AI doesn't fabricate information (validation layers)
2. ✅ Resumes pass ATS systems (testing & optimization)
3. ✅ System runs reliably daily (automation & monitoring)
4. ✅ Resume quality is high (user satisfaction 4.5+/5)
5. ✅ Complete privacy (local processing only)

### Risk Priorities
1. **Critical:** AI hallucinations → Strict validation
2. **Critical:** No review before apply → Mandatory review
3. **High:** ATS compatibility → Testing & iteration
4. **High:** Resume quality → Continuous improvement
5. **High:** Apify downtime → Fallback mechanisms

---

**For questions or clarifications, contact:**  
Aditya Vikram  
vkrm.aditya553@gmail.com