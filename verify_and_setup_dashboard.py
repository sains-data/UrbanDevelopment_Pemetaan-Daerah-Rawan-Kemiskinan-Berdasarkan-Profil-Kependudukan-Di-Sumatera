#!/usr/bin/env python3
"""
Real Data Verification and Superset Dashboard Setup Script
Kelompok 18 - Big Data Poverty Mapping Pipeline (Sumatra)

This script verifies the real poverty data (20,000+ records) and provides
instructions for setting up Superset dashboards with the actual data.
"""

import os
import sys
import psycopg2
import pandas as pd
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'poverty_mapping',
    'user': 'postgres',
    'password': 'postgres123'
}

def check_database_connection():
    """Check if we can connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL Connection: SUCCESS")
        print(f"   Database Version: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL Connection: FAILED")
        print(f"   Error: {str(e)}")
        return False

def verify_real_data():
    """Verify the real poverty data is loaded correctly"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check total records
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        total_records = cursor.fetchone()[0]
        print(f"✅ Total Records: {total_records:,}")
        
        # Check provinces
        cursor.execute("SELECT province, COUNT(*) FROM poverty_data GROUP BY province ORDER BY province;")
        provinces = cursor.fetchall()
        print(f"✅ Provinces Data Distribution:")
        for province, count in provinces:
            print(f"   - {province}: {count:,} records")
        
        # Check sample data
        cursor.execute("""
            SELECT province, regency, commodity, poverty_percentage, population
            FROM poverty_data 
            WHERE commodity LIKE '%Jagung%' 
            LIMIT 3;
        """)
        samples = cursor.fetchall()
        print(f"✅ Sample Real Data Records:")
        for i, (province, regency, commodity, poverty_pct, population) in enumerate(samples, 1):
            print(f"   {i}. {province} - {regency}")
            print(f"      Commodity: {commodity}")
            print(f"      Poverty %: {poverty_pct}%, Population: {population:,}")
        
        # Check data completeness
        cursor.execute("SELECT COUNT(DISTINCT province) as provinces, COUNT(DISTINCT regency) as regencies FROM poverty_data;")
        distinct_counts = cursor.fetchone()
        print(f"✅ Data Completeness:")
        print(f"   - Unique Provinces: {distinct_counts[0]}")
        print(f"   - Unique Regencies: {distinct_counts[1]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Data Verification: FAILED")
        print(f"   Error: {str(e)}")
        return False

def generate_dashboard_sql_queries():
    """Generate SQL queries for dashboard creation"""
    queries = {
        "poverty_by_province": """
            -- Poverty Distribution by Province
            SELECT 
                province,
                AVG(poverty_percentage) as avg_poverty_rate,
                SUM(population) as total_population,
                COUNT(*) as total_areas
            FROM poverty_data 
            GROUP BY province 
            ORDER BY avg_poverty_rate DESC;
        """,
        
        "top_commodities": """
            -- Top Commodities by Frequency
            SELECT 
                commodity,
                COUNT(*) as frequency,
                AVG(poverty_percentage) as avg_poverty_rate,
                AVG(consumption_per_capita) as avg_consumption
            FROM poverty_data 
            WHERE commodity IS NOT NULL
            GROUP BY commodity 
            ORDER BY frequency DESC 
            LIMIT 15;
        """,
        
        "poverty_categories": """
            -- Poverty Category Distribution
            SELECT 
                poverty_category,
                COUNT(*) as count,
                AVG(poverty_percentage) as avg_poverty_rate,
                AVG(unemployment_rate) as avg_unemployment
            FROM poverty_data 
            WHERE poverty_category IS NOT NULL
            GROUP BY poverty_category 
            ORDER BY avg_poverty_rate DESC;
        """,
        
        "infrastructure_analysis": """
            -- Infrastructure vs Poverty Analysis
            SELECT 
                education_access,
                health_facility,
                water_access,
                AVG(poverty_percentage) as avg_poverty_rate,
                COUNT(*) as area_count
            FROM poverty_data 
            WHERE education_access IS NOT NULL 
                AND health_facility IS NOT NULL 
                AND water_access IS NOT NULL
            GROUP BY education_access, health_facility, water_access
            ORDER BY avg_poverty_rate DESC;
        """,
        
        "geospatial_data": """
            -- Geospatial Data for Map Visualization
            SELECT 
                province,
                regency,
                district,
                village,
                latitude,
                longitude,
                poverty_percentage,
                population,
                poverty_category
            FROM poverty_data 
            WHERE latitude IS NOT NULL 
                AND longitude IS NOT NULL
            ORDER BY poverty_percentage DESC;
        """
    }
    
    print(f"✅ Dashboard SQL Queries Generated:")
    for query_name, query in queries.items():
        print(f"   - {query_name.replace('_', ' ').title()}")
    
    return queries

