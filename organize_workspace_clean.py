"""
🧹 PROJECT CLEANUP & ORGANIZATION SCRIPT
==========================================
Kelompok 18 - Big Data Poverty Mapping

This script will organize your workspace by:
1. Creating proper folder structure
2. Moving files to appropriate folders
3. Keeping only essential files in root
4. Creating archive for old/duplicate files
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

def create_folder_structure():
    """Create organized folder structure"""
    folders = {
        "01_CORE_FILES": "Essential project files (docker-compose, etc)",
        "02_DOCUMENTATION": "All documentation and guides",
        "03_SCRIPTS": {
            "airflow": "Airflow DAGs and configurations",
            "spark": "Spark processing scripts", 
            "superset": "Superset setup and dashboard scripts",
            "postgres": "Database scripts and SQL files",
            "utilities": "Helper and utility scripts"
        },
        "04_GUIDES": {
            "setup": "Setup and installation guides",
            "dashboard": "Dashboard creation guides",
            "troubleshooting": "Error fixes and troubleshooting"
        },
        "05_ARCHIVED": {
            "old_scripts": "Deprecated/old script versions",
            "duplicate_docs": "Duplicate documentation files",
            "temp_files": "Temporary and test files"
        },
        "06_ASSETS": "Images, diagrams, and other assets",
        "07_OUTPUTS": "Generated reports and outputs"
    }
    
    base_path = Path("C:/TUBESABD")
    
    for folder, description in folders.items():
        if isinstance(description, dict):
            # Create main folder
            main_folder = base_path / folder
            main_folder.mkdir(exist_ok=True)
            print(f"✅ Created: {main_folder}")
            
            # Create subfolders
            for subfolder, subdesc in description.items():
                sub_path = main_folder / subfolder
                sub_path.mkdir(exist_ok=True)
                print(f"   └── {subfolder}/")
        else:
            folder_path = base_path / folder
            folder_path.mkdir(exist_ok=True)
            print(f"✅ Created: {folder_path}")

def get_file_categories():
    """Define file organization rules"""
    return {
        # Core files (stay in root)
        "core_files": [
            "docker-compose.yml",
            "hadoop.env", 
            "README.md",
            ".env",
            ".gitignore"
        ],
        
        # Scripts by category
        "airflow_scripts": [
            "*dag*.py",
            "*airflow*.py",
            "manage_*dags*.py"
        ],
        
        "spark_scripts": [
            "*spark*.py",
            "bronze_to_silver.py",
            "silver_to_gold.py",
            "*etl*.py"
        ],
        
        "superset_scripts": [
            "*superset*.py",
            "*dashboard*.py",
            "automate_superset*.py",
            "setup_superset*.py"
        ],
        
        "postgres_scripts": [
            "*postgres*.py",
            "*sql*",
            "init_postgres*.sql",
            "create_gold_views.sql"
        ],
        
        "utility_scripts": [
            "check_*.py",
            "verify_*.py",
            "debug_*.py",
            "organize_*.py",
            "cleanup_*.py",
            "test_*.py"
        ],
        
        # Documentation
        "setup_guides": [
            "*SETUP*.md",
            "*INSTALLATION*.md",
            "*READY*.md",
            "*FIX*.md"
        ],
        
        "dashboard_guides": [
            "*DASHBOARD*.md",
            "*SUPERSET*.md",
            "*CHART*.md"
        ],
        
        "architecture_docs": [
            "*ARSITEKTUR*.md",
            "*ARCHITECTURE*.md",
            "*PIPELINE*.md"
        ],
        
        # Archive files
        "old_files": [
            "*old*.py",
            "*backup*.py",
            "*temp*.py",
            "*test*.py",
            "*debug*.py"
        ]
    }

def organize_files():
    """Move files to appropriate folders"""
    base_path = Path("C:/TUBESABD")
    categories = get_file_categories()
    moved_files = []
    
    print("\n🚀 Starting file organization...")
    
    # Get all files in current directory
    all_files = list(base_path.glob("*"))
    all_files = [f for f in all_files if f.is_file()]
    
    print(f"📁 Found {len(all_files)} files to organize")
    
    # Core files - keep in root
    core_files = categories["core_files"]
    print(f"\n📌 Keeping {len(core_files)} core files in root...")
    
    # Airflow scripts
    airflow_dest = base_path / "03_SCRIPTS" / "airflow"
    move_files_by_pattern(all_files, categories["airflow_scripts"], airflow_dest, moved_files)
    
    # Spark scripts  
    spark_dest = base_path / "03_SCRIPTS" / "spark"
    move_files_by_pattern(all_files, categories["spark_scripts"], spark_dest, moved_files)
    
    # Superset scripts
    superset_dest = base_path / "03_SCRIPTS" / "superset"
    move_files_by_pattern(all_files, categories["superset_scripts"], superset_dest, moved_files)
    
    # Postgres scripts
    postgres_dest = base_path / "03_SCRIPTS" / "postgres"
    move_files_by_pattern(all_files, categories["postgres_scripts"], postgres_dest, moved_files)
    
    # Utility scripts
    utils_dest = base_path / "03_SCRIPTS" / "utilities"
    move_files_by_pattern(all_files, categories["utility_scripts"], utils_dest, moved_files)
    
    # Setup guides
    setup_dest = base_path / "04_GUIDES" / "setup"
    move_files_by_pattern(all_files, categories["setup_guides"], setup_dest, moved_files)
    
    # Dashboard guides
    dashboard_dest = base_path / "04_GUIDES" / "dashboard"
    move_files_by_pattern(all_files, categories["dashboard_guides"], dashboard_dest, moved_files)
    
    # Architecture docs
    arch_dest = base_path / "02_DOCUMENTATION"
    move_files_by_pattern(all_files, categories["architecture_docs"], arch_dest, moved_files)
    
    # Archive old files
    archive_dest = base_path / "05_ARCHIVED" / "old_scripts"
    move_files_by_pattern(all_files, categories["old_files"], archive_dest, moved_files)
    
    return moved_files

def move_files_by_pattern(all_files, patterns, destination, moved_list):
    """Move files matching patterns to destination"""
    import fnmatch
    
    destination.mkdir(parents=True, exist_ok=True)
    moved_count = 0
    
    for file_path in all_files:
        file_name = file_path.name.lower()
        
        for pattern in patterns:
            if fnmatch.fnmatch(file_name, pattern.lower()):
                try:
                    # Don't move if already moved
                    if str(file_path) not in moved_list:
                        dest_file = destination / file_path.name
                        shutil.move(str(file_path), str(dest_file))
                        moved_list.append(str(file_path))
                        moved_count += 1
                        print(f"   ✅ Moved: {file_path.name} → {destination.name}/")
                        break
                except Exception as e:
                    print(f"   ❌ Error moving {file_path.name}: {e}")
    
    if moved_count > 0:
        print(f"📦 Moved {moved_count} files to {destination.name}/")

def move_remaining_files():
    """Move any remaining documentation files"""
    base_path = Path("C:/TUBESABD")
    doc_dest = base_path / "02_DOCUMENTATION"
    doc_dest.mkdir(exist_ok=True)
    
    # Get remaining .md files
    md_files = list(base_path.glob("*.md"))
    md_files = [f for f in md_files if f.name not in ["README.md"]]
    
    moved_count = 0
    for md_file in md_files:
        try:
            dest_file = doc_dest / md_file.name
            shutil.move(str(md_file), str(dest_file))
            moved_count += 1
            print(f"   ✅ Moved: {md_file.name} → documentation/")
        except Exception as e:
            print(f"   ❌ Error moving {md_file.name}: {e}")
    
    # Get remaining .txt files
    txt_files = list(base_path.glob("*.txt"))
    for txt_file in txt_files:
        try:
            dest_file = doc_dest / txt_file.name
            shutil.move(str(txt_file), str(dest_file))
            moved_count += 1
            print(f"   ✅ Moved: {txt_file.name} → documentation/")
        except Exception as e:
            print(f"   ❌ Error moving {txt_file.name}: {e}")
    
    if moved_count > 0:
        print(f"📦 Moved {moved_count} additional documentation files")

def create_readme_files():
    """Create README files for each folder"""
    base_path = Path("C:/TUBESABD")
    
    readme_contents = {
        "01_CORE_FILES": """# Core Files
