#!/bin/bash

# Complete ETL Pipeline Runner
# Executes the full Bronze -> Silver -> Gold -> ML pipeline

echo "🚀 Starting Complete ETL Pipeline for Poverty Mapping..."
echo "=============================================================="

# Step 1: Data Ingestion (Bronze Layer)
echo "📤 Step 1: Data Ingestion to Bronze Layer"
./scripts/ingest_data.sh
if [ $? -ne 0 ]; then
    echo "❌ Data ingestion failed"
    exit 1
fi
echo "✅ Bronze layer completed"
echo ""

# Step 2: Bronze to Silver Transformation
echo "🔄 Step 2: Bronze to Silver Transformation"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 1g \
    --total-executor-cores 2 \
    /scripts/spark/bronze_to_silver.py

if [ $? -ne 0 ]; then
    echo "❌ Bronze to Silver transformation failed"
    exit 1
fi
echo "✅ Silver layer completed"
echo ""

# Step 3: Silver to Gold Aggregation
echo "📊 Step 3: Silver to Gold Aggregation"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 1g \
    --total-executor-cores 2 \
    /scripts/spark/silver_to_gold.py

if [ $? -ne 0 ]; then
    echo "❌ Silver to Gold aggregation failed"
    exit 1
fi
echo "✅ Gold layer completed"
echo ""

# Step 4: Machine Learning Pipeline
echo "🧠 Step 4: Machine Learning Pipeline"
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 1g \
    --total-executor-cores 2 \
    /scripts/spark/ml_poverty_prediction.py

if [ $? -ne 0 ]; then
    echo "❌ Machine Learning pipeline failed"
    exit 1
fi
echo "✅ ML pipeline completed"
echo ""

# Step 5: Verify Hive Tables
echo "🐘 Step 5: Verifying Hive Tables"
docker exec hive-server beeline -u jdbc:hive2://localhost:10000 -e "
USE kemiskinan_db;
SHOW TABLES;

-- Show sample data from each table
SELECT 'kemiskinan_silver' as table_name, COUNT(*) as row_count FROM kemiskinan_silver
UNION ALL
SELECT 'province_poverty_summary' as table_name, COUNT(*) as row_count FROM province_poverty_summary
UNION ALL
SELECT 'expenditure_analysis' as table_name, COUNT(*) as row_count FROM expenditure_analysis
UNION ALL
SELECT 'poverty_statistics' as table_name, COUNT(*) as row_count FROM poverty_statistics
UNION ALL
SELECT 'poverty_correlations' as table_name, COUNT(*) as row_count FROM poverty_correlations
UNION ALL
SELECT 'poverty_predictions' as table_name, COUNT(*) as row_count FROM poverty_predictions
UNION ALL
SELECT 'feature_importance' as table_name, COUNT(*) as row_count FROM feature_importance
UNION ALL
SELECT 'model_metrics' as table_name, COUNT(*) as row_count FROM model_metrics;
"

echo "✅ Hive tables verified"
echo ""

# Step 6: Display HDFS Structure
echo "📁 Step 6: HDFS Data Structure"
echo "Bronze Layer:"
docker exec namenode hdfs dfs -ls /data/bronze/
echo ""
echo "Silver Layer:"
docker exec namenode hdfs dfs -ls /data/silver/
echo ""
echo "Gold Layer:"
docker exec namenode hdfs dfs -ls /data/gold/
echo ""

# Step 7: Show Sample Results
echo "📊 Step 7: Sample Analysis Results"
docker exec hive-server beeline -u jdbc:hive2://localhost:10000 -e "
USE kemiskinan_db;

-- Province poverty summary
SELECT 'PROVINCE POVERTY SUMMARY' as section;
SELECT provinsi, 
       ROUND(avg_poverty_rate, 2) as avg_poverty_pct,
       province_poverty_classification,
       total_population,
       ROUND(clean_water_access_pct, 2) as water_access_pct
FROM province_poverty_summary 
ORDER BY avg_poverty_rate DESC
LIMIT 5;

-- Model performance
SELECT 'MODEL PERFORMANCE' as section;
SELECT metric, ROUND(value, 4) as value FROM model_metrics;

-- Top feature importance
SELECT 'TOP FEATURE IMPORTANCE' as section;
SELECT feature, ROUND(importance, 4) as importance 
FROM feature_importance 
ORDER BY importance DESC 
LIMIT 5;
"

echo ""
echo "🎉 Complete ETL Pipeline executed successfully!"
echo "=============================================================="
echo "📊 Data Layers Summary:"
echo "   • Bronze: Raw data from CSV"
echo "   • Silver: Cleaned and standardized data"
echo "   • Gold: Aggregated analysis-ready data"
echo "   • ML: Poverty prediction model and results"
echo ""
echo "🌐 Access Points:"
echo "   • Hive CLI: docker exec -it hive-server beeline -u jdbc:hive2://localhost:10000"
echo "   • Spark UI: http://localhost:8080"
echo "   • HDFS UI: http://localhost:9870"
echo "   • Superset: http://localhost:8088 (admin/admin)"
echo ""
echo "✅ Pipeline Status: COMPLETED"
echo "=============================================================="
