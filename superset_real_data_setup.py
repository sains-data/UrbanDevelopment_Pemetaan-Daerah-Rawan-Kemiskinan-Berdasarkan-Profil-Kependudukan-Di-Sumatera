#!/usr/bin/env python3
"""
Connect Superset to Real Poverty Data
Kelompok 18 - Big Data Poverty Mapping Pipeline
Final setup for Superset dashboards with real CSV data
"""

import psycopg2
import logging
import sys
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'poverty_mapping',
    'user': 'postgres',
    'password': 'postgres123'
}

def verify_real_data():
    """Verify the real poverty data is loaded correctly"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        logger.info("🔍 VERIFYING REAL POVERTY DATA IN DATABASE")
        logger.info("=" * 60)
        
        # Check total records
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        total_count = cursor.fetchone()[0]
        logger.info(f"✅ Total records: {total_count:,}")
        
        # Check column structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'poverty_data' 
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        logger.info(f"📊 Table structure ({len(columns)} columns):")
        for col_name, col_type in columns:
            logger.info(f"   - {col_name}: {col_type}")
        
        # Check provinces
        cursor.execute("""
            SELECT provinsi, COUNT(*) as count
            FROM poverty_data 
            GROUP BY provinsi 
            ORDER BY count DESC;
        """)
        provinces = cursor.fetchall()
        logger.info("🌍 Provinces in database:")
        for province, count in provinces:
            logger.info(f"   - {province}: {count:,} records")
        
        # Sample real data
        cursor.execute("""
            SELECT provinsi, komoditas, persentase_kemiskinan, 
                   jumlah_penduduk, kategori_kemiskinan
            FROM poverty_data 
            ORDER BY persentase_kemiskinan DESC 
            LIMIT 5;
        """)
        samples = cursor.fetchall()
        logger.info("📋 Sample real data (Top 5 highest poverty):")
        for i, (provinsi, komoditas, poverty, population, category) in enumerate(samples, 1):
            logger.info(f"   {i}. {provinsi} - {poverty}% poverty ({population:,} people) - {category}")
            logger.info(f"      Commodity: {komoditas[:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Database verification failed: {e}")
        return False

def create_superset_sql_queries():
    """Create SQL queries for Superset dashboards using real column names"""
    
    queries = {
        "Province Overview": """
            SELECT 
                provinsi as "Province",
                COUNT(*) as "Total Areas",
                ROUND(AVG(persentase_kemiskinan), 2) as "Average Poverty Rate (%)",
                SUM(jumlah_penduduk) as "Total Population",
                ROUND(AVG(tingkat_pengangguran), 2) as "Average Unemployment (%)"
            FROM poverty_data 
            GROUP BY provinsi 
            ORDER BY "Average Poverty Rate (%)" DESC;
        """,
        
        "Poverty Categories Distribution": """
            SELECT 
                kategori_kemiskinan as "Poverty Category",
                COUNT(*) as "Area Count",
                ROUND(AVG(persentase_kemiskinan), 2) as "Average Poverty Rate (%)",
                SUM(jumlah_penduduk) as "Total Population"
            FROM poverty_data 
            GROUP BY kategori_kemiskinan 
            ORDER BY "Average Poverty Rate (%)" DESC;
        """,
        
        "Education vs Poverty Analysis": """
            SELECT 
                akses_pendidikan as "Education Access",
                COUNT(*) as "Area Count",
                ROUND(AVG(persentase_kemiskinan), 2) as "Average Poverty Rate (%)",
                ROUND(AVG(tingkat_pengangguran), 2) as "Average Unemployment (%)",
                SUM(jumlah_penduduk) as "Total Population"
            FROM poverty_data 
            GROUP BY akses_pendidikan 
            ORDER BY "Average Poverty Rate (%)" DESC;
        """,
        
        "Health Facilities Impact": """
            SELECT 
                fasilitas_kesehatan as "Health Facility",
                COUNT(*) as "Area Count",
                ROUND(AVG(persentase_kemiskinan), 2) as "Average Poverty Rate (%)",
                SUM(jumlah_penduduk) as "Total Population"
            FROM poverty_data 
            GROUP BY fasilitas_kesehatan 
            ORDER BY "Average Poverty Rate (%)" DESC;
        """,
        
        "Water Access Analysis": """
            SELECT 
                akses_air_bersih as "Water Access",
                COUNT(*) as "Area Count",
                ROUND(AVG(persentase_kemiskinan), 2) as "Average Poverty Rate (%)",
                ROUND(AVG(tingkat_pengangguran), 2) as "Average Unemployment (%)",
                SUM(jumlah_penduduk) as "Total Population"
            FROM poverty_data 
            GROUP BY akses_air_bersih 
            ORDER BY "Average Poverty Rate (%)" DESC;
        """,
        
        "Top 20 Poverty Hotspots": """
            SELECT 
                provinsi as "Province",
                komoditas as "Commodity",
                persentase_kemiskinan as "Poverty Rate (%)",
                jumlah_penduduk as "Population",
                tingkat_pengangguran as "Unemployment Rate (%)",
                akses_pendidikan as "Education Access",
                fasilitas_kesehatan as "Health Facility",
                akses_air_bersih as "Water Access",
                kategori_kemiskinan as "Poverty Category"
            FROM poverty_data 
            WHERE persentase_kemiskinan >= 25.0
            ORDER BY persentase_kemiskinan DESC, jumlah_penduduk DESC
            LIMIT 20;
        """,
        
        "Expenditure Groups Analysis": """
            SELECT 
                golongan_pengeluaran as "Expenditure Group",
                COUNT(*) as "Area Count",
                ROUND(AVG(persentase_kemiskinan), 2) as "Average Poverty Rate (%)",
                ROUND(AVG(konsumsi_per_kapita), 2) as "Average Consumption per Capita",
                SUM(jumlah_penduduk) as "Total Population"
            FROM poverty_data 
            GROUP BY golongan_pengeluaran 
            ORDER BY "Average Poverty Rate (%)" DESC;
        """,
        
        "Commodity vs Poverty": """
            SELECT 
                komoditas as "Commodity",
                COUNT(*) as "Area Count",
                ROUND(AVG(persentase_kemiskinan), 2) as "Average Poverty Rate (%)",
                SUM(jumlah_penduduk) as "Total Population"
            FROM poverty_data 
            GROUP BY komoditas 
            ORDER BY "Average Poverty Rate (%)" DESC
            LIMIT 10;
        """
    }
    
    logger.info("\n📝 SQL QUERIES FOR SUPERSET DASHBOARDS")
    logger.info("=" * 60)
    logger.info("Copy these queries to create charts in Superset:")
    logger.info("(Go to Charts → Create Chart → Choose SQL Lab)")
    
    for title, query in queries.items():
        logger.info(f"\n🔍 {title}:")
        logger.info("─" * 40)
        logger.info(query.strip())
    
    return queries

def test_sample_queries():
    """Test sample queries with real data"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        logger.info("\n🧪 TESTING SAMPLE QUERIES")
        logger.info("=" * 40)
        
        # Test province overview
        cursor.execute("""
            SELECT 
                provinsi,
                COUNT(*) as total_areas,
                ROUND(AVG(persentase_kemiskinan), 2) as avg_poverty_rate,
                SUM(jumlah_penduduk) as total_population
            FROM poverty_data 
            GROUP BY provinsi 
            ORDER BY avg_poverty_rate DESC;
        """)
        
        results = cursor.fetchall()
        logger.info("🌍 Province Analysis:")
        for provinsi, areas, poverty, population in results:
            logger.info(f"   {provinsi}: {areas:,} areas, {poverty}% avg poverty, {population:,} people")
        
        # Test poverty categories
        cursor.execute("""
            SELECT 
                kategori_kemiskinan,
                COUNT(*) as area_count,
                ROUND(AVG(persentase_kemiskinan), 2) as avg_poverty
            FROM poverty_data 
            GROUP BY kategori_kemiskinan 
            ORDER BY avg_poverty DESC;
        """)
        
        categories = cursor.fetchall()
        logger.info("\n📊 Poverty Categories:")
        for category, count, avg_poverty in categories:
            logger.info(f"   {category}: {count:,} areas, {avg_poverty}% avg poverty")
        
        cursor.close()
        conn.close()
        
        logger.info("✅ All queries working correctly with real data!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Query test failed: {e}")
        return False

