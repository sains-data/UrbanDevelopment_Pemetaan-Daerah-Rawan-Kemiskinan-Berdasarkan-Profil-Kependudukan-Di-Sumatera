#!/usr/bin/env python3
"""
Superset Dashboard Configuration Script
Poverty Mapping in Sumatra - Kelompok 18

This script configures Superset dashboards, datasets, and charts
for the poverty mapping pipeline.
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupersetConfigurator:
    def __init__(self, superset_url: str = "http://localhost:8088"):
        self.base_url = superset_url
        self.session = requests.Session()
        self.csrf_token = None
        self.access_token = None
    
    def login(self, username: str = "admin", password: str = "admin") -> bool:
        """Login to Superset and get authentication tokens"""
        try:
            # Get CSRF token
            response = self.session.get(f"{self.base_url}/login/")
            if response.status_code != 200:
                logger.error(f"Failed to get login page: {response.status_code}")
                return False
            
            # Login request
            login_data = {
                "username": username,
                "password": password,
                "provider": "db"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/security/login",
                json=login_data
            )
            
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.access_token}"
                })
                logger.info("✅ Successfully logged into Superset")
                return True
            else:
                logger.error(f"Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def create_database_connection(self) -> Optional[int]:
        """Create database connection to Hive"""
        database_config = {
            "database_name": "kemiskinan_hive",
            "sqlalchemy_uri": "hive://hive-server:10000/kemiskinan_db",
            "engine": "hive",
            "configuration_method": "sqlalchemy_form",
            "expose_in_sqllab": True,
            "allow_ctas": True,
            "allow_cvas": True,
            "allow_dml": True,
            "extra": json.dumps({
                "metadata_params": {},
                "engine_params": {},
                "metadata_cache_timeout": {},
                "schemas_allowed_for_csv_upload": []
            })
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/database/",
                json=database_config
            )
            
            if response.status_code == 201:
                db_id = response.json()["id"]
                logger.info(f"✅ Database connection created with ID: {db_id}")
                return db_id
            else:
                logger.error(f"Failed to create database: {response.status_code}")
                logger.error(response.text)
                return None
                
        except Exception as e:
            logger.error(f"Database creation error: {e}")
            return None
    
    def create_dataset(self, database_id: int, table_name: str) -> Optional[int]:
        """Create a dataset from Hive table"""
        dataset_config = {
            "database": database_id,
            "table_name": table_name,
            "schema": "kemiskinan_db"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/dataset/",
                json=dataset_config
            )
            
            if response.status_code == 201:
                dataset_id = response.json()["id"]
                logger.info(f"✅ Dataset '{table_name}' created with ID: {dataset_id}")
                return dataset_id
            else:
                logger.error(f"Failed to create dataset '{table_name}': {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Dataset creation error: {e}")
            return None
    
    def create_chart(self, dataset_id: int, chart_config: Dict) -> Optional[int]:
        """Create a chart"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/chart/",
                json=chart_config
            )
            
            if response.status_code == 201:
                chart_id = response.json()["id"]
                logger.info(f"✅ Chart '{chart_config['slice_name']}' created with ID: {chart_id}")
                return chart_id
            else:
                logger.error(f"Failed to create chart: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Chart creation error: {e}")
            return None
    
    def create_dashboard(self, dashboard_config: Dict, chart_ids: List[int]) -> Optional[int]:
        """Create a dashboard with charts"""
        dashboard_config["position_json"] = json.dumps(self._generate_dashboard_layout(chart_ids))
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/dashboard/",
                json=dashboard_config
            )
            
            if response.status_code == 201:
                dashboard_id = response.json()["id"]
                logger.info(f"✅ Dashboard '{dashboard_config['dashboard_title']}' created with ID: {dashboard_id}")
                return dashboard_id
            else:
                logger.error(f"Failed to create dashboard: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Dashboard creation error: {e}")
            return None
    
    def _generate_dashboard_layout(self, chart_ids: List[int]) -> Dict:
        """Generate dashboard layout JSON"""
        layout = {
            "DASHBOARD_VERSION_KEY": "v2",
            "ROOT_ID": "GRID_ID",
            "GRID_ID": {
                "type": "GRID",
                "id": "GRID_ID",
                "children": [],
                "parents": ["ROOT_ID"]
            }
        }
        
        # Create chart layouts
        for i, chart_id in enumerate(chart_ids):
            chart_key = f"CHART-{chart_id}"
            row_id = f"ROW-{i}"
            
            # Add row
            layout[row_id] = {
                "type": "ROW",
                "id": row_id,
                "children": [chart_key],
                "parents": ["GRID_ID"],
                "meta": {"background": "BACKGROUND_TRANSPARENT"}
            }
            
            # Add chart
            layout[chart_key] = {
                "type": "CHART",
                "id": chart_key,
                "children": [],
                "parents": [row_id],
                "meta": {
                    "chartId": chart_id,
                    "width": 12,
                    "height": 50
                }
            }
            
            layout["GRID_ID"]["children"].append(row_id)
        
        return layout

