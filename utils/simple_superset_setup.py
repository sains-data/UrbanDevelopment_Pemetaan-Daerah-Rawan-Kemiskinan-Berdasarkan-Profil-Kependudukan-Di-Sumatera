"""
Simple Superset Dashboard Setup
Kelompok 18 - Pemetaan Kemiskinan Sumatera
"""

import os
import csv
import sqlite3
from datetime import datetime

print("🎨 SUPERSET DASHBOARD SETUP - SIMPLE VERSION")
print("=" * 60)

# Create directory for Superset data
os.makedirs('superset_data', exist_ok=True)

# Read CSV and create SQLite database
def setup_database():
    try:
        # Connect to SQLite database
        db_path = 'superset_data/poverty_mapping.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create main table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS poverty_data (
                id INTEGER PRIMARY KEY,
                Provinsi TEXT,
                Komoditas TEXT,
                Persentase_Kemiskinan_Pct REAL,
                Tingkat_Pengangguran_Pct REAL,
                Jumlah_Penduduk_jiwa INTEGER,
                Poverty_Category TEXT,
                Economic_Health_Score REAL,
                Year INTEGER
            )
        ''')
        
        # Read and insert data
        with open('data/Profil_Kemiskinan_Sumatera.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            records_inserted = 0
            
            for row in csv_reader:
                try:
                    poverty_rate = float(row['Persentase Kemiskinan (%)'])
                    unemployment_rate = float(row['Tingkat Pengangguran (%)'])
                    population = int(row['Jumlah Penduduk (jiwa)'])
                    
                    # Calculate derived fields
                    if poverty_rate <= 5:
                        category = 'Rendah'
                    elif poverty_rate <= 10:
                        category = 'Sedang'
                    elif poverty_rate <= 15:
                        category = 'Tinggi'
                    else:
                        category = 'Sangat Tinggi'
                    
                    economic_health = 100 - poverty_rate - unemployment_rate
                    
                    cursor.execute('''
                        INSERT INTO poverty_data 
                        (Provinsi, Komoditas, Persentase_Kemiskinan_Pct, 
                         Tingkat_Pengangguran_Pct, Jumlah_Penduduk_jiwa,
                         Poverty_Category, Economic_Health_Score, Year)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (row['Provinsi'], row['Komoditas'], poverty_rate,
                          unemployment_rate, population, category, economic_health, 2025))
                    
                    records_inserted += 1
                    
                except (ValueError, KeyError) as e:
                    continue
        
        # Create summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS province_summary AS
            SELECT 
                Provinsi,
                COUNT(*) as Total_Areas,
                AVG(Persentase_Kemiskinan_Pct) as Avg_Poverty_Rate,
                MIN(Persentase_Kemiskinan_Pct) as Min_Poverty_Rate,
                MAX(Persentase_Kemiskinan_Pct) as Max_Poverty_Rate,
                AVG(Tingkat_Pengangguran_Pct) as Avg_Unemployment_Rate,
                SUM(Jumlah_Penduduk_jiwa) as Total_Population,
                AVG(Economic_Health_Score) as Avg_Economic_Health_Score
            FROM poverty_data
            GROUP BY Provinsi
        ''')
        
        # Create poverty distribution table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS poverty_distribution AS
            SELECT 
                Poverty_Category as Category,
                COUNT(*) as Count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM poverty_data), 1) as Percentage
            FROM poverty_data
            GROUP BY Poverty_Category
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database created successfully: {db_path}")
        print(f"✅ Records inserted: {records_inserted}")
        return db_path
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return None

# Create setup instructions
def create_instructions(db_path):
    abs_db_path = os.path.abspath(db_path)
    instructions = f"""# 🎨 SUPERSET DASHBOARD SETUP
## Kelompok 18 - Pemetaan Kemiskinan Sumatera

### 🚀 QUICK START
1. **Access Superset**: http://localhost:8089
2. **Login**: admin / admin
3. **Database Connection**: {abs_db_path}

### 📊 DASHBOARD CREATION GUIDE

#### STEP 1: Add Database Connection
1. Go to "Settings" → "Database Connections"
2. Click "+ DATABASE"
3. Select "SQLite"
4. Fill in:
   - Database Name: `poverty_mapping`
   - SQLAlchemy URI: `sqlite:///{abs_db_path}`
5. Click "CONNECT"

#### STEP 2: Create Dataset
1. Go to "Datasets" → "+" → "Add Dataset"
2. Select database: `poverty_mapping`
3. Select table: `poverty_data`
4. Click "CREATE DATASET AND CREATE CHART"

#### STEP 3: Create Charts

##### 📊 Chart 1: Provincial Poverty Rates
- Chart Type: Bar Chart
- Dataset: poverty_data
- X-axis: Provinsi
- Y-axis: AVG(Persentase_Kemiskinan_Pct)
- Title: "Average Poverty Rate by Province"

##### 🥧 Chart 2: Poverty Category Distribution  
- Chart Type: Pie Chart
- Dataset: poverty_distribution
- Dimension: Category
- Metric: Count
- Title: "Poverty Distribution Across Sumatra"

##### 📈 Chart 3: Unemployment vs Poverty
- Chart Type: Scatter Plot
- Dataset: poverty_data
- X-axis: Tingkat_Pengangguran_Pct
- Y-axis: Persentase_Kemiskinan_Pct
- Title: "Unemployment vs Poverty Correlation"

##### 📋 Chart 4: Province Summary Table
- Chart Type: Table
- Dataset: province_summary
- Columns: All
- Title: "Provincial Statistics Summary"

#### STEP 4: Create Dashboard
1. Go to "Dashboards" → "+"
2. Dashboard Name: "Pemetaan Kemiskinan Sumatera"
3. Add all created charts
4. Arrange and resize as needed
5. Add filters for Provinsi and Poverty_Category

### 🎯 AVAILABLE TABLES
- `poverty_data` - Main dataset with all poverty records
- `province_summary` - Aggregated statistics by province  
- `poverty_distribution` - Poverty category counts

### 🎨 RECOMMENDED VISUALIZATIONS
1. **Geographic Map** (if coordinates available)
2. **Time Series** (for trend analysis)
3. **Heat Map** (province vs metrics)
4. **Box Plot** (poverty distribution)
5. **Correlation Matrix** (economic indicators)

### 📊 KEY METRICS TO TRACK
- Average poverty rate per province
- Unemployment correlation with poverty
- Population impact on economic health
- Best and worst performing areas

---
**Database**: {abs_db_path}
**Superset URL**: http://localhost:8089
**Setup Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open('superset_data/dashboard_instructions.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ Instructions saved: superset_data/dashboard_instructions.md")

# Main execution
db_path = setup_database()
if db_path:
    create_instructions(db_path)
    print(f"\n🎉 SETUP COMPLETED!")
    print(f"🔗 Access Superset: http://localhost:8089")
    print(f"📖 Read instructions: superset_data/dashboard_instructions.md")
else:
    print(f"❌ Setup failed!")
