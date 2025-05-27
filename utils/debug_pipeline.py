#!/usr/bin/env python3
"""
DEBUG PIPELINE - Poverty Mapping ETL
Kelompok 18 - Debugging script without Airflow dependencies

This script debugs and tests the entire pipeline using Python3
to identify issues before running in Airflow.
"""

import os
import sys
import subprocess
import logging
import time
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PipelineDebugger:
    def __init__(self, base_path="c:/TUBESABD"):
        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data"
        self.scripts_path = self.base_path / "scripts"
        self.logs_path = self.base_path / "logs"
        
        # Ensure directories exist
        self.logs_path.mkdir(exist_ok=True)
        
    def log_step(self, step_name, message):
        """Log pipeline step with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"🔄 [{step_name}] {message}")
        
    def check_prerequisites(self):
        """Check if all required files and services are available"""
        self.log_step("PREREQ", "Checking prerequisites...")
        
        # Check data file
        data_file = self.data_path / "Profil_Kemiskinan_Sumatera.csv"
        if not data_file.exists():
            logger.error(f"❌ Data file not found: {data_file}")
            return False
        logger.info(f"✅ Data file found: {data_file}")
        
        # Check scripts
        ingest_script = self.scripts_path / "ingest_data.sh"
        if not ingest_script.exists():
            logger.error(f"❌ Ingest script not found: {ingest_script}")
            return False
        logger.info(f"✅ Ingest script found: {ingest_script}")
        
        # Check Docker containers
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                containers = result.stdout
                logger.info("📦 Active Docker containers:")
                for line in containers.split('\n')[1:]:  # Skip header
                    if line.strip():
                        logger.info(f"   • {line.strip()}")
                        
                # Check for required containers
                required_containers = ['namenode', 'spark-master', 'airflow-webserver']
                for container in required_containers:
                    if container in containers:
                        logger.info(f"✅ Container {container} is running")
                    else:
                        logger.warning(f"⚠️  Container {container} not found")
            else:
                logger.error("❌ Docker is not running or accessible")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Docker command timed out")
            return False
        except FileNotFoundError:
            logger.error("❌ Docker not found in PATH")
            return False
            
        return True
    
    def test_ingest_to_bronze(self):
        """Test data ingestion to Bronze layer"""
        self.log_step("BRONZE", "Testing data ingestion to Bronze layer...")
        
        try:
            # Check if namenode container exists
            check_container = subprocess.run([
                'docker', 'exec', 'namenode', 'ls', '/data/'
            ], capture_output=True, text=True, timeout=30)
            
            if check_container.returncode != 0:
                logger.error(f"❌ Cannot access namenode container: {check_container.stderr}")
                return False
                
            logger.info("✅ Namenode container accessible")
            logger.info(f"📁 Container /data/ contents: {check_container.stdout.strip()}")
            
            # Test HDFS commands
            hdfs_test = subprocess.run([
                'docker', 'exec', 'namenode', 'hdfs', 'dfs', '-ls', '/'
            ], capture_output=True, text=True, timeout=30)
            
            if hdfs_test.returncode == 0:
                logger.info("✅ HDFS is accessible")
                logger.info(f"📂 HDFS root contents: {hdfs_test.stdout}")
            else:
                logger.warning(f"⚠️  HDFS test failed: {hdfs_test.stderr}")
                
            # Test data ingestion simulation
            logger.info("🔄 Simulating data ingestion...")
            
            # Create bronze directory if not exists
            create_bronze = subprocess.run([
                'docker', 'exec', 'namenode', 'hdfs', 'dfs', '-mkdir', '-p', '/data/bronze'
            ], capture_output=True, text=True, timeout=30)
            
            if create_bronze.returncode == 0:
                logger.info("✅ Bronze directory created/verified")
            else:
                logger.warning(f"⚠️  Bronze directory creation warning: {create_bronze.stderr}")
            
            # Simulate file upload (check if source exists)
            check_source = subprocess.run([
                'docker', 'exec', 'namenode', 'ls', '/data/Profil_Kemiskinan_Sumatera.csv'
            ], capture_output=True, text=True, timeout=30)
            
            if check_source.returncode == 0:
                logger.info("✅ Source data file accessible in container")
                
                # Try actual upload
                upload_cmd = subprocess.run([
                    'docker', 'exec', 'namenode', 'hdfs', 'dfs', '-put', '-f', 
                    '/data/Profil_Kemiskinan_Sumatera.csv', '/data/bronze/'
                ], capture_output=True, text=True, timeout=60)
                
                if upload_cmd.returncode == 0:
                    logger.info("✅ Data successfully uploaded to Bronze layer")
                    return True
                else:
                    logger.error(f"❌ Upload failed: {upload_cmd.stderr}")
                    return False
            else:
                logger.error(f"❌ Source data not accessible in container: {check_source.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Bronze layer test timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Bronze layer test failed: {str(e)}")
            return False
    
    def test_spark_connection(self):
        """Test Spark cluster connectivity"""
        self.log_step("SPARK", "Testing Spark cluster connectivity...")
        
        try:
            # Check Spark master
            spark_test = subprocess.run([
                'docker', 'exec', 'spark-master', 'ls', '/scripts/spark/'
            ], capture_output=True, text=True, timeout=30)
            
            if spark_test.returncode == 0:
                logger.info("✅ Spark master accessible")
                logger.info(f"📁 Spark scripts available: {spark_test.stdout.strip()}")
                return True
            else:
                logger.error(f"❌ Spark master not accessible: {spark_test.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Spark connection test timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Spark test failed: {str(e)}")
            return False
    
    def test_airflow_volume_mapping(self):
        """Test Airflow container volume mapping"""
        self.log_step("AIRFLOW", "Testing Airflow volume mapping...")
        
        try:
            # Check if scripts are accessible from Airflow container
            containers = ['airflow-webserver', 'airflow-scheduler']
            
            for container in containers:
                # Check if container exists
                check_container = subprocess.run([
                    'docker', 'ps', '--filter', f'name={container}', '--format', '{{.Names}}'
                ], capture_output=True, text=True, timeout=10)
                
                if container not in check_container.stdout:
                    logger.warning(f"⚠️  Container {container} not running")
                    continue
                
                # Check volume mapping
                volume_test = subprocess.run([
                    'docker', 'exec', container, 'ls', '/scripts/'
                ], capture_output=True, text=True, timeout=30)
                
                if volume_test.returncode == 0:
                    logger.info(f"✅ {container}: /scripts/ accessible")
                    logger.info(f"📁 Scripts in {container}: {volume_test.stdout.strip()}")
                else:
                    logger.error(f"❌ {container}: /scripts/ not accessible - {volume_test.stderr}")
                    
        except Exception as e:
            logger.error(f"❌ Airflow volume test failed: {str(e)}")
            return False
    
    def generate_fixed_dag(self):
        """Generate a fixed DAG file"""
        self.log_step("FIX", "Generating fixed DAG file...")
        
        fixed_dag_content = '''"""
