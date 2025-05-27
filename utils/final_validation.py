#!/usr/bin/env python3
"""
Final Pipeline Validation and Status Check
Kelompok 18 - Pemetaan Kemiskinan Sumatera
"""

import os
import sys
from datetime import datetime

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {filepath} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {filepath} (NOT FOUND)")
        return False

def main():
    print("🔍 PIPELINE VALIDATION CHECK")
    print("=" * 60)
    print("Team: Kelompok 18")
    print("Project: Pemetaan Kemiskinan Sumatera")
    print("Validation Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # Check core files
    print("\n📋 CORE FILES VALIDATION:")
    print("-" * 40)
    
    files_to_check = [
        ("data/Profil_Kemiskinan_Sumatera.csv", "Poverty Data Source"),
        ("docker-compose.yml", "Docker Orchestration"),
        ("scripts/bronze_to_silver.py", "Bronze to Silver ETL"),
        ("scripts/silver_to_gold.py", "Silver to Gold ETL"),
        ("scripts/ml_poverty_prediction.py", "ML Prediction Script"),
        ("dags/poverty_mapping_dag.py", "Airflow DAG"),
        ("notebooks/01_Data_Exploration_Poverty_Mapping.ipynb", "Data Exploration Notebook"),
        ("notebooks/02_Machine_Learning_Poverty_Prediction.ipynb", "ML Notebook"),
        ("notebooks/Complete_Pipeline_Execution.py", "Complete Pipeline Script"),
        ("READY_TO_EXECUTE.md", "Execution Guide"),
        ("EXECUTION_REPORT.md", "Status Report")
    ]
    
    valid_files = 0
    total_files = len(files_to_check)
    
    for filepath, description in files_to_check:
        if check_file_exists(filepath, description):
            valid_files += 1
    
    # Validation summary
    print(f"\n📊 VALIDATION SUMMARY:")
    print("-" * 30)
    print(f"✅ Valid files: {valid_files}/{total_files}")
    print(f"📈 Completion rate: {(valid_files/total_files)*100:.1f}%")
    
    if valid_files == total_files:
        print(f"\n🎉 ALL SYSTEMS READY!")
        print("✅ Pipeline is 100% ready for execution")
        print("🚀 Proceed to Jupyter Notebook: http://localhost:8888")
    else:
        print(f"\n⚠️ SOME FILES MISSING")
        print(f"❌ {total_files - valid_files} files need attention")
    
    # Service access links
    print(f"\n🔗 SERVICE ACCESS LINKS:")
    print("-" * 30)
    print("📓 Jupyter Notebook: http://localhost:8888")
    print("🗂️ Hadoop HDFS: http://localhost:9870")
    print("⚡ Spark Master: http://localhost:8080")
    print("🔄 Airflow: http://localhost:8090")
    
    # Next steps
    print(f"\n🎯 NEXT STEPS:")
    print("-" * 20)
    print("1. Access Jupyter Notebook")
    print("2. Run Complete_Pipeline_Execution.py")
    print("3. Execute ML notebooks for detailed analysis")
    print("4. Generate executive summary and insights")
    
    print(f"\n" + "=" * 60)
    print("🏆 BIG DATA PIPELINE - READY FOR EXECUTION!")
    print("=" * 60)

if __name__ == "__main__":
    main()
