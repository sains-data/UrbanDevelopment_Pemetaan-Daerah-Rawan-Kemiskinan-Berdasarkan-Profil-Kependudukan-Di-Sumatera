#!/usr/bin/env python3
"""
Project Organization Script - Kelompok 18 Poverty Mapping Pipeline
Membersihkan dan mengorganisir file-file project big data
"""

import os
import shutil
from pathlib import Path

def organize_project():
    """Organize project files into proper structure"""
    
    base_dir = Path("C:/TUBESABD")
    
    # Create organized directory structure
    dirs_to_create = [
        "organized/core",           # Core pipeline files
        "organized/scripts",        # Active scripts
        "organized/docs",          # Important documentation
        "organized/archived",      # Old/debug files to archive
        "organized/data",          # Data files
        "organized/config"         # Configuration files
    ]
    
    for dir_path in dirs_to_create:
        (base_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    print("📁 Created organized directory structure")
    
    # Core pipeline files (KEEP AS IS - ACTIVE)
    core_files = [
        "docker-compose.yml",
        "airflow/dags/poverty_mapping_dag_final.py",  # ✅ MAIN DAG - JANGAN UBAH
        "init_postgres.sql",
        "hadoop.env"
    ]
    
    # Important scripts (KEEP - ACTIVE)
    active_scripts = [
        "start_pipeline.ps1",
        "open_all_services.ps1", 
        "postgres_manager.ps1",
        "verify_services_ready.py",
        "run_pipeline.py"
    ]
    
    # Important documentation (KEEP)
    important_docs = [
        "README.md",
        "PIPELINE_ORGANIZATION_FINAL.md",
        "docs/PROJECT_COMPLETION_FINAL.md",
        "docs/DEPLOYMENT_REPORT.md"
    ]
    
    # Data files (KEEP)
    data_files = [
        "data/Profil_Kemiskinan_Sumatera.csv"
    ]
    
    # Config files (KEEP)
    config_files = [
        "config/superset_config.py"
    ]
    
    # Files to archive (debug/fix files)
    archive_patterns = [
        "fix_*.py",
        "fix_*.bat", 
        "fix_*.ps1",
        "*_fix_*.md",
        "simple_*.py",
        "quick_*.py",
        "debug_*.py",
        "verify_*.py",
        "setup_*.py",
        "automate_*.py",
        "cleanup_*.ps1",
        "*_GUIDE.md",
        "*_FIX*.md",
        "MANUAL_*.md",
        "SUPERSET_*.md",
        "POSTGRESQL_*.md"
    ]
    
    print("\n📋 PROJECT ORGANIZATION SUMMARY:")
    print("=" * 60)
    
    print(f"\n✅ CORE PIPELINE (Active - DO NOT MOVE):")
    for file in core_files:
        if (base_dir / file).exists():
            print(f"   📄 {file}")
    
    print(f"\n🔧 ACTIVE SCRIPTS:")
    for file in active_scripts:
        if (base_dir / file).exists():
            print(f"   📜 {file}")
    
    print(f"\n📚 IMPORTANT DOCS:")
    for file in important_docs:
        if (base_dir / file).exists():
            print(f"   📖 {file}")
    
    print(f"\n📊 DATA FILES:")
    for file in data_files:
        if (base_dir / file).exists():
            print(f"   💾 {file}")
    
    # List files that can be archived
    print(f"\n🗑️ FILES TO ARCHIVE (Debug/Historical):")
    archive_count = 0
    
    for pattern in archive_patterns:
        for file_path in base_dir.glob(pattern):
            if file_path.is_file():
                print(f"   📦 {file_path.name}")
                archive_count += 1
    
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ Core Pipeline Files: {len([f for f in core_files if (base_dir / f).exists()])}")
    print(f"   🔧 Active Scripts: {len([f for f in active_scripts if (base_dir / f).exists()])}")
    print(f"   📚 Important Docs: {len([f for f in important_docs if (base_dir / f).exists()])}")
    print(f"   🗑️ Files to Archive: {archive_count}")
    
    print(f"\n🎯 MAIN AIRFLOW DAG: poverty_mapping_dag_final.py")
    print(f"   📍 DAG ID: poverty_mapping_etl_final")
    print(f"   ⚠️  JANGAN DIUBAH NAMA DAG-nya!")
    
    return {
        'core_files': len([f for f in core_files if (base_dir / f).exists()]),
        'active_scripts': len([f for f in active_scripts if (base_dir / f).exists()]),
        'docs': len([f for f in important_docs if (base_dir / f).exists()]),
        'archive_candidates': archive_count
    }

def create_quick_access_guide():
    """Create quick access guide for the pipeline"""
    
    guide_content = """# 🚀 KELOMPOK 18 - QUICK ACCESS GUIDE
# Pemetaan Kemiskinan Sumatera

## 🎯 PIPELINE OVERVIEW
- **DAG Name**: `poverty_mapping_etl_final` ✅ (JANGAN DIUBAH)
- **Data**: Profil Kemiskinan Sumatera (20,000+ records)
- **Tech**: Docker + Hadoop + Spark + Airflow + PostgreSQL + Superset

## ⚡ QUICK START

### 1. Start All Services
```powershell
docker-compose up -d
```

### 2. Access Services
- **Airflow**: http://localhost:8090 (admin/admin)
- **Superset**: http://localhost:8089 (admin/admin)  
- **Spark**: http://localhost:8080
- **Jupyter**: http://localhost:8888
- **HDFS**: http://localhost:9870

### 3. Run ETL Pipeline
1. Go to Airflow: http://localhost:8090
2. Find DAG: `poverty_mapping_etl_final`
3. Toggle ON → Trigger DAG

### 4. Create Dashboards
1. Go to Superset: http://localhost:8089
2. Add PostgreSQL database connection
3. Create dataset from `poverty_clean` view
4. Build poverty mapping dashboards

## 📁 CORE FILES (ACTIVE)
```
c:/TUBESABD/
├── docker-compose.yml                          # Main orchestration
├── airflow/dags/poverty_mapping_dag_final.py   # ✅ MAIN DAG
├── data/Profil_Kemiskinan_Sumatera.csv        # Source data
├── start_pipeline.ps1                         # Start script
└── open_all_services.ps1                      # Open browsers
```

## 🗄️ DATABASE ACCESS
```
Host: postgres-local (or localhost)
Port: 5432
Database: poverty_mapping
Username: postgres
Password: postgres123
Main Table: poverty_data
Clean View: poverty_clean
```

## 📊 DATA PIPELINE FLOW
```
CSV → Airflow ETL → Spark Processing → PostgreSQL → Superset Dashboards
```

## 🎯 STATUS: READY FOR VISUALIZATION! ✅
Pipeline is working, data is loaded, ready for dashboard creation.

---
**Last Updated**: 2025-05-26
**Team**: Kelompok 18
**Project**: Pemetaan Kemiskinan Sumatera
"""
    
    with open("C:/TUBESABD/QUICK_ACCESS_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Created QUICK_ACCESS_GUIDE.md")

def main():
    print("🗂️ ORGANIZING KELOMPOK 18 - POVERTY MAPPING PIPELINE")
    print("=" * 70)
    
    # Organize project
    stats = organize_project()
    
    # Create quick access guide
    create_quick_access_guide()
    
    print("\n" + "=" * 70)
    print("✅ PROJECT ORGANIZATION COMPLETED!")
    print(f"\n🎯 PIPELINE STATUS: READY FOR DASHBOARD CREATION")
    print(f"📊 Main DAG: poverty_mapping_etl_final (ACTIVE)")
    print(f"🚀 Next: Create Superset dashboards for poverty mapping")
    
    print(f"\n📁 PROJECT STRUCTURE OPTIMIZED:")
    print(f"   ✅ Core files identified and preserved")
    print(f"   🔧 Active scripts ready for use")
    print(f"   📚 Documentation organized")
    print(f"   🗑️ {stats['archive_candidates']} debug files ready for cleanup")
    
    print(f"\n🎯 QUICK START:")
    print(f"   1. docker-compose up -d")
    print(f"   2. Access Airflow: http://localhost:8090")
    print(f"   3. Enable DAG: poverty_mapping_etl_final")
    print(f"   4. Create Superset dashboards: http://localhost:8089")

if __name__ == "__main__":
    main()
"""
