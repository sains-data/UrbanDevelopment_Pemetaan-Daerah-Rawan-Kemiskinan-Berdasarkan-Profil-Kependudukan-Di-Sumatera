#!/usr/bin/env python3
"""
Superset Dashboard Setup for Poverty Mapping
Kelompok 18 - Pemetaan Kemiskinan Sumatera

This script creates comprehensive dashboards in Apache Superset
for visualizing poverty data across Sumatra provinces.
"""

import pandas as pd
import sqlite3
import os
import time
from datetime import datetime

print("🎨 SUPERSET DASHBOARD SETUP")
print("=" * 60)
print("Kelompok 18 - Pemetaan Kemiskinan Sumatera")
print("Setting up comprehensive poverty mapping dashboards")
print("=" * 60)

# ============================================================================
# STEP 1: PREPARE DATA FOR SUPERSET
# ============================================================================
print("\n📊 STEP 1: Preparing Data for Superset")
print("-" * 50)

def prepare_poverty_data():
    """Load and prepare poverty data for Superset visualization"""
    try:
        # Load the poverty data
        df = pd.read_csv('data/Profil_Kemiskinan_Sumatera.csv')
        print(f"✅ Loaded {len(df):,} poverty records")
        
        # Add calculated fields for better visualization
        df['Poverty_Category'] = pd.cut(
            df['Persentase Kemiskinan (%)'], 
            bins=[0, 5, 10, 15, 100], 
            labels=['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
        )
        
        df['Economic_Health_Score'] = (
            100 - df['Persentase Kemiskinan (%)'] - 
            df['Tingkat Pengangguran (%)']
        )
        
        df['Population_Density_Score'] = df['Jumlah Penduduk (jiwa)'] / 1000
        
        df['Unemployment_Risk'] = pd.cut(
            df['Tingkat Pengangguran (%)'],
            bins=[0, 3, 6, 10, 100],
            labels=['Rendah', 'Sedang', 'Tinggi', 'Kritis']
        )
        
        # Add year column for time series (assuming current data)
        df['Year'] = 2025
        df['Date'] = pd.to_datetime('2025-01-01')
        
        print(f"✅ Enhanced data with calculated fields")
        return df
        
    except Exception as e:
        print(f"❌ Error preparing data: {e}")
        return None

# ============================================================================
# STEP 2: CREATE SQLITE DATABASE FOR SUPERSET
# ============================================================================
print("\n🗄️ STEP 2: Creating SQLite Database for Superset")
print("-" * 50)

def create_superset_database(df):
    """Create SQLite database that Superset can connect to"""
    try:
        # Create database directory if it doesn't exist
        os.makedirs('superset_data', exist_ok=True)
        
        # Connect to SQLite database
        db_path = 'superset_data/poverty_mapping.db'
        conn = sqlite3.connect(db_path)
        
        # Save main poverty data
        df.to_sql('poverty_data', conn, if_exists='replace', index=False)
        print(f"✅ Created table: poverty_data ({len(df)} records)")
        
        # Create aggregated tables for dashboard performance
        
        # Provincial summary
        province_summary = df.groupby('Provinsi').agg({
            'Persentase Kemiskinan (%)': ['mean', 'min', 'max', 'std'],
            'Tingkat Pengangguran (%)': 'mean',
            'Jumlah Penduduk (jiwa)': 'sum',
            'Economic_Health_Score': 'mean'
        }).round(2)
        
        # Flatten column names
        province_summary.columns = [
            'Avg_Poverty_Rate', 'Min_Poverty_Rate', 'Max_Poverty_Rate', 'Std_Poverty_Rate',
            'Avg_Unemployment_Rate', 'Total_Population', 'Avg_Economic_Health_Score'
        ]
        province_summary = province_summary.reset_index()
        province_summary.to_sql('province_summary', conn, if_exists='replace', index=False)
        print(f"✅ Created table: province_summary ({len(province_summary)} records)")
        
        # Poverty category distribution
        poverty_dist = df['Poverty_Category'].value_counts().reset_index()
        poverty_dist.columns = ['Category', 'Count']
        poverty_dist['Percentage'] = (poverty_dist['Count'] / len(df) * 100).round(1)
        poverty_dist.to_sql('poverty_distribution', conn, if_exists='replace', index=False)
        print(f"✅ Created table: poverty_distribution ({len(poverty_dist)} records)")
        
        # Top poverty areas
        top_poverty = df.nlargest(20, 'Persentase Kemiskinan (%)')
        top_poverty.to_sql('top_poverty_areas', conn, if_exists='replace', index=False)
        print(f"✅ Created table: top_poverty_areas ({len(top_poverty)} records)")
        
        # Best performing areas
        best_areas = df.nsmallest(20, 'Persentase Kemiskinan (%)')
        best_areas.to_sql('best_performing_areas', conn, if_exists='replace', index=False)
        print(f"✅ Created table: best_performing_areas ({len(best_areas)} records)")
        
        # Correlation analysis table
        correlation_data = []
        for province in df['Provinsi'].unique():
            prov_data = df[df['Provinsi'] == province]
            if len(prov_data) > 1:
                corr = prov_data['Persentase Kemiskinan (%)'].corr(
                    prov_data['Tingkat Pengangguran (%)']
                )
                correlation_data.append({
                    'Provinsi': province,
                    'Poverty_Unemployment_Correlation': round(corr, 3),
                    'Sample_Size': len(prov_data)
                })
        
        correlation_df = pd.DataFrame(correlation_data)
        correlation_df.to_sql('correlation_analysis', conn, if_exists='replace', index=False)
        print(f"✅ Created table: correlation_analysis ({len(correlation_df)} records)")
        
        conn.close()
        print(f"✅ Database created successfully: {db_path}")
        return db_path
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return None

# ============================================================================
# STEP 3: GENERATE SUPERSET DASHBOARD CONFIGURATIONS
# ============================================================================
print("\n🎨 STEP 3: Generating Dashboard Configurations")
print("-" * 50)

def create_dashboard_configs():
    """Create dashboard configuration templates for Superset"""
    
    dashboard_configs = {
        "poverty_overview": {
            "dashboard_title": "📊 Poverty Overview - Sumatra",
            "description": "Comprehensive overview of poverty distribution across Sumatra provinces",
            "charts": [
                {
                    "chart_name": "Provincial Poverty Rates",
                    "chart_type": "bar",
                    "table": "province_summary",
                    "x_axis": "Provinsi",
                    "y_axis": "Avg_Poverty_Rate",
                    "description": "Average poverty rates by province"
                },
                {
                    "chart_name": "Poverty Distribution",
                    "chart_type": "pie",
                    "table": "poverty_distribution",
                    "x_axis": "Category",
                    "y_axis": "Count",
                    "description": "Distribution of poverty categories"
                },
                {
                    "chart_name": "Population vs Poverty",
                    "chart_type": "scatter",
                    "table": "poverty_data",
                    "x_axis": "Jumlah Penduduk (jiwa)",
                    "y_axis": "Persentase Kemiskinan (%)",
                    "description": "Relationship between population and poverty"
                }
            ]
        },
        
        "economic_analysis": {
            "dashboard_title": "💼 Economic Health Analysis",
            "description": "Economic indicators and unemployment analysis",
            "charts": [
                {
                    "chart_name": "Economic Health Score by Province",
                    "chart_type": "bar",
                    "table": "province_summary",
                    "x_axis": "Provinsi",
                    "y_axis": "Avg_Economic_Health_Score",
                    "description": "Economic health scoring across provinces"
                },
                {
                    "chart_name": "Unemployment vs Poverty Correlation",
                    "chart_type": "scatter",
                    "table": "poverty_data",
                    "x_axis": "Tingkat Pengangguran (%)",
                    "y_axis": "Persentase Kemiskinan (%)",
                    "description": "Correlation between unemployment and poverty"
                },
                {
                    "chart_name": "Top 20 Poverty Areas",
                    "chart_type": "table",
                    "table": "top_poverty_areas",
                    "description": "Areas with highest poverty rates"
                }
            ]
        },
        
        "comparative_analysis": {
            "dashboard_title": "🔍 Comparative Analysis",
            "description": "Comparative analysis between provinces and commodities",
            "charts": [
                {
                    "chart_name": "Province Performance Comparison",
                    "chart_type": "line",
                    "table": "province_summary",
                    "x_axis": "Provinsi",
                    "y_axis": ["Avg_Poverty_Rate", "Avg_Unemployment_Rate"],
                    "description": "Multi-metric comparison across provinces"
                },
                {
                    "chart_name": "Best Performing Areas",
                    "chart_type": "table",
                    "table": "best_performing_areas",
                    "description": "Areas with lowest poverty rates"
                },
                {
                    "chart_name": "Poverty Variability by Province",
                    "chart_type": "bar",
                    "table": "province_summary",
                    "x_axis": "Provinsi",
                    "y_axis": "Std_Poverty_Rate",
                    "description": "Poverty rate variability within provinces"
                }
            ]
        }
    }
    
    # Save configuration as JSON for reference
    import json
    with open('superset_data/dashboard_configs.json', 'w') as f:
        json.dump(dashboard_configs, f, indent=2)
    
    print(f"✅ Created {len(dashboard_configs)} dashboard configurations")
    return dashboard_configs

# ============================================================================
# STEP 4: GENERATE MANUAL SETUP INSTRUCTIONS
# ============================================================================
print("\n📋 STEP 4: Generating Setup Instructions")
print("-" * 50)

def create_setup_instructions(db_path):
    """Create detailed setup instructions for Superset"""
    
    instructions = f"""
# 🎨 SUPERSET DASHBOARD SETUP INSTRUCTIONS
## Kelompok 18 - Pemetaan Kemiskinan Sumatera

### 📊 DATABASE CONNECTION
1. **Access Superset**: http://localhost:8089
2. **Login Credentials**:
   - Username: `admin`
   - Password: `admin`

3. **Add Database Connection**:
   - Go to Settings → Database Connections
   - Click "+ DATABASE"
   - Select "SQLite"
   - Database Name: `poverty_mapping`
   - SQLAlchemy URI: `sqlite:///{os.path.abspath(db_path)}`

### 📈 AVAILABLE TABLES
- `poverty_data` - Main poverty dataset ({df.shape[0]} records)
- `province_summary` - Provincial aggregations
- `poverty_distribution` - Category distributions
- `top_poverty_areas` - Highest poverty areas
- `best_performing_areas` - Best performing areas
- `correlation_analysis` - Statistical correlations

### 🎯 SUGGESTED DASHBOARDS

#### 1. 📊 POVERTY OVERVIEW DASHBOARD
**Charts to Create:**
- **Bar Chart**: Provincial Poverty Rates
  - Table: `province_summary`
  - X-axis: `Provinsi`
  - Y-axis: `Avg_Poverty_Rate`

- **Pie Chart**: Poverty Distribution
  - Table: `poverty_distribution`
  - Dimension: `Category`
  - Metric: `Count`

- **Scatter Plot**: Population vs Poverty
  - Table: `poverty_data`
  - X-axis: `Jumlah Penduduk (jiwa)`
  - Y-axis: `Persentase Kemiskinan (%)`

#### 2. 💼 ECONOMIC ANALYSIS DASHBOARD
**Charts to Create:**
- **Bar Chart**: Economic Health Score
  - Table: `province_summary`
  - X-axis: `Provinsi`
  - Y-axis: `Avg_Economic_Health_Score`

- **Scatter Plot**: Unemployment vs Poverty
  - Table: `poverty_data`
  - X-axis: `Tingkat Pengangguran (%)`
  - Y-axis: `Persentase Kemiskinan (%)`

- **Table**: Top Poverty Areas
  - Table: `top_poverty_areas`
  - Columns: `Provinsi`, `Komoditas`, `Persentase Kemiskinan (%)`

#### 3. 🔍 COMPARATIVE ANALYSIS DASHBOARD
**Charts to Create:**
- **Multi-Line Chart**: Province Comparison
  - Table: `province_summary`
  - X-axis: `Provinsi`
  - Y-axis: `Avg_Poverty_Rate`, `Avg_Unemployment_Rate`

- **Heatmap**: Correlation Matrix
  - Table: `correlation_analysis`
  - Dimensions: `Provinsi`
  - Metric: `Poverty_Unemployment_Correlation`

### 🎨 STYLING RECOMMENDATIONS
- **Color Scheme**: Use red gradient for high poverty, green for low poverty
- **Filters**: Add province and category filters to all dashboards
- **Time Period**: Include year filter for future data updates
- **Export Options**: Enable CSV/PDF export for reports

### 📊 ADVANCED FEATURES
1. **Alerts**: Set up alerts for provinces with poverty > 15%
2. **Scheduled Reports**: Weekly/monthly dashboard emails
3. **SQL Lab**: Custom queries for ad-hoc analysis
4. **Annotations**: Add policy change markers on charts

### 🔧 TROUBLESHOOTING
- **Connection Issues**: Verify SQLite file path is accessible
- **Chart Errors**: Check table names and column names
- **Performance**: Use aggregated tables for better performance
- **Data Updates**: Refresh tables when new data is available

### 📈 EXPECTED VISUALIZATIONS
After setup, you'll have:
- 📊 Provincial poverty rate comparisons
- 🥧 Poverty category distributions
- 📈 Economic health trending
- 🗺️ Geographic poverty mapping
- 📉 Correlation analysis visualizations
- 📋 Executive summary tables

---
**Database Path**: {os.path.abspath(db_path)}
**Superset URL**: http://localhost:8089
**Setup Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Save instructions
    with open('superset_data/setup_instructions.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ Setup instructions saved to: superset_data/setup_instructions.md")
    return instructions

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    print(f"\n🚀 Starting Superset Dashboard Setup...")
    
    # Step 1: Prepare data
    df = prepare_poverty_data()
    if df is None:
        print("❌ Failed to prepare data. Exiting.")
        return
    
    # Step 2: Create database
    db_path = create_superset_database(df)
    if db_path is None:
        print("❌ Failed to create database. Exiting.")
        return
    
    # Step 3: Create dashboard configs
    configs = create_dashboard_configs()
    
    # Step 4: Create setup instructions
    instructions = create_setup_instructions(db_path)
    
    # Summary
    print(f"\n🎉 SUPERSET SETUP COMPLETED!")
    print("=" * 60)
    print(f"✅ Data prepared: {len(df):,} records")
    print(f"✅ Database created: {db_path}")
    print(f"✅ Dashboard configs: {len(configs)} templates")
    print(f"✅ Setup instructions: superset_data/setup_instructions.md")
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Access Superset: http://localhost:8089")
    print(f"2. Login: admin/admin")
    print(f"3. Follow setup instructions to create dashboards")
    print(f"4. Build beautiful poverty mapping visualizations!")
    print("=" * 60)

if __name__ == "__main__":
    main()
