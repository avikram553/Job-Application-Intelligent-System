from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel , Field , field_validator , ConfigDict
from typing import Optional , List , Dict , Any
from enum import Enum
import json
import os
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("./data/profiles")
PROFILE_FILE = DATA_DIR / "profile.json"

class ProfileSection(str, Enum):
    """Valid profile sections that can be updated."""
    PERSONAL = "personal"
    EXPERIENCE = "experience"
    SKILLS = "skills"
    PROJECTS = "projects"
    EDUCATION = "education"
#Why can't we have extra sections??

class UpdateProfileInput(BaseModel):
    """Input model for updating profile sections."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

        
    section: ProfileSection = Field(
        ..., 
        description="Profile section to update (personal, experience, skills, projects, education)"
    )
    
    data: Dict[str, Any] = Field(
        ..., 
        description="Data to update in the specified section. Structure depends on section type."
    )
    
    merge: bool = Field(
        default=True,
        description="If True, merge with existing data. If False, replace section entirely."
    )


# ============================================================================
# HELPER FUNCTIONS - Reusable Logic
# ============================================================================
def _ensure_data_directory() -> None:
    """Ensure data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def _load_profile() -> Dict[str, Any]:
    """Load profile data from JSON file.
    
    Returns:
        dict: Profile data or default structure if file doesn't exist
    """
    _ensure_data_directory()
    
    if not PROFILE_FILE.exists():
        # Return default profile structure
        return {
            "personal": {
                "name": "",
                "email": "",
                "phone": "",
                "location": "",
                "linkedin": "",
                "github": ""
            },
            "experience": [],
            "skills": {
                "technical": [],
                "languages": [],
                "tools": []
            },
            "projects": [],
            "education": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }
    
    try:
        with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse profile JSON: {str(e)}",
            "personal": {},
            "experience": [],
            "skills": {},
            "projects": [],
            "education": []
        }
 

def _save_profile(profile_data: Dict[str, Any]) -> bool:
    """Save profile data to JSON file.
    
    Args:
        profile_data: Profile data to save
        
    Returns:
        bool: True if save successful, False otherwise
    """
    _ensure_data_directory()
    
    # Update metadata
    if "metadata" not in profile_data:
        profile_data["metadata"] = {}
    
    profile_data["metadata"]["last_updated"] = datetime.now().isoformat()
    
    try:
        with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving profile: {str(e)}")
        return False


def _handle_error(error: Exception, context: str) -> str:
    """Consistent error formatting.
    
    Args:
        error: Exception that occurred
        context: Context where error occurred
        
    Returns:
        str: Formatted error message
    """
    error_type = type(error).__name__
    return f"Error in {context}: {error_type} - {str(error)}"


# ============================================================================
# MCP SERVER INITIALIZATION
# ============================================================================

# Initialize FastMCP server with appropriate name

mcp=FastMCP("profile_mcp")



# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

