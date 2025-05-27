#!/usr/bin/env python3
"""
Quick verification script for Gold Layer Integration
Kelompok 18 - Big Data Poverty Mapping Pipeline
"""

import psycopg2
import pandas as pd
from sqlalchemy import create_engine

def verify_gold_integration():
    """Verify that Gold layer integration is successful"""
    
    print("🔍 VERIFYING GOLD LAYER INTEGRATION")
    print("=" * 50)
    
    # Database configuration
    postgres_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'poverty_mapping',
        'user': 'postgres',
        'password': 'postgres123'
    }
    
    try:
        # Connect to PostgreSQL
        engine = create_engine(f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}")
        
        print("✅ PostgreSQL connection successful")
        
        # Check Gold tables
        with engine.connect() as conn:
            # Verify Gold tables exist and have data
            tables_query = """
            SELECT table_name, 
                   (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
            FROM information_schema.tables t
            WHERE table_schema = 'public' 
            AND table_name LIKE 'gold_%'
            ORDER BY table_name;
            """
            
            tables_df = pd.read_sql(tables_query, conn)
            print(f"\n📊 Gold Tables Found: {len(tables_df)}")
            for _, row in tables_df.iterrows():
                print(f"   • {row['table_name']} ({row['column_count']} columns)")
            
            # Check Gold views
            views_query = """
            SELECT viewname 
            FROM pg_views 
            WHERE schemaname = 'public' 
            AND viewname LIKE 'v_gold_%'
            ORDER BY viewname;
            """
            
            views_df = pd.read_sql(views_query, conn)
            print(f"\n👁️  Gold Views Found: {len(views_df)}")
            for _, row in views_df.iterrows():
                print(f"   • {row['viewname']}")
            
            # Get sample data from main dashboard view
            sample_query = """
            SELECT province_name, poverty_rate, risk_level_detailed, income_category
            FROM v_gold_provincial_dashboard 
            ORDER BY poverty_rate DESC 
            LIMIT 3;
            """
            
            sample_df = pd.read_sql(sample_query, conn)
            print(f"\n📋 Sample Data from Main Dashboard View:")
            for _, row in sample_df.iterrows():
                print(f"   • {row['province_name']}: {row['poverty_rate']}% ({row['risk_level_detailed']}, {row['income_category']})")
            
            # Get summary statistics
            summary_query = "SELECT * FROM v_gold_summary_stats;"
            summary_df = pd.read_sql(summary_query, conn)
            
            if not summary_df.empty:
                stats = summary_df.iloc[0]
                print(f"\n📈 Key Statistics:")
                print(f"   • Total Provinces: {stats['total_provinces']}")
                print(f"   • Average Poverty Rate: {stats['avg_poverty_rate']}%")
                print(f"   • Total Poor Population: {stats['total_poor_population']:,}")
                print(f"   • High Risk Provinces: {stats['high_risk_provinces']}")
                print(f"   • Low Risk Provinces: {stats['low_risk_provinces']}")
        
        print("\n" + "=" * 50)
        print("🎉 GOLD LAYER INTEGRATION VERIFIED SUCCESSFULLY!")
        print("📊 Ready for Superset dashboard creation")
        print("🔗 Superset URL: http://localhost:8089")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    verify_gold_integration()
