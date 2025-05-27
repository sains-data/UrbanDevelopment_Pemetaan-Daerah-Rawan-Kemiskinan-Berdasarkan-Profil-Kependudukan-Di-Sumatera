import sqlite3
import os

print("🔍 SUPERSET DATABASE VERIFICATION")
print("=" * 50)

# Check database
db_path = 'superset_data/poverty_mapping.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"✅ Database found: {os.path.abspath(db_path)}")
    print(f"📊 File size: {os.path.getsize(db_path):,} bytes")
    print(f"📋 Tables: {len(tables)}")
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"   • {table[0]}: {count:,} records")
    
    print(f"\n📊 Sample data from poverty_data:")
    cursor.execute("SELECT Provinsi, Kabupaten_Kota, Poverty_Rate FROM poverty_data LIMIT 5")
    for row in cursor.fetchall():
        print(f"   {row[0]} - {row[1]}: {row[2]}%")
    
    conn.close()
    
    print(f"\n🔗 Access Information:")
    print(f"   Superset URL: http://localhost:8089")
    print(f"   Username: admin")
    print(f"   Password: admin")
    print(f"   Database URI: sqlite:///{os.path.abspath(db_path).replace(chr(92), '/')}")
    
else:
    print("❌ Database not found!")
