#!/usr/bin/env python3
"""
Test script for Gold Layer to Superset Integration
"""
import sys
import traceback

try:
    print("=" * 70)
    print("🏆 TESTING GOLD LAYER TO SUPERSET INTEGRATION")
    print("📊 Kelompok 18 - Big Data Pipeline")
    print("=" * 70)
    
    # Import required modules
    print("📦 Importing required modules...")
    import pandas as pd
    import psycopg2
    from sqlalchemy import create_engine
    import logging
    from datetime import datetime
    print("✅ All modules imported successfully!")
    
    # Test PostgreSQL connection
    print("\n🔍 Testing PostgreSQL connection...")
    postgres_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'poverty_mapping',
        'user': 'postgres',
        'password': 'postgres123'
    }
    
    try:
        engine = create_engine(f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}")
        conn = engine.connect()
        print("✅ PostgreSQL connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("🔧 Trying to create database...")
        
        # Try connecting to postgres database first
        try:
            engine_root = create_engine(f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}:{postgres_config['port']}/postgres")
            conn_root = engine_root.connect()
            conn_root.execution_options(autocommit=True)
            conn_root.execute(f"CREATE DATABASE {postgres_config['database']};")
            conn_root.close()
            print(f"✅ Database '{postgres_config['database']}' created successfully!")
        except Exception as create_error:
            print(f"⚠️  Database creation info: {create_error}")
    
    # Create sample Gold layer data
    print("\n📊 Creating sample Gold layer data...")
    
    # Sample Provincial Poverty Summary
    province_data = {
        'province_name': ['Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 
                         'Sumatera Selatan', 'Bengkulu', 'Lampung', 'Kepulauan Bangka Belitung'],
        'poverty_rate': [15.97, 8.75, 6.65, 7.42, 7.65, 12.55, 15.43, 12.25, 4.55],
        'population': [5371010, 14799361, 5534472, 6394087, 3548228, 8467432, 2010670, 8205141, 1448319],
        'poor_population': [857924, 1294939, 368045, 474905, 271474, 1062663, 310333, 1005630, 65898],
        'poverty_depth_index': [3.12, 1.58, 1.23, 1.45, 1.48, 2.85, 3.01, 2.65, 0.89],
        'poverty_severity_index': [0.82, 0.35, 0.28, 0.34, 0.36, 0.73, 0.78, 0.67, 0.20],
        'avg_consumption_per_capita': [789123, 1045678, 1123456, 1087654, 1065432, 856789, 798765, 845321, 1289654],
        'risk_category': ['High', 'Medium', 'Low', 'Low', 'Low', 'High', 'High', 'High', 'Low'],
        'data_year': [2024] * 9,
        'last_updated': [datetime.now()] * 9
    }
    
    province_df = pd.DataFrame(province_data)
    print(f"✅ Created provincial data with {len(province_df)} records")
    
    # Sample Poverty Statistics
    stats_data = {
        'stat_name': ['avg_national_poverty', 'total_provinces', 'high_risk_provinces', 'avg_consumption'],
        'stat_value': [10.56, 9, 4, 945567],
        'stat_description': [
            'Average poverty rate across Sumatera provinces',
            'Total provinces analyzed',
            'Provinces with high poverty risk',
            'Average consumption per capita'
        ],
        'calculation_timestamp': [datetime.now()] * 4
    }
    
    stats_df = pd.DataFrame(stats_data)
    print(f"✅ Created statistics data with {len(stats_df)} records")
    
    # Save to PostgreSQL
    print("\n💾 Saving Gold layer data to PostgreSQL...")
    
    engine = create_engine(f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}")
    
    # Save province data
    province_df.to_sql('gold_province_poverty_summary', engine, if_exists='replace', index=False)
    print("✅ Saved gold_province_poverty_summary table")
    
    # Save statistics data  
    stats_df.to_sql('gold_poverty_statistics', engine, if_exists='replace', index=False)
    print("✅ Saved gold_poverty_statistics table")
    
    # Create Superset-optimized views
    print("\n🎯 Creating Superset-optimized views...")
    
    with engine.connect() as conn:
        # Provincial Dashboard View
        dashboard_view = """
        CREATE OR REPLACE VIEW v_gold_provincial_dashboard AS
        SELECT 
            province_name,
            poverty_rate,
            population,
            poor_population,
            ROUND((poor_population::FLOAT / population * 100), 2) as poverty_percentage,
            poverty_depth_index,
            poverty_severity_index,
            avg_consumption_per_capita,
            risk_category,
            data_year,
            CASE 
                WHEN poverty_rate >= 12 THEN 'High Risk'
                WHEN poverty_rate >= 8 THEN 'Medium Risk'
                ELSE 'Low Risk'
            END as risk_level_detailed,
            CASE 
                WHEN avg_consumption_per_capita >= 1100000 THEN 'High Income'
                WHEN avg_consumption_per_capita >= 900000 THEN 'Medium Income'
                ELSE 'Low Income'
            END as income_category
        FROM gold_province_poverty_summary
        ORDER BY poverty_rate DESC;
        """
        
        conn.execute(dashboard_view)
        print("✅ Created v_gold_provincial_dashboard view")
        
        # Poverty Hotspots View
        hotspots_view = """
        CREATE OR REPLACE VIEW v_gold_poverty_hotspots AS
        SELECT 
            province_name,
            poverty_rate,
            poor_population,
            risk_category,
            poverty_depth_index,
            'Needs Immediate Attention' as priority
        FROM gold_province_poverty_summary
        WHERE poverty_rate >= 12
        UNION ALL
        SELECT 
            province_name,
            poverty_rate,
            poor_population,
            risk_category,
            poverty_depth_index,
            'Monitor Closely' as priority
        FROM gold_province_poverty_summary
        WHERE poverty_rate >= 8 AND poverty_rate < 12
        ORDER BY poverty_rate DESC;
        """
        
        conn.execute(hotspots_view)
        print("✅ Created v_gold_poverty_hotspots view")
        
        # Summary Statistics View
        summary_view = """
        CREATE OR REPLACE VIEW v_gold_summary_stats AS
        SELECT 
            COUNT(*) as total_provinces,
            ROUND(AVG(poverty_rate), 2) as avg_poverty_rate,
            ROUND(SUM(poor_population), 0) as total_poor_population,
            ROUND(SUM(population), 0) as total_population,
            ROUND(AVG(avg_consumption_per_capita), 0) as avg_consumption,
            COUNT(CASE WHEN poverty_rate >= 12 THEN 1 END) as high_risk_provinces,
            COUNT(CASE WHEN poverty_rate < 8 THEN 1 END) as low_risk_provinces
        FROM gold_province_poverty_summary;
        """
        
        conn.execute(summary_view)
        print("✅ Created v_gold_summary_stats view")
    
    # Verify data
    print("\n🔍 Verifying created tables and views...")
    
    with engine.connect() as conn:
        # Check tables
        tables_result = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'gold_%';")
        tables = [row[0] for row in tables_result]
        print(f"📊 Created tables: {tables}")
        
        # Check views
        views_result = conn.execute("SELECT viewname FROM pg_views WHERE schemaname = 'public' AND viewname LIKE 'v_gold_%';")
        views = [row[0] for row in views_result]
        print(f"👁️  Created views: {views}")
        
        # Sample data from main view
        sample_result = conn.execute("SELECT province_name, poverty_rate, risk_level_detailed FROM v_gold_provincial_dashboard LIMIT 3;")
        print("\n📋 Sample data from v_gold_provincial_dashboard:")
        for row in sample_result:
            print(f"   • {row[0]}: {row[1]}% poverty rate, {row[2]}")
    
    print("\n" + "=" * 70)
    print("🎉 SUCCESS! Gold layer data integration completed!")
    print("📊 Tables and views created in PostgreSQL")
    print("🔗 Ready for Superset dashboard creation")
    print("=" * 70)
    print("\n📋 NEXT STEPS:")
    print("1. Open Superset: http://localhost:8089")
    print("2. Add PostgreSQL database connection:")
    print(f"   - Host: {postgres_config['host']}")
    print(f"   - Port: {postgres_config['port']}")
    print(f"   - Database: {postgres_config['database']}")
    print(f"   - Username: {postgres_config['user']}")
    print("3. Create charts using the views:")
    print("   - v_gold_provincial_dashboard (main dashboard)")
    print("   - v_gold_poverty_hotspots (risk analysis)")
    print("   - v_gold_summary_stats (overview metrics)")
    print("=" * 70)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"🔍 Error details: {traceback.format_exc()}")
    sys.exit(1)
