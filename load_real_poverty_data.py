#!/usr/bin/env python3
"""
Load Real Poverty Data from CSV to PostgreSQL
Kelompok 18 - Big Data Poverty Mapping Pipeline
Using actual Profil_Kemiskinan_Sumatera.csv data
"""

import pandas as pd
import psycopg2
import numpy as np
from sqlalchemy import create_engine
import sys

def print_header():
    print("=" * 60)
    print("📊 LOADING REAL POVERTY DATA TO POSTGRESQL")
    print("📈 Kelompok 18 - Big Data Pipeline")
    print("📋 Source: Profil_Kemiskinan_Sumatera.csv")
    print("=" * 60)

def load_csv_data():
    """Load and preview the CSV data"""
    print("\n📂 Loading CSV data...")
    
    try:
        df = pd.read_csv('c:/TUBESABD/data/Profil_Kemiskinan_Sumatera.csv')
        print(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
        
        # Show basic info
        print(f"\n📊 Data Overview:")
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Provinces: {df['Provinsi'].unique()}")
        print(f"   Province counts:")
        for province, count in df['Provinsi'].value_counts().items():
            print(f"     - {province}: {count:,} records")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None

def clean_data(df):
    """Clean and prepare the data"""
    print("\n🧹 Cleaning data...")
    
    # Create a copy
    df_clean = df.copy()
    
    # Add unique IDs and location data
    df_clean['id'] = range(1, len(df_clean) + 1)
    
    # Add dummy coordinates for mapping (realistic for Sumatra)
    np.random.seed(42)  # For reproducible results
    
    # Sumatra coordinate ranges
    sumatra_coords = {
        'Sumatera Barat': {'lat_range': (-3.0, 1.0), 'lon_range': (99.0, 102.0)},
        'Sumatera Selatan': {'lat_range': (-5.0, -1.0), 'lon_range': (102.0, 106.0)},
        'Sumatera Utara': {'lat_range': (1.0, 4.0), 'lon_range': (97.0, 100.0)}
    }
    
    latitudes = []
    longitudes = []
    
    for _, row in df_clean.iterrows():
        province = row['Provinsi']
        if province in sumatra_coords:
            lat_min, lat_max = sumatra_coords[province]['lat_range']
            lon_min, lon_max = sumatra_coords[province]['lon_range']
            
            lat = np.random.uniform(lat_min, lat_max)
            lon = np.random.uniform(lon_min, lon_max)
            
            latitudes.append(round(lat, 6))
            longitudes.append(round(lon, 6))
        else:
            latitudes.append(0.0)
            longitudes.append(0.0)
    
    df_clean['latitude'] = latitudes
    df_clean['longitude'] = longitudes
    
    # Add dummy regency/district/village based on row number
    df_clean['regency'] = df_clean['Provinsi'] + ' Regency ' + (df_clean.index % 10 + 1).astype(str)
    df_clean['district'] = df_clean['Provinsi'] + ' District ' + (df_clean.index % 5 + 1).astype(str)
    df_clean['village'] = df_clean['Provinsi'] + ' Village ' + (df_clean.index % 3 + 1).astype(str)
    
    print(f"✅ Data cleaned: {len(df_clean)} rows ready")
    return df_clean

def connect_to_postgres():
    """Connect to PostgreSQL database"""
    print("\n🔌 Connecting to PostgreSQL...")
    
    try:
        # Connection parameters
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'poverty_mapping',
            'user': 'postgres',
            'password': 'postgres123'
        }
        
        # Create connection
        conn = psycopg2.connect(**conn_params)
        engine = create_engine(f"postgresql://postgres:postgres123@localhost:5432/poverty_mapping")
        
        print("✅ Connected to PostgreSQL successfully")
        return conn, engine
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None, None

