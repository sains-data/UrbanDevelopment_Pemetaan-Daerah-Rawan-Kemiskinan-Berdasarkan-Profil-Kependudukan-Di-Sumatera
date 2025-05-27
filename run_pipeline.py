#!/usr/bin/env python3
"""
Big Data Pipeline Executor - Sumatra Poverty Mapping
Kelompok 18 - Automated ETL Pipeline

This script orchestrates the complete data pipeline from ingestion to visualization.
"""

import subprocess
import time
import logging
import sys
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/pipeline_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class PovertyMappingPipeline:
    def __init__(self):
        self.base_path = "c:/TUBESABD"
        self.services_required = [
            "namenode", "datanode1", "datanode2", "resourcemanager", 
            "nodemanager", "historyserver", "spark-master", "spark-worker-1",
            "airflow-webserver", "airflow-scheduler", "jupyter", "superset"
        ]
        
    def log_step(self, step_name):
        """Decorator untuk logging setiap step"""
        logging.info(f"🚀 Starting: {step_name}")
        
    def check_docker_services(self):
        """Periksa status semua Docker services"""
        self.log_step("Docker Services Check")
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"],
                capture_output=True, text=True, check=True
            )
            
            running_services = []
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if line.strip():
                    service_name = line.split('\t')[0]
                    if any(req in service_name for req in self.services_required):
                        running_services.append(service_name)
            
            logging.info(f"✅ Running services: {len(running_services)}")
            for service in running_services:
                logging.info(f"  - {service}")
                
            if len(running_services) < 10:  # Minimum required services
                logging.warning("⚠️  Some services may not be running. Starting stack...")
                self.start_docker_stack()
                
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to check Docker services: {e}")
            return False
    
    def start_docker_stack(self):
        """Start Docker Compose stack"""
        self.log_step("Docker Stack Startup")
        try:
            subprocess.run(
                ["docker-compose", "up", "-d"],
                cwd=self.base_path, check=True
            )
            logging.info("✅ Docker stack started successfully")
            time.sleep(30)  # Wait for services to initialize
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to start Docker stack: {e}")
            return False
    
    def validate_data_source(self):
        """Validate source data availability"""
        self.log_step("Data Source Validation")
        data_file = f"{self.base_path}/data/Profil_Kemiskinan_Sumatera.csv"
        
        if not os.path.exists(data_file):
            logging.error(f"❌ Data file not found: {data_file}")
            return False
            
        # Check file size and basic structure
        file_size = os.path.getsize(data_file) / (1024 * 1024)  # MB
        logging.info(f"✅ Data file found: {file_size:.2f} MB")
        
        # Quick validation of CSV structure
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                header = f.readline().strip()
                sample_line = f.readline().strip()
                
            logging.info(f"✅ CSV Header: {header[:100]}...")
            logging.info(f"✅ Sample data available")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to validate data structure: {e}")
            return False
    
    def ingest_to_hdfs(self):
        """Ingest data to HDFS Bronze layer"""
        self.log_step("HDFS Data Ingestion")
        try:
            # Create HDFS directories
            subprocess.run([
                "docker", "exec", "namenode", "hdfs", "dfs", "-mkdir", "-p", "/data/bronze"
            ], check=True)
            
            # Copy data to HDFS
            subprocess.run([
                "docker", "exec", "namenode", "hdfs", "dfs", "-put", 
                "/data/Profil_Kemiskinan_Sumatera.csv", "/data/bronze/"
            ], check=True)
            
            # Verify ingestion
            result = subprocess.run([
                "docker", "exec", "namenode", "hdfs", "dfs", "-ls", "/data/bronze/"
            ], capture_output=True, text=True, check=True)
            
            logging.info("✅ Data successfully ingested to HDFS Bronze layer")
            logging.info(f"HDFS Contents: {result.stdout}")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to ingest data to HDFS: {e}")
            return False
    
    def run_spark_etl(self):
        """Execute Spark ETL transformations"""
        self.log_step("Spark ETL Processing")
        
        spark_jobs = [
            ("Bronze to Silver", "/scripts/spark/bronze_to_silver.py"),
            ("Silver to Gold", "/scripts/spark/silver_to_gold.py"),
            ("ML Analysis", "/scripts/spark/ml_poverty_prediction.py")
        ]
        
        for job_name, script_path in spark_jobs:
            try:
                logging.info(f"🔄 Running: {job_name}")
                subprocess.run([
                    "docker", "exec", "spark-master", 
                    "spark-submit", "--master", "spark://spark-master:7077", script_path
                ], check=True)
                
                logging.info(f"✅ Completed: {job_name}")
                
            except subprocess.CalledProcessError as e:
                logging.error(f"❌ Failed: {job_name} - {e}")
                return False
        
        return True
    
    def trigger_airflow_dag(self):
        """Trigger Airflow DAG execution"""
        self.log_step("Airflow DAG Execution")
        try:
            # Enable DAG
            subprocess.run([
                "docker", "exec", "airflow-webserver", 
                "airflow", "dags", "unpause", "poverty_mapping_dag_final"
            ], check=True)
            
            # Trigger DAG run
            subprocess.run([
                "docker", "exec", "airflow-webserver",
                "airflow", "dags", "trigger", "poverty_mapping_dag_final"
            ], check=True)
            
            logging.info("✅ Airflow DAG triggered successfully")
            logging.info("🌐 Monitor progress at: http://localhost:8090")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to trigger Airflow DAG: {e}")
            return False
    
    def setup_superset_dashboard(self):
        """Setup Superset dashboard"""
        self.log_step("Superset Dashboard Setup")
        try:
            # Check if Superset is accessible
            subprocess.run([
                "docker", "exec", "superset", "superset", "fab", "list-views"
            ], check=True)
            
            logging.info("✅ Superset is ready")
            logging.info("🌐 Access dashboard at: http://localhost:8089")
            logging.info("🔑 Login: admin/admin")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Superset not ready: {e}")
            return False
    
    def generate_pipeline_report(self):
        """Generate execution report"""
        self.log_step("Pipeline Report Generation")
        
        report = f"""
# PIPELINE EXECUTION REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 EXECUTION STATUS
- Docker Services: ✅ Running
- Data Ingestion: ✅ Complete 
- Spark ETL: ✅ Complete
- Airflow DAG: ✅ Triggered
- Superset: ✅ Ready

## 🔗 ACCESS URLS
- Airflow: http://localhost:8090 (admin/admin)
- Superset: http://localhost:8089 (admin/admin)
- Spark: http://localhost:8080
- HDFS: http://localhost:9870
- Jupyter: http://localhost:8888

## 📊 DATA PIPELINE
- Source: 20,001 Sumatra poverty records
- Storage: HDFS Bronze/Silver/Gold layers
- Processing: Spark distributed computing
- Visualization: Superset dashboards
- Orchestration: Airflow workflows

## 🚀 NEXT STEPS
1. Monitor DAG execution in Airflow UI
2. Create Superset dashboards
3. Analyze results in Jupyter notebooks
4. Generate policy insights

Pipeline executed successfully! 🎉
"""
        
        report_file = f"logs/pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logging.info(f"📋 Report generated: {report_file}")
        return True
    
    def run_complete_pipeline(self):
        """Execute the complete pipeline"""
        logging.info("🚀 STARTING BIG DATA PIPELINE - SUMATRA POVERTY MAPPING")
        logging.info("=" * 60)
        
        steps = [
            ("Check Docker Services", self.check_docker_services),
            ("Validate Data Source", self.validate_data_source),
            ("Ingest to HDFS", self.ingest_to_hdfs),
            ("Run Spark ETL", self.run_spark_etl),
            ("Trigger Airflow DAG", self.trigger_airflow_dag),
            ("Setup Superset", self.setup_superset_dashboard),
            ("Generate Report", self.generate_pipeline_report)
        ]
        
        for step_name, step_function in steps:
            logging.info(f"\n🔄 Step: {step_name}")
            if not step_function():
                logging.error(f"❌ Pipeline failed at step: {step_name}")
                return False
            logging.info(f"✅ Step completed: {step_name}")
        
        logging.info("\n🎉 PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
        logging.info("🌐 Access your dashboards:")
        logging.info("   - Airflow: http://localhost:8090")
        logging.info("   - Superset: http://localhost:8089")
        logging.info("   - Spark: http://localhost:8080")
        
        return True

def main():
    """Main execution function"""
    pipeline = PovertyMappingPipeline()
    
    try:
        success = pipeline.run_complete_pipeline()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logging.info("\n⏹️ Pipeline execution interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
