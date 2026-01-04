# Complete MCP Job Application System - Architecture & Flow

## 🎯 System Goal

**Input:** User's basic resume (PDF/DOCX)  
**Process:** Scrape jobs from last 24 hours, analyze, personalize  
**Output:** ATS-friendly Overleaf resume tailored to each job description

---

## 📊 HIGH-LEVEL SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     USER INTERACTION LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User uploads resume (PDF/DOCX) ──────────────────────┐                │
│                                                        │                │
│  User sets preferences (job types, locations, etc.)   │                │
│                                                        ▼                │
└────────────────────────────────────────────────────────┬────────────────┘
                                                         │
                                                         │
┌────────────────────────────────────────────────────────▼────────────────┐
│                         MCP ORCHESTRATION LAYER                         │
│                         (Main Coordinator)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Master Workflow Controller                                     │   │
│  │  - Coordinates all MCP servers                                  │   │
│  │  - Manages state transitions                                    │   │
│  │  - Handles errors and retries                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
┌──────────────────────┐  ┌─────────────────┐  ┌────────────────────┐
│  PROFILE MCP SERVER  │  │  JOB SCRAPER    │  │  DOCUMENT GEN      │
│                      │  │  MCP SERVER     │  │  MCP SERVER        │
├──────────────────────┤  ├─────────────────┤  ├────────────────────┤
│ • Extract resume     │  │ • Web scraping  │  │ • LaTeX generation │
│ • Parse skills       │  │ • Job boards    │  │ • ATS optimization │
│ • Store profile      │  │ • Filter jobs   │  │ • Overleaf format  │
│ • Manage variants    │  │ • 24hr filter   │  │ • Personalization  │
└──────────┬───────────┘  └────────┬────────┘  └─────────┬──────────┘
           │                       │                      │
           └───────────┬───────────┴──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       ANALYSIS & MATCHING LAYER                         │
│                       (AI-Powered with Ollama)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │  JD Analyzer     │  │  Profile Matcher │  │  Content Generator│    │
│  │  (Ollama LLM)    │  │  (Ollama LLM)    │  │  (Ollama LLM)     │    │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤     │
│  │ • Parse JD       │  │ • Match skills   │  │ • Personalized   │     │
│  │ • Extract reqs   │  │ • Score fit      │  │   bullets        │     │
│  │ • Identify keys  │  │ • Recommend      │  │ • Keywords       │     │
│  │ • ATS keywords   │  │   variant        │  │ • Achievements   │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          STORAGE LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Profile DB  │  │ Jobs DB      │  │ Applications │  │ Generated   │ │
│  │ (SQLite)    │  │ (SQLite)     │  │ DB (SQLite)  │  │ Resumes     │ │
│  └─────────────┘  └──────────────┘  └──────────────┘  └─────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          OUTPUT LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  • ATS-friendly LaTeX resume (Overleaf compatible)                     │
│  • Personalized cover letter (optional)                                │
│  • Application tracking metadata                                       │
│  • Match score and recommendations                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 COMPLETE WORKFLOW - SEQUENCE DIAGRAM

