#!/usr/bin/env python3
"""
Superset Dataset Creation Troubleshooter
Kelompok 18 - Big Data Poverty Mapping

This script diagnoses and fixes common issues with Superset dataset creation
"""

import os
import sys
import time
import requests
import psycopg2
import subprocess
from datetime import datetime

def check_containers():
    """Check if required containers are running"""
    print("🔍 Checking Container Status...")
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            containers = {}
            for line in lines[1:]:  # Skip header
                if '\t' in line:
                    name, status = line.split('\t', 1)
                    containers[name.strip()] = status.strip()
            
            postgres_running = any('postgres' in name.lower() for name in containers.keys())
            superset_running = any('superset' in name.lower() for name in containers.keys())
            
            print(f"✅ PostgreSQL Container: {'Running' if postgres_running else 'Not Found'}")
            print(f"✅ Superset Container: {'Running' if superset_running else 'Not Found'}")
            
            return postgres_running and superset_running
        else:
            print("❌ Failed to check container status")
            return False
    except Exception as e:
        print(f"❌ Error checking containers: {e}")
        return False

def test_postgres_connection():
    """Test PostgreSQL connection and data"""
    print("\n🔍 Testing PostgreSQL Connection...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='poverty_mapping',
            user='postgres',
            password='postgres123'
        )
        cursor = conn.cursor()
        
        # Test basic connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL Connected: {version[:50]}...")
        
        # Check poverty_data table
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        count = cursor.fetchone()[0]
        print(f"✅ poverty_data table: {count:,} records")
        
        # Check table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'poverty_data' 
            ORDER BY ordinal_position 
            LIMIT 5;
        """)
        columns = cursor.fetchall()
        print(f"✅ Table structure: {len(columns)} columns (showing first 5):")
        for col, dtype in columns:
            print(f"   - {col}: {dtype}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL Connection Failed: {e}")
        return False

def test_superset_connection():
    """Test Superset web interface"""
    print("\n🔍 Testing Superset Connection...")
    try:
        response = requests.get('http://localhost:8089/health', timeout=10)
        if response.status_code == 200:
            print("✅ Superset Web Interface: Accessible")
            return True
        else:
            print(f"❌ Superset returned status: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ Superset Web Interface: Not accessible")
        return False
    except Exception as e:
        print(f"❌ Superset test failed: {e}")
        return False

def create_dataset_fix_script():
    """Create a script to fix dataset creation issues"""
    fix_script = """
# SUPERSET DATASET CREATION - TROUBLESHOOTING GUIDE

## COMMON ISSUES & SOLUTIONS

### Issue 1: "Dataset could not be created"
**Causes:**
- Database connection not properly configured
- Table permissions issues
- Superset cache problems
- Network connectivity issues

**Solutions:**

### 1. Verify Database Connection in Superset
```
Settings → Database Connections → Test Connection
```
Use these EXACT details:
```
Database: PostgreSQL
Host: postgres-local
Port: 5432
Database name: poverty_mapping
Username: postgres
Password: postgres123
```

### 2. Alternative Connection Methods

#### Method A: Use SQLAlchemy URI
```
postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping
```

#### Method B: Use localhost (if container method fails)
```
Host: localhost
Port: 5432
Database name: poverty_mapping
Username: postgres
Password: postgres123
```

### 3. Manual Dataset Creation Steps

1. **First, test in SQL Lab:**
   ```sql
   SELECT COUNT(*) FROM poverty_data;
   SELECT * FROM poverty_data LIMIT 5;
   ```

2. **If SQL Lab works, create dataset:**
   - Datasets → + Dataset
   - Choose your database connection
   - Schema: public
   - Table: poverty_data

3. **If dataset creation still fails:**
   - Clear browser cache
   - Refresh Superset metadata
   - Restart Superset container

### 4. Container-specific fixes
```bash
# Restart containers
docker-compose restart superset postgres

# Check logs
docker logs superset
docker logs postgres-local

# Rebuild if needed
docker-compose down
docker-compose up -d postgres superset
```

### 5. Permission fixes
```sql
-- Connect to PostgreSQL and run:
GRANT ALL PRIVILEGES ON TABLE poverty_data TO postgres;
GRANT USAGE ON SCHEMA public TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO postgres;
```

## VERIFICATION CHECKLIST
- [ ] Containers running (postgres-local, superset)
- [ ] PostgreSQL accessible on port 5432
- [ ] Superset accessible on port 8089
- [ ] Database connection test succeeds in Superset
- [ ] SQL Lab can query poverty_data table
- [ ] Dataset creation completes successfully

## STEP-BY-STEP DATASET CREATION

1. Open Superset: http://localhost:8089
2. Login: admin/admin
3. Settings → Database Connections
4. Test existing connection or create new one
5. SQL Lab → Test query: `SELECT * FROM poverty_data LIMIT 10;`
6. Datasets → + Dataset → Select database → public schema → poverty_data table
7. Save dataset with name: "Poverty Data Sumatra"

If you still get errors, check the specific error message in Superset logs.
"""
    
    with open("SUPERSET_DATASET_FIX_GUIDE.md", "w", encoding='utf-8') as f:
        f.write(fix_script)
    
    print("✅ Created: SUPERSET_DATASET_FIX_GUIDE.md")

def run_container_restart():
    """Restart containers to fix connection issues"""
    print("\n🔄 Restarting Containers...")
    try:
        # Restart containers
        subprocess.run(['docker-compose', 'restart', 'superset', 'postgres'], 
                      shell=True, check=True)
        print("✅ Containers restarted")
        
        # Wait for services to be ready
        print("⏳ Waiting for services to be ready...")
        time.sleep(30)
        
        return True
    except Exception as e:
        print(f"❌ Failed to restart containers: {e}")
        return False

def main():
    """Main troubleshooting function"""
    print("=" * 70)
    print("🔧 SUPERSET DATASET CREATION TROUBLESHOOTER")
    print("   Kelompok 18 - Poverty Data Analysis")
    print("=" * 70)
    
    # Step 1: Check containers
    containers_ok = check_containers()
    
    # Step 2: Test PostgreSQL
    postgres_ok = test_postgres_connection()
    
    # Step 3: Test Superset
    superset_ok = test_superset_connection()
    
    # Step 4: Create fix guide
    create_dataset_fix_script()
    
    # Step 5: Provide diagnosis
    print("\n" + "=" * 70)
    print("📋 DIAGNOSIS SUMMARY")
    print("=" * 70)
    
    if containers_ok and postgres_ok and superset_ok:
        print("✅ All services are working properly!")
        print("\n🎯 LIKELY CAUSES OF DATASET CREATION ERROR:")
        print("1. Browser cache issues - Clear cache and retry")
        print("2. Database connection configuration in Superset")
        print("3. Network timing issues - Wait and retry")
        print("\n📖 Follow SUPERSET_DATASET_FIX_GUIDE.md for detailed solutions")
    else:
        print("❌ Found issues with infrastructure:")
        if not containers_ok:
            print("   - Container issues detected")
        if not postgres_ok:
            print("   - PostgreSQL connection problems")
        if not superset_ok:
            print("   - Superset accessibility issues")
        
        print("\n🔄 Recommended Action: Restart containers")
        restart = input("Restart containers now? (y/n): ").lower().strip()
        if restart == 'y':
            run_container_restart()
    
    print("\n🚀 NEXT STEPS:")
    print("1. Open Superset: http://localhost:8089")
    print("2. Follow SUPERSET_DATASET_FIX_GUIDE.md")
    print("3. Try dataset creation again")
    print("4. If still failing, check Superset error logs")

if __name__ == "__main__":
    main()
"""
