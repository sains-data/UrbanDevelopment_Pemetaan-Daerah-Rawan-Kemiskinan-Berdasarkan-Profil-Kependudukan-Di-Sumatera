    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    import sys

    try:
        import findspark
        findspark.init()
        from pyspark.sql import SparkSession
        print("PySpark initialized for report generation.")
        SPARK_AVAILABLE = True
    except ImportError:
        print("PySpark not found, running without SparkSession for report generation.")
        SPARK_AVAILABLE = False

    # Get report output directory from command line argument
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <report_output_directory>")
        REPORT_OUTPUT_DIR = "./data/reports" # Default for local testing if run manually
    else:
        REPORT_OUTPUT_DIR = sys.argv[1] # This will be /data/reports when run from Airflow

    # HDFS paths for data
    HDFS_GOLD_PATH = "/data/gold/kemiskinan_curated/"
    HDFS_ML_OUTPUT_PATH = "/data/gold/poverty_predictions/"

    def generate_poverty_report(spark_session=None, output_dir="."):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"Generating report to: {output_dir}")

        df_report = pd.DataFrame() # Initialize empty DataFrame
        if spark_session and SPARK_AVAILABLE:
            try:
                df_gold = spark_session.read.parquet(HDFS_GOLD_PATH)
                df_predictions = spark_session.read.parquet(HDFS_ML_OUTPUT_PATH)
                
                # Join for reporting
                df_report_spark = df_gold.join(df_predictions, on=["provinsi", "tahun"], how="left")
                df_report = df_report_spark.toPandas()
                print("Data loaded from HDFS for reporting.")

            except Exception as e:
                print(f"Could not load data from HDFS for reporting: {e}. Running with dummy data instead.")
                SPARK_AVAILABLE = False # Fallback if HDFS load fails
        
        if not SPARK_AVAILABLE or df_report.empty:
            # Dummy data for local execution without Spark or if HDFS load failed
            df_report = pd.DataFrame({
                'provinsi': ['Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 'Sumatera Selatan', 'Bengkulu'],
                'tahun': [2022, 2022, 2022, 2022, 2022, 2022, 2022],
                'rata_rata_persentase_kemiskinan_provinsi': [15.33, 8.42, 6.04, 7.02, 7.50, 10.20, 14.50],
                'is_high_poverty_province': [1, 0, 0, 0, 0, 1, 1],
                'prediction': [1, 0, 0, 0, 0, 1, 1]
            })
            print("Running report generation with dummy data.")

        if df_report.empty:
            print("No data available for report generation after all attempts.")
            return

        # Plot 1: Bar chart of average poverty percentage per province in the latest year
        latest_year = df_report['tahun'].max()
        df_latest = df_report[df_report['tahun'] == latest_year].sort_values(
            'rata_rata_persentase_kemiskinan_provinsi', ascending=False
        )

        plt.figure(figsize=(12, 7))
        sns.barplot(x='provinsi', y='rata_rata_persentase_kemiskinan_provinsi', data=df_latest, palette='viridis')
        plt.title(f'Rata-rata Persentase Kemiskinan per Provinsi di Sumatera ({latest_year})')
        plt.xlabel('Provinsi')
        plt.ylabel('Persentase Kemiskinan (%)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'poverty_percentage_by_province.png'))
        plt.close()
        print(f"Saved: {os.path.join(output_dir, 'poverty_percentage_by_province.png')}")

        # Plot 2: Trend of average poverty percentage in Sumatera over years
        df_trend = df_report.groupby('tahun')['rata_rata_persentase_kemiskinan_provinsi'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='tahun', y='rata_rata_persentase_kemiskinan_provinsi', data=df_trend, marker='o')
        plt.title('Tren Rata-rata Persentase Kemiskinan di Sumatera')
        plt.xlabel('Tahun')
        plt.ylabel('Rata-rata Persentase Kemiskinan (%)')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'poverty_trend_sumatera.png'))
        plt.close()
        print(f"Saved: {os.path.join(output_dir, 'poverty_trend_sumatera.png')}")

        # Plot 3: Distribution of "High Poverty" vs "Low Poverty" predictions
        if 'prediction' in df_report.columns:
            plt.figure(figsize=(8, 5))
            sns.countplot(x='prediction', data=df_report, palette='coolwarm')
            plt.title('Distribusi Prediksi Daerah Rawan Kemiskinan (0=Tidak Rawan, 1=Rawan)')
            plt.xlabel('Prediksi')
            plt.ylabel('Jumlah Provinsi/Data Point')
            plt.xticks([0, 1], ['Tidak Rawan', 'Rawan'])
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'poverty_prediction_distribution.png'))
            plt.close()
            print(f"Saved: {os.path.join(output_dir, 'poverty_prediction_distribution.png')}")

        print("Report generation complete.")

    if __name__ == "__main__":
        if SPARK_AVAILABLE:
            spark = SparkSession.builder \
                .appName("ReportGeneration") \
                .master("yarn") \
                .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \
                .getOrCreate()
            generate_poverty_report(spark_session=spark, output_dir=REPORT_OUTPUT_DIR)
            spark.stop()
        else:
            generate_poverty_report(output_dir=REPORT_OUTPUT_DIR)