```
USER              ORCHESTRATOR         PROFILE-SERVER      JOB-SCRAPER       OLLAMA-AI        DOCGEN-SERVER      OUTPUT
 │                     │                    │                   │                │                 │              │
 │ 1. Upload Resume    │                    │                   │                │                 │              │
 ├────────────────────►│                    │                   │                │                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │ 2. Extract Profile │                   │                │                 │              │
 │                     ├───────────────────►│                   │                │                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │                    │ 3. Parse Resume   │                │                 │              │
 │                     │                    │   (Extract text,  │                │                 │              │
 │                     │                    │    skills, exp)   │                │                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │ 4. Profile Stored  │                   │                │                 │              │
 │                     │◄───────────────────┤                   │                │                 │              │
 │                     │                    │                   │                │                 │              │
 │ 5. Set Preferences  │                    │                   │                │                 │              │
 │ (ML Engineer,       │                    │                   │                │                 │              │
 │  Germany, last 24h) │                    │                   │                │                 │              │
 ├────────────────────►│                    │                   │                │                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │ 6. Scrape Jobs     │                   │                │                 │              │
 │                     ├───────────────────────────────────────►│                │                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │                    │                   │ 7. Query job   │                 │              │
 │                     │                    │                   │    boards      │                 │              │
 │                     │                    │                   │  (LinkedIn,    │                 │              │
 │                     │                    │                   │   Indeed, etc) │                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │ 8. Jobs Found (50) │                   │                │                 │              │
 │                     │◄───────────────────────────────────────┤                │                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │ FOR EACH JOB (Loop starts)             │                │                 │              │
 │                     │ ─────────────────────────────────────────────────────────────────────────────────────── │
 │                     │                    │                   │                │                 │              │
 │                     │ 9. Analyze Job Description             │                │                 │              │
 │                     ├───────────────────────────────────────────────────────►│                 │              │
 │                     │                    │                   │                │                 │              │
 │                     │                    │                   │                │ 10. Extract:   │              │
 │                     │                    │                   │                │  • Required    │              │
 │                     │                    │                   │                │    skills      │              │
 │                     │                    │                   │                │  • Keywords    │              │
 │                     │                    │                   │                │  • ATS terms   │              │
 │                     │                    │                   │                │  • Role type   │              │
 │                     │                    │                   │                │                │              │
 │                     │ 11. JD Analysis    │                   │                │                │              │
 │                     │◄───────────────────────────────────────────────────────┤                │              │
 │                     │                    │                   │                │                │              │
 │                     │ 12. Match Profile  │                   │                │                │              │
 │                     ├────────────────────┼──────────────────────────────────►│                │              │
 │                     │    (Send profile + │                   │                │                │              │
 │                     │     JD analysis)   │                   │                │                │              │
 │                     │                    │                   │                │                │              │
 │                     │                    │                   │                │ 13. Calculate: │              │
 │                     │                    │                   │                │  • Match score │              │
 │                     │                    │                   │                │  • Best variant│              │
 │                     │                    │                   │                │  • Key skills  │              │
 │                     │                    │                   │                │    to highlight│              │
 │                     │                    │                   │                │                │              │
 │                     │ 14. Match Result   │                   │                │                │              │
 │                     │    (85% match,     │                   │                │                │              │
 │                     │     use ML variant)│                   │                │                │              │
 │                     │◄───────────────────────────────────────────────────────┤                │              │
 │                     │                    │                   │                │                │              │
 │                     │ 15. IF match >= 70% THEN Generate Resume               │                │              │
 │                     │ ───────────────────────────────────────────────────────────────────────►│              │
 │                     │    (Send: profile, │                   │                │                │              │
 │                     │     variant,       │                   │                │                │              │
 │                     │     JD analysis,   │                   │                │                │              │
 │                     │     keywords)      │                   │                │                │              │
 │                     │                    │                   │                │                │              │
 │                     │                    │                   │                │                │ 16. Build:  │
 │                     │                    │                   │                │                │  • LaTeX    │
 │                     │                    │                   │                │                │    template │
 │                     │                    │                   │                │                │  • Insert   │
 │                     │                    │                   │                │                │    profile  │
 │                     │                    │                   │                │                │  • Add ATS  │
 │                     │                    │                   │                │                │    keywords │
 │                     │                    │                   │                │                │  • Optimize │
 │                     │                    │                   │                │                │    format   │
 │                     │                    │                   │                │                │             │
 │                     │ 17. Resume Generated                   │                │                │              │
 │                     │    (LaTeX file)    │                   │                │                │              │
 │                     │◄───────────────────────────────────────────────────────────────────────┤              │
 │                     │                    │                   │                │                │              │
 │                     │ 18. Store Application                  │                │                │              │
 │                     ├───────────────────►│                   │                │                │              │
 │                     │    (Job, Resume,   │                   │                │                │              │
 │                     │     Match score,   │                   │                │                │              │
 │                     │     Status)        │                   │                │                │              │
 │                     │                    │                   │                │                │              │
 │                     │ END LOOP ───────────────────────────────────────────────────────────────────────────── │
 │                     │                    │                   │                │                │              │
 │                     │ 19. Compile Results│                   │                │                │              │
 │                     │    (Generated 15   │                   │                │                │              │
 │                     │     resumes out of │                   │                │                │              │
 │                     │     50 jobs)       │                   │                │                │              │
 │                     │                    │                   │                │                │              │
 │ 20. Output Package  │                    │                   │                │                │              │
 │◄────────────────────┤                    │                   │                │                │              │
 │  • Resume files     │                    │                   │                │                │              │
 │  • Match scores     │                    │                   │                │                │              │
 │  • Recommendations  │                    │                   │                │                │              │
 │                     │                    │                   │                │                │              │
```

