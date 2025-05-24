from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'naufal',
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    'bronze_silver_gold_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # 1. Load raw CSV to Bronze layer (misal copy dari sumber ke folder bronze)
    bronze_task = BashOperator(
        task_id='bronze_load',
        bash_command='cp /mnt/c/bigdata_kemiskinan_sumatera/raw_data/*.csv /mnt/c/bigdata_kemiskinan_sumatera/data/bronze/',
    )

    # 2. Transform Bronze → Silver pakai Spark submit script
    silver_task = BashOperator(
        task_id='silver_transform',
        bash_command='spark-submit /mnt/c/bigdata_kemiskinan_sumatera/scripts/bronze_to_silver.py',
    )

    # 3. Transform Silver → Gold pakai Spark submit script
    gold_task = BashOperator(
        task_id='gold_transform',
        bash_command='spark-submit /mnt/c/bigdata_kemiskinan_sumatera/scripts/silver_to_gold.py',
    )

    # Urutkan task
    bronze_task >> silver_task >> gold_task
