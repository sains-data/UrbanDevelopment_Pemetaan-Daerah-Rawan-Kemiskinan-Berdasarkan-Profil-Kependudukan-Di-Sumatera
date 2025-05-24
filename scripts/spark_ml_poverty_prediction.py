import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.types import IntegerType

# Konfigurasi Spark
spark = SparkSession.builder \
    .appName("MLPovertyPrediction") \
    .master("yarn") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \
    .getOrCreate()

# Path HDFS Gold Layer
HDFS_GOLD_PATH = "/data/gold/kemiskinan_curated/"
# Path untuk menyimpan hasil prediksi
HDFS_ML_OUTPUT_PATH = "/data/gold/poverty_predictions/"

print(f"Membaca data dari Gold Layer untuk ML: {HDFS_GOLD_PATH}")
try:
    df_gold = spark.read.parquet(HDFS_GOLD_PATH)
    print("Skema Gold Layer (Input ML):")
    df_gold.printSchema()

    # --- Persiapan Data untuk ML ---
    threshold_poverty = 10.0 # Ambang batas persentase kemiskinan untuk "rawan"

    df_ml = df_gold.withColumn("is_high_poverty_province", 
                               (col("rata_rata_persentase_kemiskinan_provinsi") >= threshold_poverty).cast(IntegerType()))

    feature_columns = [
        "rata_rata_persentase_kemiskinan_provinsi",
        "total_penduduk_miskin_provinsi_ribu_jiwa"
    ]

    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

    rf = RandomForestClassifier(labelCol="is_high_poverty_province", featuresCol="features", numTrees=10, seed=42)

    pipeline = Pipeline(stages=[assembler, rf])

    (trainingData, testData) = df_ml.randomSplit([0.8, 0.2], seed=42)

    print("Mulai melatih model Random Forest...")
    model = pipeline.fit(trainingData)
    print("Model berhasil dilatih.")

    predictions = model.transform(testData)

    evaluator = MulticlassClassificationEvaluator(labelCol="is_high_poverty_province", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    print(f"Akurasi Model: {accuracy}")

    print("\nContoh Prediksi:")
    predictions.select("provinsi", "tahun", "rata_rata_persentase_kemiskinan_provinsi", 
                       "is_high_poverty_province", "prediction").show(10)

    predictions.select("provinsi", "tahun", "is_high_poverty_province", "prediction", "probability") \
               .write.mode("overwrite").parquet(HDFS_ML_OUTPUT_PATH)
    print(f"Hasil prediksi disimpan ke: {HDFS_ML_OUTPUT_PATH}")

except Exception as e:
    print(f"Terjadi kesalahan saat menjalankan ML Pipeline: {e}")
    spark.stop()
    raise

spark.stop()
print("ML Poverty Prediction process completed.")