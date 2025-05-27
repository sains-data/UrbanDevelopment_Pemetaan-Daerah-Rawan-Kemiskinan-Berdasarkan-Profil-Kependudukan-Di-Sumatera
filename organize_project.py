# 📁 File Organization Script
# Kelompok 18 - Big Data Project Organization

import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_directories():
    """Create project directories"""
    dirs = ['utils', 'docs']
    
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logging.info(f"📁 Created directory: {dir_name}")
        else:
            logging.info(f"📁 Directory exists: {dir_name}")

def move_files():
    """Move files to appropriate directories"""
    
    # Files to move to utils/
    util_files = [
        'check_database.py',
        'demo_pipeline_execution.py', 
        'final_validation.py',
        'manual_superset_setup.py',
        'next_steps.py',
        'run_etl_pipeline.py',
        'run_pipeline_simple.py', 
        'setup_superset_dashboard.py',
        'simple_demo.py',
        'simple_superset_setup.py',
        'start_complete_pipeline.py',
        'superset_api_setup.py',
        'verify_superset_setup.py',
        'test_dag_syntax.py',
        'debug_pipeline_comprehensive.py',
        'debug_pipeline.py',
        'test_airflow_dag.py',
        'test_components.py',
        'organize_files.ps1',
        'check_services.ps1',
        'open_superset.ps1', 
        'prepare_github.ps1',
        'quick_access.ps1',
        'fix_airflow.sh',
        'prepare_github.sh',
        'quick_access.sh', 
        'run_complete_pipeline.sh',
        'start.sh',
        'validate_pipeline.bat'
    ]
    
    # Files to move to docs/
    doc_files = [
        'DEPLOYMENT_REPORT.md',
        'EXECUTION_REPORT.md',
        'FINAL_PROJECT_REPORT.md', 
        'PROJECT_COMPLETE.md',
        'PROJECT_STATUS_FINAL.md',
        'READY_TO_EXECUTE.md',
        'SUPERSET_READY.md',
        'AIRFLOW_DAG_FIX_SUMMARY.md',
        'Dokumen Spesifikasi Proyek Big Data Kelompok 18 (1) (1).pdf'
    ]
    
    # Move utility files
    for file_name in util_files:
        if os.path.exists(file_name):
            try:
                shutil.move(file_name, f'utils/{file_name}')
                logging.info(f"✅ Moved to utils/: {file_name}")
            except Exception as e:
                logging.error(f"❌ Error moving {file_name}: {e}")
        else:
            logging.warning(f"⚠️ File not found: {file_name}")
    
    # Move documentation files  
    for file_name in doc_files:
        if os.path.exists(file_name):
            try:
                shutil.move(file_name, f'docs/{file_name}')
                logging.info(f"✅ Moved to docs/: {file_name}")
            except Exception as e:
                logging.error(f"❌ Error moving {file_name}: {e}")
        else:
            logging.warning(f"⚠️ File not found: {file_name}")

def show_final_structure():
    """Show final project structure"""
    logging.info("\n📋 FINAL PROJECT STRUCTURE:")
    logging.info("=" * 50)
    
    # Root files
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    logging.info("🗂️ ROOT DIRECTORY:")
    for f in sorted(root_files):
        logging.info(f"  📄 {f}")
    
    # Directories
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    for dir_name in sorted(dirs):
        logging.info(f"\n📁 {dir_name}/")
        try:
            for f in sorted(os.listdir(dir_name)):
                if os.path.isfile(os.path.join(dir_name, f)):
                    logging.info(f"  📄 {f}")
                else:
                    logging.info(f"  📁 {f}/")
        except Exception as e:
            logging.error(f"  ❌ Error reading directory: {e}")

def main():
    logging.info("🚀 STARTING FILE ORGANIZATION")
    logging.info("=" * 50)
    
    create_directories()
    move_files()
    show_final_structure()
    
    logging.info("\n🎉 FILE ORGANIZATION COMPLETED!")
    logging.info("📦 Project ready for GitHub push")

if __name__ == "__main__":
    main()
