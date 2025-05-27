"""
📊 SUPERSET CHART CREATION SCRIPT - REAL COLUMN SCHEMA
=====================================================
Kelompok 18 - Enhanced Dashboard with Actual Data Columns

This script provides exact configurations for your dataset columns:
- province_name, poverty_rate, population, poor_population
- poverty_depth_index, poverty_severity_index, avg_consumption_per_capita
- risk_category, data_year, last_updated
"""

import json
from datetime import datetime

def print_header():
    print("🎯 SUPERSET ENHANCED DASHBOARD CONFIGURATION")
    print("=" * 60)
    print("Using YOUR ACTUAL DATASET COLUMNS:")
    print("📍 province_name, 📊 poverty_rate, 👥 population")  
    print("💰 avg_consumption_per_capita, 🎯 risk_category")
    print("📈 poverty_depth_index, 📉 poverty_severity_index")
    print("=" * 60)

def get_chart_configs():
    """Return exact chart configurations for your columns"""
    
    configs = {
        "kpi_cards": {
            "total_population": {
                "chart_type": "Big Number",
                "metric": "SUM(population)",
                "title": "Total Population", 
                "number_format": ",d",
                "color": "#1f77b4",
                "subtitle": "3 Sumatera Provinces"
            },
            "avg_poverty_rate": {
                "chart_type": "Big Number", 
                "metric": "AVG(poverty_rate)",
                "title": "Average Poverty Rate",
                "number_format": ".2%",
                "color": "#d62728", 
                "subtitle": "Provincial Average"
            },
            "total_poor": {
                "chart_type": "Big Number",
                "metric": "SUM(poor_population)", 
                "title": "Total Poor Population",
                "number_format": ",d",
                "color": "#d62728",
                "subtitle": "People Below Poverty Line"
            },
            "avg_consumption": {
                "chart_type": "Big Number",
                "metric": "AVG(avg_consumption_per_capita)",
                "title": "Avg Consumption Per Capita", 
                "number_format": ",d",
                "color": "#2ca02c",
                "subtitle": "Economic Health (IDR)"
            }
        },
        
        "main_charts": {
            "poverty_bar": {
                "chart_type": "Bar Chart",
                "dimension": "province_name",
                "metric": "poverty_rate", 
                "title": "Poverty Rate by Province",
                "sort": "Descending",
                "color_scheme": "Sequential Red",
                "show_values": True,
                "value_format": ".2%"
            },
            "risk_gauge": {
                "chart_type": "Gauge Chart",
                "metric": "AVG(poverty_rate)",
                "title": "Overall Poverty Risk Level",
                "min_value": 0,
                "max_value": 25,
                "target_value": 15,
                "ranges": {
                    "low": {"min": 0, "max": 10, "color": "green"},
                    "medium": {"min": 10, "max": 15, "color": "yellow"},
                    "high": {"min": 15, "max": 25, "color": "red"}
                }
            }
        },
        
        "distribution_charts": {
            "population_pie": {
                "chart_type": "Pie Chart",
                "dimension": "province_name",
                "metric": "population",
                "title": "Population Distribution",
                "show_labels": True,
                "show_values": True,
                "legend_position": "right"
            },
            "poor_population_hbar": {
                "chart_type": "Bar Chart",
                "orientation": "horizontal", 
                "dimension": "province_name",
                "metric": "poor_population",
                "title": "Poor Population Count by Province",
                "sort": "Descending",
                "color_scheme": "Sequential Red"
            }
        },
        
        "analysis_charts": {
            "depth_severity_scatter": {
                "chart_type": "Scatter Plot",
                "x_axis": "poverty_depth_index",
                "y_axis": "poverty_severity_index", 
                "size": "poor_population",
                "series": "province_name",
                "title": "Poverty Depth vs Severity Analysis",
                "show_labels": True
            },
            "risk_donut": {
                "chart_type": "Pie Chart",
                "dimension": "risk_category",
                "metric": "COUNT(*)",
                "title": "Risk Category Distribution", 
                "donut": True,
                "inner_radius": 40,
                "colors": {
                    "High": "#ff4444",
                    "Medium": "#ff8800", 
                    "Low": "#44ff44"
                }
            }
        },
        
        "comprehensive_table": {
            "complete_stats": {
                "chart_type": "Table",
                "columns": [
                    {"name": "province_name", "label": "Province"},
                    {"name": "poverty_rate", "label": "Poverty Rate (%)", "format": ".2%"},
                    {"name": "population", "label": "Population", "format": ",d"},
                    {"name": "poor_population", "label": "Poor Population", "format": ",d"},
                    {"name": "poverty_depth_index", "label": "Depth Index", "format": ".2f"},
                    {"name": "poverty_severity_index", "label": "Severity Index", "format": ".2f"},
                    {"name": "avg_consumption_per_capita", "label": "Avg Consumption (IDR)", "format": ",d"},
                    {"name": "risk_category", "label": "Risk Level"},
                    {"name": "data_year", "label": "Year"}
                ],
                "title": "Complete Province Statistics",
                "sortable": True,
                "searchable": True
            }
        }
    }
    
    return configs

