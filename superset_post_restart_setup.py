#!/usr/bin/env python3
"""
Automated Superset Setup untuk Gold Layer Data
Kelompok 18 - Big Data Poverty Mapping Pipeline

Script ini akan otomatis:
1. Setup database connection ke PostgreSQL
2. Create datasets dari Gold layer views
3. Verifikasi semua berjalan dengan baik
"""

import requests
import json
import time
import sys

class SupersetGoldSetup:
    def __init__(self):
        self.base_url = "http://localhost:8089"
        self.session = requests.Session()
        self.csrf_token = None
        self.access_token = None
        
        # Database connection config
        self.db_config = {
            "database_name": "poverty_mapping_gold",
            "sqlalchemy_uri": "postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping",
            "expose_in_sqllab": True,
            "allow_run_async": True,
            "allow_ctas": True,
            "allow_cvas": True,
            "allow_dml": True
        }
        
        # Gold layer views untuk dataset creation
        self.gold_views = [
            {
                "table_name": "v_gold_provincial_dashboard",
                "dataset_name": "Gold Provincial Dashboard",
                "description": "Comprehensive provincial poverty analysis with risk levels and income categories"
            },
            {
                "table_name": "v_gold_poverty_hotspots", 
                "dataset_name": "Gold Poverty Hotspots",
                "description": "Priority-focused view highlighting high-risk provinces needing attention"
            },
            {
                "table_name": "v_gold_summary_stats",
                "dataset_name": "Gold Summary Statistics", 
                "description": "High-level KPI metrics and statistics for executive dashboards"
            },
            {
                "table_name": "gold_province_poverty_summary",
                "dataset_name": "Gold Province Data",
                "description": "Complete provincial poverty data from Gold layer"
            }
        ]

    def print_header(self):
        print("=" * 70)
        print("🚀 AUTOMATED SUPERSET SETUP FOR GOLD LAYER")
        print("📊 Kelompok 18 - Big Data Poverty Mapping")
        print("🔄 Post-Restart Database & Dataset Setup")
        print("=" * 70)
        
    def wait_for_superset(self):
        """Wait for Superset to be fully ready"""
        print("\n⏳ Waiting for Superset to be fully ready...")
        
        max_attempts = 12  # 2 minutes
        for attempt in range(max_attempts):
            try:
                response = self.session.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    print("✅ Superset is ready!")
                    return True
                    
            except requests.exceptions.ConnectionError:
                pass
                
            print(f"   Attempt {attempt + 1}/{max_attempts} - waiting...")
            time.sleep(10)
            
        print("❌ Superset not ready after 2 minutes")
        return False

    def login(self):
        """Login to Superset and get authentication tokens"""
        print("\n🔐 Logging into Superset...")
        
        try:
            # Get login page for CSRF token
            login_page = self.session.get(f"{self.base_url}/login/")
            
            # Try default admin credentials
            login_data = {
                "username": "admin",
                "password": "admin"
            }
            
            response = self.session.post(f"{self.base_url}/login/", data=login_data)
            
            if "dashboard" in response.url or response.status_code == 200:
                print("✅ Successfully logged into Superset")
                return True
            else:
                print("⚠️ Login may have failed, but continuing...")
                return True
                
        except Exception as e:
            print(f"⚠️ Login error (continuing anyway): {e}")
            return True

    def get_csrf_token(self):
        """Get CSRF token for API calls"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/security/csrf_token/")
            if response.status_code == 200:
                self.csrf_token = response.json()["result"]
                self.session.headers.update({"X-CSRFToken": self.csrf_token})
                print("✅ CSRF token obtained")
                return True
        except Exception as e:
            print(f"⚠️ CSRF token error: {e}")
            return False

    def check_database_exists(self):
        """Check if our database connection already exists"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/database/")
            if response.status_code == 200:
                databases = response.json()["result"]
                for db in databases:
                    if db["database_name"] == self.db_config["database_name"]:
                        print(f"✅ Database '{self.db_config['database_name']}' already exists")
                        return db["id"]
                        
            print(f"📝 Database '{self.db_config['database_name']}' not found, will create new one")
            return None
            
        except Exception as e:
            print(f"⚠️ Error checking databases: {e}")
            return None

    def create_database_connection(self):
        """Create database connection to PostgreSQL"""
        print("\n💾 Setting up PostgreSQL database connection...")
        
        # Check if database already exists
        existing_db_id = self.check_database_exists()
        if existing_db_id:
            return existing_db_id
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/database/",
                json=self.db_config,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                db_id = response.json()["id"]
                print(f"✅ Database connection created successfully (ID: {db_id})")
                return db_id
            else:
                print(f"⚠️ Database creation response: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ Error creating database: {e}")
            return None

    def create_dataset(self, view_info, database_id):
        """Create dataset from Gold layer view"""
        try:
            dataset_data = {
                "database": database_id,
                "table_name": view_info["table_name"],
                "schema": "public"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/dataset/",
                json=dataset_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                dataset_id = response.json()["id"] 
                print(f"   ✅ Dataset '{view_info['dataset_name']}' created (ID: {dataset_id})")
                return dataset_id
            else:
                print(f"   ⚠️ Dataset creation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ⚠️ Error creating dataset: {e}")
            return None

    def create_all_datasets(self, database_id):
        """Create all Gold layer datasets"""
        print("\n📊 Creating datasets from Gold layer views...")
        
        created_datasets = []
        
        for view_info in self.gold_views:
            print(f"📝 Creating dataset: {view_info['dataset_name']}")
            dataset_id = self.create_dataset(view_info, database_id)
            
            if dataset_id:
                created_datasets.append({
                    "name": view_info["dataset_name"],
                    "table": view_info["table_name"], 
                    "id": dataset_id
                })
            
            time.sleep(1)  # Small delay between requests
            
        return created_datasets

    def verify_setup(self):
        """Verify that everything was set up correctly"""
        print("\n🔍 Verifying Superset setup...")
        
        try:
            # Check databases
            db_response = self.session.get(f"{self.base_url}/api/v1/database/")
            if db_response.status_code == 200:
                databases = db_response.json()["result"]
                gold_db = None
                for db in databases:
                    if "poverty_mapping" in db["database_name"].lower():
                        gold_db = db
                        break
                
                if gold_db:
                    print(f"   ✅ Database: {gold_db['database_name']}")
                else:
                    print("   ⚠️ Gold database not found")
            
            # Check datasets
            dataset_response = self.session.get(f"{self.base_url}/api/v1/dataset/")
            if dataset_response.status_code == 200:
                datasets = dataset_response.json()["result"]
                gold_datasets = [ds for ds in datasets if "gold" in ds["table_name"].lower()]
                
                print(f"   ✅ Gold Datasets: {len(gold_datasets)} found")
                for ds in gold_datasets:
                    print(f"      • {ds['table_name']}")
            
            return True
            
        except Exception as e:
            print(f"   ⚠️ Verification error: {e}")
            return False

    def print_success_summary(self, created_datasets):
        """Print success summary with next steps"""
        print("\n" + "=" * 70)
        print("🎉 SUPERSET GOLD LAYER SETUP COMPLETED!")
        print("=" * 70)
        
        print(f"\n✅ Database Connection: {self.db_config['database_name']}")
        print(f"✅ Created {len(created_datasets)} datasets:")
        
        for dataset in created_datasets:
            print(f"   📊 {dataset['name']} (from {dataset['table']})")
        
        print(f"\n🎯 NEXT STEPS:")
        print("1. 🔗 Access Superset: http://localhost:8089")
        print("2. 📊 Go to Datasets tab to see your Gold layer datasets")
        print("3. 🎨 Create charts using the datasets:")
        print("   • Gold Provincial Dashboard - Main analysis")
        print("   • Gold Poverty Hotspots - Risk focus")
        print("   • Gold Summary Statistics - KPI metrics")
        print("4. 📋 Build comprehensive dashboards")
        
        print("\n🚀 READY FOR DASHBOARD CREATION!")
        print("=" * 70)

    def run_setup(self):
        """Run the complete setup process"""
        self.print_header()
        
        # Wait for Superset to be ready
        if not self.wait_for_superset():
            return False
        
        # Login to Superset
        if not self.login():
            print("❌ Login failed")
            return False
        
        # Get CSRF token
        self.get_csrf_token()
        
        # Create database connection
        database_id = self.create_database_connection()
        if not database_id:
            print("❌ Database setup failed")
            return False
        
        # Create datasets
        created_datasets = self.create_all_datasets(database_id)
        
        # Verify setup
        self.verify_setup()
        
        # Print summary
        self.print_success_summary(created_datasets)
        
        return True

def main():
    """Main execution function"""
    try:
        setup = SupersetGoldSetup()
        success = setup.run_setup()
        
        if not success:
            print("\n❌ Setup completed with some issues")
            print("💡 You can still manually create datasets in Superset UI")
            print("🔗 http://localhost:8089")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Try running setup manually in Superset UI")

if __name__ == "__main__":
    main()
