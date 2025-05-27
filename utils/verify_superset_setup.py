"""
Database Verification and Quick Access
Kelompok 18 - Superset Dashboard Helper
"""

import sqlite3
import os
from datetime import datetime

print("🔍 VERIFIKASI DATABASE SUPERSET")
print("=" * 50)

# Check database file
db_path = 'superset_data/poverty_mapping.db'
abs_path = os.path.abspath(db_path)

if os.path.exists(db_path):
    print(f"✅ Database file found: {abs_path}")
    file_size = os.path.getsize(db_path)
    print(f"📊 File size: {file_size:,} bytes")
    
    # Connect and verify tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\n📋 AVAILABLE TABLES:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   • {table_name}: {count:,} records")
    
    # Show sample data from main table
    print(f"\n📊 SAMPLE DATA FROM poverty_data:")
    cursor.execute("SELECT * FROM poverty_data LIMIT 3")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute("PRAGMA table_info(poverty_data)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print("   Columns:", " | ".join(columns))
    for i, row in enumerate(rows):
        print(f"   Row {i+1}: {row}")
    
    # Show provincial summary
    print(f"\n🗺️ PROVINCIAL SUMMARY:")
    cursor.execute("""
        SELECT Provinsi, Total_Areas, Avg_Poverty_Rate, Avg_Unemployment_Rate 
        FROM province_summary 
        ORDER BY Avg_Poverty_Rate DESC
    """)
    
    summary_rows = cursor.fetchall()
    for row in summary_rows:
        print(f"   • {row[0]}: {row[2]}% poverty, {row[3]}% unemployment ({row[1]} areas)")
    
    conn.close()
    
else:
    print(f"❌ Database file not found: {abs_path}")
    print("   Run setup script first!")

print(f"\n🔗 QUICK ACCESS LINKS:")
print(f"   • Superset Dashboard: http://localhost:8089")
print(f"   • Jupyter Notebooks: http://localhost:8888")
print(f"   • Hadoop HDFS: http://localhost:9870")
print(f"   • Spark Master: http://localhost:8080")

print(f"\n📖 DOCUMENTATION:")
print(f"   • Dashboard Guide: superset_data/PANDUAN_DASHBOARD_LENGKAP.md")
print(f"   • Database Path: {abs_path}")

print(f"\n🎯 SUPERSET LOGIN:")
print(f"   • Username: admin")
print(f"   • Password: admin")
print(f"   • SQLAlchemy URI: sqlite:///{abs_path}")

print(f"\n" + "=" * 50)
print(f"🎨 Ready to create amazing dashboards!")
print(f"📅 Verification completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
