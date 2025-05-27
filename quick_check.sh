#!/bin/bash

# Quick Pipeline Checker and Runner
# Kelompok 18 - Sumatra Poverty Mapping

echo "🚀 QUICK PIPELINE STATUS CHECK"
echo "=============================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check key services
echo "🔍 Checking key services..."

services=(
    "namenode:9870:Hadoop NameNode"
    "spark-master:8080:Spark Master"
    "airflow-webserver:8090:Airflow"
    "superset:8089:Superset"
)

all_running=true

for service in "${services[@]}"; do
    IFS=':' read -r name port desc <<< "$service"
    
    if docker ps | grep -q "$name"; then
        echo "  ✅ $desc: http://localhost:$port"
    else
        echo "  ❌ $desc: Not running"
        all_running=false
    fi
done

echo ""

if [ "$all_running" = true ]; then
    echo "✅ All services are running!"
    echo ""
    echo "🎯 Ready to execute pipeline!"
    echo "Run: python run_pipeline.py"
    echo ""
    echo "🌐 Access URLs:"
    echo "  - Airflow: http://localhost:8090 (admin/admin)"
    echo "  - Superset: http://localhost:8089 (admin/admin)" 
    echo "  - Spark: http://localhost:8080"
    echo "  - HDFS: http://localhost:9870"
else
    echo "⚠️  Some services are not running."
    echo "Start services with: docker-compose up -d"
fi

echo ""
echo "🚀 Quick commands:"
echo "  docker-compose up -d     # Start all services"
echo "  python run_pipeline.py   # Run complete pipeline"
echo "  docker-compose logs -f   # View logs"
