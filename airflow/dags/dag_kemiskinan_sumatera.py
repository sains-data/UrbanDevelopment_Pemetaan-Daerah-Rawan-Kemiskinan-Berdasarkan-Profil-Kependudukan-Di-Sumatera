from airflow import DAG  # hapus extra 'f'
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# definisi direktori dan file sama seperti kamu tulis

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'kemiskinan_sumatera_pipeline',
    default_args=default_args,
    description='Pipeline data untuk pemetaan daerah rawan kemiskinan di Sumatera',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['kemiskinan', 'sumatera', 'bigdata', 'spark', 'hadoop', 'ml', 'hive', 'superset'],
) as dag:

    ingest_to_bronze_task = BashOperator(
        task_id='ingest_data_to_bronze_hdfs',
        bash_command=f"bash -c '{SCRIPTS_DIR}/ingest_to_hdfs.sh \"{DATA_RAW_PATH}\" \"{HDFS_BRONZE_PATH}\"'"
    )

    process_silver_task = BashOperator(
        task_id='process_data_to_silver_layer',
        bash_command=(
            f"spark-submit --master yarn --deploy-mode client "
            f"--conf spark.hadoop.fs.defaultFS=hdfs://namenode:8020 "
            f"{SCRIPTS_DIR}/spark_silver_layer.py"
        )
    )

    process_gold_task = BashOperator(
        task_id='process_data_to_gold_layer',
        bash_command=(
            f"spark-submit --master yarn --deploy-mode client "
            f"--conf spark.hadoop.fs.defaultFS=hdfs://namenode:8020 "
            f"{SCRIPTS_DIR}/spark_gold_layer.py"
        )
    )

    run_ml_poverty_prediction_task = BashOperator(
        task_id='run_ml_poverty_prediction',
        bash_command=(
            f"spark-submit --master yarn --deploy-mode client "
            f"--conf spark.hadoop.fs.defaultFS=hdfs://namenode:8020 "
            f"{SCRIPTS_DIR}/spark_ml_poverty_prediction.py"
        )
    )

    generate_report_task = BashOperator(
        task_id='generate_final_report',
        bash_command=f"bash -c 'python {SCRIPTS_DIR}/generate_report.py \"{REPORT_OUTPUT_DIR}\"'"
    )

    ingest_to_bronze_task >> process_silver_task >> process_gold_task >> run_ml_poverty_prediction_task >> generate_report_task