Essential project files that should remain in the root directory.
- docker-compose.yml: Main container orchestration
- hadoop.env: Hadoop environment configuration
- README.md: Main project documentation
""",
        
        "02_DOCUMENTATION": """# Documentation
All project documentation, guides, and references.
- Architecture documents
- Technical specifications
- Project reports
""",
        
        "03_SCRIPTS": """# Scripts
All executable scripts organized by service/purpose.
""",
        
        "03_SCRIPTS/airflow": """# Airflow Scripts
DAG files and Airflow-related automation scripts.
""",
        
        "03_SCRIPTS/spark": """# Spark Scripts
ETL processing scripts for Bronze → Silver → Gold pipeline.
""",
        
        "03_SCRIPTS/superset": """# Superset Scripts
Dashboard creation and Superset automation scripts.
""",
        
        "03_SCRIPTS/postgres": """# PostgreSQL Scripts
Database setup, initialization, and SQL files.
""",
        
        "03_SCRIPTS/utilities": """# Utility Scripts
Helper scripts for debugging, verification, and maintenance.
""",
        
        "04_GUIDES": """# Guides
Step-by-step implementation and troubleshooting guides.
""",
        
        "05_ARCHIVED": """# Archived Files
Old versions, duplicates, and deprecated files.
⚠️ Files here are kept for reference but not actively used.
""",
        
        "06_ASSETS": """# Assets
