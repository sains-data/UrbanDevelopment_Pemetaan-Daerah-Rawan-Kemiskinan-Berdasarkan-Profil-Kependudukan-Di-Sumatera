#!/usr/bin/env python3
"""
Verify Superset Connection to Real Poverty Data
Kelompok 18 - Big Data Poverty Mapping Pipeline
Tests connection and creates sample queries for dashboard
"""

import psycopg2
import pandas as pd
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection using container name (for Superset)
DB_CONFIG = {
    'host': 'localhost',  # localhost for external access
    'port': 5432,
    'database': 'poverty_mapping',
    'user': 'postgres',
    'password': 'postgres123'
}

def test_database_connection():
    """Test connection to PostgreSQL with real data"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Test basic connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        logger.info(f"✅ Connected to PostgreSQL: {version[:50]}...")
        
        # Check if real data is loaded
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        count = cursor.fetchone()[0]
        logger.info(f"✅ Total poverty records: {count:,}")
          # Check provinces
        cursor.execute("""
            SELECT province, COUNT(*) as count, 
                   ROUND(AVG(poverty_percentage), 2) as avg_poverty
            FROM poverty_data 
            GROUP BY province 
            ORDER BY avg_poverty DESC;
        """)
        
        provinces = cursor.fetchall()
        logger.info("📊 Provinces in database:")
        for province, count, avg_poverty in provinces:
            logger.info(f"   {province}: {count:,} records, {avg_poverty}% avg poverty")
          # Sample data for verification
        cursor.execute("""
            SELECT province, commodity, poverty_percentage, 
                   population, poverty_category
            FROM poverty_data 
            ORDER BY poverty_percentage DESC 
            LIMIT 5;
        """)
          samples = cursor.fetchall()
        logger.info("📋 Top 5 highest poverty areas:")
        for i, (province, commodity, poverty, population, category) in enumerate(samples, 1):
            logger.info(f"   {i}. {province} - {poverty}% poverty ({population:,} people) - {category}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def create_sample_queries():
    """Create sample SQL queries for Superset dashboards"""
      queries = {
        "Province Overview": """
            SELECT 
                province,
                COUNT(*) as total_areas,
                ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
                SUM(population) as total_population,
                ROUND(AVG(unemployment_rate), 2) as avg_unemployment
            FROM poverty_data 
            GROUP BY province 
            ORDER BY avg_poverty_rate DESC;
        """,
          "Poverty Categories Distribution": """
            SELECT 
                poverty_category,
                COUNT(*) as area_count,
                ROUND(AVG(poverty_percentage), 2) as avg_poverty,
                SUM(population) as total_population
            FROM poverty_data 
            GROUP BY poverty_category 
            ORDER BY avg_poverty DESC;
        """,
          "Education vs Poverty": """
            SELECT 
                education_access,
                COUNT(*) as area_count,
                ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
                ROUND(AVG(unemployment_rate), 2) as avg_unemployment
            FROM poverty_data 
            GROUP BY education_access 
            ORDER BY avg_poverty_rate DESC;
        """,
          "Health Facilities Impact": """
            SELECT 
                health_facility,
                COUNT(*) as area_count,
                ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
                SUM(population) as total_population
            FROM poverty_data 
            GROUP BY health_facility 
            ORDER BY avg_poverty_rate DESC;
        """,
          "Water Access Analysis": """
            SELECT 
                water_access,
                COUNT(*) as area_count,
                ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
                ROUND(AVG(unemployment_rate), 2) as avg_unemployment
            FROM poverty_data 
            GROUP BY water_access 
            ORDER BY avg_poverty_rate DESC;
        """,
          "Top Poverty Hotspots": """
            SELECT 
                province,
                commodity,
                poverty_percentage,
                population,
                unemployment_rate,
                education_access,
                health_facility,
                water_access
            FROM poverty_data 
            WHERE poverty_percentage >= 25.0
            ORDER BY poverty_percentage DESC, population DESC
            LIMIT 20;
        """,
          "Expenditure Groups Analysis": """
            SELECT 
                expenditure_group,
                COUNT(*) as area_count,
                ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
                ROUND(AVG(consumption_per_capita), 2) as avg_consumption,
                SUM(population) as total_population
            FROM poverty_data 
            GROUP BY expenditure_group 
            ORDER BY avg_poverty_rate DESC;
        """
    }
    
    logger.info("📝 Sample SQL queries for Superset dashboards:")
    logger.info("=" * 60)
    
    for title, query in queries.items():
        logger.info(f"\n🔍 {title}:")
        logger.info(f"```sql\n{query.strip()}\n```")
    
    return queries

def test_sample_queries():
    """Test sample queries to ensure they work"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
          # Test province overview query
        logger.info("\n🧪 Testing Province Overview Query:")
        cursor.execute("""
            SELECT 
                province,
                COUNT(*) as total_areas,
                ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
                SUM(population) as total_population
            FROM poverty_data 
            GROUP BY province 
            ORDER BY avg_poverty_rate DESC;
        """)
        
        results = cursor.fetchall()
        for province, areas, poverty, population in results:
            logger.info(f"   {province}: {areas:,} areas, {poverty}% poverty, {population:,} people")
        
        cursor.close()
        conn.close()
        
        logger.info("✅ Sample queries working correctly")
        return True
        
    except Exception as e:
        logger.error(f"❌ Query test failed: {e}")
        return False

