import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim
from pyspark.sql.types import IntegerType, DoubleType

spark = SparkSession.builder \
    .appName("BronzeToSilver") \
    .master("local[*]") \
    .getOrCreate()

bronze_path = "/mnt/c/bigdata_kemiskinan_sumatera/data/bronze/Profil_Kemiskinan_Sumatera.csv"
silver_path = "/mnt/c/bigdata_kemiskinan_sumatera/data/silver/kemiskinan_clean"

df_bronze = spark.read.csv(bronze_path, header=True, inferSchema=True)

# Drop rows yang ada NULL di kolom penting
df_silver = df_bronze.dropna(subset=["Provinsi", "Jumlah Penduduk (jiwa)", "Persentase Kemiskinan (%)"])

# Bersihkan dan ubah tipe data
df_silver = df_silver.withColumn("Provinsi", trim(col("Provinsi"))) \
                     .withColumn("Jumlah Penduduk (jiwa)", col("Jumlah Penduduk (jiwa)").cast(IntegerType())) \
                     .withColumn("Persentase Kemiskinan (%)", col("Persentase Kemiskinan (%)").cast(DoubleType())) \
                     .withColumn("Tingkat Pengangguran (%)", col("Tingkat Pengangguran (%)").cast(DoubleType()))

# Rename kolom supaya konsisten lowercase dan tanpa spasi
df_silver = df_silver.withColumnRenamed("Provinsi", "provinsi") \
                     .withColumnRenamed("Komoditas", "komoditas") \
                     .withColumnRenamed("Golongan Pengeluaran", "golongan_pengeluaran") \
                     .withColumnRenamed("Konsumsi (per kapita per minggu)", "konsumsi_perkapita_per_minggu") \
                     .withColumnRenamed("Jumlah Penduduk (jiwa)", "jumlah_penduduk") \
                     .withColumnRenamed("Persentase Kemiskinan (%)", "persentase_kemiskinan") \
                     .withColumnRenamed("Tingkat Pengangguran (%)", "tingkat_pengangguran") \
                     .withColumnRenamed("Akses Pendidikan", "akses_pendidikan") \
                     .withColumnRenamed("Fasilitas Kesehatan", "fasilitas_kesehatan") \
                     .withColumnRenamed("Akses Air Bersih", "akses_air_bersih") \
                     .withColumnRenamed("Kategori Kemiskinan", "kategori_kemiskinan")

df_silver.printSchema()
df_silver.show(5)

df_silver.write.mode("overwrite").parquet(silver_path)
print(f"Data silver sudah disimpan ke {silver_path}")

spark.stop()
