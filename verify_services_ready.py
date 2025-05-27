#!/usr/bin/env python3
"""
Quick verification script to ensure all services are ready for dataset creation
"""

import requests
import psycopg2
import time
import sys

def check_superset():
    """Check if Superset is accessible"""
    try:
        response = requests.get('http://localhost:8089', timeout=10)
        if response.status_code == 200:
            print("✅ Superset is accessible at http://localhost:8089")
            return True
        else:
            print(f"❌ Superset returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access Superset: {e}")
        return False

def check_postgresql():
    """Check if PostgreSQL is accessible and has data"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='poverty_mapping',
            user='postgres',
            password='postgres123'
        )
        cursor = conn.cursor()
        
        # Check poverty_data table
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        count_data = cursor.fetchone()[0]
        print(f"✅ poverty_data table has {count_data:,} records")
        
        # Check poverty_clean view
        cursor.execute("SELECT COUNT(*) FROM poverty_clean;")
        count_clean = cursor.fetchone()[0]
        print(f"✅ poverty_clean view has {count_clean:,} records")
        
        # Sample data from clean view
        cursor.execute("SELECT province, regency, district, village, poverty_rate FROM poverty_clean LIMIT 3;")
        samples = cursor.fetchall()
        print("✅ Sample data from poverty_clean:")
        for sample in samples:
            print(f"   {sample[0]}, {sample[1]}, {sample[2]}, {sample[3]}, {sample[4]}%")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def main():
    print("🔍 Verifying services for Superset dataset creation...")
    print("=" * 60)
    
    superset_ok = check_superset()
    postgresql_ok = check_postgresql()
    
    print("=" * 60)
    
    if superset_ok and postgresql_ok:
        print("🎉 All services are ready!")
        print("\n📋 Next steps:")
        print("1. Open http://localhost:8089 in your browser")
        print("2. Login with admin/admin")
        print("3. Follow the MANUAL_DATASET_CREATION_GUIDE.md")
        print("4. Use 'poverty_clean' view for dataset creation")
        print("\n💡 Connection details:")
        print("   Host: postgres-local (or localhost)")
        print("   Port: 5432")
        print("   Database: poverty_mapping")
        print("   Username: postgres")
        print("   Password: postgres123")
    else:
        print("❌ Some services are not ready. Please check Docker containers.")
        print("   Run: docker ps | findstr 'superset\\|postgres'")
    
    return 0 if (superset_ok and postgresql_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
