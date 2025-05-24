import findspark
findspark.init()

from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

# Inisialisasi SparkSession (local mode)
spark = SparkSession.builder \
    .appName("VisualisasiGoldLayer") \
    .master("local[*]") \
    .getOrCreate()

HDFS_GOLD_PATH = "/mnt/c/bigdata_kemiskinan_sumatera/data/gold/kemiskinan_aggregated/"

print(f"Membaca data Gold Layer dari: {HDFS_GOLD_PATH}")
try:
    df_gold = spark.read.parquet(HDFS_GOLD_PATH)
    df_gold.printSchema()
    
    pdf = df_gold.toPandas()
    
    # Urutkan provinsi berdasarkan persentase kemiskinan (descending)
    pdf_sorted = pdf.sort_values(by='rata_rata_persen_kemiskinan', ascending=False)
    
    plt.figure(figsize=(12,8))
    plt.bar(pdf_sorted['provinsi'], pdf_sorted['rata_rata_persen_kemiskinan'], color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Rata-rata Persentase Kemiskinan per Provinsi')
    plt.xlabel('Provinsi')
    plt.ylabel('Persentase Kemiskinan (%)')
    plt.tight_layout()
    
    output_file = "output_rata_persen_kemiskinan_per_provinsi.png"
    plt.savefig(output_file)
    print(f"Grafik sudah disimpan ke file: {output_file}")
    
except Exception as e:
    print(f"Error saat baca data atau buat visualisasi: {e}")

spark.stop()
