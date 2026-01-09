"""
User preferences management
Stores and manages job search criteria
"""

import json
from pathlib import Path
from typing import Dict, Any, List

PREFERENCES_FILE = Path("./data/preferences.json")

DEFAULT_PREFERENCES = {
    "roles": ["Machine Learning Engineer", "AI Engineer", "Software Engineer - ML"],
    "locations": ["Munich", "Berlin", "Stuttgart", "Remote"],
    "job_type": "Full-time",
    "experience_level": "Senior",
    "work_mode": "Hybrid",
    "must_have_keywords": ["Python", "Machine Learning", "PyTorch", "TensorFlow"],
    "exclude_keywords": ["PhD required", "C++ only"],
    "salary_min": 70000,
    "posted_within": "24h",
    "match_threshold": 70.0  # Minimum match score to generate resume
}


def load_preferences() -> Dict[str, Any]:
    """Load user preferences from file

    Returns:
        dict: User preferences or defaults if file doesn't exist
    """
    if not PREFERENCES_FILE.exists():
        save_preferences(DEFAULT_PREFERENCES)
        return DEFAULT_PREFERENCES.copy()

    try:
        with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing preferences file: {e}")
        return DEFAULT_PREFERENCES.copy()


def save_preferences(prefs: Dict[str, Any]) -> bool:
    """Save preferences to file

    Args:
        prefs: Preferences dictionary

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(prefs, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving preferences: {e}")
        return False


def update_preference(key: str, value: Any) -> bool:
    """Update a single preference

    Args:
        key: Preference key
        value: New value

    Returns:
        bool: True if successful
    """
    prefs = load_preferences()
    prefs[key] = value
    return save_preferences(prefs)


def get_preference(key: str, default: Any = None) -> Any:
    """Get a specific preference value

    Args:
        key: Preference key
        default: Default value if key not found

    Returns:
        Preference value or default
    """
    prefs = load_preferences()
    return prefs.get(key, default)


def reset_preferences() -> bool:
    """Reset preferences to defaults

    Returns:
        bool: True if successful
    """
    return save_preferences(DEFAULT_PREFERENCES)


def display_preferences() -> str:
    """Display current preferences in a formatted way

    Returns:
        str: Formatted preferences
    """
    prefs = load_preferences()

    output = []
    output.append("=" * 60)
    output.append("CURRENT JOB SEARCH PREFERENCES")
    output.append("=" * 60)

    output.append(f"\nTarget Roles:")
    for role in prefs.get("roles", []):
        output.append(f"  - {role}")

    output.append(f"\nTarget Locations:")
    for loc in prefs.get("locations", []):
        output.append(f"  - {loc}")

    output.append(f"\nJob Details:")
    output.append(f"  Job Type: {prefs.get('job_type', 'N/A')}")
    output.append(f"  Experience Level: {prefs.get('experience_level', 'N/A')}")
    output.append(f"  Work Mode: {prefs.get('work_mode', 'N/A')}")
    output.append(f"  Minimum Salary: €{prefs.get('salary_min', 0):,}")

    output.append(f"\nMust-Have Keywords:")
    for kw in prefs.get("must_have_keywords", []):
        output.append(f"  - {kw}")

    output.append(f"\nExclude Keywords:")
    for kw in prefs.get("exclude_keywords", []):
        output.append(f"  - {kw}")

    output.append(f"\nSearch Settings:")
    output.append(f"  Posted Within: {prefs.get('posted_within', 'N/A')}")
    output.append(f"  Match Threshold: {prefs.get('match_threshold', 70)}%")

    output.append("=" * 60)

    return "\n".join(output)
