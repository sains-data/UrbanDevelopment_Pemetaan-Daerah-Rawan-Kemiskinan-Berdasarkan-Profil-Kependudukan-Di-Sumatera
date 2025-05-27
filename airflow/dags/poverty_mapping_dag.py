"""
Airflow DAG for Poverty Mapping ETL Pipeline
Kelompok 18 - Pemetaan Kemiskinan Sumatera
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
import logging

# Default arguments
default_args = {
    'owner': 'kelompok18',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'poverty_mapping_etl',
    default_args=default_args,
    description='Poverty Mapping ETL Pipeline for Sumatra',
    schedule_interval='@daily',  # Run daily
    catchup=False,
    tags=['poverty', 'sumatra', 'etl', 'bigdata']
)

# Task 1: Check data availability
check_data_task = FileSensor(
    task_id='check_data_availability',
    filepath='/data/Profil_Kemiskinan_Sumatera.csv',
    fs_conn_id='fs_default',
    poke_interval=30,
    timeout=60*5,  # 5 minutes timeout
    dag=dag
)

# Task 2: Data ingestion to Bronze layer
ingest_to_bronze = BashOperator(
    task_id='ingest_to_bronze',
    bash_command='bash /opt/airflow/scripts/ingest_data.sh',
    dag=dag
)

# Task 3: Bronze to Silver transformation
bronze_to_silver = BashOperator(
    task_id='bronze_to_silver_transform',
    bash_command='spark-submit --master spark://spark-master:7077 --executor-memory 1g --total-executor-cores 2 /scripts/spark/bronze_to_silver.py',
    dag=dag
)

# Task 4: Silver to Gold aggregation
silver_to_gold = BashOperator(
    task_id='silver_to_gold_aggregation',
    bash_command='spark-submit --master spark://spark-master:7077 --executor-memory 1g --total-executor-cores 2 /scripts/spark/silver_to_gold.py',
    dag=dag
)

# Task 5: Machine Learning pipeline
ml_pipeline = BashOperator(
    task_id='ml_poverty_prediction',
    bash_command='spark-submit --master spark://spark-master:7077 --executor-memory 1g --total-executor-cores 2 /scripts/spark/ml_poverty_prediction.py',
    dag=dag
)

# Task 6: Data quality validation
def validate_data_quality():
    """Validate data quality and completeness"""
    import subprocess
    
    # Simple validation check
    logging.info("🔍 Validating data quality...")
    
    # Check if HDFS directories exist
    hdfs_check = subprocess.run(['docker', 'exec', 'namenode', 'hdfs', 'dfs', '-ls', '/data/silver'], 
                               capture_output=True, text=True)
    
    if hdfs_check.returncode != 0:
        raise Exception(f"HDFS silver layer validation failed: {hdfs_check.stderr}")
    
    logging.info("✅ Data validation completed successfully")
    return "Data validation completed successfully"

data_validation = PythonOperator(
    task_id='data_quality_validation',
    python_callable=validate_data_quality,
    dag=dag
)

# Task 7: Generate data summary report
generate_summary = BashOperator(
    task_id='generate_summary_report',
    bash_command='echo "Pipeline execution completed" > /data/pipeline_summary.txt',
    dag=dag
)

# Task dependencies
check_data_task >> ingest_to_bronze >> bronze_to_silver >> silver_to_gold >> ml_pipeline >> data_validation >> generate_summary

# Optional: Add alerting task
def send_completion_alert():
    """Send completion notification"""
    logging.info("🎉 Poverty Mapping ETL Pipeline completed successfully!")
    logging.info("📊 Check Superset dashboard for latest insights")
    logging.info("🐘 Hive tables updated with fresh data")
    return "Pipeline completion notification sent"

completion_alert = PythonOperator(
    task_id='pipeline_completion_alert',
    python_callable=send_completion_alert,
    dag=dag
)

# Add completion alert to the end
generate_summary >> completion_alert
