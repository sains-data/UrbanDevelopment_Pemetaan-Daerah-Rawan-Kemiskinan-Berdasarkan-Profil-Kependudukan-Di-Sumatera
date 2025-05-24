from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 5, 22),
}

with DAG('kemiskinan_sumatera_pipeline',
         schedule_interval=None,
         default_args=default_args,
         catchup=False) as dag:

    spark_job = BashOperator(
        task_id='run_spark_job',
        bash_command="""
        /opt/bitnami/spark/bin/spark-shell << EOF
        import org.apache.spark.sql.functions._
        val df = spark.read.parquet("file:/mnt/c/bigdata_kemiskinan_sumatera/data/silver/kemiskinan_clean")
        val dfTyped = df.selectExpr("provinsi", "cast(persentase_kemiskinan as double) as persentase_kemiskinan")
        val result = dfTyped.groupBy("provinsi").agg(avg("persentase_kemiskinan").alias("rata_rata_kemiskinan"))
        result.write.mode("overwrite").parquet("file:/mnt/c/bigdata_kemiskinan_sumatera/data/gold/avg_kemiskinan_per_provinsi")
        EOF
        """
    )
