#!/usr/bin/env python3
"""
Fix Superset Dataset Creation Issue
Kelompok 18 - Poverty Mapping
"""

import requests
import json
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Superset configuration
SUPERSET_URL = "http://localhost:8089"
USERNAME = "admin"
PASSWORD = "admin"

def get_superset_session():
    """Get authenticated session with Superset"""
    session = requests.Session()
    
    # Get CSRF token
    csrf_url = f"{SUPERSET_URL}/api/v1/security/csrf_token/"
    csrf_response = session.get(csrf_url)
    csrf_token = csrf_response.json().get('result')
    
    # Login
    login_url = f"{SUPERSET_URL}/api/v1/security/login"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "provider": "db"
    }
    
    headers = {
        "X-CSRFToken": csrf_token,
        "Content-Type": "application/json"
    }
    
    login_response = session.post(login_url, json=login_data, headers=headers)
    
    if login_response.status_code != 200:
        raise Exception(f"Login failed: {login_response.text}")
    
    # Update session headers
    session.headers.update({
        "X-CSRFToken": csrf_token,
        "Authorization": f"Bearer {login_response.json().get('access_token')}"
    })
    
    return session

def check_database_connection(session):
    """Check if database connection exists"""
    logger.info("🔍 Checking database connections...")
    
    url = f"{SUPERSET_URL}/api/v1/database/"
    response = session.get(url)
    
    if response.status_code == 200:
        databases = response.json().get('result', [])
        for db in databases:
            if 'postgres' in db.get('database_name', '').lower():
                logger.info(f"✅ Found PostgreSQL database: {db['database_name']} (ID: {db['id']})")
                return db['id']
    
    logger.error("❌ No PostgreSQL database connection found")
    return None

def delete_existing_dataset(session, dataset_name="poverty_data"):
    """Delete existing dataset if it exists"""
    logger.info(f"🗑️ Checking for existing dataset: {dataset_name}")
    
    url = f"{SUPERSET_URL}/api/v1/dataset/"
    response = session.get(url)
    
    if response.status_code == 200:
        datasets = response.json().get('result', [])
        for dataset in datasets:
            if dataset.get('table_name') == dataset_name:
                dataset_id = dataset['id']
                logger.info(f"🗑️ Deleting existing dataset ID: {dataset_id}")
                
                delete_url = f"{SUPERSET_URL}/api/v1/dataset/{dataset_id}"
                delete_response = session.delete(delete_url)
                
                if delete_response.status_code == 200:
                    logger.info("✅ Existing dataset deleted successfully")
                else:
                    logger.warning(f"⚠️ Failed to delete dataset: {delete_response.text}")

def create_dataset(session, database_id, table_name="poverty_data"):
    """Create dataset in Superset"""
    logger.info(f"📊 Creating dataset for table: {table_name}")
    
    url = f"{SUPERSET_URL}/api/v1/dataset/"
    
    dataset_data = {
        "database": database_id,
        "table_name": table_name,
        "schema": "public",
        "always_filter_main_dttm": False,
        "external_url": None
    }
    
    response = session.post(url, json=dataset_data)
    
    if response.status_code == 201:
        dataset_id = response.json().get('id')
        logger.info(f"✅ Dataset created successfully! ID: {dataset_id}")
        return dataset_id
    else:
        logger.error(f"❌ Failed to create dataset: {response.text}")
        logger.error(f"Status code: {response.status_code}")
        return None

def refresh_dataset_columns(session, dataset_id):
    """Refresh dataset columns"""
    logger.info(f"🔄 Refreshing columns for dataset ID: {dataset_id}")
    
    url = f"{SUPERSET_URL}/api/v1/dataset/{dataset_id}/refresh"
    response = session.put(url)
    
    if response.status_code == 200:
        logger.info("✅ Dataset columns refreshed successfully")
    else:
        logger.warning(f"⚠️ Failed to refresh columns: {response.text}")

def main():
    """Main function to fix dataset issue"""
    try:
        logger.info("🚀 Starting Superset dataset fix...")
        
        # Wait for Superset to be ready
        logger.info("⏳ Waiting for Superset to be ready...")
        time.sleep(10)
        
        # Get authenticated session
        session = get_superset_session()
        logger.info("✅ Successfully authenticated with Superset")
        
        # Check database connection
        database_id = check_database_connection(session)
        if not database_id:
            logger.error("❌ Cannot proceed without database connection")
            return False
        
        # Delete existing dataset if it exists
        delete_existing_dataset(session, "poverty_data")
        
        # Create new dataset
        dataset_id = create_dataset(session, database_id, "poverty_data")
        if not dataset_id:
            logger.error("❌ Failed to create dataset")
            return False
        
        # Refresh columns
        refresh_dataset_columns(session, dataset_id)
        
        logger.info("🎉 Dataset fix completed successfully!")
        logger.info(f"📊 Dataset 'poverty_data' is now ready for chart creation")
        logger.info(f"🔗 Access Superset: {SUPERSET_URL}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ SUCCESS: Dataset issue fixed!")
        print("🎯 You can now create charts with the poverty_data table")
    else:
        print("\n❌ FAILED: Could not fix dataset issue")
        print("💡 Try manual dataset creation in Superset UI")