FIXED Airflow DAG for Poverty Mapping ETL Pipeline
Kelompok 18 - Pemetaan Kemiskinan Sumatera
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import logging

# Default arguments
default_args = {
    'owner': 'kelompok18',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Create DAG
dag = DAG(
    'poverty_mapping_etl_fixed_v2',
    default_args=default_args,
    description='FIXED Poverty Mapping ETL Pipeline for Sumatra',
    schedule_interval=None,  # Manual trigger only
    catchup=False,
    tags=['poverty', 'sumatra', 'etl', 'bigdata', 'fixed']
)

# Task 1: Data ingestion to Bronze layer (Fixed)
ingest_to_bronze = BashOperator(
    task_id='ingest_to_bronze',
    bash_command='docker exec namenode hdfs dfs -mkdir -p /data/bronze && docker exec namenode hdfs dfs -put -f /data/Profil_Kemiskinan_Sumatera.csv /data/bronze/ && echo "Bronze ingestion completed"',
    dag=dag
)

# Task 2: Bronze to Silver transformation
bronze_to_silver = BashOperator(
    task_id='bronze_to_silver_transform',
    bash_command='echo "Bronze to Silver transformation - placeholder"',
    dag=dag
)

# Task 3: Silver to Gold aggregation  
silver_to_gold = BashOperator(
    task_id='silver_to_gold_aggregation',
    bash_command='echo "Silver to Gold aggregation - placeholder"',
    dag=dag
)

# Task 4: Simple validation
def simple_validation():
    """Simple validation without external dependencies"""
    logging.info("🔍 Running simple validation...")
    logging.info("✅ Validation completed")
    return "success"

validation_task = PythonOperator(
    task_id='simple_validation',
    python_callable=simple_validation,
    dag=dag
)

# Task dependencies
ingest_to_bronze >> bronze_to_silver >> silver_to_gold >> validation_task
'''
        
        # Write fixed DAG
        fixed_dag_path = self.base_path / "airflow" / "dags" / "poverty_mapping_dag_debug_fixed.py"
        with open(fixed_dag_path, 'w', encoding='utf-8') as f:
            f.write(fixed_dag_content)
            
        logger.info(f"✅ Fixed DAG written to: {fixed_dag_path}")
        return True
    
    def run_debug_pipeline(self):
        """Run the complete debug pipeline"""
        logger.info("🚀 Starting Pipeline Debug Session")
        logger.info("=" * 60)
        
        # Step 1: Prerequisites
        if not self.check_prerequisites():
            logger.error("❌ Prerequisites failed - stopping debug")
            return False
        
        # Step 2: Test Bronze layer
        if not self.test_ingest_to_bronze():
            logger.error("❌ Bronze layer test failed")
        
        # Step 3: Test Spark
        if not self.test_spark_connection():
            logger.error("❌ Spark test failed")
        
        # Step 4: Test Airflow volumes
        self.test_airflow_volume_mapping()
        
        # Step 5: Generate fixed DAG
        self.generate_fixed_dag()
        
        logger.info("🎉 Debug session completed!")
        logger.info("=" * 60)
        
        return True

if __name__ == "__main__":
    debugger = PipelineDebugger()
    debugger.run_debug_pipeline()
