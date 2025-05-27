"""
Spark ETL Pipeline - Bronze to Silver Layer
Pemetaan Kemiskinan Sumatera - Kelompok 18

This script performs data cleaning and transformation from Bronze to Silver layer
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_spark_session():
    """Create Spark session with Hive support"""
    spark = SparkSession.builder \
        .appName("PovertyMapping-BronzeToSilver") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .enableHiveSupport() \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def read_bronze_data(spark):
    """Read raw data from Bronze layer"""
    logger.info("Reading data from Bronze layer...")
    
    bronze_path = "hdfs://namenode:9000/data/bronze/kemiskinan_raw.csv"
    
    df = spark.read.option("header", "true") \
                  .option("inferSchema", "true") \
                  .csv(bronze_path)
    
    logger.info(f"Bronze data loaded: {df.count()} rows, {len(df.columns)} columns")
    return df

def clean_and_transform_data(df):
    """Clean and transform data for Silver layer"""
    logger.info("Starting data cleaning and transformation...")
    
    # Show initial data info
    df.printSchema()
    logger.info(f"Initial row count: {df.count()}")
    
    # 1. Remove duplicates
    df_clean = df.dropDuplicates()
    logger.info(f"After removing duplicates: {df_clean.count()} rows")
    
    # 2. Handle missing values
    # Fill missing numeric values with median
    numeric_cols = [f.name for f in df_clean.schema.fields if isinstance(f.dataType, (IntegerType, DoubleType, FloatType))]
    
    for col_name in numeric_cols:
        median_value = df_clean.approxQuantile(col_name, [0.5], 0.01)[0]
        df_clean = df_clean.fillna({col_name: median_value})
    
    # Fill missing string values with "Unknown"
    string_cols = [f.name for f in df_clean.schema.fields if isinstance(f.dataType, StringType)]
    for col_name in string_cols:
        df_clean = df_clean.fillna({col_name: "Unknown"})
    
    # 3. Standardize column names (lowercase, replace spaces with underscores)
    for old_col in df_clean.columns:
        new_col = old_col.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "_pct")
        df_clean = df_clean.withColumnRenamed(old_col, new_col)
    
    # 4. Data type conversions and validations
    if "persentase_kemiskinan__pct" in df_clean.columns:
        df_clean = df_clean.withColumn("persentase_kemiskinan__pct", 
                                     when(col("persentase_kemiskinan__pct") > 100, 100)
                                     .when(col("persentase_kemiskinan__pct") < 0, 0)
                                     .otherwise(col("persentase_kemiskinan__pct")))
    
    # 5. Create derived columns
    # Standardize boolean columns
    if "akses_air_bersih" in df_clean.columns:
        df_clean = df_clean.withColumn("akses_air_bersih_bool", 
                                     when(lower(col("akses_air_bersih")) == "ya", True)
                                     .when(lower(col("akses_air_bersih")) == "tidak", False)
                                     .otherwise(None))
    
    # Create poverty level categorization
    if "kategori_kemiskinan" in df_clean.columns:
        df_clean = df_clean.withColumn("poverty_level_numeric",
                                     when(lower(col("kategori_kemiskinan")) == "rendah", 1)
                                     .when(lower(col("kategori_kemiskinan")) == "sedang", 2)
                                     .when(lower(col("kategori_kemiskinan")) == "tinggi", 3)
                                     .otherwise(0))
    
    # Add processing timestamp
    df_clean = df_clean.withColumn("processed_timestamp", current_timestamp())
    
    logger.info(f"Final cleaned data: {df_clean.count()} rows")
    return df_clean

def write_silver_data(df):
    """Write cleaned data to Silver layer"""
    logger.info("Writing data to Silver layer...")
    
    silver_path = "hdfs://namenode:9000/data/silver/kemiskinan_clean"
    
    # Write as Parquet for better performance
    df.write.mode("overwrite") \
           .option("compression", "snappy") \
           .parquet(silver_path)
    
    logger.info(f"Data written to Silver layer: {silver_path}")
    
    # Also register as Hive table
    df.createOrReplaceTempView("kemiskinan_silver_temp")
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.kemiskinan_silver
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/silver/kemiskinan_clean'
        AS SELECT * FROM kemiskinan_silver_temp
    """)
    
    logger.info("Hive table 'kemiskinan_silver' created/updated")

def main():
    """Main ETL pipeline execution"""
    logger.info("Starting Bronze to Silver ETL pipeline...")
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Read Bronze data
        bronze_df = read_bronze_data(spark)
        
        # Clean and transform data
        silver_df = clean_and_transform_data(bronze_df)
        
        # Write to Silver layer
        write_silver_data(silver_df)
        
        # Show sample of cleaned data
        logger.info("Sample of cleaned data:")
        silver_df.show(10, truncate=False)
        
        # Data quality summary
        logger.info("Data quality summary:")
        silver_df.describe().show()
        
        logger.info("Bronze to Silver ETL pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