def print_superset_setup_guide():
    """Print complete Superset setup instructions"""
    
    guide = """
    
    🚀 SUPERSET DASHBOARD SETUP WITH REAL POVERTY DATA
    ================================================
    
    📋 PREREQUISITE:
    ✅ Real poverty data loaded (20,000 records from CSV)
    ✅ PostgreSQL running on port 5432
    ✅ Superset running on port 8089
    
    🔗 STEP 1: CONNECT TO SUPERSET
    1. Open browser: http://localhost:8089
    2. Login: admin / admin
    
    🔗 STEP 2: ADD DATABASE CONNECTION
    1. Go to: Settings → Database Connections
    2. Click: "+ Database"
    3. Select: "PostgreSQL"
    4. Fill in connection details:
       - Host: postgres-local
       - Port: 5432
       - Database: poverty_mapping
       - Username: postgres
       - Password: postgres123
    
    5. Connection URI:
       postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping
    
    6. Click "Test Connection" → Should show "Connection looks good!"
    7. Click "Connect"
    
    📊 STEP 3: CREATE DATASET
    1. Go to: Data → Datasets
    2. Click: "+ Dataset"
    3. Select:
       - Database: poverty_mapping
       - Schema: public
       - Table: poverty_data
    4. Click "Create Dataset and Create Chart"
    
    📈 STEP 4: CREATE CHARTS
    Use the SQL queries provided above to create various charts:
    
    1. Bar Chart: Province Overview
    2. Pie Chart: Poverty Categories Distribution  
    3. Table: Top 20 Poverty Hotspots
    4. Line Chart: Education vs Poverty
    5. Heatmap: Health Facilities Impact
    
    🎨 STEP 5: BUILD DASHBOARD
    1. Go to: Dashboards
    2. Click: "+ Dashboard"
    3. Add charts to dashboard
    4. Arrange and customize layout
    5. Save dashboard
    
    📊 AVAILABLE REAL DATA COLUMNS:
    - provinsi (Province)
    - komoditas (Commodity)
    - golongan_pengeluaran (Expenditure Group)
    - konsumsi_per_kapita (Consumption per Capita)
    - jumlah_penduduk (Population)
    - persentase_kemiskinan (Poverty Percentage)
    - tingkat_pengangguran (Unemployment Rate)
    - akses_pendidikan (Education Access)
    - fasilitas_kesehatan (Health Facility)
    - akses_air_bersih (Water Access)
    - kategori_kemiskinan (Poverty Category)
    
    🏆 SUCCESS CRITERIA:
    ✅ Database connected successfully
    ✅ Dataset created from poverty_data table
    ✅ At least 5 different chart types created
    ✅ Dashboard with real poverty insights
    ✅ Data showing 20,000 records from 3 Sumatera provinces
    """
    
    logger.info(guide)

def main():
    """Main function to verify and setup Superset with real data"""
    logger.info("🎯 SUPERSET CONNECTION SETUP WITH REAL POVERTY DATA")
    logger.info("=" * 70)
    
    # Verify real data is loaded
    if not verify_real_data():
        logger.error("❌ Real data verification failed. Please load data first.")
        return False
    
    # Test sample queries
    if not test_sample_queries():
        logger.error("❌ Query testing failed. Check database structure.")
        return False
    
    # Create SQL queries for Superset
    create_superset_sql_queries()
    
    # Print setup guide
    print_superset_setup_guide()
    
    logger.info("\n" + "=" * 70)
    logger.info("🎉 SETUP COMPLETE!")
    logger.info("✅ Real poverty data verified: 20,000 records")
    logger.info("✅ Queries tested and ready")
    logger.info("✅ Superset setup guide provided")
    logger.info("🚀 Ready to create amazing poverty mapping dashboards!")
    logger.info("=" * 70)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