---

## 🔄 STATE DIAGRAM - Application Lifecycle

```
                        ┌──────────────────┐
                        │   USER UPLOADS   │
                        │     RESUME       │
                        └─────────┬────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │  STATE: PARSING  │
                        │                  │
                        │ • Extract text   │
                        │ • Parse sections │
                        │ • Build profile  │
                        └─────────┬────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │ STATE: READY     │
                        │                  │
                        │ Profile stored,  │
                        │ awaiting job     │
                        │ preferences      │
                        └─────────┬────────┘
                                  │
                                  │ User sets preferences
                                  │ (roles, location, etc.)
                                  ▼
                        ┌──────────────────┐
                        │ STATE: SCRAPING  │
                        │                  │
                        │ • Query job      │
                        │   boards         │
                        │ • Filter by date │
                        │ • Collect JDs    │
                        └─────────┬────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │ STATE: ANALYZING │
                        │                  │
                        │ FOR EACH JOB:    │
                        │ ┌──────────────┐ │
                        │ │ Parse JD     │ │
                        │ └──────┬───────┘ │
                        │        ▼         │
                        │ ┌──────────────┐ │
                        │ │ Match skills │ │
                        │ └──────┬───────┘ │
                        │        ▼         │
                        │ ┌──────────────┐ │
                        │ │ Score fit    │ │
                        │ └──────────────┘ │
                        └─────────┬────────┘
                                  │
                        ┌─────────┴─────────┐
                        │                   │
                 Match < 70%         Match >= 70%
                        │                   │
                        ▼                   ▼
              ┌─────────────────┐ ┌─────────────────┐
              │ STATE: SKIPPED  │ │STATE: GENERATING│
              │                 │ │                 │
              │ Job not a good  │ │ • Select variant│
              │ fit - archived  │ │ • Build LaTeX   │
              │                 │ │ • Add keywords  │
              └─────────────────┘ │ • Optimize ATS  │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │STATE: GENERATED │
                                  │                 │
                                  │ Resume ready    │
                                  │ for download    │
                                  └────────┬────────┘
                                           │
                                           │ User reviews
                                           │
                                  ┌────────┴────────┐
                                  │                 │
                          User approves      User edits
                                  │                 │
                                  ▼                 ▼
                        ┌─────────────────┐ ┌─────────────────┐
                        │ STATE: APPROVED │ │ STATE: EDITING  │
                        │                 │ │                 │
                        │ Ready to apply  │ │ User modifies   │
                        └────────┬────────┘ │ in Overleaf     │
                                 │          └────────┬────────┘
                                 │                   │
                                 └─────────┬─────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │ STATE: APPLIED  │
                                  │                 │
                                  │ Application     │
                                  │ submitted       │
                                  └────────┬────────┘
                                           │
                                           ▼
                        ┌──────────────────────────────┐
                        │      TRACKING STATES         │
                        ├──────────────────────────────┤
                        │                              │
                        │ • SUBMITTED                  │
                        │      ↓                       │
                        │ • UNDER_REVIEW               │
                        │      ↓                       │
                        │ • INTERVIEW_SCHEDULED        │
                        │      ↓                       │
                        │ • OFFER / REJECTED           │
                        │                              │
                        └──────────────────────────────┘
```

