#!/usr/bin/env python3
"""
Fresh Superset Dataset Creation - After Restart
Kelompok 18 - Poverty Mapping
"""

import time
import requests
import psycopg2
import json

def wait_for_superset():
    """Wait for Superset to be fully ready"""
    print("⏳ Menunggu Superset siap...")
    
    for i in range(10):
        try:
            response = requests.get("http://localhost:8089/health", timeout=5)
            if response.status_code == 200:
                print("✅ Superset ready!")
                return True
        except:
            pass
        
        print(f"   Percobaan {i+1}/10...")
        time.sleep(10)
    
    return False

def test_postgres_fresh():
    """Test PostgreSQL connection fresh"""
    print("🔍 Testing PostgreSQL connection...")
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            database="poverty_mapping",
            user="postgres",
            password="postgres123"
        )
        
        cursor = conn.cursor()
        
        # Check if data exists
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        count = cursor.fetchone()[0]
        print(f"✅ PostgreSQL OK: {count:,} records")
        
        # Check if view exists
        cursor.execute("SELECT COUNT(*) FROM poverty_summary;")
        view_count = cursor.fetchone()[0]
        print(f"✅ View OK: {view_count:,} records")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL error: {e}")
        return False

def create_fresh_view():
    """Create fresh view for dataset"""
    print("🔧 Creating fresh view...")
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="poverty_mapping",
            user="postgres", 
            password="postgres123"
        )
        
        cursor = conn.cursor()
        
        # Drop and recreate view
        cursor.execute("DROP VIEW IF EXISTS poverty_clean;")
        
        # Create new clean view
        create_view_sql = """
        CREATE VIEW poverty_clean AS
        SELECT 
            id,
            province,
            regency,
            district,
            village,
            poverty_percentage,
            population,
            unemployment_rate,
            consumption_per_capita,
            education_access,
            health_facility,
            water_access,
            poverty_category,
            commodity,
            expenditure_group,
            latitude,
            longitude,
            created_at
        FROM poverty_data
        WHERE poverty_percentage IS NOT NULL
        AND province IS NOT NULL
        ORDER BY province, poverty_percentage DESC;
        """
        
        cursor.execute(create_view_sql)
        conn.commit()
        
        # Test view
        cursor.execute("SELECT COUNT(*) FROM poverty_clean;")
        count = cursor.fetchone()[0]
        
        print(f"✅ Created poverty_clean view: {count:,} records")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ View creation error: {e}")
        return False

def open_superset():
    """Open Superset in browser"""
    import subprocess
    print("🌐 Opening Superset...")
    try:
        subprocess.run(["start", "http://localhost:8089"], shell=True)
        return True
    except:
        return False

def main():
    """Main refresh function"""
    print("🚀 FRESH SUPERSET DATASET CREATION")
    print("=" * 50)
    
    # Step 1: Wait for Superset
    if not wait_for_superset():
        print("❌ Superset tidak ready")
        return False
    
    # Step 2: Test PostgreSQL
    if not test_postgres_fresh():
        print("❌ PostgreSQL connection gagal")
        return False
    
    # Step 3: Create fresh view
    if not create_fresh_view():
        print("❌ View creation gagal")
        return False
    
    # Step 4: Open Superset
    open_superset()
    
    print("\n🎉 DATASET CREATION READY!")
    print("\n📋 MANUAL STEPS SEKARANG:")
    print("1. Login ke Superset: admin/admin")
    print("2. Settings → Database Connections")
    print("3. Edit PostgreSQL connection:")
    print("   Host: postgres-local")
    print("   Port: 5432")
    print("   Database: poverty_mapping")
    print("   Username: postgres")
    print("   Password: postgres123")
    print("4. Test Connection (harus ✅)")
    print("5. Data → Datasets → + Dataset")
    print("6. Database: PostgreSQL")
    print("7. Schema: public")
    print("8. Table: poverty_clean ← GUNAKAN INI!")
    print("9. Create Dataset and Explore")
    
    print("\n🔧 FRESH VIEW INFO:")
    print("- View name: poverty_clean")
    print("- Data: Clean, no NULL values")
    print("- Sorted by province and poverty %")
    print("- Ready for visualization")
    
    print("\n💡 TIPS:")
    print("- Gunakan 'poverty_clean' bukan 'poverty_data'")
    print("- Fresh restart menghilangkan cache error")
    print("- Jika masih error, coba browser incognito")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ SIAP UNTUK DATASET CREATION!")
    else:
        print("\n❌ ADA MASALAH - CHECK LOG DIATAS")