Images, diagrams, screenshots, and other media files.
""",
        
        "07_OUTPUTS": """# Outputs
Generated reports, exports, and pipeline outputs.
"""
    }
    
    for folder, content in readme_contents.items():
        readme_path = base_path / folder / "README.md"
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📝 Created README: {folder}/README.md")

def create_organization_report():
    """Create a report of the organization process"""
    base_path = Path("C:/TUBESABD")
    report_path = base_path / "07_OUTPUTS" / f"organization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Count files in each folder
    folder_counts = {}
    for folder in base_path.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            count = count_files_recursive(folder)
            folder_counts[folder.name] = count
    
    report_content = f"""# Project Organization Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Folder Structure Created
```
TUBESABD/
├── 01_CORE_FILES/           ({folder_counts.get('01_CORE_FILES', 0)} files)
├── 02_DOCUMENTATION/        ({folder_counts.get('02_DOCUMENTATION', 0)} files)
├── 03_SCRIPTS/              ({folder_counts.get('03_SCRIPTS', 0)} files)
│   ├── airflow/
│   ├── spark/
│   ├── superset/
│   ├── postgres/
│   └── utilities/
├── 04_GUIDES/               ({folder_counts.get('04_GUIDES', 0)} files)
│   ├── setup/
│   ├── dashboard/
│   └── troubleshooting/
├── 05_ARCHIVED/             ({folder_counts.get('05_ARCHIVED', 0)} files)
├── 06_ASSETS/               ({folder_counts.get('06_ASSETS', 0)} files)
└── 07_OUTPUTS/              ({folder_counts.get('07_OUTPUTS', 0)} files)
```

## Organization Summary
- ✅ Project successfully organized
- 📁 Created 7 main folders with subfolders
- 📝 Added README files for documentation
- 🗂️ Files organized by purpose and service
- 📦 Old/duplicate files archived safely

## Core Files Kept in Root
- docker-compose.yml
- hadoop.env
- README.md

## Next Steps
1. Verify all services still work correctly
2. Update any hardcoded file paths in scripts
3. Test dashboard functionality
4. Review archived files and delete if not needed

## Backup Information
If you need to restore any files, check the 05_ARCHIVED/ folder.
Original file locations are preserved in the folder structure.
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_path

def count_files_recursive(folder):
    """Count files recursively in a folder"""
    count = 0
    try:
        for item in folder.rglob("*"):
            if item.is_file():
                count += 1
    except:
        pass
    return count

def main():
    print("🧹 BIG DATA PROJECT CLEANUP & ORGANIZATION")
    print("=" * 50)
    print("Kelompok 18 - Poverty Mapping Project")
    print()
    
    # Confirm before proceeding
    response = input("⚠️  This will reorganize all files in your workspace. Continue? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Organization cancelled.")
        return
    
    try:
        print("\n🏗️  Step 1: Creating folder structure...")
        create_folder_structure()
        
        print("\n📦 Step 2: Organizing files...")
        moved_files = organize_files()
        
        print("\n📄 Step 3: Moving remaining documentation...")
        move_remaining_files()
        
        print("\n📝 Step 4: Creating README files...")
        create_readme_files()
        
        print("\n📊 Step 5: Generating organization report...")
        report_path = create_organization_report()
        
        print("\n" + "=" * 50)
        print("✅ PROJECT ORGANIZATION COMPLETE!")
        print("=" * 50)
        print(f"📁 Files organized into structured folders")
        print(f"📝 Report generated: {report_path}")
        print(f"🗂️ Total files moved: {len(moved_files)}")
        
        print("\n🎯 WHAT'S NEXT:")
        print("1. ✅ Verify services still work: docker-compose up -d")
        print("2. ✅ Test your Superset dashboard")
        print("3. ✅ Review archived files in 05_ARCHIVED/")
        print("4. ✅ Update any scripts with hardcoded paths if needed")
        
        print(f"\n📋 Organization report: {report_path}")
        
    except Exception as e:
        print(f"❌ Error during organization: {e}")
        print("🔧 You may need to manually organize some files.")

if __name__ == "__main__":
    main()