---

## 🎯 DATA FLOW DIAGRAM

```
┌─────────────┐
│   RESUME    │
│  (PDF/DOCX) │
└──────┬──────┘
       │
       │ Upload
       ▼
┌────────────────────────────────┐
│  EXTRACTION & PARSING          │
│  ─────────────────────────     │
│  Tools:                        │
│  • PyPDF2 / python-docx        │
│  • Text extraction             │
│  • Section identification      │
└───────────────┬────────────────┘
                │
                ▼
         ┌──────────────┐
         │   PROFILE    │
         │     DATA     │
         │              │
         │ {            │
         │   personal,  │
         │   experience,│
         │   skills,    │
         │   education  │
         │ }            │
         └──────┬───────┘
                │
                │ Store
                ▼
         ┌──────────────┐          ┌─────────────────┐
         │  PROFILE DB  │          │  USER PREFS     │
         │              │          │                 │
         │  SQLite      │          │ • Roles         │
         └──────────────┘          │ • Locations     │
                │                  │ • Keywords      │
                │                  └────────┬────────┘
                │                           │
                │                           │
                └────────────┬──────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   JOB SCRAPER       │
                  │   ────────────      │
                  │   Sources:          │
                  │   • LinkedIn API    │
                  │   • Indeed Scraping │
                  │   • Company sites   │
                  │                     │
                  │   Filter:           │
                  │   • Last 24 hours   │
                  │   • Match prefs     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   JOB POSTINGS      │
                  │   ────────────      │
                  │   [                 │
                  │     {               │
                  │       title,        │
                  │       company,      │
                  │       description,  │
                  │       requirements, │
                  │       posted_date   │
                  │     },              │
                  │     ...             │
                  │   ]                 │
                  └──────────┬──────────┘
                             │
                             │ FOR EACH JOB
                             ▼
              ┌──────────────────────────────┐
              │   OLLAMA AI ANALYSIS         │
              │   ────────────────────       │
              │   LLM: Llama 3.1 8B          │
              │                              │
              │   Tasks:                     │
              │   1. Parse job description   │
              │   2. Extract requirements    │
              │   3. Identify ATS keywords   │
              │   4. Determine role type     │
              └───────────┬──────────────────┘
                          │
                          ▼
              ┌──────────────────────────────┐
              │   JD ANALYSIS RESULT         │
              │   ────────────────────       │
              │   {                          │
              │     required_skills: [...],  │
              │     nice_to_have: [...],     │
              │     ats_keywords: [...],     │
              │     role_category: "ML Eng"  │
              │   }                          │
              └───────────┬──────────────────┘
                          │
                          │ + Profile Data
                          ▼
              ┌──────────────────────────────┐
              │   PROFILE MATCHER            │
              │   (Ollama AI)                │
              │   ────────────────────       │
              │   Compare:                   │
              │   • Skills overlap           │
              │   • Experience relevance     │
              │   • Education fit            │
              │                              │
              │   Output:                    │
              │   • Match score (0-100)      │
              │   • Best profile variant     │
              │   • Skills to highlight      │
              └───────────┬──────────────────┘
                          │
                          │
              ┌───────────┴───────────┐
              │                       │
       Match < 70%              Match >= 70%
              │                       │
              ▼                       ▼
      ┌──────────────┐     ┌─────────────────────────┐
      │   SKIP JOB   │     │   RESUME GENERATOR      │
      │              │     │   ──────────────────    │
      │   Archive    │     │   Input:                │
      │   for later  │     │   • Profile data        │
      └──────────────┘     │   • Selected variant    │
                           │   • JD analysis         │
                           │   • ATS keywords        │
                           │                         │
                           │   Process:              │
                           │   1. Load LaTeX template│
                           │   2. Inject profile data│
                           │   3. Personalize bullets│
                           │   4. Add ATS keywords   │
                           │   5. Optimize format    │
                           └────────────┬────────────┘
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │   GENERATED RESUME      │
                           │   ──────────────────    │
                           │   File: resume_IBM.tex  │
                           │                         │
                           │   Metadata:             │
                           │   • Job ID              │
                           │   • Match score: 85%    │
                           │   • Variant used        │
                           │   • Generated date      │
                           └────────────┬────────────┘
                                        │
                                        │ Store
                                        ▼
                           ┌─────────────────────────┐
                           │   APPLICATIONS DB       │
                           │   ──────────────────    │
                           │   Tracks:               │
                           │   • All applications    │
                           │   • Status              │
                           │   • Scores              │
                           │   • Files               │
                           └─────────────────────────┘
                                        │
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │   OUTPUT TO USER        │
                           │   ──────────────────    │
                           │   • LaTeX files         │
                           │   • Match scores        │
                           │   • Recommendations     │
                           │   • Apply links         │
                           └─────────────────────────┘
```

