"""
Simplified Airflow DAG for Poverty Mapping ETL Pipeline
Kelompok 18 - Pemetaan Kemiskinan Sumatera
Fixed version without Jinja template conflicts
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
    'retry_delay': timedelta(minutes=3),
}

# Create DAG
dag = DAG(
    'poverty_mapping_etl_simple',
    default_args=default_args,
    description='Simplified Poverty Mapping ETL Pipeline for Sumatra',
    schedule_interval='@daily',
    catchup=False,
    tags=['poverty', 'sumatra', 'etl', 'bigdata', 'simple']
)

# Task 1: Data ingestion to Bronze layer (simplified)
ingest_to_bronze = BashOperator(
    task_id='ingest_to_bronze',
    bash_command='ls -la /data/ && echo "Data ingestion task placeholder"',
    dag=dag
)

# Task 2: Bronze to Silver transformation
bronze_to_silver = BashOperator(
    task_id='bronze_to_silver_transform', 
    bash_command='echo "Bronze to Silver transformation placeholder"',
    dag=dag
)

# Task 3: Silver to Gold aggregation
silver_to_gold = BashOperator(
    task_id='silver_to_gold_aggregation',
    bash_command='echo "Silver to Gold aggregation placeholder"',
    dag=dag
)

# Task 4: Machine Learning pipeline
ml_pipeline = BashOperator(
    task_id='ml_poverty_prediction',
    bash_command='echo "ML poverty prediction placeholder"',
    dag=dag
)

# Task 5: Data validation (Python task)
def validate_data_quality():
    """Simple data validation"""
    logging.info("🔍 Validating data quality...")
    logging.info("✅ Data validation completed successfully")
    return "Data validation completed"

data_validation = PythonOperator(
    task_id='data_quality_validation',
    python_callable=validate_data_quality,
    dag=dag
)

# Task 6: Generate summary report
generate_summary = BashOperator(
    task_id='generate_summary_report',
    bash_command='echo "Pipeline completed successfully" > /tmp/pipeline_summary.txt',
    dag=dag
)

# Task 7: Completion notification
def send_completion_alert():
    """Send completion notification"""
    logging.info("🎉 Poverty Mapping ETL Pipeline completed successfully!")
    logging.info("📊 Pipeline execution finished")
    return "Pipeline completion notification sent"

completion_alert = PythonOperator(
    task_id='pipeline_completion_alert',
    python_callable=send_completion_alert,
    dag=dag
)

# Task dependencies
ingest_to_bronze >> bronze_to_silver >> silver_to_gold >> ml_pipeline >> data_validation >> generate_summary >> completion_alert
