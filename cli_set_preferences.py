#!/usr/bin/env python3
"""
CLI tool to set job search preferences
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preferences import (
    load_preferences,
    save_preferences,
    reset_preferences,
    display_preferences,
    update_preference
)


def main():
    """Main CLI interface"""
    print("\n" + "=" * 60)
    print("JOB SEARCH PREFERENCES CONFIGURATION")
    print("=" * 60 + "\n")

    while True:
        print("\nOptions:")
        print("1. View current preferences")
        print("2. Update roles")
        print("3. Update locations")
        print("4. Update job type")
        print("5. Update salary minimum")
        print("6. Update must-have keywords")
        print("7. Update exclude keywords")
        print("8. Update match threshold")
        print("9. Reset to defaults")
        print("0. Exit")

        choice = input("\nEnter your choice (0-9): ").strip()

        if choice == "0":
            print("\n✓ Exiting preferences configuration\n")
            break

        elif choice == "1":
            print("\n" + display_preferences())

        elif choice == "2":
            prefs = load_preferences()
            print("\nCurrent roles:", prefs.get("roles", []))
            roles_input = input("Enter new roles (comma-separated): ").strip()
            if roles_input:
                roles = [r.strip() for r in roles_input.split(",")]
                update_preference("roles", roles)
                print(f"✓ Updated roles to: {roles}")

        elif choice == "3":
            prefs = load_preferences()
            print("\nCurrent locations:", prefs.get("locations", []))
            locs_input = input("Enter new locations (comma-separated): ").strip()
            if locs_input:
                locs = [l.strip() for l in locs_input.split(",")]
                update_preference("locations", locs)
                print(f"✓ Updated locations to: {locs}")

        elif choice == "4":
            prefs = load_preferences()
            print(f"\nCurrent job type: {prefs.get('job_type', 'N/A')}")
            job_type = input("Enter job type (Full-time/Part-time/Contract/Remote): ").strip()
            if job_type:
                update_preference("job_type", job_type)
                print(f"✓ Updated job type to: {job_type}")

        elif choice == "5":
            prefs = load_preferences()
            print(f"\nCurrent minimum salary: €{prefs.get('salary_min', 0):,}")
            salary_input = input("Enter minimum salary (EUR): ").strip()
            if salary_input:
                try:
                    salary = int(salary_input)
                    update_preference("salary_min", salary)
                    print(f"✓ Updated minimum salary to: €{salary:,}")
                except ValueError:
                    print("Error: Please enter a valid number")

        elif choice == "6":
            prefs = load_preferences()
            print("\nCurrent must-have keywords:", prefs.get("must_have_keywords", []))
            keywords_input = input("Enter must-have keywords (comma-separated): ").strip()
            if keywords_input:
                keywords = [k.strip() for k in keywords_input.split(",")]
                update_preference("must_have_keywords", keywords)
                print(f"✓ Updated must-have keywords to: {keywords}")

        elif choice == "7":
            prefs = load_preferences()
            print("\nCurrent exclude keywords:", prefs.get("exclude_keywords", []))
            keywords_input = input("Enter exclude keywords (comma-separated): ").strip()
            if keywords_input:
                keywords = [k.strip() for k in keywords_input.split(",")]
                update_preference("exclude_keywords", keywords)
                print(f"✓ Updated exclude keywords to: {keywords}")

        elif choice == "8":
            prefs = load_preferences()
            print(f"\nCurrent match threshold: {prefs.get('match_threshold', 70)}%")
            threshold_input = input("Enter match threshold (0-100): ").strip()
            if threshold_input:
                try:
                    threshold = float(threshold_input)
                    if 0 <= threshold <= 100:
                        update_preference("match_threshold", threshold)
                        print(f"✓ Updated match threshold to: {threshold}%")
                    else:
                        print("Error: Threshold must be between 0 and 100")
                except ValueError:
                    print("Error: Please enter a valid number")

        elif choice == "9":
            confirm = input("\nAre you sure you want to reset to defaults? (yes/no): ").strip().lower()
            if confirm == "yes":
                reset_preferences()
                print("✓ Preferences reset to defaults")
            else:
                print("Reset cancelled")

        else:
            print("Invalid choice. Please enter a number between 0 and 9.")


if __name__ == "__main__":
    main()