---

## 🏗️ MCP SERVERS ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                 │
│  (User Interface - CLI / Web / Claude.ai)                          │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              │ MCP Protocol
                              │
┌─────────────────────────────┴───────────────────────────────────────┐
│                    MCP SERVERS ECOSYSTEM                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────┐  ┌───────────────────┐  ┌────────────────┐ │
│  │ PROFILE SERVER    │  │ SCRAPER SERVER    │  │ DOCGEN SERVER  │ │
│  ├───────────────────┤  ├───────────────────┤  ├────────────────┤ │
│  │ TOOLS:            │  │ TOOLS:            │  │ TOOLS:         │ │
│  │ • parse_resume    │  │ • scrape_linkedin │  │ • generate_tex │ │
│  │ • store_profile   │  │ • scrape_indeed   │  │ • optimize_ats │ │
│  │ • get_profile     │  │ • filter_jobs     │  │ • compile_pdf  │ │
│  │ • update_section  │  │ • get_job_details │  │                │ │
│  │                   │  │                   │  │                │ │
│  │ RESOURCES:        │  │ RESOURCES:        │  │ RESOURCES:     │ │
│  │ • profile://me    │  │ • jobs://recent   │  │ • resume://    │ │
│  │ • variants://     │  │ • jobs://{id}     │  │ • templates:// │ │
│  └───────────────────┘  └───────────────────┘  └────────────────┘ │
│                                                                     │
│  ┌───────────────────┐  ┌───────────────────┐  ┌────────────────┐ │
│  │ ANALYSIS SERVER   │  │ MATCHER SERVER    │  │ TRACKER SERVER │ │
│  ├───────────────────┤  ├───────────────────┤  ├────────────────┤ │
│  │ TOOLS:            │  │ TOOLS:            │  │ TOOLS:         │ │
│  │ • analyze_jd      │  │ • match_profile   │  │ • create_app   │ │
│  │ • extract_keywords│  │ • score_fit       │  │ • update_status│ │
│  │ • identify_ats    │  │ • recommend_      │  │ • list_apps    │ │
│  │                   │  │   variant         │  │ • get_stats    │ │
│  │                   │  │                   │  │                │ │
│  │ Uses: Ollama LLM  │  │ Uses: Ollama LLM  │  │ RESOURCES:     │ │
│  │ (Llama 3.1)       │  │ (Llama 3.1)       │  │ • apps://      │ │
│  └───────────────────┘  └───────────────────┘  └────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │
┌─────────────────────────────┴───────────────────────────────────────┐
│                      DATA PERSISTENCE LAYER                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Profile  │  │ Jobs     │  │ Apps     │  │ Generated│          │
│  │ SQLite   │  │ SQLite   │  │ SQLite   │  │ Files    │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ PROCESS STATES FOR EACH JOB

