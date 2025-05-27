#!/usr/bin/env python3
import psycopg2
import pandas as pd

def check_postgresql_data():
    """Check PostgreSQL data status"""
    try:
        # Connection details
        conn = psycopg2.connect(
            host="localhost",
            port=5433,  # External port from docker-compose
            database="poverty_mapping", 
            user="postgres",
            password="postgres123"
        )
        
        cursor = conn.cursor()
        
        # Check poverty_data table
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        poverty_data_count = cursor.fetchone()[0]
        print(f"✅ poverty_data table: {poverty_data_count:,} records")
        
        # Check poverty_clean view
        cursor.execute("SELECT COUNT(*) FROM poverty_clean;")
        poverty_clean_count = cursor.fetchone()[0] 
        print(f"✅ poverty_clean view: {poverty_clean_count:,} records")
        
        # Sample data from poverty_clean
        cursor.execute("""
            SELECT provinsi, kabupaten_kota, persentase_penduduk_miskin 
            FROM poverty_clean 
            ORDER BY persentase_penduduk_miskin DESC 
            LIMIT 5;
        """)
        sample_data = cursor.fetchall()
        
        print("\n📊 Top 5 highest poverty rates:")
        for row in sample_data:
            print(f"   {row[0]} - {row[1]}: {row[2]:.2f}%")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ PostgreSQL Status: READY")
        print(f"   - Total Records: {poverty_clean_count:,}")
        print(f"   - Connection: Host=localhost, Port=5433")
        print(f"   - Database: poverty_mapping")
        
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking Big Data Pipeline Status...")
    print("=" * 50)
    
    # Check PostgreSQL
    postgres_ok = check_postgresql_data()
    
    print("\n" + "=" * 50)
    if postgres_ok:
        print("🎯 READY FOR SUPERSET DATASET CREATION!")
        print("\nNext Steps:")
        print("1. Open Superset: http://localhost:8089")
        print("2. Login: admin / admin")
        print("3. Add PostgreSQL database connection")
        print("4. Create dataset from 'poverty_clean' view")
    else:
        print("❌ Pipeline not ready - please check services")