def display_step_by_step():
    """Display step-by-step implementation guide"""
    
    print("\n🔧 STEP-BY-STEP IMPLEMENTATION GUIDE")
    print("=" * 50)
    
    configs = get_chart_configs()
    
    # ROW 1: KPI Cards
    print("\n📊 ROW 1 - KPI CARDS (4 cards):")
    print("-" * 30)
    for i, (key, config) in enumerate(configs["kpi_cards"].items(), 1):
        print(f"\n{i}. {config['title']}:")
        print(f"   • Chart Type: {config['chart_type']}")
        print(f"   • Metric: {config['metric']}")
        print(f"   • Format: {config['number_format']}")
        print(f"   • Color: {config['color']}")
        print(f"   • Save as: KPI_{key}")
    
    # ROW 2: Main Charts
    print("\n\n🎯 ROW 2 - MAIN INSIGHTS (2 large charts):")
    print("-" * 40)
    for i, (key, config) in enumerate(configs["main_charts"].items(), 1):
        print(f"\n{i}. {config['title']}:")
        print(f"   • Chart Type: {config['chart_type']}")
        if 'dimension' in config:
            print(f"   • Dimension: {config['dimension']}")
        print(f"   • Metric: {config['metric']}")
        print(f"   • Save as: {key}")
    
    # ROW 3: Distribution
    print("\n\n🥧 ROW 3 - DISTRIBUTION ANALYSIS (2 medium charts):")
    print("-" * 45)
    for i, (key, config) in enumerate(configs["distribution_charts"].items(), 1):
        print(f"\n{i}. {config['title']}:")
        print(f"   • Chart Type: {config['chart_type']}")
        print(f"   • Dimension: {config['dimension']}")
        print(f"   • Metric: {config['metric']}")
        print(f"   • Save as: {key}")
    
    # ROW 4: Analysis
    print("\n\n📈 ROW 4 - POVERTY INDICES ANALYSIS (2 medium charts):")
    print("-" * 50)
    for i, (key, config) in enumerate(configs["analysis_charts"].items(), 1):
        print(f"\n{i}. {config['title']}:")
        print(f"   • Chart Type: {config['chart_type']}")
        if 'x_axis' in config:
            print(f"   • X-axis: {config['x_axis']}")
            print(f"   • Y-axis: {config['y_axis']}")
        else:
            print(f"   • Dimension: {config['dimension']}")
            print(f"   • Metric: {config['metric']}")
        print(f"   • Save as: {key}")
    
    # ROW 5: Table
    print("\n\n📋 ROW 5 - COMPREHENSIVE TABLE (full width):")
    print("-" * 45)
    table_config = configs["comprehensive_table"]["complete_stats"]
    print(f"\n1. {table_config['title']}:")
    print(f"   • Chart Type: {table_config['chart_type']}")
    print(f"   • Columns: {len(table_config['columns'])} fields")
    print("   • All your dataset columns included!")
    print("   • Sortable & Searchable: Yes")

