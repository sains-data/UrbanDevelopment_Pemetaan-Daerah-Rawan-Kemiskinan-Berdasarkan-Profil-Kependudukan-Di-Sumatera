#!/bin/bash
# PostgreSQL Initialization Script for Poverty Mapping Database

# Create databases
echo "Creating databases..."
psql -U postgres -c "CREATE DATABASE IF NOT EXISTS poverty_mapping;"
psql -U postgres -c "CREATE DATABASE IF NOT EXISTS superset_db;"
psql -U postgres -c "CREATE DATABASE IF NOT EXISTS analytics_db;"

# Create user for applications
psql -U postgres -c "CREATE USER bigdata_user WITH PASSWORD 'bigdata123';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE poverty_mapping TO bigdata_user;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE superset_db TO bigdata_user;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE analytics_db TO bigdata_user;"

# Create schema for poverty data
psql -U postgres -d poverty_mapping -c "
CREATE SCHEMA IF NOT EXISTS poverty_data;
CREATE SCHEMA IF NOT EXISTS processed_data;
CREATE SCHEMA IF NOT EXISTS ml_models;
"

echo "PostgreSQL databases initialized successfully!"
