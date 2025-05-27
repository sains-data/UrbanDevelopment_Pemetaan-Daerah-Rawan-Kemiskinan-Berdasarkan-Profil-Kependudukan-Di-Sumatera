#!/usr/bin/env python3
"""
Quick Real Data Status Check
Kelompok 18 - Sumatra Poverty Data Verification
"""

import psycopg2
from datetime import datetime

def quick_verify():
    try:
        # Connect to database
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='poverty_mapping',
            user='postgres',
            password='postgres123'
        )
        cursor = conn.cursor()
        
        print("🎯 REAL DATA STATUS CHECK")
        print("=" * 50)
        
        # Quick count
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        total = cursor.fetchone()[0]
        print(f"✅ Total Records: {total:,}")
        
        # Province distribution
        cursor.execute("SELECT province, COUNT(*) FROM poverty_data GROUP BY province;")
        provinces = cursor.fetchall()
        print(f"✅ Province Distribution:")
        for prov, count in provinces:
            print(f"   {prov}: {count:,} records")
        
        # Sample check
        cursor.execute("SELECT commodity FROM poverty_data WHERE commodity IS NOT NULL LIMIT 1;")
        sample = cursor.fetchone()
        if sample and 'Jagung' in sample[0]:
            print(f"✅ Real Data Confirmed: {sample[0]}")
        
        cursor.close()
        conn.close()
        
        print("=" * 50)
        if total >= 20000:
            print("🎉 SUCCESS: Real poverty data loaded!")
            print("🚀 Ready for Superset dashboard creation")
            print("📊 Access Superset: http://localhost:8089")
        else:
            print("⚠️  Warning: Expected 20,000+ records")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    quick_verify()
