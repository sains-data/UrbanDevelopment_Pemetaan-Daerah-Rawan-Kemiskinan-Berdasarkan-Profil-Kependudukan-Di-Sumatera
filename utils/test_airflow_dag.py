#!/usr/bin/env python3
"""
Test script untuk DAG Airflow Poverty Mapping
Test semua fungsi tanpa menjalankan Airflow
"""

import sys
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_dag_import():
    """Test import DAG file"""
    try:
        # Add airflow dags directory to path
        dag_path = os.path.join(os.getcwd(), 'airflow', 'dags')
        sys.path.insert(0, dag_path)
        
        # Try to import the final DAG
        import poverty_mapping_dag_final
        
        logging.info("✅ DAG import successful")
        logging.info(f"📋 DAG ID: {poverty_mapping_dag_final.dag.dag_id}")
        logging.info(f"🏷️ Tags: {poverty_mapping_dag_final.dag.tags}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ DAG import failed: {str(e)}")
        return False

def test_data_validation():
    """Test data validation function"""
    try:
        from poverty_mapping_dag_final import validate_data_files
        
        logging.info("🔍 Testing data validation...")
        result = validate_data_files()
        logging.info(f"✅ Data validation result: {result}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Data validation test failed: {str(e)}")
        return False

def test_hdfs_ingestion():
    """Test HDFS ingestion function"""
    try:
        from poverty_mapping_dag_final import ingest_to_hdfs
        
        logging.info("📤 Testing HDFS ingestion...")
        result = ingest_to_hdfs()
        logging.info(f"✅ HDFS ingestion result: {result}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ HDFS ingestion test failed: {str(e)}")
        logging.info("ℹ️ This is expected if Docker containers are not accessible")
        return False

def test_bronze_to_silver():
    """Test Bronze to Silver transformation"""
    try:
        from poverty_mapping_dag_final import process_bronze_to_silver
        
        logging.info("🔄 Testing Bronze to Silver transformation...")
        result = process_bronze_to_silver()
        logging.info(f"✅ Bronze to Silver result: {result}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Bronze to Silver test failed: {str(e)}")
        return False

def test_silver_to_gold():
    """Test Silver to Gold aggregation"""
    try:
        from poverty_mapping_dag_final import process_silver_to_gold
        
        logging.info("⚡ Testing Silver to Gold aggregation...")
        result = process_silver_to_gold()
        logging.info(f"✅ Silver to Gold result: {result}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Silver to Gold test failed: {str(e)}")
        return False

def test_ml_analysis():
    """Test ML analysis function"""
    try:
        from poverty_mapping_dag_final import run_ml_analysis
        
        logging.info("🤖 Testing ML analysis...")
        result = run_ml_analysis()
        logging.info(f"✅ ML analysis result: {result}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ ML analysis test failed: {str(e)}")
        return False

def test_final_report():
    """Test final report generation"""
    try:
        from poverty_mapping_dag_final import generate_final_report
        
        logging.info("📋 Testing final report generation...")
        result = generate_final_report()
        logging.info(f"✅ Final report result: {result}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Final report test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    logging.info("🚀 STARTING AIRFLOW DAG TESTING")
    logging.info("=" * 60)
    
    tests = [
        ("DAG Import", test_dag_import),
        ("Data Validation", test_data_validation),
        ("HDFS Ingestion", test_hdfs_ingestion),
        ("Bronze to Silver", test_bronze_to_silver),
        ("Silver to Gold", test_silver_to_gold),
        ("ML Analysis", test_ml_analysis),
        ("Final Report", test_final_report)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logging.info(f"\n🧪 Testing: {test_name}")
        logging.info("-" * 40)
        
        try:
            success = test_func()
            if success:
                passed += 1
                logging.info(f"✅ {test_name}: PASSED")
            else:
                logging.info(f"❌ {test_name}: FAILED")
        except Exception as e:
            logging.error(f"❌ {test_name}: ERROR - {str(e)}")
    
    logging.info("\n" + "=" * 60)
    logging.info(f"🎯 TEST SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        logging.info("🎉 ALL TESTS PASSED! DAG is ready for deployment")
    elif passed >= total - 2:
        logging.info("⚠️ MOSTLY PASSING - DAG should work with running containers")
    else:
        logging.info("❌ MULTIPLE FAILURES - DAG needs review")
    
    logging.info("\n📋 NEXT STEPS:")
    logging.info("1. Ensure all Docker containers are running")
    logging.info("2. Check Airflow UI: http://localhost:8090")
    logging.info("3. Enable and trigger the DAG: poverty_mapping_etl_final")
    logging.info("4. Monitor execution progress")

if __name__ == "__main__":
    main()
