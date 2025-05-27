"""
Spark Machine Learning Pipeline
Pemetaan Kemiskinan Sumatera - Kelompok 18

This script performs poverty prediction using machine learning
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml.classification import RandomForestClassifier, LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.pipeline import Pipeline
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_spark_session():
    """Create Spark session with MLlib support"""
    spark = SparkSession.builder \
        .appName("PovertyMapping-MachineLearning") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .enableHiveSupport() \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def prepare_ml_data(spark):
    """Prepare data for machine learning"""
    logger.info("Preparing data for machine learning...")
    
    # Read from Silver layer
    silver_path = "hdfs://namenode:9000/data/silver/kemiskinan_clean"
    df = spark.read.parquet(silver_path)
    
    # Feature engineering
    df_ml = df.select(
        col("persentase_kemiskinan__pct").alias("poverty_rate"),
        col("tingkat_pengangguran__pct").alias("unemployment_rate"),
        col("konsumsi_per_kapita_per_minggu").alias("consumption"),
        col("jumlah_penduduk_jiwa").alias("population"),
        col("akses_pendidikan").alias("education_access"),
        col("fasilitas_kesehatan").alias("health_facilities"),
        col("akses_air_bersih").alias("clean_water"),
        col("kategori_kemiskinan").alias("poverty_category"),
        col("provinsi").alias("province")
    ).filter(col("poverty_category").isNotNull())
    
    # Create binary features
    df_ml = df_ml.withColumn("education_good", 
                           when(col("education_access") == "baik", 1.0).otherwise(0.0)) \
                 .withColumn("health_adequate", 
                           when(col("health_facilities") == "memadai", 1.0).otherwise(0.0)) \
                 .withColumn("water_access", 
                           when(col("clean_water") == "ya", 1.0).otherwise(0.0))
    
    # Remove rows with null values in key features
    df_ml = df_ml.filter(
        col("poverty_rate").isNotNull() &
        col("unemployment_rate").isNotNull() &
        col("consumption").isNotNull() &
        col("population").isNotNull()
    )
    
    logger.info(f"ML dataset prepared: {df_ml.count()} rows")
    return df_ml

def build_ml_pipeline(df):
    """Build machine learning pipeline"""
    logger.info("Building ML pipeline...")
    
    # String indexer for province
    province_indexer = StringIndexer(inputCol="province", outputCol="province_index")
    
    # String indexer for target variable
    label_indexer = StringIndexer(inputCol="poverty_category", outputCol="label")
    
    # Feature vector assembler
    feature_cols = [
        "poverty_rate", "unemployment_rate", "consumption", "population",
        "education_good", "health_adequate", "water_access", "province_index"
    ]
    
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features_raw")
    
    # Feature scaling
    scaler = StandardScaler(inputCol="features_raw", outputCol="features")
    
    # Random Forest Classifier
    rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=100)
    
    # Create pipeline
    pipeline = Pipeline(stages=[province_indexer, label_indexer, assembler, scaler, rf])
    
    return pipeline

def train_and_evaluate_model(pipeline, df):
    """Train and evaluate the model"""
    logger.info("Training and evaluating model...")
    
    # Split data
    train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
    
    logger.info(f"Training set: {train_data.count()} rows")
    logger.info(f"Test set: {test_data.count()} rows")
    
    # Train model
    model = pipeline.fit(train_data)
    
    # Make predictions
    predictions = model.transform(test_data)
    
    # Evaluate model
    evaluator = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="accuracy"
    )
    
    accuracy = evaluator.evaluate(predictions)
    logger.info(f"Model accuracy: {accuracy:.4f}")
    
    # Additional metrics
    f1_evaluator = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="f1"
    )
    f1_score = f1_evaluator.evaluate(predictions)
    logger.info(f"Model F1 Score: {f1_score:.4f}")
    
    return model, predictions, accuracy, f1_score

def feature_importance_analysis(model, feature_cols):
    """Analyze feature importance"""
    logger.info("Analyzing feature importance...")
    
    # Get feature importance from Random Forest
    rf_model = model.stages[-1]
    feature_importance = rf_model.featureImportances.toArray()
    
    # Create feature importance dataframe
    spark = SparkSession.getActiveSession()
    importance_data = [(feature_cols[i], float(feature_importance[i])) 
                      for i in range(len(feature_cols))]
    
    importance_df = spark.createDataFrame(importance_data, ["feature", "importance"])
    importance_df = importance_df.orderBy(col("importance").desc())
    
    logger.info("Feature Importance:")
    importance_df.show()
    
    return importance_df

def save_model_and_predictions(model, predictions, accuracy, f1_score, importance_df):
    """Save model results to Gold layer"""
    logger.info("Saving model and predictions...")
    
    # Save predictions
    predictions_path = "hdfs://namenode:9000/data/gold/poverty_predictions"
    predictions.select("province", "poverty_category", "prediction", "probability") \
              .write.mode("overwrite") \
              .option("compression", "snappy") \
              .parquet(predictions_path)
    
    # Save feature importance
    importance_path = "hdfs://namenode:9000/data/gold/feature_importance"
    importance_df.write.mode("overwrite") \
                       .option("compression", "snappy") \
                       .parquet(importance_path)
    
    # Save model metrics
    spark = SparkSession.getActiveSession()
    metrics_data = [("accuracy", accuracy), ("f1_score", f1_score)]
    metrics_df = spark.createDataFrame(metrics_data, ["metric", "value"]) \
                     .withColumn("model_type", lit("RandomForest")) \
                     .withColumn("training_timestamp", current_timestamp())
    
    metrics_path = "hdfs://namenode:9000/data/gold/model_metrics"
    metrics_df.write.mode("overwrite") \
                    .option("compression", "snappy") \
                    .parquet(metrics_path)
    
    logger.info("Model results saved to Gold layer")

def create_ml_hive_tables(spark):
    """Create Hive tables for ML results"""
    logger.info("Creating Hive tables for ML results...")
    
    # Create predictions table
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.poverty_predictions
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/gold/poverty_predictions'
    """)
    
    # Create feature importance table
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.feature_importance
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/gold/feature_importance'
    """)
    
    # Create model metrics table
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.model_metrics
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/gold/model_metrics'
    """)
    
    logger.info("ML Hive tables created successfully")

def main():
    """Main ML pipeline execution"""
    logger.info("Starting Machine Learning pipeline...")
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Prepare data
        df_ml = prepare_ml_data(spark)
        
        # Build pipeline
        pipeline = build_ml_pipeline(df_ml)
        
        # Train and evaluate model
        feature_cols = [
            "poverty_rate", "unemployment_rate", "consumption", "population",
            "education_good", "health_adequate", "water_access", "province_index"
        ]
        
        model, predictions, accuracy, f1_score = train_and_evaluate_model(pipeline, df_ml)
        
        # Feature importance analysis
        importance_df = feature_importance_analysis(model, feature_cols)
        
        # Save results
        save_model_and_predictions(model, predictions, accuracy, f1_score, importance_df)
        
        # Create Hive tables
        create_ml_hive_tables(spark)
        
        # Show sample predictions
        logger.info("Sample predictions:")
        predictions.select("province", "poverty_category", "prediction", "probability") \
                  .show(10, truncate=False)
        
        logger.info("Machine Learning pipeline completed successfully!")
        logger.info(f"Final Model Accuracy: {accuracy:.4f}")
        logger.info(f"Final Model F1 Score: {f1_score:.4f}")
        
    except Exception as e:
        logger.error(f"ML pipeline failed: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
