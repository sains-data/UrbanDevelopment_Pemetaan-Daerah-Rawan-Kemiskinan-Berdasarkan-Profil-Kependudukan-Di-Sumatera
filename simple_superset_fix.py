#!/usr/bin/env python3
"""
Simple Superset Dataset Fix
Kelompok 18 - Test Connection and Create Dataset
"""

import psycopg2
import time
import subprocess

def test_postgres_connection():
    """Test PostgreSQL connection directly"""
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
        cursor.execute("SELECT COUNT(*) FROM poverty_data;")
        count = cursor.fetchone()[0]
        
        print(f"✅ PostgreSQL connection successful!")
        print(f"📊 Found {count:,} records in poverty_data table")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def check_superset_status():
    """Check if Superset is running"""
    print("🔍 Checking Superset status...")
    
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=superset", "--format", "{{.Status}}"],
            capture_output=True,
            text=True
        )
        
        if "Up" in result.stdout:
            print("✅ Superset container is running")
            return True
        else:
            print("❌ Superset container is not running")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Superset: {e}")
        return False

def restart_superset():
    """Restart Superset container"""
    print("🔄 Restarting Superset container...")
    
    try:
        # Stop superset
        subprocess.run(["docker", "stop", "superset"], check=True)
        time.sleep(5)
        
        # Start superset
        subprocess.run(["docker", "start", "superset"], check=True)
        print("✅ Superset restarted successfully")
        
        # Wait for it to be ready
        print("⏳ Waiting for Superset to be ready...")
        time.sleep(30)
        
        return True
        
    except Exception as e:
        print(f"❌ Error restarting Superset: {e}")
        return False

def main():
    """Main troubleshooting function"""
    print("🚀 Superset Dataset Troubleshooting")
    print("=" * 50)
    
    # Test 1: PostgreSQL Connection
    if not test_postgres_connection():
        print("💡 Fix PostgreSQL connection first")
        return False
    
    # Test 2: Superset Status
    if not check_superset_status():
        print("💡 Starting Superset...")
        subprocess.run(["docker", "start", "superset"])
        time.sleep(30)
    
    # Test 3: Try restarting Superset
    print("\n🔄 Restarting Superset to clear any cache issues...")
    if restart_superset():
        print("\n✅ Troubleshooting completed!")
        print("\n📋 NEXT STEPS:")
        print("1. Go to http://localhost:8089")
        print("2. Login with admin/admin") 
        print("3. Go to Settings > Database Connections")
        print("4. Edit PostgreSQL connection and test it")
        print("5. Go to Data > Datasets > + Dataset")
        print("6. Select: Database=PostgreSQL, Schema=public, Table=poverty_data")
        print("7. Click 'Create Dataset and Explore'")
        
        print("\n🔧 DATABASE CONNECTION DETAILS:")
        print("Host: postgres-local")
        print("Port: 5432") 
        print("Database: poverty_mapping")
        print("Username: postgres")
        print("Password: postgres123")
        
        return True
    else:
        print("❌ Failed to restart Superset")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Ready to create dataset manually in Superset UI!")
    else:
        print("\n❌ Please check the issues above and try again")