def create_tables(conn):
    """Create tables for poverty data"""
    print("\n🗄️ Creating database tables...")
    
    try:
        cursor = conn.cursor()
        
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS poverty_data CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS province_summary CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS regency_summary CASCADE;")
        cursor.execute("DROP VIEW IF EXISTS v_poverty_hotspots CASCADE;")
        cursor.execute("DROP VIEW IF EXISTS v_poverty_by_province CASCADE;")
        
        # Create main poverty_data table
        create_table_sql = """
        CREATE TABLE poverty_data (
            id SERIAL PRIMARY KEY,
            province VARCHAR(100),
            regency VARCHAR(100),
            district VARCHAR(100),
            village VARCHAR(100),
            poverty_percentage DECIMAL(5,2),
            population INTEGER,
            unemployment_rate DECIMAL(5,2),
            consumption_per_capita DECIMAL(10,2),
            education_access VARCHAR(50),
            health_facility VARCHAR(50),
            water_access VARCHAR(20),
            poverty_category VARCHAR(20),
            commodity VARCHAR(100),
            expenditure_group VARCHAR(100),
            latitude DECIMAL(10,6),
            longitude DECIMAL(10,6),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        
        print("✅ Tables created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_data(df, engine):
    """Insert data into PostgreSQL"""
    print(f"\n📥 Inserting {len(df)} records into PostgreSQL...")
    
    try:
        # Map CSV columns to database columns
        df_mapped = pd.DataFrame({
            'province': df['Provinsi'],
            'regency': df['regency'],
            'district': df['district'],
            'village': df['village'],
            'poverty_percentage': df['Persentase Kemiskinan (%)'],
            'population': df['Jumlah Penduduk (jiwa)'],
            'unemployment_rate': df['Tingkat Pengangguran (%)'],
            'consumption_per_capita': df['Konsumsi (per kapita per minggu)'],
            'education_access': df['Akses Pendidikan'],
            'health_facility': df['Fasilitas Kesehatan'],
            'water_access': df['Akses Air Bersih'],
            'poverty_category': df['Kategori Kemiskinan'],
            'commodity': df['Komoditas'],
            'expenditure_group': df['Golongan Pengeluaran'],
            'latitude': df['latitude'],
            'longitude': df['longitude']
        })
        
        # Insert data in chunks for better performance
        chunk_size = 1000
        total_chunks = len(df_mapped) // chunk_size + 1
        
        for i in range(0, len(df_mapped), chunk_size):
            chunk = df_mapped.iloc[i:i+chunk_size]
            chunk.to_sql('poverty_data', engine, if_exists='append', index=False)
            
            chunk_num = i // chunk_size + 1
            print(f"   Inserted chunk {chunk_num}/{total_chunks} ({len(chunk)} records)")
        
        print(f"✅ All {len(df_mapped)} records inserted successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False

def create_summary_tables(conn):
    """Create summary tables and views"""
    print("\n📊 Creating summary tables and views...")
    
    try:
        cursor = conn.cursor()
        
        # Province summary
        cursor.execute("""
        CREATE TABLE province_summary AS
        SELECT 
            province,
            COUNT(*) as total_areas,
            ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
            ROUND(MIN(poverty_percentage), 2) as min_poverty_rate,
            ROUND(MAX(poverty_percentage), 2) as max_poverty_rate,
            ROUND(AVG(unemployment_rate), 2) as avg_unemployment_rate,
            SUM(population) as total_population
        FROM poverty_data 
        GROUP BY province;
        """)
        
        # Regency summary
        cursor.execute("""
        CREATE TABLE regency_summary AS
        SELECT 
            province,
            regency,
            COUNT(*) as total_villages,
            ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
            ROUND(AVG(unemployment_rate), 2) as avg_unemployment_rate,
            SUM(population) as total_population
        FROM poverty_data 
        GROUP BY province, regency;
        """)
        
        # Poverty hotspots view (areas with poverty > 20%)
        cursor.execute("""
        CREATE VIEW v_poverty_hotspots AS
        SELECT *
        FROM poverty_data
        WHERE poverty_percentage > 20.0
        ORDER BY poverty_percentage DESC;
        """)
        
        # Province comparison view
        cursor.execute("""
        CREATE VIEW v_poverty_by_province AS
        SELECT 
            province,
            ROUND(AVG(poverty_percentage), 2) as avg_poverty,
            COUNT(*) as total_records,
            ROUND(AVG(unemployment_rate), 2) as avg_unemployment
        FROM poverty_data
        GROUP BY province
        ORDER BY avg_poverty DESC;
        """)
        
        conn.commit()
        print("✅ Summary tables and views created")
        return True
        
    except Exception as e:
        print(f"❌ Error creating summaries: {e}")
        return False

def verify_data(conn):
    """Verify the loaded data"""
    print("\n🔍 Verifying loaded data...")
    
    try:
        cursor = conn.cursor()
        
        # Total records
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        total_records = cursor.fetchone()[0]
        print(f"   Total records: {total_records:,}")
        
        # Province counts
        cursor.execute("""
        SELECT province, COUNT(*) as count 
        FROM poverty_data 
        GROUP BY province 
        ORDER BY count DESC;
        """)
        
        print("   Records per province:")
        for province, count in cursor.fetchall():
            print(f"     - {province}: {count:,}")
        
        # Sample data
        cursor.execute("""
        SELECT province, regency, poverty_percentage, population 
        FROM poverty_data 
        ORDER BY poverty_percentage DESC 
        LIMIT 5;
        """)
        
        print("   Top 5 highest poverty areas:")
        for row in cursor.fetchall():
            print(f"     - {row[0]}, {row[1]}: {row[2]}% poverty, {row[3]:,} population")
        
        # Summary statistics
        cursor.execute("SELECT * FROM province_summary ORDER BY avg_poverty_rate DESC;")
        print("   Province summaries:")
        for row in cursor.fetchall():
            print(f"     - {row[0]}: {row[2]}% avg poverty, {row[1]:,} areas")
        
        print("✅ Data verification completed")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main execution function"""
    print_header()
    
    # Load CSV data
    df = load_csv_data()
    if df is None:
        sys.exit(1)
    
    # Clean data
    df_clean = clean_data(df)
    
    # Connect to PostgreSQL
    conn, engine = connect_to_postgres()
    if conn is None:
        sys.exit(1)
    
    try:
        # Create tables
        if not create_tables(conn):
            sys.exit(1)
        
        # Insert data
        if not insert_data(df_clean, engine):
            sys.exit(1)
        
        # Create summaries
        if not create_summary_tables(conn):
            sys.exit(1)
        
        # Verify data
        if not verify_data(conn):
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("🎉 DATA LOADING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📊 Loaded: {len(df_clean):,} poverty records")
        print("📍 Provinces: Sumatera Barat, Sumatera Selatan, Sumatera Utara")
        print("🗄️ Tables: poverty_data, province_summary, regency_summary")
        print("👁️ Views: v_poverty_hotspots, v_poverty_by_province")
        print("\n🚀 Ready for Superset dashboard creation!")
        print("🔗 Use connection: postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping")
        
    finally:
        conn.close()
        engine.dispose()

if __name__ == "__main__":
    main()
