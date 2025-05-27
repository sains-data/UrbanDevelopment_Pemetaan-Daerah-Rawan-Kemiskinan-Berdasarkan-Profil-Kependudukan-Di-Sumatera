"""
Superset API Dashboard Creation Automation
Kelompok 18 - Big Data Pipeline for Poverty Mapping in Sumatra
Automated dashboard creation using Superset REST API
"""

import requests
import json
import time
import sqlite3
import os
from datetime import datetime

class SupersetDashboardCreator:
    def __init__(self, base_url="http://localhost:8089"):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None
        self.access_token = None
        
    def login(self, username="admin", password="admin"):
        """Login to Superset and get tokens"""
        print("🔐 Logging into Superset...")
        
        # Get CSRF token
        csrf_response = self.session.get(f"{self.base_url}/api/v1/security/csrf_token/")
        if csrf_response.status_code == 200:
            self.csrf_token = csrf_response.json()["result"]
            print("✅ CSRF token obtained")
        else:
            print(f"❌ Failed to get CSRF token: {csrf_response.status_code}")
            return False
            
        # Login
        login_data = {
            "username": username,
            "password": password,
            "provider": "db",
            "refresh": True
        }
        
        headers = {
            "X-CSRFToken": self.csrf_token,
            "Content-Type": "application/json",
            "Referer": self.base_url
        }
        
        login_response = self.session.post(
            f"{self.base_url}/api/v1/security/login",
            json=login_data,
            headers=headers
        )
        
        if login_response.status_code == 200:
            result = login_response.json()
            self.access_token = result.get("access_token")
            print("✅ Successfully logged in")
            return True
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
    
    def get_headers(self):
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "X-CSRFToken": self.csrf_token,
            "Content-Type": "application/json",
            "Referer": self.base_url
        }
    
    def create_database_connection(self):
        """Create database connection in Superset"""
        print("🗄️ Creating database connection...")
        
        db_path = os.path.abspath("superset_data/poverty_mapping.db")
        sqlalchemy_uri = f"sqlite:///{db_path.replace(chr(92), '/')}"  # Convert Windows paths
        
        database_config = {
            "database_name": "Poverty_Mapping_Sumatra",
            "sqlalchemy_uri": sqlalchemy_uri,
            "expose_in_sqllab": True,
            "allow_run_async": True,
            "allow_ctas": True,
            "allow_cvas": True,
            "allow_dml": True,
            "force_ctas_schema": "",
            "extra": "{\"metadata_params\":{},\"engine_params\":{},\"metadata_cache_timeout\":{},\"schemas_allowed_for_csv_upload\":[]}",
            "server_cert": "",
            "encrypted_extra": "",
            "impersonate_user": False,
            "allow_csv_upload": True
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/database/",
            json=database_config,
            headers=self.get_headers()
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            database_id = result.get("id")
            print(f"✅ Database connection created with ID: {database_id}")
            return database_id
        else:
            print(f"❌ Failed to create database: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def create_dataset(self, database_id, table_name):
        """Create dataset from table"""
        print(f"📊 Creating dataset for table: {table_name}")
        
        dataset_config = {
            "database": database_id,
            "table_name": table_name,
            "schema": "",
            "sql": "",
            "is_sqllab_view": False,
            "template_params": "",
            "extra": "{}"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/dataset/",
            json=dataset_config,
            headers=self.get_headers()
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            dataset_id = result.get("id")
            print(f"✅ Dataset created for {table_name} with ID: {dataset_id}")
            return dataset_id
        else:
            print(f"❌ Failed to create dataset for {table_name}: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def create_chart(self, dataset_id, chart_config):
        """Create a chart"""
        print(f"📈 Creating chart: {chart_config['slice_name']}")
        
        chart_data = {
            "slice_name": chart_config["slice_name"],
            "description": chart_config.get("description", ""),
            "viz_type": chart_config["viz_type"],
            "datasource_id": dataset_id,
            "datasource_type": "table",
            "params": json.dumps(chart_config["params"]),
            "cache_timeout": 0
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/chart/",
            json=chart_data,
            headers=self.get_headers()
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            chart_id = result.get("id")
            print(f"✅ Chart '{chart_config['slice_name']}' created with ID: {chart_id}")
            return chart_id
        else:
            print(f"❌ Failed to create chart '{chart_config['slice_name']}': {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    def create_dashboard(self, dashboard_title, chart_ids):
        """Create dashboard with charts"""
        print(f"🎨 Creating dashboard: {dashboard_title}")
        
        # Create basic dashboard layout
        position_json = {}
        row_id = 0
        
        for i, chart_id in enumerate(chart_ids):
            if chart_id:
                position_json[f"CHART-{chart_id}"] = {
                    "children": [],
                    "id": f"CHART-{chart_id}",
                    "meta": {
                        "chartId": chart_id,
                        "height": 50,
                        "sliceName": f"Chart {i+1}",
                        "width": 6
                    },
                    "parents": [f"ROOT_ID", f"TABS-{row_id}", f"ROW-{row_id}"],
                    "type": "CHART"
                }
                
                if i % 2 == 0:  # New row every 2 charts
                    row_id += 1
                    position_json[f"ROW-{row_id}"] = {
                        "children": [f"CHART-{chart_id}"],
                        "id": f"ROW-{row_id}",
                        "meta": {"background": "BACKGROUND_TRANSPARENT"},
                        "parents": [f"ROOT_ID", f"TABS-{row_id}"],
                        "type": "ROW"
                    }
        
        dashboard_config = {
            "dashboard_title": dashboard_title,
            "slug": dashboard_title.lower().replace(" ", "_"),
            "position_json": json.dumps(position_json),
            "css": "",
            "json_metadata": json.dumps({
                "filter_scopes": {},
                "expanded_slices": {},
                "refresh_frequency": 0,
                "timed_refresh_immune_slices": [],
                "default_filters": "{}",
                "color_scheme": ""
            }),
            "published": True
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/dashboard/",
            json=dashboard_config,
            headers=self.get_headers()
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            dashboard_id = result.get("id")
            print(f"✅ Dashboard '{dashboard_title}' created with ID: {dashboard_id}")
            return dashboard_id
        else:
            print(f"❌ Failed to create dashboard '{dashboard_title}': {response.status_code}")
            print(f"Response: {response.text}")
            return None

def get_chart_configurations():
    """Define all chart configurations"""
    return [
        {
            "slice_name": "Poverty Rate by Province",
            "viz_type": "dist_bar",
            "description": "Bar chart showing average poverty rates across Sumatra provinces",
            "params": {
                "metrics": ["Avg_Poverty_Rate"],
                "groupby": ["Provinsi"],
                "viz_type": "dist_bar",
                "color_scheme": "bnbColors",
                "show_legend": True,
                "rich_tooltip": True,
                "show_bar_value": True
            }
        },
        {
            "slice_name": "Unemployment vs Poverty Scatter",
            "viz_type": "bubble",
            "description": "Scatter plot showing relationship between unemployment and poverty rates",
            "params": {
                "x": "Unemployment_Rate",
                "y": "Poverty_Rate", 
                "size": "Population",
                "viz_type": "bubble",
                "color_scheme": "bnbColors",
                "show_legend": True
            }
        },
        {
            "slice_name": "Economic Health Distribution",
            "viz_type": "pie",
            "description": "Pie chart showing distribution of economic health categories",
            "params": {
                "groupby": ["Poverty_Category"],
                "metric": "count",
                "viz_type": "pie",
                "color_scheme": "bnbColors",
                "show_legend": True,
                "show_labels": True
            }
        },
        {
            "slice_name": "Regional Poverty Summary Table",
            "viz_type": "table",
            "description": "Detailed table with poverty statistics by region",
            "params": {
                "groupby": ["Provinsi", "Kabupaten_Kota"],
                "metrics": ["Poverty_Rate", "Unemployment_Rate", "Population"],
                "viz_type": "table",
                "page_length": 25,
                "table_timestamp_format": "%Y-%m-%d"
            }
        },
        {
            "slice_name": "Poverty Trend Over Time",
            "viz_type": "line",
            "description": "Line chart showing poverty trends",
            "params": {
                "metrics": ["Poverty_Rate"],
                "groupby": ["Tahun"],
                "viz_type": "line",
                "color_scheme": "bnbColors",
                "show_legend": True,
                "rich_tooltip": True
            }
        },
        {
            "slice_name": "Geographic Heat Map",
            "viz_type": "heatmap",
            "description": "Heat map of poverty intensity across regions",
            "params": {
                "all_columns_x": "Provinsi",
                "all_columns_y": "Kabupaten_Kota", 
                "metric": "Poverty_Rate",
                "viz_type": "heatmap",
                "color_scheme": "bnbColors"
            }
        }
    ]

def main():
    """Main execution function"""
    print("🚀 SUPERSET DASHBOARD AUTOMATION")
    print("=" * 60)
    print("📋 Kelompok 18 - Big Data Pipeline for Poverty Mapping")
    print("🗓️ Starting automation:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 60)
    
    # Initialize creator
    creator = SupersetDashboardCreator()
    
    # Step 1: Login
    if not creator.login():
        print("❌ Cannot proceed without login")
        return
    
    time.sleep(2)
    
    # Step 2: Create database connection
    database_id = creator.create_database_connection()
    if not database_id:
        print("❌ Cannot proceed without database connection")
        return
    
    time.sleep(2)
    
    # Step 3: Create datasets
    main_dataset_id = creator.create_dataset(database_id, "poverty_data")
    summary_dataset_id = creator.create_dataset(database_id, "province_summary")
    
    if not main_dataset_id:
        print("❌ Cannot proceed without main dataset")
        return
    
    time.sleep(2)
    
    # Step 4: Create charts
    chart_configs = get_chart_configurations()
    chart_ids = []
    
    for config in chart_configs:
        chart_id = creator.create_chart(main_dataset_id, config)
        chart_ids.append(chart_id)
        time.sleep(1)  # Rate limiting
    
    # Step 5: Create dashboard
    dashboard_id = creator.create_dashboard(
        "Poverty Mapping Dashboard - Sumatra", 
        [cid for cid in chart_ids if cid is not None]
    )
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 AUTOMATION COMPLETED!")
    print("=" * 60)
    print(f"📊 Database ID: {database_id}")
    print(f"📈 Main Dataset ID: {main_dataset_id}")
    print(f"📋 Summary Dataset ID: {summary_dataset_id}")
    print(f"🎨 Dashboard ID: {dashboard_id}")
    print(f"📈 Charts Created: {len([c for c in chart_ids if c])}/{len(chart_configs)}")
    
    print(f"\n🔗 ACCESS YOUR DASHBOARD:")
    print(f"   🌐 Superset: http://localhost:8089")
    print(f"   📊 Dashboard URL: http://localhost:8089/superset/dashboard/{dashboard_id}/")
    print(f"   👤 Login: admin / admin")
    
    print(f"\n📖 DOCUMENTATION:")
    print(f"   📋 Setup Guide: superset_data/PANDUAN_DASHBOARD_LENGKAP.md")
    print(f"   📊 Database: superset_data/poverty_mapping.db")
    
    print(f"\n✨ Ready for poverty analysis and policy insights!")
    print(f"🕒 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
