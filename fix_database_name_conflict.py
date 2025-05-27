#!/usr/bin/env python3
"""
Fix for 'Database with the same name already exists' error in Superset
This script provides multiple solutions to resolve the database connection issue.
"""

import requests
import json
import time

# Superset connection details
SUPERSET_URL = "http://localhost:8089"
USERNAME = "admin"
PASSWORD = "admin"

def get_auth_token():
    """Get authentication token from Superset"""
    login_url = f"{SUPERSET_URL}/api/v1/security/login"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "provider": "db",
        "refresh": True
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def list_existing_databases(token):
    """List all existing database connections"""
    headers = {"Authorization": f"Bearer {token}"}
    databases_url = f"{SUPERSET_URL}/api/v1/database/"
    
    try:
        response = requests.get(databases_url, headers=headers)
        if response.status_code == 200:
            databases = response.json().get("result", [])
            print("📋 Existing database connections:")
            for db in databases:
                print(f"   ID: {db['id']}, Name: '{db['database_name']}'")
            return databases
        else:
            print(f"❌ Failed to fetch databases: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error fetching databases: {e}")
        return []

def delete_database_connection(token, db_id, db_name):
    """Delete an existing database connection"""
    headers = {"Authorization": f"Bearer {token}"}
    delete_url = f"{SUPERSET_URL}/api/v1/database/{db_id}"
    
    try:
        response = requests.delete(delete_url, headers=headers)
        if response.status_code == 200:
            print(f"✅ Deleted database connection: {db_name}")
            return True
        else:
            print(f"❌ Failed to delete database {db_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting database: {e}")
        return False

def create_postgres_connection(token, db_name="poverty_mapping_db"):
    """Create a new PostgreSQL connection"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    database_data = {
        "database_name": db_name,
        "sqlalchemy_uri": "postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping",
        "expose_in_sqllab": True,
        "allow_ctas": True,
        "allow_cvas": True,
        "allow_dml": True,
        "configuration_method": "sqlalchemy_form",
        "engine": "postgresql"
    }
    
    create_url = f"{SUPERSET_URL}/api/v1/database/"
    
    try:
        response = requests.post(create_url, headers=headers, json=database_data)
        if response.status_code == 201:
            print(f"✅ Created database connection: {db_name}")
            return response.json()
        else:
            print(f"❌ Failed to create database: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return None

def main():
    print("🔧 Fixing 'Database with same name already exists' error")
    print("=" * 60)
    
    # Get authentication token
    print("1. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    print("✅ Authentication successful")
    
    # List existing databases
    print("\n2. Checking existing database connections...")
    existing_dbs = list_existing_databases(token)
    
    # Look for PostgreSQL connections
    postgres_dbs = [db for db in existing_dbs if 'postgres' in db['database_name'].lower() or 'poverty' in db['database_name'].lower()]
    
    if postgres_dbs:
        print(f"\n3. Found {len(postgres_dbs)} existing PostgreSQL connection(s):")
        for db in postgres_dbs:
            print(f"   - {db['database_name']} (ID: {db['id']})")
        
        # Ask user what to do
        print("\n🤔 Options to resolve the conflict:")
        print("   A) Delete existing connection and create new one")
        print("   B) Use existing connection (skip to dataset creation)")
        print("   C) Create new connection with different name")
        
        choice = input("\nEnter your choice (A/B/C): ").upper().strip()
        
        if choice == 'A':
            # Delete existing connections
            for db in postgres_dbs:
                delete_database_connection(token, db['id'], db['database_name'])
            
            # Create new connection
            print("\n4. Creating new PostgreSQL connection...")
            result = create_postgres_connection(token, "poverty_mapping_fresh")
            if result:
                print("✅ New database connection created successfully!")
        
        elif choice == 'B':
            print("✅ Using existing connection. You can proceed to dataset creation.")
            print("   Go to Datasets → + DATASET → Select existing PostgreSQL connection")
            
        elif choice == 'C':
            # Create with unique name
            unique_name = f"poverty_mapping_{int(time.time())}"
            print(f"\n4. Creating connection with unique name: {unique_name}")
            result = create_postgres_connection(token, unique_name)
            if result:
                print("✅ New database connection created with unique name!")
        
        else:
            print("❌ Invalid choice. Please run the script again.")
    
    else:
        # No existing PostgreSQL connections, create new one
        print("\n3. No existing PostgreSQL connections found.")
        print("4. Creating new PostgreSQL connection...")
        result = create_postgres_connection(token, "poverty_mapping_db")
        if result:
            print("✅ Database connection created successfully!")
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("1. Go to Superset UI: http://localhost:8089")
    print("2. Navigate to Datasets → + DATASET")
    print("3. Select your PostgreSQL connection")
    print("4. Choose 'poverty_clean' table/view")
    print("5. Click 'Create Dataset and Explore'")
    print("\n💡 If you still get errors, try using 'localhost' instead of 'postgres-local' as host")

if __name__ == "__main__":
    main()
