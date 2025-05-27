#!/bin/bash

# Data Ingestion Script - Bronze Layer
# Uploads data from local filesystem to HDFS Bronze layer

echo "📤 Starting data ingestion to Bronze Layer..."

# Source data directory (inside container)
SOURCE_DIR="/data"
BRONZE_PATH="/data/bronze"

# Check if source data exists
if [ ! -f "$SOURCE_DIR/Profil_Kemiskinan_Sumatera.csv" ]; then
    echo "❌ Source data file not found: $SOURCE_DIR/Profil_Kemiskinan_Sumatera.csv"
    exit 1
fi

echo "✅ Source data file found"

# Upload to HDFS Bronze layer
echo "📂 Uploading data to HDFS Bronze layer..."

# Remove existing data if any
docker exec namenode hdfs dfs -rm -r -f $BRONZE_PATH/kemiskinan_raw.csv

# Upload new data
docker exec namenode hdfs dfs -put /data/Profil_Kemiskinan_Sumatera.csv $BRONZE_PATH/kemiskinan_raw.csv

# Verify upload
if docker exec namenode hdfs dfs -test -e $BRONZE_PATH/kemiskinan_raw.csv; then
    echo "✅ Data successfully uploaded to HDFS Bronze layer"
    
    # Show file info
    echo "📊 File information:"
    docker exec namenode hdfs dfs -ls $BRONZE_PATH/
    docker exec namenode hdfs dfs -du -h $BRONZE_PATH/kemiskinan_raw.csv
else
    echo "❌ Failed to upload data to HDFS"
    exit 1
fi

echo "🎉 Data ingestion completed successfully!"