def setup_poverty_dashboards():
    """Main function to set up poverty mapping dashboards"""
    configurator = SupersetConfigurator()
    
    # Login to Superset
    if not configurator.login():
        logger.error("❌ Failed to login to Superset")
        return False
    
    # Wait for services to be ready
    logger.info("⏳ Waiting for Hive service to be ready...")
    time.sleep(30)
    
    # Create database connection
    db_id = configurator.create_database_connection()
    if not db_id:
        logger.error("❌ Failed to create database connection")
        return False
    
    # Create datasets
    datasets = [
        "poverty_gold_aggregated",
        "poverty_silver_cleaned", 
        "poverty_bronze_raw",
        "poverty_risk_assessment",
        "poverty_ml_predictions"
    ]
    
    dataset_ids = {}
    for table_name in datasets:
        dataset_id = configurator.create_dataset(db_id, table_name)
        if dataset_id:
            dataset_ids[table_name] = dataset_id
    
    if not dataset_ids:
        logger.error("❌ Failed to create any datasets")
        return False
    
    # Chart configurations
    chart_configs = [
        {
            "slice_name": "Poverty Rate by Province",
            "viz_type": "dist_bar",
            "datasource_id": dataset_ids.get("poverty_gold_aggregated"),
            "datasource_type": "table",
            "params": json.dumps({
                "metrics": ["avg_poverty_rate"],
                "groupby": ["provinsi"],
                "color_scheme": "supersetColors",
                "show_legend": True,
                "rich_tooltip": True,
                "bar_stacked": False
            }),
            "cache_timeout": 3600
        },
        {
            "slice_name": "Unemployment vs Poverty Correlation", 
            "viz_type": "scatter",
            "datasource_id": dataset_ids.get("poverty_gold_aggregated"),
            "datasource_type": "table",
            "params": json.dumps({
                "x": "avg_unemployment_rate",
                "y": "avg_poverty_rate",
                "size": "total_population",
                "entity": "provinsi",
                "color_scheme": "supersetColors"
            }),
            "cache_timeout": 3600
        },
        {
            "slice_name": "Infrastructure Access Distribution",
            "viz_type": "pie",
            "datasource_id": dataset_ids.get("poverty_silver_cleaned"),
            "datasource_type": "table", 
            "params": json.dumps({
                "metrics": ["count"],
                "groupby": ["akses_pendidikan"],
                "color_scheme": "supersetColors",
                "show_legend": True,
                "rich_tooltip": True
            }),
            "cache_timeout": 3600
        },
        {
            "slice_name": "Poverty Trend Analysis",
            "viz_type": "line",
            "datasource_id": dataset_ids.get("poverty_gold_aggregated"),
            "datasource_type": "table",
            "params": json.dumps({
                "metrics": ["avg_poverty_rate", "avg_unemployment_rate"],
                "groupby": ["provinsi"],
                "color_scheme": "supersetColors",
                "show_legend": True,
                "rich_tooltip": True
            }),
            "cache_timeout": 3600
        },
        {
            "slice_name": "High Risk Areas Map",
            "viz_type": "big_number_total",
            "datasource_id": dataset_ids.get("poverty_risk_assessment"),
            "datasource_type": "table",
            "params": json.dumps({
                "metric": "count",
                "where": "risk_level = 'high'",
                "color_scheme": "supersetColors"
            }),
            "cache_timeout": 3600
        },
        {
            "slice_name": "ML Prediction Accuracy",
            "viz_type": "big_number",
            "datasource_id": dataset_ids.get("poverty_ml_predictions"),
            "datasource_type": "table",
            "params": json.dumps({
                "metric": "avg_accuracy",
                "color_scheme": "supersetColors",
                "y_axis_format": ".2%"
            }),
            "cache_timeout": 3600
        }
    ]
    
    # Create charts
    chart_ids = []
    for chart_config in chart_configs:
        if chart_config["datasource_id"]:  # Only create if dataset exists
            chart_id = configurator.create_chart(chart_config["datasource_id"], chart_config)
            if chart_id:
                chart_ids.append(chart_id)
    
    if not chart_ids:
        logger.error("❌ Failed to create any charts")
        return False
    
    # Create main dashboard
    dashboard_config = {
        "dashboard_title": "Poverty Mapping Dashboard - Sumatra",
        "slug": "poverty-mapping-sumatra",
        "json_metadata": json.dumps({
            "timed_refresh_immune_slices": [],
            "expanded_slices": {},
            "refresh_frequency": 0,
            "default_filters": {},
            "color_scheme": "supersetColors"
        }),
        "published": True
    }
    
    dashboard_id = configurator.create_dashboard(dashboard_config, chart_ids)
    
    if dashboard_id:
        logger.info("🎉 Poverty mapping dashboard setup completed successfully!")
        logger.info(f"📊 Dashboard URL: {configurator.base_url}/superset/dashboard/{dashboard_id}/")
        return True
    else:
        logger.error("❌ Failed to create dashboard")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Superset dashboards for Poverty Mapping...")
    print("=" * 60)
    
    success = setup_poverty_dashboards()
    
    if success:
        print("\n✅ Dashboard setup completed successfully!")
        print("🔗 Access your dashboard at: http://localhost:8088")
        print("👤 Login with admin/admin")
    else:
        print("\n❌ Dashboard setup failed!")
        print("🔧 Check Superset logs for details")
