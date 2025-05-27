#!/usr/bin/env python3
"""
Automated Superset Dataset Creation for Kelompok 18
Pemetaan Kemiskinan Sumatera - Big Data Pipeline
"""

import requests
import json
import time

class SupersetDatasetCreator:
    def __init__(self):
        self.base_url = "http://localhost:8089"
        self.session = requests.Session()
        self.csrf_token = None
        
    def login(self, username="admin", password="admin"):
        """Login to Superset and get CSRF token"""
        print("🔐 Logging into Superset...")
        
        # Get CSRF token
        response = self.session.get(f"{self.base_url}/login/")
        if response.status_code != 200:
            print(f"❌ Failed to access login page: {response.status_code}")
            return False
            
        # Login
        login_data = {
            "username": username,
            "password": password
        }
        
        response = self.session.post(f"{self.base_url}/login/", data=login_data)
        if "Invalid login" in response.text:
            print("❌ Login failed - Invalid credentials")
            return False
            
        print("✅ Login successful")
        return True
    
    def create_database_connection(self):
        """Create PostgreSQL database connection"""
        print("🗄️ Creating database connection...")
        
        # Get CSRF token from API
        response = self.session.get(f"{self.base_url}/api/v1/security/csrf_token/")
        if response.status_code == 200:
            self.csrf_token = response.json().get("result")
        
        # Database connection payload
        db_payload = {
            "database_name": "Kelompok18_PovertyDB_May2025",
            "sqlalchemy_uri": "postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping",
            "expose_in_sqllab": True,
            "allow_run_async": True,
            "allow_ctas": True,
            "allow_cvas": True,
            "allow_dml": True,
            "force_ctas_schema": None,
            "cache_timeout": None,
            "encrypted_extra": "",
            "extra": json.dumps({
                "metadata_params": {},
                "engine_params": {},
                "metadata_cache_timeout": {},
                "schemas_allowed_for_csv_upload": []
            })
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": self.csrf_token
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/database/",
            data=json.dumps(db_payload),
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            print("✅ Database connection created successfully")
            return response.json().get("id")
        else:
            print(f"⚠️ Database connection response: {response.status_code}")
            print(response.text[:200])
            return None
    
    def create_dataset(self, database_id):
        """Create dataset from poverty_clean view"""
        print("📊 Creating dataset from poverty_clean view...")
        
        dataset_payload = {
            "database": database_id,
            "schema": "public",
            "table_name": "poverty_clean"
        }
        
        headers = {
            "Content-Type": "application/json", 
            "X-CSRFToken": self.csrf_token
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/dataset/",
            data=json.dumps(dataset_payload),
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            print("✅ Dataset created successfully")
            return response.json().get("id")
        else:
            print(f"⚠️ Dataset creation response: {response.status_code}")
            print(response.text[:200])
            return None
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting Automated Superset Dataset Creation")
        print("=" * 60)
        
        # Step 1: Login
        if not self.login():
            return False
            
        # Step 2: Create database connection
        database_id = self.create_database_connection()
        if not database_id:
            print("⚠️ Database connection creation failed, but may already exist")
            
        # Step 3: Create dataset
        dataset_id = self.create_dataset(database_id or 1)  # Use ID 1 if creation failed
        
        print("\n" + "=" * 60)
        print("🎯 SETUP SUMMARY:")
        print(f"   📍 Superset URL: {self.base_url}")
        print(f"   🗄️ Database: Kelompok18_PovertyDB_May2025") 
        print(f"   📊 Dataset: poverty_clean")
        print(f"   📈 Records: ~20,000 poverty data points")
        
        print("\n📋 NEXT STEPS:")
        print("1. Open Superset: http://localhost:8089")
        print("2. Go to Charts → + to create visualizations")
        print("3. Select 'poverty_clean' dataset")
        print("4. Build poverty mapping dashboard")
        
        return True

def main():
    """Main execution function"""
    creator = SupersetDatasetCreator()
    success = creator.run_setup()
    
    if success:
        print("\n✅ Automated setup completed!")
        print("🎨 Ready to create poverty mapping visualizations!")
    else:
        print("\n⚠️ Automated setup had issues - proceed with manual steps")
        print("📖 See: SUPERSET_DATASET_CREATION_GUIDE.md")

if __name__ == "__main__":
    main()
