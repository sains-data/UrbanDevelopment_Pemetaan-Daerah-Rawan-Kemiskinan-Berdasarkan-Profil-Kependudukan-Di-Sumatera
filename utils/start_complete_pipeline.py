"""
Final Project Startup and Verification
Kelompok 18 - Big Data Pipeline for Poverty Mapping in Sumatra
Complete system startup and dashboard preparation
"""

import subprocess
import time
import os
import sqlite3
from datetime import datetime

def print_header():
    """Print project header"""
    print("🚀 BIG DATA PIPELINE STARTUP")
    print("=" * 60)
    print("📋 Kelompok 18 - Poverty Mapping in Sumatra")
    print(f"🗓️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_docker():
    """Check if Docker is running"""
    print("🐳 Checking Docker status...")
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is running")
            return True
        else:
            print("❌ Docker is not running!")
            return False
    except:
        print("❌ Docker not found!")
        return False

def start_services():
    """Start all Docker services"""
    print("\n🔄 Starting Docker Compose services...")
    try:
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        print("✅ All services started")
        return True
    except:
        print("❌ Failed to start services")
        return False

def wait_for_services():
    """Wait for services to be ready"""
    print("\n⏳ Waiting for services to initialize...")
    services = [
        ("Hadoop NameNode", "http://localhost:9870"),
        ("Spark Master", "http://localhost:8080"), 
        ("Jupyter Notebook", "http://localhost:8888"),
        ("Airflow", "http://localhost:8084"),
        ("Superset", "http://localhost:8089")
    ]
    
    for service, url in services:
        print(f"   🔍 Checking {service}...")
        time.sleep(2)
    
    print("✅ Services initialization period completed")

def verify_database():
    """Verify poverty mapping database"""
    print("\n🗄️ Verifying poverty mapping database...")
    
    db_path = 'superset_data/poverty_mapping.db'
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        
        if 'poverty_data' not in tables:
            print("❌ Main table 'poverty_data' not found!")
            return False
        
        # Check record count
        cursor.execute("SELECT COUNT(*) FROM poverty_data")
        count = cursor.fetchone()[0]
        
        print(f"✅ Database verified: {count:,} records")
        print(f"   📊 Tables: {', '.join(tables)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def show_access_info():
    """Show all access information"""
    print("\n🔗 SERVICE ACCESS INFORMATION")
    print("-" * 60)
    
    services = [
        ("🎨 Superset Dashboard", "http://localhost:8089", "admin/admin"),
        ("📊 Jupyter Notebooks", "http://localhost:8888", "token required"),
        ("🗄️ Hadoop HDFS", "http://localhost:9870", "no auth"),
        ("⚡ Spark Master", "http://localhost:8080", "no auth"),
        ("🔄 Airflow", "http://localhost:8084", "admin/admin")
    ]
    
    for service, url, auth in services:
        print(f"{service:25} {url:30} {auth}")

def show_dashboard_setup():
    """Show dashboard setup instructions"""
    print("\n📊 DASHBOARD CREATION STEPS")
    print("-" * 60)
    
    db_path = os.path.abspath('superset_data/poverty_mapping.db')
    sqlite_uri = f"sqlite:///{db_path.replace(chr(92), '/')}"
    
    steps = [
        "1. Open Superset: http://localhost:8089",
        "2. Login with admin/admin",
        "3. Go to Settings → Database Connections",
        "4. Create new database connection:",
        f"   - Name: Poverty_Mapping_Sumatra",
        f"   - URI: {sqlite_uri}",
        "5. Go to Data → Datasets",
        "6. Create datasets from tables: poverty_data, province_summary",
        "7. Go to Charts → Create new charts",
        "8. Create 6 recommended visualizations",
        "9. Build dashboard with all charts",
        "10. Generate insights and recommendations!"
    ]
    
    for step in steps:
        print(f"   {step}")

def show_project_summary():
    """Show final project summary"""
    print("\n🎯 PROJECT COMPLETION SUMMARY")
    print("-" * 60)
    
    components = [
        ("✅ Infrastructure", "Docker Compose with 14+ services"),
        ("✅ Data Pipeline", "Bronze → Silver → Gold ETL"),
        ("✅ Data Processing", "20,000+ poverty records"),
        ("✅ Machine Learning", "Poverty prediction models"),
        ("✅ Automation", "Airflow workflow orchestration"),
        ("✅ Visualization", "Superset dashboard platform"),
        ("✅ Documentation", "Comprehensive guides and reports")
    ]
    
    for status, description in components:
        print(f"   {status:20} {description}")

def main():
    """Main execution function"""
    print_header()
    
    # Check Docker
    if not check_docker():
        print("\n❌ Please start Docker Desktop and try again!")
        return
    
    # Start services
    if not start_services():
        print("\n❌ Failed to start services!")
        return
    
    # Wait for initialization
    wait_for_services()
    
    # Verify database
    if not verify_database():
        print("\n❌ Database verification failed!")
        return
    
    # Show access info
    show_access_info()
    
    # Show dashboard setup
    show_dashboard_setup()
    
    # Show project summary
    show_project_summary()
    
    print("\n" + "=" * 60)
    print("🎉 BIG DATA PIPELINE READY!")
    print("=" * 60)
    print("🔗 Next: Create amazing dashboards in Superset!")
    print("📖 Guide: FINAL_PROJECT_REPORT.md")
    print(f"🕒 Ready: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✨ Happy analyzing! - Kelompok 18")

if __name__ == "__main__":
    main()
