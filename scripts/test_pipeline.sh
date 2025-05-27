#!/bin/bash

# Big Data Pipeline Testing Script
# Poverty Mapping in Sumatra - Kelompok 18

echo "🧪 Starting Big Data Pipeline Testing..."
echo "============================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS") echo -e "${GREEN}✅ $message${NC}" ;;
        "ERROR") echo -e "${RED}❌ $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "INFO") echo -e "${BLUE}ℹ️  $message${NC}" ;;
    esac
}

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    local timeout=10
    
    if curl -s --max-time $timeout "$url" > /dev/null 2>&1; then
        print_status "SUCCESS" "$service_name is healthy"
        return 0
    else
        print_status "ERROR" "$service_name is not responding"
        return 1
    fi
}

# Function to check Docker container status
check_container() {
    local container_name=$1
    
    if docker ps --format "table {{.Names}}" | grep -q "^$container_name$"; then
        print_status "SUCCESS" "$container_name container is running"
        return 0
    else
        print_status "ERROR" "$container_name container is not running"
        return 1
    fi
}

# Function to test HDFS operations
test_hdfs() {
    print_status "INFO" "Testing HDFS operations..."
    
    # Test HDFS connectivity
    if docker exec namenode hdfs dfs -ls / > /dev/null 2>&1; then
        print_status "SUCCESS" "HDFS is accessible"
    else
        print_status "ERROR" "HDFS is not accessible"
        return 1
    fi
    
    # Check if data directories exist
    for dir in "/data/bronze" "/data/silver" "/data/gold"; do
        if docker exec namenode hdfs dfs -test -d $dir; then
            print_status "SUCCESS" "HDFS directory $dir exists"
        else
            print_status "ERROR" "HDFS directory $dir does not exist"
        fi
    done
    
    # Check if data file exists in bronze layer
    if docker exec namenode hdfs dfs -test -f /data/bronze/Profil_Kemiskinan_Sumatera.csv; then
        print_status "SUCCESS" "Data file exists in bronze layer"
        
        # Show file size
        file_size=$(docker exec namenode hdfs dfs -du -h /data/bronze/Profil_Kemiskinan_Sumatera.csv | awk '{print $1}')
        print_status "INFO" "Data file size: $file_size"
    else
        print_status "WARNING" "Data file not found in bronze layer"
    fi
}

