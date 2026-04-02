#!/usr/bin/env python3
import os
from detector import detect_project
from generator import generate_all

def main():
    print("🔍 Scanning project...")
    project_type = detect_project()

    if not project_type:
        print("❌ Could not detect project type.")
        return

    print(f"✅ Detected project type: {project_type}")
    generate_all(project_type)
    print("🚀 Files generated successfully!")

if __name__ == "__main__":
    main()
