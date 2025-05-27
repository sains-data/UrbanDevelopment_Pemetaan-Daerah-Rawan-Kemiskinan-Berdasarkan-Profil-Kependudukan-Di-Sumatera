"""
Spark ETL Pipeline - Silver to Gold Layer
Pemetaan Kemiskinan Sumatera - Kelompok 18

This script performs data aggregation and analysis from Silver to Gold layer
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
        .appName("PovertyMapping-SilverToGold") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .enableHiveSupport() \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark

def read_silver_data(spark):
    """Read cleaned data from Silver layer"""
    logger.info("Reading data from Silver layer...")
    
    silver_path = "hdfs://namenode:9000/data/silver/kemiskinan_clean"
    df = spark.read.parquet(silver_path)
    
    logger.info(f"Silver data loaded: {df.count()} rows")
    return df

def create_province_aggregation(df):
    """Create province-level aggregation"""
    logger.info("Creating province-level aggregation...")
    
    province_agg = df.groupBy("provinsi") \
        .agg(
            avg("persentase_kemiskinan__pct").alias("avg_poverty_rate"),
            avg("tingkat_pengangguran__pct").alias("avg_unemployment_rate"),
            sum("jumlah_penduduk_jiwa").alias("total_population"),
            count("*").alias("record_count"),
            countDistinct("golongan_pengeluaran").alias("expenditure_groups"),
            avg("konsumsi_per_kapita_per_minggu").alias("avg_consumption"),
            
            # Calculate access percentages
            sum(when(col("akses_pendidikan") == "baik", 1).otherwise(0)).alias("good_education_access"),
            sum(when(col("fasilitas_kesehatan") == "memadai", 1).otherwise(0)).alias("adequate_health_facilities"),
            sum(when(col("akses_air_bersih") == "ya", 1).otherwise(0)).alias("clean_water_access"),
            
            # Poverty level distribution
            sum(when(col("kategori_kemiskinan") == "rendah", 1).otherwise(0)).alias("low_poverty_count"),
            sum(when(col("kategori_kemiskinan") == "sedang", 1).otherwise(0)).alias("medium_poverty_count"),
            sum(when(col("kategori_kemiskinan") == "tinggi", 1).otherwise(0)).alias("high_poverty_count"),
            
            current_timestamp().alias("aggregation_timestamp")
        )
    
    # Calculate percentages
    province_agg = province_agg.withColumn("good_education_access_pct", 
                                         round((col("good_education_access") / col("record_count")) * 100, 2)) \
                              .withColumn("adequate_health_facilities_pct", 
                                         round((col("adequate_health_facilities") / col("record_count")) * 100, 2)) \
                              .withColumn("clean_water_access_pct", 
                                         round((col("clean_water_access") / col("record_count")) * 100, 2))
    
    # Classify province poverty level
    province_agg = province_agg.withColumn("province_poverty_classification",
                                         when(col("avg_poverty_rate") <= 10, "Low")
                                         .when(col("avg_poverty_rate") <= 20, "Medium")
                                         .otherwise("High"))
    
    logger.info(f"Province aggregation created: {province_agg.count()} provinces")
    return province_agg

def create_expenditure_analysis(df):
    """Create expenditure group analysis"""
    logger.info("Creating expenditure group analysis...")
    
    # Clean expenditure groups
    expenditure_df = df.withColumn("expenditure_group_clean",
                                  regexp_replace(col("golongan_pengeluaran"), r"\.[\d]+$", ""))
    
    expenditure_agg = expenditure_df.groupBy("expenditure_group_clean", "provinsi") \
        .agg(
            avg("persentase_kemiskinan__pct").alias("avg_poverty_rate"),
            avg("konsumsi_per_kapita_per_minggu").alias("avg_consumption"),
            sum("jumlah_penduduk_jiwa").alias("total_population"),
            count("*").alias("record_count"),
            
            # Most common poverty category
            mode(col("kategori_kemiskinan")).alias("most_common_poverty_level"),
            
            current_timestamp().alias("aggregation_timestamp")
        )
    
    logger.info(f"Expenditure analysis created: {expenditure_agg.count()} groups")
    return expenditure_agg

def create_poverty_insights(df):
    """Create poverty insights and correlations"""
    logger.info("Creating poverty insights...")
    
    # Overall statistics
    overall_stats = df.agg(
        avg("persentase_kemiskinan__pct").alias("national_avg_poverty"),
        avg("tingkat_pengangguran__pct").alias("national_avg_unemployment"),
        sum("jumlah_penduduk_jiwa").alias("total_sumatra_population"),
        count("*").alias("total_records")
    ).withColumn("region", lit("Sumatera")) \
     .withColumn("analysis_timestamp", current_timestamp())
    
    # Correlation analysis
    correlations = df.select(
        corr("persentase_kemiskinan__pct", "tingkat_pengangguran__pct").alias("poverty_unemployment_corr"),
        corr("persentase_kemiskinan__pct", "konsumsi_per_kapita_per_minggu").alias("poverty_consumption_corr"),
        current_timestamp().alias("correlation_timestamp")
    ).withColumn("analysis_type", lit("correlation"))
    
    logger.info("Poverty insights created")
    return overall_stats, correlations

def write_gold_data(province_agg, expenditure_agg, overall_stats, correlations):
    """Write aggregated data to Gold layer"""
    logger.info("Writing data to Gold layer...")
    
    # Write province aggregation
    province_path = "hdfs://namenode:9000/data/gold/province_poverty_summary"
    province_agg.write.mode("overwrite") \
                     .option("compression", "snappy") \
                     .parquet(province_path)
    
    # Write expenditure analysis
    expenditure_path = "hdfs://namenode:9000/data/gold/expenditure_analysis"
    expenditure_agg.write.mode("overwrite") \
                         .option("compression", "snappy") \
                         .parquet(expenditure_path)
    
    # Write overall statistics
    stats_path = "hdfs://namenode:9000/data/gold/poverty_statistics"
    overall_stats.write.mode("overwrite") \
                       .option("compression", "snappy") \
                       .parquet(stats_path)
    
    # Write correlations
    corr_path = "hdfs://namenode:9000/data/gold/poverty_correlations"
    correlations.write.mode("overwrite") \
                      .option("compression", "snappy") \
                      .parquet(corr_path)
    
    logger.info("Data written to Gold layer")

def create_hive_tables(spark, province_agg, expenditure_agg, overall_stats, correlations):
    """Create Hive tables for Gold layer"""
    logger.info("Creating Hive tables for Gold layer...")
    
    # Register temporary views
    province_agg.createOrReplaceTempView("province_summary_temp")
    expenditure_agg.createOrReplaceTempView("expenditure_analysis_temp")
    overall_stats.createOrReplaceTempView("poverty_stats_temp")
    correlations.createOrReplaceTempView("correlations_temp")
    
    # Create Hive tables
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.province_poverty_summary
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/gold/province_poverty_summary'
        AS SELECT * FROM province_summary_temp
    """)
    
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.expenditure_analysis
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/gold/expenditure_analysis'
        AS SELECT * FROM expenditure_analysis_temp
    """)
    
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.poverty_statistics
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/gold/poverty_statistics'
        AS SELECT * FROM poverty_stats_temp
    """)
    
    spark.sql("""
        CREATE TABLE IF NOT EXISTS kemiskinan_db.poverty_correlations
        USING PARQUET
        LOCATION 'hdfs://namenode:9000/data/gold/poverty_correlations'
        AS SELECT * FROM correlations_temp
    """)
    
    logger.info("Hive tables created successfully")

def main():
    """Main ETL pipeline execution"""
    logger.info("Starting Silver to Gold ETL pipeline...")
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Read Silver data
        silver_df = read_silver_data(spark)
        
        # Create aggregations
        province_agg = create_province_aggregation(silver_df)
        expenditure_agg = create_expenditure_analysis(silver_df)
        overall_stats, correlations = create_poverty_insights(silver_df)
        
        # Write to Gold layer
        write_gold_data(province_agg, expenditure_agg, overall_stats, correlations)
        
        # Create Hive tables
        create_hive_tables(spark, province_agg, expenditure_agg, overall_stats, correlations)
        
        # Show results
        logger.info("Province Poverty Summary:")
        province_agg.show(10, truncate=False)
        
        logger.info("Overall Statistics:")
        overall_stats.show(truncate=False)
        
        logger.info("Correlations:")
        correlations.show(truncate=False)
        
        logger.info("Silver to Gold ETL pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