# Function to test Spark
test_spark() {
    print_status "INFO" "Testing Spark cluster..."
    
    # Test Spark Master connectivity
    if check_service "Spark Master" "http://localhost:8080"; then
        # Get worker count
        worker_count=$(curl -s http://localhost:8080/json/ | grep -o '"workers":\[.*\]' | grep -o '{}' | wc -l)
        print_status "INFO" "Spark workers active: $worker_count"
    fi
    
    # Test simple Spark job
    print_status "INFO" "Testing Spark job execution..."
    spark_test_output=$(docker exec spark-master spark-submit --class org.apache.spark.examples.SparkPi \
        /opt/spark/examples/jars/spark-examples_2.12-3.3.0.jar 2 2>&1)
    
    if echo "$spark_test_output" | grep -q "Pi is roughly"; then
        print_status "SUCCESS" "Spark job execution successful"
    else
        print_status "ERROR" "Spark job execution failed"
    fi
}

# Function to test Hive
test_hive() {
    print_status "INFO" "Testing Hive connection..."
    
    # Test Hive server connectivity
    if check_service "Hive Server" "http://localhost:10002"; then
        # Test database creation
        hive_test=$(docker exec hive-server beeline -u jdbc:hive2://localhost:10000 \
            -e "SHOW DATABASES;" 2>&1)
        
        if echo "$hive_test" | grep -q "kemiskinan_db\|default"; then
            print_status "SUCCESS" "Hive database accessible"
        else
            print_status "ERROR" "Hive database not accessible"
        fi
    fi
}

# Function to test ETL pipeline
test_etl_pipeline() {
    print_status "INFO" "Testing ETL pipeline scripts..."
    
    # Check if ETL scripts exist
    etl_scripts=("bronze_to_silver.py" "silver_to_gold.py" "ml_poverty_prediction.py")
    
    for script in "${etl_scripts[@]}"; do
        if [ -f "scripts/spark/$script" ]; then
            print_status "SUCCESS" "ETL script $script exists"
            
            # Basic syntax check
            if python3 -m py_compile "scripts/spark/$script" 2>/dev/null; then
                print_status "SUCCESS" "$script syntax is valid"
            else
                print_status "ERROR" "$script has syntax errors"
            fi
        else
            print_status "ERROR" "ETL script $script not found"
        fi
    done
    
    # Test pipeline execution script
    if [ -f "scripts/run_etl_pipeline.sh" ]; then
        print_status "SUCCESS" "ETL pipeline script exists"
        if [ -x "scripts/run_etl_pipeline.sh" ]; then
            print_status "SUCCESS" "ETL pipeline script is executable"
        else
            print_status "WARNING" "ETL pipeline script is not executable"
        fi
    else
        print_status "ERROR" "ETL pipeline script not found"
    fi
}

# Function to test Airflow
test_airflow() {
    print_status "INFO" "Testing Airflow..."
    
    if check_service "Airflow" "http://localhost:8080/health"; then
        # Check if DAG exists
        dag_file="airflow/dags/poverty_mapping_dag.py"
        if [ -f "$dag_file" ]; then
            print_status "SUCCESS" "Poverty mapping DAG exists"
            
            # Basic syntax check
            if python3 -m py_compile "$dag_file" 2>/dev/null; then
                print_status "SUCCESS" "DAG syntax is valid"
            else
                print_status "ERROR" "DAG has syntax errors"
            fi
        else
            print_status "ERROR" "Poverty mapping DAG not found"
        fi
    fi
}

# Function to test Superset
test_superset() {
    print_status "INFO" "Testing Superset..."
    
    if check_service "Superset" "http://localhost:8088/health"; then
        print_status "SUCCESS" "Superset is accessible"
        
        # Check configuration file
        if [ -f "config/superset_config.py" ]; then
            print_status "SUCCESS" "Superset configuration exists"
        else
            print_status "WARNING" "Superset configuration not found"
        fi
    fi
}

# Function to test data quality
test_data_quality() {
    print_status "INFO" "Testing data quality..."
    
    # Check if source data exists
    if [ -f "data/Profil_Kemiskinan_Sumatera.csv" ]; then
        print_status "SUCCESS" "Source data file exists"
        
        # Check file size
        file_size=$(wc -l < "data/Profil_Kemiskinan_Sumatera.csv")
        print_status "INFO" "Source data has $file_size lines"
        
        # Check for CSV header
        header=$(head -n 1 "data/Profil_Kemiskinan_Sumatera.csv")
        if echo "$header" | grep -q "Provinsi.*Kemiskinan"; then
            print_status "SUCCESS" "Data file has expected headers"
        else
            print_status "WARNING" "Data file headers may be incorrect"
        fi
        
        # Check for empty lines
        empty_lines=$(grep -c '^$' "data/Profil_Kemiskinan_Sumatera.csv" || true)
        if [ $empty_lines -eq 0 ]; then
            print_status "SUCCESS" "No empty lines in data file"
        else
            print_status "WARNING" "Found $empty_lines empty lines in data file"
        fi
    else
        print_status "ERROR" "Source data file not found"
        return 1
    fi
}

# Function to test notebooks
test_notebooks() {
    print_status "INFO" "Testing Jupyter notebooks..."
    
    notebooks=("01_Data_Exploration_Poverty_Mapping.ipynb" "02_Machine_Learning_Poverty_Prediction.ipynb")
    
    for notebook in "${notebooks[@]}"; do
        if [ -f "notebooks/$notebook" ]; then
            print_status "SUCCESS" "Notebook $notebook exists"
            
            # Check if it's valid JSON
            if python3 -m json.tool "notebooks/$notebook" > /dev/null 2>&1; then
                print_status "SUCCESS" "$notebook is valid JSON"
            else
                print_status "ERROR" "$notebook is not valid JSON"
            fi
        else
            print_status "ERROR" "Notebook $notebook not found"
        fi
    done
}

# Function to generate test report
generate_report() {
    local total_tests=$1
    local passed_tests=$2
    local failed_tests=$3
    
    echo ""
    echo "📋 TEST SUMMARY REPORT"
    echo "======================"
    echo "Total Tests: $total_tests"
    echo "Passed: $passed_tests"
    echo "Failed: $failed_tests"
    echo "Success Rate: $(( passed_tests * 100 / total_tests ))%"
    echo ""
    
    if [ $failed_tests -eq 0 ]; then
        print_status "SUCCESS" "All tests passed! Pipeline is ready for production."
    else
        print_status "WARNING" "Some tests failed. Please check the issues above."
    fi
}

# Main test execution
main() {
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    echo "Starting comprehensive pipeline testing..."
    echo ""
    
    # Test 1: Container Status
    print_status "INFO" "=== Testing Container Status ==="
    containers=("namenode" "datanode1" "datanode2" "resourcemanager" "nodemanager" 
               "historyserver" "spark-master" "spark-worker-1" "spark-worker-2" 
               "hive-server" "hive-metastore" "superset" "airflow-webserver")
    
    for container in "${containers[@]}"; do
        ((total_tests++))
        if check_container "$container"; then
            ((passed_tests++))
        else
            ((failed_tests++))
        fi
    done
    
    echo ""
    
    # Test 2: Service Health
    print_status "INFO" "=== Testing Service Health ==="
    ((total_tests++))
    if check_service "Namenode" "http://localhost:9870"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    ((total_tests++))
    if check_service "Resource Manager" "http://localhost:8088"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 3: HDFS
    print_status "INFO" "=== Testing HDFS ==="
    ((total_tests++))
    if test_hdfs; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 4: Spark
    print_status "INFO" "=== Testing Spark ==="
    ((total_tests++))
    if test_spark; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 5: Hive
    print_status "INFO" "=== Testing Hive ==="
    ((total_tests++))
    if test_hive; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 6: ETL Pipeline
    print_status "INFO" "=== Testing ETL Pipeline ==="
    ((total_tests++))
    if test_etl_pipeline; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 7: Airflow
    print_status "INFO" "=== Testing Airflow ==="
    ((total_tests++))
    if test_airflow; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 8: Superset
    print_status "INFO" "=== Testing Superset ==="
    ((total_tests++))
    if test_superset; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 9: Data Quality
    print_status "INFO" "=== Testing Data Quality ==="
    ((total_tests++))
    if test_data_quality; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Test 10: Notebooks
    print_status "INFO" "=== Testing Notebooks ==="
    ((total_tests++))
    if test_notebooks; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    
    echo ""
    
    # Generate final report
    generate_report $total_tests $passed_tests $failed_tests
    
    # Return appropriate exit code
    if [ $failed_tests -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# Execute main function
main "$@"
