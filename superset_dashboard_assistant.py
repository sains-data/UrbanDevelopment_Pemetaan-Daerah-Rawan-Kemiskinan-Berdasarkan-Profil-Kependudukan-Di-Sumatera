#!/usr/bin/env python3
"""
Superset Dashboard Creation Assistant
Kelompok 18 - Automated Setup untuk Dashboard Poverty Mapping
"""

import time
import webbrowser
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SupersetDashboardAssistant:
    def __init__(self):
        self.superset_url = "http://localhost:8089"
        self.database_config = {
            'name': 'Poverty Mapping DB',
            'uri': 'postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping',
            'host': 'postgres-local',
            'port': 5432,
            'database': 'poverty_mapping',
            'username': 'postgres',
            'password': 'postgres123'
        }
    
    def print_welcome(self):
        print("=" * 70)
        print("📊 SUPERSET DASHBOARD CREATION ASSISTANT")
        print("🎯 Kelompok 18 - Poverty Mapping Sumatera")
        print("🚀 Automated Setup & Step-by-Step Guide")
        print("=" * 70)
    
    def open_superset(self):
        """Open Superset in browser"""
        print("\n🌐 Opening Superset in your browser...")
        try:
            webbrowser.open(self.superset_url)
            print(f"✅ Superset opened: {self.superset_url}")
            print("🔑 Login credentials: admin / admin")
            return True
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"📱 Manual access: {self.superset_url}")
            return False
    
    def show_database_connection_info(self):
        """Display database connection information"""
        print("\n🗄️ DATABASE CONNECTION INFORMATION:")
        print("=" * 50)
        print("📋 COPY THESE VALUES TO SUPERSET:")
        print(f"   Display Name: {self.database_config['name']}")
        print(f"   SQLAlchemy URI: {self.database_config['uri']}")
        print("\n📝 OR FILL MANUALLY:")
        print(f"   Host: {self.database_config['host']}")
        print(f"   Port: {self.database_config['port']}")
        print(f"   Database: {self.database_config['database']}")
        print(f"   Username: {self.database_config['username']}")
        print(f"   Password: {self.database_config['password']}")
        print("=" * 50)
    
    def show_datasets_info(self):
        """Show available datasets"""
        datasets = [
            'v_gold_provincial_dashboard',
            'v_gold_poverty_hotspots', 
            'v_gold_summary_stats',
            'gold_province_poverty_summary'
        ]
        
        print("\n📊 AVAILABLE DATASETS (Gold Layer Views):")
        print("=" * 50)
        for i, dataset in enumerate(datasets, 1):
            print(f"   {i}. {dataset}")
        print("🎯 START WITH: v_gold_provincial_dashboard")
        print("=" * 50)
    
    def show_chart_recommendations(self):
        """Show recommended charts"""
        charts = {
            'KPI Cards': {
                'type': 'Big Number',
                'metrics': ['SUM(population)', 'AVG(poverty_rate)', 'COUNT(province_name)'],
                'purpose': 'Key performance indicators'
            },
            'Bar Chart': {
                'type': 'Bar Chart',
                'dimensions': 'province_name',
                'metrics': 'AVG(poverty_rate)',
                'purpose': 'Compare poverty rates across provinces'
            },
            'Pie Chart': {
                'type': 'Pie Chart',
                'dimensions': 'province_name',
                'metrics': 'SUM(population)',
                'purpose': 'Population distribution'
            },
            'Table': {
                'type': 'Table',
                'columns': ['province_name', 'poverty_rate', 'population', 'risk_category'],
                'purpose': 'Detailed province statistics'
            }
        }
        
        print("\n🎨 RECOMMENDED CHARTS:")
        print("=" * 50)
        for chart_name, config in charts.items():
            print(f"📈 {chart_name}:")
            print(f"   Type: {config['type']}")
            if 'metrics' in config:
                if isinstance(config['metrics'], list):
                    print(f"   Metrics: {', '.join(config['metrics'])}")
                else:
                    print(f"   Metrics: {config['metrics']}")
            if 'dimensions' in config:
                print(f"   Dimensions: {config['dimensions']}")
            if 'columns' in config:
                print(f"   Columns: {', '.join(config['columns'])}")
            print(f"   Purpose: {config['purpose']}")
            print()
    
    def show_step_by_step_guide(self):
        """Show detailed steps"""
        steps = [
            "🌐 Open Superset & Login (admin/admin)",
            "🗄️ Add Database Connection (PostgreSQL)",
            "📊 Create Datasets from Gold layer views",
            "📈 Create Charts (KPI, Bar, Pie, Table)",
            "🎨 Create Dashboard & Add Charts",
            "✨ Customize Layout & Colors",
            "🎯 Test & Validate Dashboard"
        ]
        
        print("\n🚀 STEP-BY-STEP WORKFLOW:")
        print("=" * 50)
        for i, step in enumerate(steps, 1):
            print(f"   {i}. {step}")
        print("=" * 50)
    
    def wait_for_user_input(self, message):
        """Wait for user to complete a step"""
        input(f"\n⏸️ {message} (Press Enter to continue...)")
    
    def run_interactive_guide(self):
        """Run interactive step-by-step guide"""
        self.print_welcome()
        
        # Step 1: Open Superset
        print("\n📋 STEP 1: OPEN SUPERSET")
        self.open_superset()
        self.wait_for_user_input("Complete login with admin/admin")
        
        # Step 2: Database Connection
        print("\n📋 STEP 2: DATABASE CONNECTION")
        self.show_database_connection_info()
        print("\n📝 INSTRUCTIONS:")
        print("1. Click Settings (⚙️) → Database Connections")
        print("2. Click + DATABASE")
        print("3. Select PostgreSQL")
        print("4. Use connection info above")
        print("5. Test connection (must be SUCCESS ✅)")
        self.wait_for_user_input("Complete database connection setup")
        
        # Step 3: Datasets
        print("\n📋 STEP 3: CREATE DATASETS")
        self.show_datasets_info()
        print("\n📝 INSTRUCTIONS:")
        print("1. Click Data → Datasets")
        print("2. Click + DATASET")
        print("3. Select 'Poverty Mapping DB'")
        print("4. Select schema 'public'")
        print("5. Select table 'v_gold_provincial_dashboard'")
        print("6. Click CREATE DATASET AND CREATE CHART")
        self.wait_for_user_input("Complete first dataset creation")
        
        # Step 4: Charts
        print("\n📋 STEP 4: CREATE CHARTS")
        self.show_chart_recommendations()
        print("\n📝 START WITH KPI CARD:")
        print("1. Chart Type: 'Big Number'")
        print("2. Metrics: SUM(population)")
        print("3. Title: 'Total Population'")
        print("4. Update Chart → Save")
        self.wait_for_user_input("Complete first chart creation")
        
        # Step 5: Dashboard
        print("\n📋 STEP 5: CREATE DASHBOARD")
        print("📝 INSTRUCTIONS:")
        print("1. Click Dashboards")
        print("2. Click + DASHBOARD")
        print("3. Title: 'Poverty Mapping Sumatera - Kelompok 18'")
        print("4. Save dashboard")
        print("5. Edit Dashboard → Add your charts")
        print("6. Arrange layout nicely")
        
        print("\n🎉 CONGRATULATIONS!")
        print("Follow the complete guide in: SUPERSET_DASHBOARD_STEP_BY_STEP_GUIDE.md")
        print("📊 Happy dashboard creation! 🚀")

def main():
    """Main execution"""
    try:
        assistant = SupersetDashboardAssistant()
        
        print("🤔 Choose your preferred mode:")
        print("1. 🚀 Interactive Step-by-Step Guide")
        print("2. 📋 Show Information Only")
        print("3. 🌐 Just Open Superset")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            assistant.run_interactive_guide()
        elif choice == "2":
            assistant.print_welcome()
            assistant.show_database_connection_info()
            assistant.show_datasets_info()
            assistant.show_chart_recommendations()
            assistant.show_step_by_step_guide()
            print(f"\n🌐 Access Superset: {assistant.superset_url}")
        elif choice == "3":
            assistant.open_superset()
        else:
            print("❌ Invalid choice. Opening Superset...")
            assistant.open_superset()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Process cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
