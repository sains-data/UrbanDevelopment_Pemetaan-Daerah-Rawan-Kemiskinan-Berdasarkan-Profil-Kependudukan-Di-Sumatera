#!/usr/bin/env python3
"""
Integrate Gold Layer Data to Superset
Kelompok 18 - Big Data Poverty Mapping Pipeline

This script loads processed Gold layer data into PostgreSQL for Superset visualization
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import subprocess
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoldLayerIntegrator:
    def __init__(self):
        self.postgres_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'poverty_mapping',
            'user': 'postgres',
            'password': 'postgres123'
        }
        
        self.hive_config = {
            'host': 'localhost',
            'port': 10000,
            'database': 'kemiskinan_db'
        }
        
    def print_header(self):
        print("=" * 70)
        print("🏆 INTEGRATING GOLD LAYER DATA TO SUPERSET")
        print("📊 Kelompok 18 - Clean Data from Medallion Architecture")
        print("🔄 Bronze → Silver → Gold → Superset Dashboard")
        print("=" * 70)
        
    def check_hive_tables(self):
        """Check available Gold layer tables in Hive"""
        logger.info("🔍 Checking Gold layer tables in Hive...")
        
        try:
            # Check Hive tables using beeline command
            cmd = [
                "docker", "exec", "hive-server", "beeline", 
                "-u", "jdbc:hive2://localhost:10000/kemiskinan_db",
                "-e", "SHOW TABLES;"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info("✅ Available Gold layer tables:")
                tables = []
                for line in result.stdout.split('\n'):
                    if line.strip() and 'province_poverty_summary' in line:
                        tables.append('province_poverty_summary')
                    elif line.strip() and 'expenditure_analysis' in line:
                        tables.append('expenditure_analysis')
                    elif line.strip() and 'poverty_statistics' in line:
                        tables.append('poverty_statistics')
                    elif line.strip() and 'poverty_correlations' in line:
                        tables.append('poverty_correlations')
                
                for table in tables:
                    logger.info(f"   📊 {table}")
                
                return tables
            else:
                logger.error(f"❌ Failed to check Hive tables: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error checking Hive tables: {e}")
            return []
    
    def extract_gold_data(self, table_name):
        """Extract data from Gold layer Hive table"""
        logger.info(f"📤 Extracting data from {table_name}...")
        
        try:
            # Use beeline to extract data as CSV
            query = f"SELECT * FROM kemiskinan_db.{table_name};"
            
            cmd = [
                "docker", "exec", "hive-server", "beeline",
                "-u", "jdbc:hive2://localhost:10000/kemiskinan_db",
                "--outputformat=csv2",
                "-e", query
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Parse CSV output
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:  # Skip header
                    # Create DataFrame from CSV output
                    from io import StringIO
                    csv_data = '\n'.join(lines)
                    df = pd.read_csv(StringIO(csv_data))
                    
                    logger.info(f"✅ Extracted {len(df)} rows from {table_name}")
                    return df
                else:
                    logger.warning(f"⚠️ No data found in {table_name}")
                    return pd.DataFrame()
            else:
                logger.error(f"❌ Failed to extract from {table_name}: {result.stderr}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ Error extracting from {table_name}: {e}")
            return pd.DataFrame()
    
    def create_gold_tables_in_postgres(self):
        """Create tables for Gold layer data in PostgreSQL"""
        logger.info("🗄️ Creating Gold layer tables in PostgreSQL...")
        
        try:
            conn = psycopg2.connect(**self.postgres_config)
            cursor = conn.cursor()
            
            # Drop existing Gold tables
            gold_tables = [
                'gold_province_summary',
                'gold_expenditure_analysis', 
                'gold_poverty_statistics',
                'gold_poverty_correlations'
            ]
            
            for table in gold_tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            
            # Create province summary table
            cursor.execute("""
                CREATE TABLE gold_province_summary (
                    provinsi VARCHAR(100) PRIMARY KEY,
                    avg_poverty_rate DECIMAL(5,2),
                    avg_unemployment_rate DECIMAL(5,2),
                    total_population BIGINT,
                    record_count INTEGER,
                    expenditure_groups INTEGER,
                    avg_consumption DECIMAL(10,2),
                    good_education_access INTEGER,
                    adequate_health_facilities INTEGER,
                    clean_water_access INTEGER,
                    good_education_access_pct DECIMAL(5,2),
                    adequate_health_facilities_pct DECIMAL(5,2),
                    clean_water_access_pct DECIMAL(5,2),
                    province_poverty_classification VARCHAR(20),
                    low_poverty_count INTEGER,
                    medium_poverty_count INTEGER,
                    high_poverty_count INTEGER,
                    aggregation_timestamp TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create expenditure analysis table  
            cursor.execute("""
                CREATE TABLE gold_expenditure_analysis (
                    id SERIAL PRIMARY KEY,
                    expenditure_group_clean VARCHAR(100),
                    provinsi VARCHAR(100),
                    avg_poverty_rate DECIMAL(5,2),
                    avg_consumption DECIMAL(10,2),
                    total_population BIGINT,
                    record_count INTEGER,
                    most_common_poverty_level VARCHAR(20),
                    aggregation_timestamp TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create poverty statistics table
            cursor.execute("""
                CREATE TABLE gold_poverty_statistics (
                    id SERIAL PRIMARY KEY,
                    metric_name VARCHAR(100),
                    metric_value DECIMAL(10,2),
                    calculation_timestamp TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create poverty correlations table
            cursor.execute("""
                CREATE TABLE gold_poverty_correlations (
                    id SERIAL PRIMARY KEY,
                    factor_1 VARCHAR(100),
                    factor_2 VARCHAR(100),
                    correlation_value DECIMAL(5,4),
                    calculation_timestamp TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info("✅ Gold layer tables created in PostgreSQL")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating Gold tables: {e}")
            return False
    
    def load_gold_data_to_postgres(self):
        """Load Gold layer data into PostgreSQL"""
        logger.info("📥 Loading Gold layer data into PostgreSQL...")
        
        try:
            engine = create_engine(f"postgresql://postgres:postgres123@localhost:5432/poverty_mapping")
            
            # Extract and load each Gold table
            gold_tables = {
                'province_poverty_summary': 'gold_province_summary',
                'expenditure_analysis': 'gold_expenditure_analysis',
                'poverty_statistics': 'gold_poverty_statistics', 
                'poverty_correlations': 'gold_poverty_correlations'
            }
            
            loaded_tables = 0
            
            for hive_table, postgres_table in gold_tables.items():
                df = self.extract_gold_data(hive_table)
                
                if not df.empty:
                    # Clean column names
                    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
                    
                    # Load to PostgreSQL
                    df.to_sql(postgres_table, engine, if_exists='append', index=False)
                    
                    logger.info(f"✅ Loaded {len(df)} rows into {postgres_table}")
                    loaded_tables += 1
                else:
                    logger.warning(f"⚠️ Skipping {hive_table} - no data available")
            
            logger.info(f"🎉 Successfully loaded {loaded_tables} Gold layer tables into PostgreSQL")
            return loaded_tables > 0
            
        except Exception as e:
            logger.error(f"❌ Error loading Gold data: {e}")
            return False
    
    def create_gold_views(self):
        """Create views for easier dashboard creation"""
        logger.info("📊 Creating Gold layer views for Superset...")
        
        try:
            conn = psycopg2.connect(**self.postgres_config)
            cursor = conn.cursor()
            
            # Drop existing views
            cursor.execute("DROP VIEW IF EXISTS v_gold_province_dashboard CASCADE;")
            cursor.execute("DROP VIEW IF EXISTS v_gold_poverty_insights CASCADE;")
            cursor.execute("DROP VIEW IF EXISTS v_gold_expenditure_insights CASCADE;")
            
            # Create province dashboard view
            cursor.execute("""
                CREATE VIEW v_gold_province_dashboard AS
                SELECT 
                    provinsi,
                    avg_poverty_rate,
                    avg_unemployment_rate,
                    total_population,
                    avg_consumption,
                    good_education_access_pct,
                    adequate_health_facilities_pct,
                    clean_water_access_pct,
                    province_poverty_classification,
                    CASE 
                        WHEN avg_poverty_rate <= 10 THEN 'Low Risk'
                        WHEN avg_poverty_rate <= 15 THEN 'Medium Risk'
                        ELSE 'High Risk'
                    END as risk_category,
                    ROUND((good_education_access_pct + adequate_health_facilities_pct + clean_water_access_pct) / 3, 2) as infrastructure_score
                FROM gold_province_summary
                ORDER BY avg_poverty_rate DESC;
            """)
            
            # Create poverty insights view
            cursor.execute("""
                CREATE VIEW v_gold_poverty_insights AS
                SELECT 
                    'Total Provinces' as metric,
                    COUNT(*)::DECIMAL as value,
                    'count' as unit
                FROM gold_province_summary
                UNION ALL
                SELECT 
                    'Average Poverty Rate' as metric,
                    ROUND(AVG(avg_poverty_rate), 2) as value,
                    'percentage' as unit
                FROM gold_province_summary
                UNION ALL
                SELECT 
                    'Total Population' as metric,
                    SUM(total_population)::DECIMAL as value,
                    'people' as unit
                FROM gold_province_summary
                UNION ALL
                SELECT 
                    'Average Infrastructure Access' as metric,
                    ROUND(AVG((good_education_access_pct + adequate_health_facilities_pct + clean_water_access_pct) / 3), 2) as value,
                    'percentage' as unit
                FROM gold_province_summary;
            """)
            
            # Create expenditure insights view
            cursor.execute("""
                CREATE VIEW v_gold_expenditure_insights AS
                SELECT 
                    expenditure_group_clean,
                    provinsi,
                    avg_poverty_rate,
                    avg_consumption,
                    total_population,
                    most_common_poverty_level,
                    CASE 
                        WHEN avg_consumption > 150000 THEN 'High Consumption'
                        WHEN avg_consumption > 100000 THEN 'Medium Consumption'
                        ELSE 'Low Consumption'
                    END as consumption_category
                FROM gold_expenditure_analysis
                WHERE avg_poverty_rate IS NOT NULL
                ORDER BY avg_poverty_rate DESC;
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info("✅ Gold layer views created for Superset")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating Gold views: {e}")
            return False
    
    def verify_gold_data(self):
        """Verify Gold layer data in PostgreSQL"""
        logger.info("🔍 Verifying Gold layer data in PostgreSQL...")
        
        try:
            conn = psycopg2.connect(**self.postgres_config)
            cursor = conn.cursor()
            
            # Check table counts
            tables = [
                'gold_province_summary',
                'gold_expenditure_analysis', 
                'gold_poverty_statistics',
                'gold_poverty_correlations'
            ]
            
            logger.info("📊 Gold layer data summary:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                logger.info(f"   📋 {table}: {count} records")
            
            # Show sample data from province summary
            cursor.execute("""
                SELECT provinsi, avg_poverty_rate, province_poverty_classification, total_population
                FROM gold_province_summary 
                ORDER BY avg_poverty_rate DESC 
                LIMIT 5;
            """)
            
            results = cursor.fetchall()
            if results:
                logger.info("\n🏆 Top provinces by poverty rate (Gold layer):")
                for row in results:
                    logger.info(f"   • {row[0]}: {row[1]}% ({row[2]}) - Population: {row[3]:,}")
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error verifying Gold data: {e}")
            return False
    
    def create_superset_guide(self):
        """Create guide for using Gold layer data in Superset"""
        guide_content = f"""
# 🏆 SUPERSET GOLD LAYER DATA INTEGRATION GUIDE
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ✅ GOLD LAYER DATA AVAILABLE IN SUPERSET

### 📊 Gold Layer Tables:
1. **gold_province_summary** - Aggregated province-level insights
2. **gold_expenditure_analysis** - Expenditure group analysis  
3. **gold_poverty_statistics** - Overall poverty statistics
4. **gold_poverty_correlations** - Factor correlations

### 📈 Gold Layer Views (Ready for Charts):
1. **v_gold_province_dashboard** - Province dashboard data
2. **v_gold_poverty_insights** - Key poverty metrics
3. **v_gold_expenditure_insights** - Expenditure analysis

## 🚀 CREATING GOLD LAYER DASHBOARDS

### Step 1: Access Superset
- URL: http://localhost:8089
- Login: admin / admin

### Step 2: Create Datasets from Gold Tables
1. Go to **Data** → **Datasets** → **+ DATASET**
2. Select database: **Poverty Mapping DB** (PostgreSQL)
3. Choose from Gold tables:
   - `v_gold_province_dashboard` (recommended for main dashboard)
   - `v_gold_poverty_insights` (for KPI metrics)
   - `v_gold_expenditure_insights` (for expenditure analysis)

### Step 3: Recommended Chart Types

#### A. Province Performance Dashboard (v_gold_province_dashboard)
- **Bar Chart**: Poverty rate by province
- **Scatter Plot**: Population vs Poverty Rate
- **Heat Map**: Infrastructure scores by province
- **Pie Chart**: Province classification distribution

#### B. KPI Metrics (v_gold_poverty_insights) 
- **Big Number**: Total provinces, Average poverty rate
- **Gauge**: Infrastructure access percentage
- **Table**: All key metrics summary

#### C. Expenditure Analysis (v_gold_expenditure_insights)
- **Bar Chart**: Consumption by expenditure group
- **Box Plot**: Poverty distribution by consumption category
- **Treemap**: Population by expenditure group

## 🎨 SAMPLE QUERIES FOR VERIFICATION

```sql
-- Verify Gold province data
SELECT * FROM v_gold_province_dashboard 
ORDER BY avg_poverty_rate DESC;

-- Check KPI metrics
SELECT * FROM v_gold_poverty_insights;

-- Expenditure insights
SELECT expenditure_group_clean, AVG(avg_poverty_rate) as avg_poverty
FROM v_gold_expenditure_insights 
GROUP BY expenditure_group_clean 
ORDER BY avg_poverty DESC;
```

## 🔄 DATA LINEAGE

```
CSV Source → Bronze Layer (HDFS) → Silver Layer (Spark) → Gold Layer (Hive) → PostgreSQL → Superset
```

✅ **Your dashboard now uses CLEAN, PROCESSED data from the Gold layer!**

## 🏆 ADVANTAGES OF GOLD LAYER DATA:

1. **Pre-aggregated** - Faster dashboard performance
2. **Cleaned & Validated** - No missing values or duplicates  
3. **Business Logic Applied** - Classification and scoring
4. **Optimized for Analytics** - Structured for insights
5. **Consistent Calculations** - Standardized metrics

---
**🎉 Happy Dashboard Building with Clean Gold Data!**
**Kelompok 18 - Big Data Medallion Architecture Success!**
"""
        
        with open('c:/TUBESABD/SUPERSET_GOLD_LAYER_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        logger.info("📖 Created Superset Gold Layer integration guide")
    
    def run_integration(self):
        """Run the complete Gold layer integration"""
        self.print_header()
        
        try:
            # Step 1: Check Hive tables
            tables = self.check_hive_tables()
            if not tables:
                logger.error("❌ No Gold layer tables found. Run ETL pipeline first!")
                return False
            
            # Step 2: Create PostgreSQL tables
            if not self.create_gold_tables_in_postgres():
                return False
            
            # Step 3: Load Gold data
            if not self.load_gold_data_to_postgres():
                return False
            
            # Step 4: Create views
            if not self.create_gold_views():
                return False
            
            # Step 5: Verify data
            if not self.verify_gold_data():
                return False
            
            # Step 6: Create guide
            self.create_superset_guide()
            
            print("\n" + "="*70)
            print("🎉 GOLD LAYER INTEGRATION COMPLETED SUCCESSFULLY!")
            print("📊 Clean, processed data now available in Superset")
            print("🔗 Connection: postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping")
            print("📖 Guide: SUPERSET_GOLD_LAYER_GUIDE.md")
            print("🚀 Next: Create Superset datasets from Gold tables/views")
            print("="*70)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Integration failed: {e}")
            return False

def main():
    integrator = GoldLayerIntegrator()
    success = integrator.run_integration()
    
    if success:
        print("\n🎯 QUICK ACTIONS:")
        print("1. Open Superset: http://localhost:8089")
        print("2. Create datasets from Gold views: v_gold_province_dashboard")
        print("3. Build dashboards with clean, aggregated data!")
    else:
        print("\n❌ Integration failed. Check logs above.")

if __name__ == "__main__":
    main()