```
                    JOB DISCOVERED
                         │
                         ▼
                  ┌─────────────┐
                  │   FETCHED   │
                  │             │
                  │ Job scraped │
                  │ from source │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  ANALYZING  │
                  │             │
                  │ Ollama      │
                  │ parsing JD  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  MATCHING   │
                  │             │
                  │ Profile vs  │
                  │ JD analysis │
                  └──────┬──────┘
                         │
              ┌──────────┴──────────┐
              │                     │
       Match < 70%           Match >= 70%
              │                     │
              ▼                     ▼
       ┌─────────────┐      ┌─────────────┐
       │  LOW_MATCH  │      │ GENERATING  │
       │             │      │             │
       │ Archived    │      │ Creating    │
       │             │      │ resume      │
       └─────────────┘      └──────┬──────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │  GENERATED  │
                            │             │
                            │ Resume ready│
                            │ for review  │
                            └──────┬──────┘
                                   │
                          ┌────────┴────────┐
                          │                 │
                     Approved          Needs Edit
                          │                 │
                          ▼                 ▼
                   ┌─────────────┐   ┌─────────────┐
                   │   READY     │   │   EDITING   │
                   │             │   │             │
                   │ Can apply   │   │ User mods   │
                   └──────┬──────┘   └──────┬──────┘
                          │                 │
                          └────────┬────────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │   APPLIED   │
                            │             │
                            │ Submitted   │
                            │ to company  │
                            └──────┬──────┘
                                   │
                                   ▼
                        ┌──────────────────┐
                        │   TRACKING       │
                        │                  │
                        │ • Submitted      │
                        │ • Under Review   │
                        │ • Interview      │
                        │ • Offer/Rejected │
                        └──────────────────┘
```

---

## 🔄 SYSTEM INTERACTION FLOW

```
┌──────┐     ┌───────────┐     ┌─────────┐     ┌────────┐     ┌────────┐
│ USER │────▶│  PROFILE  │────▶│   JOB   │────▶│ANALYSIS│────▶│MATCHER │
└──────┘     │  SERVER   │     │ SCRAPER │     │ SERVER │     │ SERVER │
             └───────────┘     └─────────┘     └────────┘     └────────┘
                   │                │                │              │
                   │                │                │              │
                   ▼                ▼                ▼              ▼
             Upload resume    Find 50 jobs    Parse each JD   Match profile
             Parse sections   (last 24h)      Extract reqs    Score: 85%
             Store profile    Filter prefs    ATS keywords    Variant: ML
                   │                │                │              │
                   │                │                │              │
                   └────────────────┴────────────────┴──────────────┘
                                         │
                                         ▼
                                  ┌────────────┐
                                  │  DOCUMENT  │
                                  │  GENERATOR │
                                  └──────┬─────┘
                                         │
                                         ▼
                                  Generate LaTeX
                                  Personalize
                                  Optimize ATS
                                  Store file
                                         │
                                         ▼
                                  ┌────────────┐
                                  │  TRACKER   │
                                  │  SERVER    │
                                  └──────┬─────┘
                                         │
                                         ▼
                                  Save application
                                  Track status
                                  Provide metrics
                                         │
                                         ▼
                                  ┌────────────┐
                                  │   OUTPUT   │
                                  │            │
                                  │ • Resumes  │
                                  │ • Scores   │
                                  │ • Stats    │
                                  └────────────┘
```

---

## 📊 DECISION FLOW - Should We Generate Resume?

```
                        Job Scraped
                             │
                             ▼
                    ┌────────────────┐
                    │ Check Posting  │
                    │ Date           │
                    └────────┬───────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              < 24 hours         > 24 hours
                    │                 │
                    ▼                 ▼
            ┌──────────────┐    ┌─────────┐
            │ Analyze JD   │    │  SKIP   │
            └──────┬───────┘    └─────────┘
                   │
                   ▼
            ┌──────────────┐
            │ Match Skills │
            └──────┬───────┘
                   │
          ┌────────┴────────┐
          │                 │
     Score < 70%      Score >= 70%
          │                 │
          ▼                 ▼
    ┌─────────┐      ┌──────────────┐
    │  SKIP   │      │ Check Apply  │
    │ (Archive)      │ Requirements │
    └─────────┘      └──────┬───────┘
                            │
                   ┌────────┴────────┐
                   │                 │
           Requires Visa      No Visa Issue
           (You need visa)    (You're in EU)
                   │                 │
                   ▼                 ▼
            ┌─────────┐      ┌──────────────┐
            │  SKIP   │      │ Check Salary │
            └─────────┘      └──────┬───────┘
                                    │
                            ┌───────┴────────┐
                            │                │
                    Salary too low    Salary OK
                            │                │
                            ▼                ▼
                     ┌─────────┐      ┌──────────────┐
                     │  SKIP   │      │  GENERATE    │
                     └─────────┘      │   RESUME     │
                                      └──────────────┘
```