def show_validation_queries():
    """Show SQL queries to validate your data"""
    
    print("\n\n💾 DATA VALIDATION QUERIES")
    print("=" * 35)
    
    queries = {
        "basic_preview": """
-- Basic data preview
SELECT 
    province_name,
    poverty_rate,
    population, 
    poor_population,
    poverty_depth_index,
    poverty_severity_index,
    avg_consumption_per_capita,
    risk_category,
    data_year
FROM your_dataset_name
ORDER BY poverty_rate DESC;
""",
        
        "kpi_calculations": """
-- KPI metrics calculation  
SELECT 
    COUNT(*) as total_provinces,
    ROUND(AVG(poverty_rate), 2) as avg_poverty_rate,
    SUM(population) as total_population,
    SUM(poor_population) as total_poor_population,
    ROUND(AVG(avg_consumption_per_capita), 0) as avg_consumption
FROM your_dataset_name;
""",
        
        "risk_distribution": """
-- Risk category breakdown
SELECT 
    risk_category,
    COUNT(*) as province_count,
    ROUND(AVG(poverty_rate), 2) as avg_poverty_in_category,
    ROUND(AVG(poverty_depth_index), 2) as avg_depth,
    ROUND(AVG(poverty_severity_index), 2) as avg_severity
FROM your_dataset_name
GROUP BY risk_category
ORDER BY avg_poverty_in_category DESC;
""",
        
        "correlation_check": """
-- Poverty indices correlation
SELECT 
    province_name,
    poverty_rate,
    poverty_depth_index,
    poverty_severity_index,
    (poverty_depth_index * poverty_severity_index) as poverty_intensity_score
FROM your_dataset_name
ORDER BY poverty_intensity_score DESC;
"""
    }
    
    for query_name, sql in queries.items():
        print(f"\n🔍 {query_name.replace('_', ' ').title()}:")
        print(sql)

def main():
    """Main execution function"""
    print_header()
    display_step_by_step()
    show_validation_queries()
    
    print("\n\n🎨 COLOR SCHEME REFERENCE:")
    print("=" * 30)
    color_scheme = {
        "Population": "#1f77b4 (Blue)",
        "Poverty Rate": "#d62728 (Red)", 
        "Poor Population": "#cc0000 (Dark Red)",
        "Consumption": "#2ca02c (Green)",
        "Depth Index": "#ff7f0e (Orange)",
        "Severity Index": "#9467bd (Purple)",
        "High Risk": "#ff4444 (Bright Red)",
        "Medium Risk": "#ff8800 (Orange)",
        "Low Risk": "#44ff44 (Bright Green)"
    }
    
    for metric, color in color_scheme.items():
        print(f"• {metric}: {color}")
    
    print("\n\n🚀 QUICK ACCESS LINKS:")
    print("=" * 25)
    print("🌐 Superset: http://localhost:8088")
    print("📊 Charts: http://localhost:8088/chart/list/")
    print("📈 Dashboards: http://localhost:8088/dashboard/list/")
    print("📋 Datasets: http://localhost:8088/tablemodelview/list/")
    
    print("\n\n✅ READY TO CREATE ENHANCED DASHBOARD!")
    print("Your rich dataset with poverty indices provides deep analytical insights!")
    print("\n🎯 Total Charts to Create: 11")
    print("📊 4 KPI Cards + 6 Visualizations + 1 Comprehensive Table")
    
    # Save configuration 
    configs = get_chart_configs()
    with open("enhanced_dashboard_config.json", "w") as f:
        json.dump(configs, f, indent=2)
    
    print(f"\n💾 Configuration saved to: enhanced_dashboard_config.json")
    print("📝 Use this file as reference during chart creation!")

if __name__ == "__main__":
    main()
