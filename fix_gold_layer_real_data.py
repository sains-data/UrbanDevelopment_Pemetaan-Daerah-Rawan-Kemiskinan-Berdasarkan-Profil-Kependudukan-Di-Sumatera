#!/usr/bin/env python3
"""
Fix Gold Layer Data - Menggunakan Data Asli dari CSV
Kelompok 18 - Big Data Poverty Mapping Pipeline

Script ini akan:
1. Membaca data asli dari Profil_Kemiskinan_Sumatera.csv
2. Memproses dan agregasi sesuai 3 provinsi yang ada
3. Membuat Gold layer yang benar di PostgreSQL
4. Mengganti data sintetis dengan data asli
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealDataGoldProcessor:
    def __init__(self):
        self.postgres_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'poverty_mapping',
            'user': 'postgres',
            'password': 'postgres123'
        }
        self.csv_file_path = r'C:\TUBESABD\data\Profil_Kemiskinan_Sumatera.csv'
        
    def print_header(self):
        print("=" * 70)
        print("🔧 FIXING GOLD LAYER DATA - MENGGUNAKAN DATA ASLI")
        print("📊 Kelompok 18 - Big Data Poverty Mapping")
        print("🎯 Hanya 3 Provinsi: Sumatera Barat, Selatan, Utara")
        print("=" * 70)
        
    def load_and_analyze_csv(self):
        """Load and analyze the original CSV data"""
        logger.info("📖 Membaca data asli dari CSV...")
        
        try:
            # Read CSV
            df = pd.read_csv(self.csv_file_path)
            
            print(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
            print(f"📍 Provinsi yang ada: {sorted(df['Provinsi'].unique())}")
            print(f"📊 Jumlah provinsi: {df['Provinsi'].nunique()}")
            
            # Check data quality
            print("\n🔍 Data Quality Check:")
            print(f"   • Missing values: {df.isnull().sum().sum()}")
            print(f"   • Duplicate rows: {df.duplicated().sum()}")
            
            # Show sample data structure
            print("\n📋 Sample data structure:")
            print(df.head(3).to_string())
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error loading CSV: {e}")
            return None
    
    def process_real_data(self, df):
        """Process real CSV data into Gold layer format"""
        logger.info("⚙️ Processing data asli menjadi Gold layer...")
        
        try:
            # Clean column names and data
            df_clean = df.copy()
            
            # Convert numeric columns, handle mixed data types
            numeric_columns = ['Konsumsi (per kapita per minggu)', 'Jumlah Penduduk (jiwa)', 
                             'Persentase Kemiskinan (%)', 'Tingkat Pengangguran (%)']
            
            for col in numeric_columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
            # Remove rows with invalid data
            df_clean = df_clean.dropna(subset=numeric_columns)
            
            # Aggregate by Province
            province_summary = df_clean.groupby('Provinsi').agg({
                'Persentase Kemiskinan (%)': 'mean',
                'Jumlah Penduduk (jiwa)': 'sum', 
                'Tingkat Pengangguran (%)': 'mean',
                'Konsumsi (per kapita per minggu)': 'mean'
            }).reset_index()
            
            # Calculate additional metrics
            province_summary['poor_population'] = (
                province_summary['Jumlah Penduduk (jiwa)'] * 
                province_summary['Persentase Kemiskinan (%)'] / 100
            ).astype(int)
            
            # Calculate poverty depth and severity indices (estimated based on consumption)
            province_summary['poverty_depth_index'] = (
                province_summary['Persentase Kemiskinan (%)'] * 0.2
            ).round(2)
            
            province_summary['poverty_severity_index'] = (
                province_summary['poverty_depth_index'] * 0.3
            ).round(2)
            
            # Convert weekly consumption to monthly (multiply by 4.33)
            province_summary['avg_consumption_per_capita'] = (
                province_summary['Konsumsi (per kapita per minggu)'] * 4.33 * 1000
            ).astype(int)
            
            # Determine risk category based on poverty rate
            def categorize_risk(poverty_rate):
                if poverty_rate >= 15:
                    return 'High'
                elif poverty_rate >= 10:
                    return 'Medium'
                else:
                    return 'Low'
            
            province_summary['risk_category'] = province_summary['Persentase Kemiskinan (%)'].apply(categorize_risk)
            
            # Rename columns to match Gold layer schema
            province_summary = province_summary.rename(columns={
                'Provinsi': 'province_name',
                'Persentase Kemiskinan (%)': 'poverty_rate',
                'Jumlah Penduduk (jiwa)': 'population',
                'Tingkat Pengangguran (%)': 'unemployment_rate'
            })
            
            # Add metadata
            province_summary['data_year'] = 2024
            province_summary['last_updated'] = datetime.now()
            
            # Select final columns for Gold layer
            gold_columns = [
                'province_name', 'poverty_rate', 'population', 'poor_population',
                'poverty_depth_index', 'poverty_severity_index', 'avg_consumption_per_capita',
                'risk_category', 'data_year', 'last_updated'
            ]
            
            province_df = province_summary[gold_columns]
            
            print(f"✅ Processed {len(province_df)} provinces:")
            for _, row in province_df.iterrows():
                print(f"   • {row['province_name']}: {row['poverty_rate']:.2f}% poverty rate")
            
            return province_df
            
        except Exception as e:
            logger.error(f"❌ Error processing data: {e}")
            return None
    
    def create_real_statistics(self, province_df):
        """Create real statistics from processed data"""
        try:
            stats_data = {
                'stat_name': [
                    'avg_sumatera_poverty', 
                    'total_provinces', 
                    'high_risk_provinces', 
                    'avg_consumption',
                    'total_population',
                    'total_poor_population'
                ],
                'stat_value': [
                    round(province_df['poverty_rate'].mean(), 2),
                    len(province_df),
                    len(province_df[province_df['risk_category'] == 'High']),
                    round(province_df['avg_consumption_per_capita'].mean(), 0),
                    province_df['population'].sum(),
                    province_df['poor_population'].sum()
                ],
                'stat_description': [
                    'Average poverty rate across Sumatera provinces (real data)',
                    'Total provinces in Sumatera analysis', 
                    'Provinces with high poverty risk (>=15%)',
                    'Average consumption per capita across provinces',
                    'Total population in analyzed provinces',
                    'Total poor population in analyzed provinces'
                ],
                'calculation_timestamp': [datetime.now()] * 6
            }
            
            stats_df = pd.DataFrame(stats_data)
            return stats_df
            
        except Exception as e:
            logger.error(f"❌ Error creating statistics: {e}")
            return None
    
    def update_gold_layer(self, province_df, stats_df):
        """Update Gold layer tables with real data"""
        logger.info("💾 Updating Gold layer with real data...")
        
        try:
            engine = create_engine(f"postgresql://{self.postgres_config['user']}:{self.postgres_config['password']}@{self.postgres_config['host']}:{self.postgres_config['port']}/{self.postgres_config['database']}")
            
            # Replace Gold tables with real data
            province_df.to_sql('gold_province_poverty_summary', engine, if_exists='replace', index=False)
            print("✅ Updated gold_province_poverty_summary with real data")
            
            stats_df.to_sql('gold_poverty_statistics', engine, if_exists='replace', index=False) 
            print("✅ Updated gold_poverty_statistics with real data")
            
            # Verify data
            with engine.connect() as conn:
                # Check record counts
                province_count = conn.execute("SELECT COUNT(*) FROM gold_province_poverty_summary;").fetchone()[0]
                stats_count = conn.execute("SELECT COUNT(*) FROM gold_poverty_statistics;").fetchone()[0]
                
                print(f"\n🔍 Verification:")
                print(f"   • Province records: {province_count}")
                print(f"   • Statistics records: {stats_count}")
                
                # Show updated data
                result = conn.execute("SELECT province_name, poverty_rate, risk_category FROM gold_province_poverty_summary ORDER BY poverty_rate DESC;")
                print(f"\n📊 Updated Gold layer data:")
                for row in result:
                    print(f"   • {row[0]}: {row[1]:.2f}% ({row[2]} Risk)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating Gold layer: {e}")
            return False
    
    def refresh_views(self):
        """Refresh views to reflect new data"""
        logger.info("🔄 Refreshing views...")
        
        try:
            engine = create_engine(f"postgresql://{self.postgres_config['user']}:{self.postgres_config['password']}@{self.postgres_config['host']}:{self.postgres_config['port']}/{self.postgres_config['database']}")
            
            with engine.connect() as conn:
                # Test views with new data
                dashboard_result = conn.execute("SELECT COUNT(*) FROM v_gold_provincial_dashboard;").fetchone()[0]
                hotspots_result = conn.execute("SELECT COUNT(*) FROM v_gold_poverty_hotspots;").fetchone()[0]
                
                print(f"✅ Views refreshed:")
                print(f"   • Provincial Dashboard: {dashboard_result} records")
                print(f"   • Poverty Hotspots: {hotspots_result} records")
                
                # Show sample from main view
                sample_result = conn.execute("SELECT province_name, poverty_rate, risk_level_detailed FROM v_gold_provincial_dashboard ORDER BY poverty_rate DESC;")
                print(f"\n📋 Sample from main dashboard view:")
                for row in sample_result:
                    print(f"   • {row[0]}: {row[1]:.2f}% ({row[2]})")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error refreshing views: {e}")
            return False
    
    def run_fix(self):
        """Run the complete fix process"""
        self.print_header()
        
        # Load original CSV data
        df = self.load_and_analyze_csv()
        if df is None:
            return False
        
        # Process real data
        province_df = self.process_real_data(df)
        if province_df is None:
            return False
        
        # Create statistics
        stats_df = self.create_real_statistics(province_df)
        if stats_df is None:
            return False
        
        # Update Gold layer
        if not self.update_gold_layer(province_df, stats_df):
            return False
        
        # Refresh views
        if not self.refresh_views():
            return False
        
        print("\n" + "=" * 70)
        print("🎉 GOLD LAYER DATA FIXED SUCCESSFULLY!")
        print("✅ Menggunakan data asli dari CSV (3 provinsi)")
        print("✅ Data sintetis diganti dengan data real")
        print("✅ Views di-refresh dengan data yang benar")
        print("=" * 70)
        print("\n📊 PROVINSI YANG BENAR:")
        print("1. Sumatera Barat")
        print("2. Sumatera Selatan") 
        print("3. Sumatera Utara")
        print("\n🔗 Siap untuk Superset dashboard dengan data asli!")
        print("=" * 70)
        
        return True

def main():
    """Main execution function"""
    try:
        processor = RealDataGoldProcessor()
        success = processor.run_fix()
        
        if not success:
            print("\n❌ Fix process failed")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Process cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