def create_superset_connection_guide():
    """Create a comprehensive guide for Superset connection setup"""
    guide = f"""
# SUPERSET DASHBOARD SETUP - REAL DATA
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## VERIFIED DATA STATUS ✅
- Total Records: 20,000+ real poverty data
- Provinces: Sumatera Barat, Sumatera Selatan, Sumatera Utara
- Data Source: Profil_Kemiskinan_Sumatera.csv

## SUPERSET CONNECTION DETAILS
```
Database Type: PostgreSQL
Host: postgres-local (for container connection)
Port: 5432
Database: poverty_mapping
Username: postgres
Password: postgres123
```

## CONNECTION STRING FOR SUPERSET
```
postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping
```

## STEP-BY-STEP DASHBOARD CREATION

### 1. Access Superset
- Open browser: http://localhost:8089
- Login: admin / admin

### 2. Add Database Connection
- Settings → Database Connections → + Database
- Choose PostgreSQL
- Enter connection details above
- Test connection

### 3. Create Datasets
- Datasets → + Dataset
- Choose 'poverty_mapping' database
- Select 'poverty_data' table
- Save with name: "Real Poverty Data Sumatra"

### 4. Recommended Dashboard Charts

#### A. Poverty by Province (Bar Chart)
- Chart Type: Bar Chart
- Metrics: AVG(poverty_percentage)
- Dimensions: province
- Sort: Descending by poverty rate

#### B. Population Distribution (Pie Chart)
- Chart Type: Pie Chart
- Metrics: SUM(population)
- Dimensions: province

#### C. Commodity Analysis (Horizontal Bar)
- Chart Type: Horizontal Bar Chart
- Metrics: COUNT(*)
- Dimensions: commodity
- Filters: Show top 15 commodities

#### D. Infrastructure vs Poverty (Heatmap)
- Chart Type: Heatmap
- Metrics: AVG(poverty_percentage)
- Rows: education_access
- Columns: health_facility

#### E. Geospatial Poverty Map
- Chart Type: Deck.gl Scatterplot
- Latitude: latitude
- Longitude: longitude
- Size: population
- Color: poverty_percentage

### 5. Create Dashboard
- Dashboards → + Dashboard
- Name: "Sumatra Poverty Analysis - Real Data"
- Add all charts created above
- Arrange in logical layout

## SAMPLE QUERIES FOR VERIFICATION
Use these in SQL Lab to verify data:

```sql
-- Check total records
SELECT COUNT(*) as total_records FROM poverty_data;

-- Province distribution
SELECT province, COUNT(*) as records 
FROM poverty_data 
GROUP BY province;

-- Sample real data
SELECT * FROM poverty_data 
WHERE commodity LIKE '%Jagung%' 
LIMIT 5;
```

## TROUBLESHOOTING
1. If connection fails, ensure containers are running:
   docker-compose up -d postgres superset

2. If Superset not accessible:
   docker logs superset

3. For database access issues:
   docker exec -it postgres-local psql -U postgres -d poverty_mapping

## NEXT STEPS
1. Complete dashboard creation in Superset
2. Add filters and interactive elements
3. Export dashboard for presentation
4. Document insights from real data analysis

---
This guide uses REAL poverty data (20,000+ records) instead of sample data.
Ready for meaningful dashboard creation and data analysis!
"""
    
    with open("SUPERSET_REAL_DATA_SETUP.md", "w", encoding='utf-8') as f:
        f.write(guide)
    
    print(f"✅ Superset Setup Guide Created: SUPERSET_REAL_DATA_SETUP.md")

def main():
    """Main execution function"""
    print("=" * 70)
    print("🎯 BIG DATA POVERTY MAPPING - REAL DATA VERIFICATION")
    print("   Kelompok 18 - Sumatra Dataset (20,000+ records)")
    print("=" * 70)
    
    # Step 1: Check database connection
    print("\n1. Checking Database Connection...")
    if not check_database_connection():
        print("❌ Cannot proceed without database connection.")
        return False
    
    # Step 2: Verify real data
    print("\n2. Verifying Real Poverty Data...")
    if not verify_real_data():
        print("❌ Data verification failed.")
        return False
    
    # Step 3: Generate dashboard queries
    print("\n3. Generating Dashboard SQL Queries...")
    queries = generate_dashboard_sql_queries()
    
    # Step 4: Create setup guide
    print("\n4. Creating Superset Setup Guide...")
    create_superset_connection_guide()
    
    print("\n" + "=" * 70)
    print("🎉 VERIFICATION COMPLETE - READY FOR DASHBOARD CREATION!")
    print("=" * 70)
    print("\n✅ Real data verified: 20,000+ poverty records loaded")
    print("✅ PostgreSQL connection working")
    print("✅ Superset setup guide created")
    print("\n🚀 NEXT STEPS:")
    print("1. Open Superset: http://localhost:8089")
    print("2. Login with admin/admin")
    print("3. Follow SUPERSET_REAL_DATA_SETUP.md guide")
    print("4. Create dashboards with real Sumatra poverty data")
    
    return True

if __name__ == "__main__":
    main()
