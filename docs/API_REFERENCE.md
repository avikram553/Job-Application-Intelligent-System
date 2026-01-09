# API Reference - MCP Job Application Intelligence System

**Version:** 1.0.0
**Last Updated:** January 9, 2026

---

## Table of Contents

1. [Profile MCP Server](#profile-mcp-server)
2. [Job Scraper MCP Server](#job-scraper-mcp-server)
3. [Analysis MCP Server](#analysis-mcp-server)
4. [Matcher MCP Server](#matcher-mcp-server)
5. [Document Generator MCP Server](#document-generator-mcp-server)
6. [Tracker MCP Server](#tracker-mcp-server)
7. [Data Schemas](#data-schemas)
8. [Error Handling](#error-handling)

---

## Profile MCP Server

**Server Name:** `profile_mcp`
**File:** `src/models/profile_server.py`
**Status:** ✅ Implemented
**Purpose:** Manage user profile data for resume generation

### Tools

#### 1. get_profile_json()

**Description:** Retrieve the complete user profile as JSON

**Parameters:** None

**Returns:** `str` - JSON-formatted profile data

**Example:**
```json
{
  "personal": {
    "name": "Aditya Vikram",
    "email": "vkrm.aditya553@gmail.com",
    "phone": "+49 015510469686",
    "location": "Chemnitz, Germany",
    "linkedin": "linkedin.com/in/avikram553",
    "github": "",
    "title": "Senior Software Engineer"
  },
  "experience": [...],
  "skills": {...},
  "education": [...],
  "projects": [...],
  "metadata": {...}
}
```

**Annotations:**
- `readOnlyHint`: true
- `destructiveHint`: false
- `idempotentHint`: true

**Use Cases:**
- Resume generation systems need profile data
- External tools query user information
- Profile verification and validation

---

#### 2. update_profile(params)

**Description:** Update a specific section of the user profile

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| section | ProfileSection | Yes | - | Section to update (personal, experience, skills, projects, education, certifications, awards, recognitions, publications, volunteer, languages, interests) |
| data | Dict[str, Any] | Yes | - | Data to update in the specified section |
| merge | bool | No | true | If true, merge with existing data; if false, replace section entirely |

**Valid Profile Sections:**
- `personal` - Personal information (name, email, phone, location, etc.)
- `experience` - Work experience entries
- `skills` - Technical and soft skills
- `projects` - Personal/professional projects
- `education` - Educational background
- `certifications` - Professional certifications
- `awards` - Awards and recognitions
- `recognitions` - Professional recognitions
- `publications` - Research publications
- `volunteer` - Volunteer experience
- `languages` - Language proficiency
- `interests` - Personal interests and hobbies

**Returns:** `str` - Success message with updated section details

**Example Request:**
```python
{
  "section": "personal",
  "data": {
    "name": "Aditya Vikram",
    "email": "new.email@example.com"
  },
  "merge": true
}
```

**Example Response:**
```
✓ Successfully updated 'personal' section.

Updated data:
{
  "name": "Aditya Vikram",
  "email": "new.email@example.com",
  "phone": "+49 015510469686",
  ...
}
```

**Annotations:**
- `readOnlyHint`: false
- `destructiveHint`: false
- `idempotentHint`: false

**Use Cases:**
- Update personal information (email, phone)
- Add new work experience
- Update skills after learning new technologies
- Modify project details

**Merge Behavior:**

**For Dictionary Sections (personal, skills):**
```python
# Original
{"name": "John", "email": "old@example.com"}

# Update with merge=True
{"email": "new@example.com"}

# Result
{"name": "John", "email": "new@example.com"}
```

**For List Sections (experience, education, projects):**
```python
# Original
[{"company": "Bosch", "role": "Engineer"}]

# Update with merge=True (single dict)
{"company": "Microsoft", "role": "Senior Engineer"}

# Result
[
  {"company": "Bosch", "role": "Engineer"},
  {"company": "Microsoft", "role": "Senior Engineer"}
]
```

---

### Resources

#### 1. profile://me

**Description:** Expose complete profile as an MCP resource

**Returns:** `str` - JSON-formatted complete profile

**Use Cases:**
- AI agents need access to user profile
- Resume generation requires full profile context
- External tools query profile data

**Example:**
```json
{
  "personal": {...},
  "experience": [...],
  "skills": {...},
  ...
}
```

---

#### 2. profile://me/{section}

**Description:** Expose individual profile sections as resources

**Parameters:**
- `section` - Section name (personal, experience, skills, etc.)

**Returns:** `str` - JSON-formatted section data

**Valid Sections:**
- `personal`, `experience`, `skills`, `projects`, `education`, `certifications`,
  `awards`, `recognitions`, `publications`, `volunteer`, `languages`, `interests`, `metadata`

**Example Request:**
```
profile://me/experience
```

**Example Response:**
```json
[
  {
    "id": "bosch",
    "company": "Bosch Global Software Technologies",
    "role": "Senior Software Engineer",
    "duration": "March 2022 - September 2025",
    "highlights": [...],
    "technologies": [...],
    "latex_variants": {...}
  }
]
```

**Error Response (invalid section):**
```json
{
  "error": "Section 'invalid_section' not found",
  "available_sections": ["personal", "experience", "skills", ...]
}
```

**Use Cases:**
- Query specific section without loading full profile
- Optimize data transfer for large profiles
- Section-specific AI agents

---

### Storage

**Database:** SQLite
**File Path:** `./data/profiles/profile.json`
**Schema:** See [Profile Schema](#profile-schema)

**Metadata Tracking:**
- `created_at` - Profile creation timestamp
- `last_updated` - Last modification timestamp (auto-updated on save)
- `version` - Profile schema version

---

### Error Handling

**Error Format:**
```
Error in {context}: {ErrorType} - {error message}
```

**Common Errors:**

1. **Section Not Found**
   ```
   Error: Section 'invalid_section' not found in profile structure
   ```

2. **JSON Parse Error**
   ```
   Error in get_profile_json: JSONDecodeError - Failed to parse profile JSON
   ```

3. **File Save Error**
   ```
   Error: Failed to save profile updates
   ```

**Validation:**
- Input parameters validated using Pydantic
- Section names validated against ProfileSection enum
- Data types validated before storage
- Extra fields forbidden (ConfigDict extra='forbid')

---

## Job Scraper MCP Server

**Server Name:** `job_scraper_mcp`
**File:** `src/scraper/job_scraper_server.py`
**Status:** 🚧 To Be Implemented
**Purpose:** Scrape job postings from LinkedIn and Indeed using Apify

### Tools (Planned)

#### 1. scrape_jobs(params)

**Description:** Scrape job postings from job boards

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| keywords | str | Yes | - | Job search keywords (e.g., "Machine Learning Engineer") |
| location | str | Yes | - | Job location (e.g., "Munich, Germany") |
| job_type | str | No | "Full-time" | Job type (Full-time, Part-time, Remote) |
| max_results | int | No | 50 | Maximum number of jobs to scrape |

**Returns:** `str` - Summary of jobs found and stored

**Example Response:**
```
✓ Scraped 73 jobs (48 unique) from LinkedIn and Indeed
```

---

#### 2. filter_jobs(criteria)

**Description:** Filter scraped jobs by criteria

**Parameters:** User preference criteria (TBD)

**Returns:** Filtered job list

---

#### 3. get_job_details(job_id)

**Description:** Retrieve specific job details

**Parameters:**
- `job_id` - Unique job identifier

**Returns:** Complete job details

---

## Analysis MCP Server

**Server Name:** `analysis_mcp`
**File:** `src/analysis/analysis_server.py`
**Status:** 🚧 To Be Implemented
**Purpose:** Analyze job descriptions using Ollama (Llama 3.1)

### Tools (Planned)

#### 1. analyze_jd(job_id)

**Description:** Analyze job description using AI

**Parameters:**
- `job_id` - Job ID to analyze

**Returns:** Structured analysis as JSON

**Analysis Output:**
```json
{
  "required_skills": ["Python", "TensorFlow", "AWS"],
  "nice_to_have_skills": ["PyTorch", "Docker"],
  "ats_keywords": ["machine learning", "deep learning"],
  "role_category": "ML Engineer",
  "experience_level": "Senior"
}
```

---

## Matcher MCP Server

**Server Name:** `matcher_mcp`
**File:** `src/matcher/matcher_server.py`
**Status:** 🚧 To Be Implemented
**Purpose:** Match user profile to job requirements

### Tools (Planned)

#### 1. match_profile(job_id, profile_path)

**Description:** Calculate profile-to-job match score

**Parameters:**
- `job_id` - Job ID to match against
- `profile_path` - Path to profile JSON (default: ./data/profile.json)

**Returns:** Match score and recommendations

**Example Response:**
```json
{
  "job_id": "abc123",
  "overall_score": 87.5,
  "recommended_variant": "ml_focused",
  "breakdown": {
    "skills": 92.0,
    "experience": 85.0,
    "domain": 85.0
  }
}
```

---

## Document Generator MCP Server

**Server Name:** `document_generator_mcp`
**File:** `src/generator/document_generator_server.py`
**Status:** 🚧 To Be Implemented
**Purpose:** Generate personalized LaTeX resumes

### Tools (Planned)

#### 1. generate_resume(job_id, profile_path)

**Description:** Generate customized resume for job

**Parameters:**
- `job_id` - Job ID to generate resume for
- `profile_path` - Path to profile (default: ./data/profile.json)

**Returns:** Path to generated .tex file

**Example Response:**
```json
{
  "status": "success",
  "file": "./generated_resumes/resume_Bosch_abc12345.tex",
  "job_id": "abc12345",
  "company": "Bosch",
  "match_score": 87.5
}
```

---

## Tracker MCP Server

**Server Name:** `tracker_mcp`
**File:** `src/tracker/tracker_server.py`
**Status:** 🚧 To Be Implemented
**Purpose:** Track application status and outcomes

### Tools (Planned)

#### 1. create_application(params)

**Description:** Log a new job application

**Parameters:**
- `job_id` - Job identifier
- `resume_file` - Path to resume used
- `match_score` - Match score
- `variant_used` - Profile variant used

**Returns:** Confirmation message

---

#### 2. get_stats()

**Description:** Get application statistics

**Returns:** Statistics summary

**Example Response:**
```json
{
  "total_applications": 48,
  "by_status": {
    "submitted": 35,
    "under_review": 8,
    "interview": 3,
    "rejected": 2
  },
  "average_match_score": 84.2
}
```

---

## Data Schemas

### Profile Schema

```json
{
  "personal": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "linkedin": "string",
    "github": "string",
    "title": "string",
    "summary": "string"
  },
  "experience": [
    {
      "id": "string",
      "company": "string",
      "role": "string",
      "location": "string",
      "duration": "string",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM",
      "highlights": ["string"],
      "technologies": ["string"],
      "latex_variants": {
        "ml_focused": "string",
        "automotive_focused": "string",
        "backend_focused": "string",
        "leadership_focused": "string"
      }
    }
  ],
  "skills": {
    "programming_languages": ["string"],
    "ml_frameworks": ["string"],
    "ai_frameworks": ["string"],
    "backend_frameworks": ["string"],
    "data_science": ["string"],
    "cloud_platforms": ["string"],
    "automotive": ["string"],
    "security": ["string"],
    "other": ["string"],
    "languages_spoken": ["string"]
  },
  "projects": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "technologies": ["string"],
      "highlights": ["string"],
      "category": "string"
    }
  ],
  "education": [
    {
      "id": "string",
      "degree": "string",
      "institution": "string",
      "location": "string",
      "duration": "string",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM or Present",
      "status": "In Progress | Completed",
      "courses": ["string"]
    }
  ],
  "achievements": [
    {
      "id": "string",
      "title": "string",
      "organization": "string",
      "date": "string",
      "description": "string"
    }
  ],
  "certifications": [
    {
      "id": "string",
      "name": "string",
      "issuer": "string",
      "date": "string",
      "category": "string"
    }
  ],
  "metadata": {
    "created_at": "ISO8601 timestamp",
    "last_updated": "ISO8601 timestamp",
    "version": "string",
    "source": "string",
    "profile_completeness": "percentage",
    "years_of_experience": "string",
    "current_status": "string",
    "target_roles": ["string"]
  }
}
```

### Job Schema (SQLite)

```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    description TEXT,
    requirements TEXT,
    posted_date TIMESTAMP,
    source TEXT,
    url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'new'
);
```

---

## Error Handling

### Standard Error Format

All MCP servers use consistent error formatting:

```
Error in {context}: {ErrorType} - {error_message}
```

### Common Error Types

1. **Validation Errors** - Pydantic validation failures
2. **File Not Found** - Missing profile or data files
3. **Database Errors** - SQLite connection or query errors
4. **API Errors** - External service (Apify, Ollama) failures
5. **Permission Errors** - File system access issues

### Error Response Examples

**Validation Error:**
```
Error in update_profile: ValidationError - Field 'section' is required
```

**File Not Found:**
```
Error in get_profile_json: FileNotFoundError - Profile file not found
```

**Database Error:**
```
Error in scrape_jobs: sqlite3.OperationalError - Database locked
```

---

## Authentication & Security

**Current:** All MCP servers run locally with stdio transport (no authentication needed)

**Environment Variables:**
- `APIFY_API_TOKEN` - Apify API key for job scraping
- `OLLAMA_URL` - Ollama API endpoint (default: http://localhost:11434)

**Data Privacy:**
- All data stored locally
- No cloud services except Apify (for job scraping)
- Profile data never sent to external services

---

## Rate Limits

**Apify API:**
- Free tier: $5 credit/month
- Scraping frequency: Once per day recommended
- Monitor usage via Apify dashboard

**Ollama:**
- Local inference (no rate limits)
- Performance depends on hardware
- Recommended: 8GB+ RAM for smooth operation

---

## Versioning

**API Version:** 1.0.0
**MCP Protocol Version:** Latest
**Profile Schema Version:** 1.0.0

**Breaking Changes Policy:**
- Major version bump for breaking changes
- Backward compatibility maintained within major version
- Migration scripts provided for schema updates

---

## Support & Documentation

**GitHub Repository:** (TBD)
**Issues:** (TBD)
**Contact:** vkrm.aditya553@gmail.com

---

**Last Updated:** January 9, 2026
**Maintainer:** Aditya Vikram
