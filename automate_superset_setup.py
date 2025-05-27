#!/usr/bin/env python3
"""
Automated Superset Dashboard Setup Script
Kelompok 18 - Big Data Poverty Mapping Pipeline

This script automates the initial setup of Superset dashboards
for poverty mapping analysis.
"""

import requests
import json
import time
import sys

# Superset configuration
SUPERSET_URL = "http://localhost:8089"
DATABASE_URI = "postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping"

def print_header():
    print("=" * 60)
    print("🚀 SUPERSET DASHBOARD AUTOMATION")
    print("📊 Kelompok 18 - Poverty Mapping Pipeline")
    print("=" * 60)

def login_to_superset():
    """Login to Superset and get access token"""
    print("\n🔐 Logging into Superset...")
    
    # Get CSRF token
    session = requests.Session()
    
    try:
        # Login request
        login_data = {
            "username": "admin",
            "password": "admin",
            "provider": "db"
        }
        
        response = session.post(f"{SUPERSET_URL}/api/v1/security/login", json=login_data)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("  ✅ Successfully logged into Superset")
            return session, token
        else:
            print(f"  ❌ Login failed: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"  ❌ Login error: {e}")
        return None, None

def add_database_connection(session, token):
    """Add PostgreSQL database connection"""
    print("\n🗄️ Adding PostgreSQL database connection...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    database_config = {
        "database_name": "Poverty Mapping DB",
        "sqlalchemy_uri": DATABASE_URI,
        "expose_in_sqllab": True,
        "allow_ctas": True,
        "allow_cvas": True,
        "allow_dml": True,
        "force_ctas_schema": "public",
        "extra": json.dumps({
            "metadata_params": {},
            "engine_params": {},
            "metadata_cache_timeout": {},
            "schemas_allowed_for_csv_upload": ["public"]
        })
    }
    
    try:
        response = session.post(
            f"{SUPERSET_URL}/api/v1/database/",
            headers=headers,
            json=database_config
        )
        
        if response.status_code in [200, 201]:
            print("  ✅ Database connection added successfully")
            return response.json().get("id")
        else:
            print(f"  ❌ Failed to add database: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"  ❌ Database connection error: {e}")
        return None

def create_datasets(session, token, database_id):
    """Create datasets for poverty data tables"""
    print("\n📊 Creating datasets...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    tables = [
        ("poverty_data", "Main poverty data by area"),
        ("province_summary", "Aggregated data by province"),
        ("regency_summary", "Aggregated data by regency"),
        ("v_poverty_hotspots", "Areas with high poverty rates")
    ]
    
    created_datasets = []
    
    for table_name, description in tables:
        dataset_config = {
            "database": database_id,
            "schema": "public",
            "table_name": table_name,
            "description": description
        }
        
        try:
            response = session.post(
                f"{SUPERSET_URL}/api/v1/dataset/",
                headers=headers,
                json=dataset_config
            )
            
            if response.status_code in [200, 201]:
                dataset_id = response.json().get("id")
                created_datasets.append((table_name, dataset_id))
                print(f"  ✅ Created dataset: {table_name}")
            else:
                print(f"  ❌ Failed to create dataset {table_name}: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Dataset creation error for {table_name}: {e}")
    
    return created_datasets

def create_sample_chart(session, token, dataset_info):
    """Create a sample chart"""
    print("\n📈 Creating sample chart...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    table_name, dataset_id = dataset_info[1]  # Use province_summary
    
    chart_config = {
        "slice_name": "Poverty Rate by Province - Sample",
        "viz_type": "dist_bar",
        "datasource_id": dataset_id,
        "datasource_type": "table",
        "params": json.dumps({
            "metrics": ["avg_poverty_rate"],
            "groupby": ["province"],
            "viz_type": "dist_bar",
            "order_desc": True,
            "color_scheme": "bnbColors",
            "show_legend": True,
            "rich_tooltip": True,
            "show_bar_value": True
        }),
        "description": "Sample chart showing poverty rates by Sumatra province"
    }
    
    try:
        response = session.post(
            f"{SUPERSET_URL}/api/v1/chart/",
            headers=headers,
            json=chart_config
        )
        
        if response.status_code in [200, 201]:
            chart_id = response.json().get("id")
            print(f"  ✅ Created sample chart: ID {chart_id}")
            return chart_id
        else:
            print(f"  ❌ Failed to create chart: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Chart creation error: {e}")
        return None

def print_next_steps():
    """Print what to do next"""
    print("\n" + "=" * 60)
    print("🎯 SETUP COMPLETE! Next Steps:")
    print("=" * 60)
    print("\n1. 🌐 Open Superset: http://localhost:8089")
    print("2. 🔑 Login with: admin / admin")
    print("3. 📊 Go to 'Data' → 'Datasets' to see your datasets")
    print("4. 📈 Go to 'Charts' to see the sample chart")
    print("5. 🎨 Create more charts using the datasets")
    print("6. 📋 Build your dashboard by combining charts")
    
    print("\n🗄️ Available Datasets:")
    print("  • poverty_data - Individual area records")
    print("  • province_summary - Provincial aggregates")
    print("  • regency_summary - Regency aggregates")
    print("  • v_poverty_hotspots - High poverty areas")
    
    print("\n📈 Suggested Charts:")
    print("  • Bar chart: Province poverty comparison")
    print("  • Pie chart: Poverty distribution")
    print("  • Table: Detailed area breakdown")
    print("  • Scatter plot: Geographic distribution")
    
    print("\n📚 Full Guide: SUPERSET_DASHBOARD_CREATION_GUIDE.md")
    print("=" * 60)

def main():
    """Main execution function"""
    print_header()
    
    # Login to Superset
    session, token = login_to_superset()
    if not session or not token:
        print("\n❌ Cannot proceed without Superset access")
        sys.exit(1)
    
    # Add database connection
    database_id = add_database_connection(session, token)
    if not database_id:
        print("\n❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Create datasets
    datasets = create_datasets(session, token, database_id)
    if not datasets:
        print("\n❌ No datasets created")
        sys.exit(1)
    
    # Create sample chart
    if len(datasets) > 1:
        chart_id = create_sample_chart(session, token, datasets)
    
    # Print next steps
    print_next_steps()
    
    print("\n✅ Automation completed successfully!")
    print("🚀 Ready to build amazing poverty mapping dashboards!")

if __name__ == "__main__":
    main()
