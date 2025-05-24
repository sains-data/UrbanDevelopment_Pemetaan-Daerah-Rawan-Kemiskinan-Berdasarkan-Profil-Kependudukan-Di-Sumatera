from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, sum, round

def main():
    spark = SparkSession.builder \
        .appName("SilverToGold") \
        .master("local[*]") \
        .getOrCreate()

    silver_path = "/data/silver/kemiskinan_clean"
    gold_path = "/data/gold/kemiskinan_aggregated"

    # Baca data silver
    df_silver = spark.read.parquet(silver_path)

    # Agregasi per provinsi
    df_gold = df_silver.groupBy("provinsi") \
                      .agg(
                          round(avg("persentase_kemiskinan"), 2).alias("rata_rata_persen_kemiskinan"),
                          sum("jumlah_penduduk").alias("total_penduduk")
                      ) \
                      .orderBy("provinsi")

    # Tampilkan contoh hasil
    df_gold.show(10)

    # Simpan hasil gold layer
    df_gold.write.mode("overwrite").parquet(gold_path)
    print(f"Data gold sudah disimpan ke {gold_path}")

    spark.stop()

if __name__ == "__main__":
    main()