---

## 🎯 KEY METRICS TO TRACK

```
┌─────────────────────────────────────────────────────────┐
│              SYSTEM METRICS DASHBOARD                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Daily Stats:                                           │
│  ├─ Jobs Scraped: 50                                    │
│  ├─ Jobs Analyzed: 50                                   │
│  ├─ Good Matches (>=70%): 15                            │
│  ├─ Resumes Generated: 15                               │
│  └─ Applications Submitted: 12                          │
│                                                         │
│  Success Rates:                                         │
│  ├─ Match Rate: 30% (15/50)                             │
│  ├─ Generation Rate: 100% (15/15)                       │
│  └─ Apply Rate: 80% (12/15)                             │
│                                                         │
│  Application Tracking:                                  │
│  ├─ Submitted: 12                                       │
│  ├─ Under Review: 8                                     │
│  ├─ Interviews: 3                                       │
│  ├─ Offers: 1                                           │
│  └─ Rejections: 2                                       │
│                                                         │
│  Top Matched Companies:                                 │
│  ├─ BMW (92%)                                           │
│  ├─ Bosch (90%)                                         │
│  ├─ IBM (85%)                                           │
│  └─ Mercedes (82%)                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 SECURITY & PRIVACY CONSIDERATIONS

```
┌─────────────────────────────────────────────────────────┐
│              SECURITY ARCHITECTURE                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User Data (Encrypted at Rest):                         │
│  ├─ Profile information (AES-256)                       │
│  ├─ Resume files (Encrypted storage)                    │
│  └─ Application history (SQLite + encryption)           │
│                                                         │
│  API Keys (Environment variables):                      │
│  ├─ LinkedIn API (if using official API)                │
│  ├─ Indeed API                                          │
│  └─ Ollama endpoint (local - no external API)           │
│                                                         │
│  Data Privacy:                                          │
│  ├─ All processing happens locally                      │
│  ├─ Ollama runs on your machine (no cloud LLM)          │
│  ├─ No data sent to third parties                       │
│  └─ User controls all data                              │
│                                                         │
│  Rate Limiting:                                         │
│  ├─ Job scraping: Max 10 requests/minute                │
│  ├─ Profile updates: No limit (local)                   │
│  └─ Ollama calls: Depends on your hardware              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 SUMMARY

**Complete Flow in One Sentence:**

User uploads resume → Profile parsed & stored → System scrapes jobs (last 24h) → Ollama analyzes each JD → Matches profile to JD → Generates personalized ATS-friendly LaTeX resume for good matches (≥70%) → Tracks applications → User downloads and applies.

**Key Features:**
- ✅ Automated job discovery (last 24 hours)
- ✅ AI-powered JD analysis (Ollama/Llama 3.1)
- ✅ Intelligent profile matching
- ✅ Personalized resume generation
- ✅ ATS optimization
- ✅ Overleaf-compatible LaTeX
- ✅ Application tracking
- ✅ Local & private (no cloud LLM)

**Technologies:**
- MCP Protocol (server communication)
- Ollama + Llama 3.1 (local LLM)
- Python (backend)
- SQLite (databases)
- LaTeX (resume generation)
- Web scraping (job discovery)

---

This architecture provides a complete, end-to-end automated job application system! 🎯