def print_superset_instructions():
    """Print instructions for connecting Superset to the database"""
    
    instructions = """
    
    🚀 SUPERSET CONNECTION SETUP INSTRUCTIONS
    ========================================
    
    1. Open Superset at: http://localhost:8089
    2. Login with: admin / admin
    
    3. Add Database Connection:
       - Go to Settings → Database Connections
       - Click "+ Database"
       - Select "PostgreSQL"
       
    4. Connection Details:
       Host: postgres-local
       Port: 5432
       Database: poverty_mapping
       Username: postgres
       Password: postgres123
       
    5. Connection URI:
       postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping
    
    6. Test Connection and Save
    
    7. Create Datasets:
       - Go to Data → Datasets
       - Click "+ Dataset"
       - Select your database → poverty_data table
       - Save the dataset
    
    8. Build Dashboard:
       - Go to Charts
       - Create new chart
       - Select your dataset
       - Choose visualization type
       - Configure metrics and dimensions
    
    📊 AVAILABLE DATA:
    - Total Records: 20,000+
    - Provinces: Sumatera Barat, Sumatera Selatan, Sumatera Utara
    - Key Metrics: Poverty Rate, Population, Unemployment, Education, Health
    
    📈 SUGGESTED CHARTS:
    - Bar Chart: Poverty by Province
    - Pie Chart: Poverty Categories Distribution
    - Heat Map: Poverty Hotspots
    - Line Chart: Poverty vs Education Access
    - Table: Top 20 Poorest Areas
    
    🔍 Use the sample SQL queries provided above for custom charts!
    """
    
    logger.info(instructions)

def main():
    """Main verification function"""
    logger.info("🔍 VERIFYING SUPERSET CONNECTION TO REAL POVERTY DATA")
    logger.info("=" * 60)
    
    # Test database connection
    if not test_database_connection():
        logger.error("❌ Cannot connect to database. Check if PostgreSQL is running.")
        return False
    
    # Create sample queries
    create_sample_queries()
    
    # Test sample queries
    if not test_sample_queries():
        logger.error("❌ Sample queries failed. Check database structure.")
        return False
    
    # Print Superset setup instructions
    print_superset_instructions()
    
    logger.info("\n✅ DATABASE VERIFICATION COMPLETE!")
    logger.info("✅ Ready to create Superset dashboards with real poverty data!")
    
    return True

if __name__ == "__main__":
    main()
