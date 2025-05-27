#!/usr/bin/env python3
"""
Simple test untuk functions DAG tanpa import Airflow
"""

import subprocess
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_docker_containers():
    """Test Docker containers"""
    logging.info("🐳 Testing Docker containers...")
    
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            logging.info("✅ Docker containers status:")
            logging.info(result.stdout)
            
            # Check specific containers
            containers = ['namenode', 'spark-master', 'airflow']
            for container in containers:
                if container in result.stdout:
                    logging.info(f"✅ {container} is running")
                else:
                    logging.warning(f"⚠️ {container} not found")
                    
        else:
            logging.error(f"❌ Docker command failed: {result.stderr}")
            
    except Exception as e:
        logging.error(f"❌ Error checking containers: {str(e)}")

def test_data_file():
    """Test if data file exists"""
    logging.info("📊 Testing data file...")
    
    data_file = "data/Profil_Kemiskinan_Sumatera.csv"
    
    if os.path.exists(data_file):
        size_mb = os.path.getsize(data_file) / (1024 * 1024)
        logging.info(f"✅ Data file found: {data_file} ({size_mb:.2f} MB)")
        
        # Count lines
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                lines = sum(1 for line in f)
            logging.info(f"📋 Total lines: {lines:,}")
        except Exception as e:
            logging.error(f"❌ Error reading file: {str(e)}")
    else:
        logging.error(f"❌ Data file not found: {data_file}")

def test_hdfs_basic():
    """Test basic HDFS operations"""
    logging.info("🗂️ Testing HDFS basic operations...")
    
    try:
        # Test HDFS connection
        cmd = ['docker', 'exec', 'namenode', 'hdfs', 'dfs', '-ls', '/']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            logging.info("✅ HDFS connection successful")
            logging.info("📁 HDFS root directory:")
            logging.info(result.stdout)
        else:
            logging.error(f"❌ HDFS connection failed: {result.stderr}")
            
    except Exception as e:
        logging.error(f"❌ Error testing HDFS: {str(e)}")

def test_spark_connection():
    """Test Spark connection"""
    logging.info("⚡ Testing Spark connection...")
    
    try:
        cmd = ['docker', 'exec', 'spark-master', 'spark-submit', '--version']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            logging.info("✅ Spark connection successful")
            # Parse version from stderr (Spark writes version to stderr)
            version_info = result.stderr.split('\n')[0] if result.stderr else "Version info in stdout"
            logging.info(f"🔧 Spark version: {version_info}")
        else:
            logging.error(f"❌ Spark connection failed: {result.stderr}")
            
    except Exception as e:
        logging.error(f"❌ Error testing Spark: {str(e)}")

def test_airflow_connection():
    """Test Airflow connection"""
    logging.info("🔄 Testing Airflow connection...")
    
    try:
        cmd = ['docker', 'exec', 'airflow', 'airflow', 'version']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            logging.info("✅ Airflow connection successful")
            logging.info(f"🔧 Airflow version: {result.stdout.strip()}")
        else:
            logging.error(f"❌ Airflow connection failed: {result.stderr}")
            
    except Exception as e:
        logging.error(f"❌ Error testing Airflow: {str(e)}")

def test_dag_files():
    """Test DAG files"""
    logging.info("📋 Testing DAG files...")
    
    dag_dir = "airflow/dags"
    
    if os.path.exists(dag_dir):
        dag_files = [f for f in os.listdir(dag_dir) if f.endswith('.py')]
        logging.info(f"✅ Found {len(dag_files)} DAG files:")
        
        for dag_file in dag_files:
            logging.info(f"  📄 {dag_file}")
            
            # Check file size
            file_path = os.path.join(dag_dir, dag_file)
            size_kb = os.path.getsize(file_path) / 1024
            logging.info(f"     Size: {size_kb:.1f} KB")
            
    else:
        logging.error(f"❌ DAG directory not found: {dag_dir}")

def main():
    """Run all tests"""
    logging.info("🚀 STARTING PIPELINE COMPONENT TESTS")
    logging.info("=" * 60)
    
    tests = [
        ("Docker Containers", test_docker_containers),
        ("Data File", test_data_file),
        ("HDFS Connection", test_hdfs_basic),
        ("Spark Connection", test_spark_connection),
        ("Airflow Connection", test_airflow_connection),
        ("DAG Files", test_dag_files)
    ]
    
    for test_name, test_func in tests:
        logging.info(f"\n🧪 Running: {test_name}")
        logging.info("-" * 40)
        
        try:
            test_func()
        except Exception as e:
            logging.error(f"❌ {test_name} failed: {str(e)}")
    
    logging.info("\n" + "=" * 60)
    logging.info("🎯 COMPONENT TEST COMPLETED")
    logging.info("\n📋 NEXT STEPS:")
    logging.info("1. Check Airflow UI: http://localhost:8090")
    logging.info("2. Look for DAG: poverty_mapping_etl_final")
    logging.info("3. Enable and trigger the DAG")
    logging.info("4. Monitor execution in Airflow logs")
    
    logging.info("\n🔗 SERVICE URLs:")
    logging.info("   • Airflow: http://localhost:8090")
    logging.info("   • Spark UI: http://localhost:8080")
    logging.info("   • HDFS: http://localhost:9870")
    logging.info("   • Jupyter: http://localhost:8888")
    logging.info("   • Superset: http://localhost:8089")

if __name__ == "__main__":
    main()
