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
    CERTIFICATION = "certifications"
    AWARDS="awards"
    RECOGNITIONS = "recognitions"
    PUBLICATIONS = "publications"
    VOLUNTEER = "volunteer"            # Volunteer experience
    LANGUAGES = "languages"            # Language proficiency
    INTERESTS = "interests"            # Personal interests/hobbies
    
#Why can't we have extra sections?? --Definately we can have 

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

@mcp.tool(
    name="get_profile_json",
    annotations={
        "title": "Get Profile as JSON",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
    
)


# Question--> Why get_profile_json? Why not reusing the _load_profile --> Because the MCP tool will not have the access to it

async def get_profile_json() -> str:
    '''   This tool returns the raw profile data in JSON format, suitable for
    programmatic processing by resume generation tools and other services.'''

    try:
        profile_data=_load_profile()
        return json.dumps(profile_data, indent=2 , ensure_ascii=False)
    except Exception as e:
        return _handle_error(e, "get_profile_json")

@mcp.tool(
    name="update_profile",
    annotations={
        "title": "Update Profile Section",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)

async def update_profile(params: UpdateProfileInput) -> str:
    """Update a specific section of the user profile.
    
    This tool allows you to update individual sections of the profile.
    You can either merge new data with existing data or replace the
    entire section.
    
    Args:
        params (UpdateProfileInput): Contains:
            - section (str): Section to update (personal, experience, skills, projects, education)
            - data (dict): New data for the section
            - merge (bool): If True, merge with existing; if False, replace entirely
    
    Returns:
        str: Success message with updated section details
        
    Examples:
        Update personal info:
            section="personal"
            data={"name": "John Doe", "email": "john@example.com"}
            
        Add new experience:
            section="experience"
            data={
                "company": "TechCorp",
                "role": "Senior Engineer",
                "duration": "2020-2023",
                "highlights": ["Led team of 5", "Increased performance by 40%"]
            }
    """
    try:
        # Load current profile
        profile_data = _load_profile()
        
        # Validate section exists
        if params.section.value not in profile_data:
            return f"Error: Section '{params.section.value}' not found in profile structure"
        
        # Update the section
        if params.merge:
            # Merge mode
            current = profile_data[params.section.value]
            
            if isinstance(current, dict) and isinstance(params.data, dict):
                # Merge dictionaries
                current.update(params.data)
            elif isinstance(current, list) and isinstance(params.data, (list, dict)):
                # Append to list
                if isinstance(params.data, dict):
                    current.append(params.data)
                else:
                    current.extend(params.data)
            else:
                # Direct replacement if types don't match
                profile_data[params.section.value] = params.data
        else:
            # Replace mode
            profile_data[params.section.value] = params.data
        
        # Save updated profile
        if _save_profile(profile_data):
            updated_data = profile_data[params.section.value]
            return f"✓ Successfully updated '{params.section.value}' section.\n\nUpdated data:\n{json.dumps(updated_data, indent=2)}"
        else:
            return "Error: Failed to save profile updates"
            
    except Exception as e:
        return _handle_error(e, "update_profile")
    

# ============================================================================
# RESOURCE IMPLEMENTATIONS
# ============================================================================

@mcp.resource("profile://me")
async def get_profile_resource() -> str:
    """Expose profile as an MCP resource.
    
    This resource provides direct access to the complete profile data
    via the URI: profile://me
    
    Returns:
        str: JSON-formatted complete profile
    """
    try:
        profile_data = _load_profile()
        return json.dumps(profile_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.resource("profile://me/{section}")
async def get_profile_section(section: str) -> str:
    """Expose individual profile sections as resources.
    
    Access specific profile sections via URIs like:
    - profile://me/personal
    - profile://me/experience
    - profile://me/skills
    
    Args:
        section: Section name (personal, experience, skills, projects, education)
    
    Returns:
        str: JSON-formatted section data
    """
    try:
        profile_data = _load_profile()
        
        if section in profile_data:
            return json.dumps(profile_data[section], indent=2, ensure_ascii=False)
        else:
            return json.dumps({
                "error": f"Section '{section}' not found",
                "available_sections": list(profile_data.keys())
            })
    except Exception as e:
        return json.dumps({"error": str(e)})


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def main():
    """Run the Profile MCP server using stdio transport."""
    # Ensure data directory exists on startup
    _ensure_data_directory()
    
    # Run server with stdio transport (local execution)
    mcp.run()


if __name__ == "__main__":
    main()
