#!/usr/bin/env python3
"""
System Validation Tests
Verifies all components are working correctly
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")

    try:
        import json
        import sqlite3
        from pathlib import Path
        from pydantic import BaseModel
        print("✓ Core Python modules OK")
    except ImportError as e:
        print(f"✗ Core module import failed: {e}")
        return False

    try:
        from mcp.server.fastmcp import FastMCP
        print("✓ FastMCP OK")
    except ImportError as e:
        print(f"✗ FastMCP import failed: {e}")
        print("  Install: pip install fastmcp")
        return False

    try:
        import httpx
        print("✓ httpx OK")
    except ImportError as e:
        print(f"✗ httpx import failed: {e}")
        print("  Install: pip install httpx")
        return False

    try:
        from jinja2 import Template
        print("✓ Jinja2 OK")
    except ImportError as e:
        print(f"✗ Jinja2 import failed: {e}")
        print("  Install: pip install jinja2")
        return False

    try:
        from preferences import load_preferences
        print("✓ Preferences module OK")
    except ImportError as e:
        print(f"✗ Preferences module import failed: {e}")
        return False

    return True


def test_directories():
    """Test that required directories exist"""
    print("\nTesting directory structure...")

    required_dirs = [
        "data/profiles",
        "data/databases",
        "generated_resumes",
        "templates",
        "src/models",
        "src/scraper",
        "src/analysis",
        "src/matcher",
        "src/generator",
        "src/tracker",
        "docs"
    ]

    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} missing")
            all_exist = False

    return all_exist


def test_profile():
    """Test that profile exists and is valid"""
    print("\nTesting profile...")

    profile_path = Path("data/profiles/profile.json")

    if not profile_path.exists():
        print(f"✗ Profile not found at {profile_path}")
        return False

    try:
        import json
        with open(profile_path, 'r') as f:
            profile = json.load(f)

        required_sections = ["personal", "experience", "skills", "education"]
        for section in required_sections:
            if section in profile:
                print(f"✓ Profile section '{section}' exists")
            else:
                print(f"✗ Profile missing section '{section}'")
                return False

        print(f"✓ Profile is valid")
        return True

    except json.JSONDecodeError as e:
        print(f"✗ Profile JSON is invalid: {e}")
        return False
    except Exception as e:
        print(f"✗ Error reading profile: {e}")
        return False


def test_preferences():
    """Test that preferences can be loaded"""
    print("\nTesting preferences...")

    try:
        from preferences import load_preferences

        prefs = load_preferences()

        required_keys = ["roles", "locations", "job_type", "match_threshold"]
        for key in required_keys:
            if key in prefs:
                print(f"✓ Preference '{key}' exists: {prefs[key]}")
            else:
                print(f"✗ Preference '{key}' missing")
                return False

        print("✓ Preferences are valid")
        return True

    except Exception as e:
        print(f"✗ Error loading preferences: {e}")
        return False


def test_template():
    """Test that LaTeX template exists"""
    print("\nTesting LaTeX template...")

    template_path = Path("templates/resume_template.tex")

    if not template_path.exists():
        print(f"✗ Template not found at {template_path}")
        return False

    try:
        with open(template_path, 'r') as f:
            content = f.read()

        if "{{" in content and "}}" in content:
            print("✓ Template contains Jinja2 placeholders")
        else:
            print("⚠ Template might not be a Jinja2 template")

        print("✓ LaTeX template exists")
        return True

    except Exception as e:
        print(f"✗ Error reading template: {e}")
        return False


def test_env_file():
    """Test environment configuration"""
    print("\nTesting environment configuration...")

    env_path = Path(".env")

    if not env_path.exists():
        print("⚠ .env file not found (will be created by setup.sh)")
        return True

    try:
        with open(env_path, 'r') as f:
            content = f.read()

        if "APIFY_API_TOKEN" in content:
            if "your_apify_api_token_here" in content:
                print("⚠ APIFY_API_TOKEN not configured (placeholder detected)")
            else:
                print("✓ APIFY_API_TOKEN is configured")

        if "OLLAMA_URL" in content:
            print("✓ OLLAMA_URL is set")

        return True

    except Exception as e:
        print(f"✗ Error reading .env: {e}")
        return False


def test_ollama():
    """Test if Ollama is accessible"""
    print("\nTesting Ollama connection...")

    try:
        import httpx
        import asyncio

        async def check_ollama():
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get("http://localhost:11434/api/tags")
                    if response.status_code == 200:
                        print("✓ Ollama is running")
                        models = response.json()
                        if any("llama3.1" in str(m) for m in models.get("models", [])):
                            print("✓ Llama 3.1 model is available")
                        else:
                            print("⚠ Llama 3.1 model not found. Run: ollama pull llama3.1:8b")
                        return True
                    else:
                        print(f"✗ Ollama returned status {response.status_code}")
                        return False
            except Exception as e:
                print(f"⚠ Ollama not accessible: {e}")
                print("  Start Ollama with: ollama serve")
                return False

        return asyncio.run(check_ollama())

    except Exception as e:
        print(f"✗ Error testing Ollama: {e}")
        return False


def test_database():
    """Test database creation"""
    print("\nTesting database...")

    db_path = Path("data/databases/jobs.db")

    try:
        import sqlite3

        # Create database if it doesn't exist
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Test creating tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)

        # Test insert
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        conn.commit()

        # Test select
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchone()

        # Cleanup
        cursor.execute("DROP TABLE test_table")
        conn.commit()
        conn.close()

        print("✓ Database operations successful")
        return True

    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print(" MCP JOB APPLICATION INTELLIGENCE SYSTEM - VALIDATION")
    print("=" * 70)
    print()

    tests = [
        ("Imports", test_imports),
        ("Directories", test_directories),
        ("Profile", test_profile),
        ("Preferences", test_preferences),
        ("LaTeX Template", test_template),
        ("Environment", test_env_file),
        ("Ollama", test_ollama),
        ("Database", test_database)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print(" SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Tests Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Configure Apify token in .env")
        print("  2. Set job preferences: python cli_set_preferences.py")
        print("  3. Run workflow: python orchestrator.py --workflow")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        print("   Run setup.sh if you haven't already.")

    print()


if __name__ == "__main__":
    main()
