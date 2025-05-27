#!/bin/bash
# Quick Access Script for Big Data Services
# Kelompok 18 - Pemetaan Kemiskinan Sumatera

echo "🚀 BIG DATA SERVICES - QUICK ACCESS"
echo "=" * 50
echo "Kelompok 18 - Pemetaan Kemiskinan Sumatera"
echo "=" * 50

echo ""
echo "🎨 SUPERSET DASHBOARD (Primary)"
echo "   URL: http://localhost:8089"
echo "   Login: admin / admin"
echo "   Status: Database ready with 20,000 records"
echo ""

echo "📓 JUPYTER NOTEBOOKS"
echo "   URL: http://localhost:8888"
echo "   Purpose: Data analysis and ML modeling"
echo ""

echo "🗂️ HADOOPjinja2.exceptions.TemplateNotFound: cd /scripts && ./ingest_data.sh
[2025-05-25, 14:03:57 UTC] {taskinstance.py:1400} INFO - Marking task as FAILED. dag_id=poverty_mapping_etl, task_id=ingest_to_bronze, execution_date=20250525T133616, start_date=20250525T140356, end_date=20250525T140357
[2025-05-25, 14:03:57 UTC] {standard_task_runner.py:104} ERROR - Failed to execute job 14 for task ingest_to_bronze (cd /scripts && ./ingest_data.sh; 1239)
[2025-05-25, 14:03:57 UTC] {local_task_job_runner.py:228} INFO - Task exited with return code 1
[2025-05-25, 14:03:57 UTC] {taskinstance.py:2784} INFO - 0 downstream tasks scheduled from follow-on schedule check HDFS"
echo "   URL: http://localhost:9870"
echo "   Purpose: Distributed file system management"
echo ""

echo "⚡ SPARK CLUSTER"
echo "   URL: http://localhost:8080"
echo "   Purpose: Data processing monitoring"
echo ""

echo "🔄 AIRFLOW"
echo "   URL: http://localhost:8090"  
echo "   Purpose: Workflow orchestration"
echo ""

echo "📊 DATABASE INFO"
echo "   Type: SQLite"
echo "   Path: C:/TUBESABD/superset_data/poverty_mapping.db"
echo "   Records: 20,000 poverty data points"
echo "   Tables: poverty_data, province_summary, poverty_distribution"
echo ""

echo "🎯 NEXT ACTIONS"
echo "1. Open Superset: http://localhost:8089"
echo "2. Login with admin/admin"
echo "3. Add database connection using SQLite URI"
echo "4. Create datasets from tables"
echo "5. Build amazing poverty mapping dashboards!"
echo ""

echo "📖 GUIDES AVAILABLE"
echo "   • Complete Guide: superset_data/PANDUAN_DASHBOARD_LENGKAP.md"
echo "   • Quick Start: SUPERSET_READY.md"
echo "   • Verification: python verify_superset_setup.py"
echo ""

echo "🎉 ALL SYSTEMS READY - START CREATING DASHBOARDS!"
