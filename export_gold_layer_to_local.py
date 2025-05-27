#!/usr/bin/env python3
"""
Export Gold Layer Data to Local Files
Kelompok 18 - Poverty Mapping Pipeline

Script ini akan:
1. Connect ke PostgreSQL database
2. Export Gold layer tables ke CSV files
3. Simpan ke folder lokal 'gold' di workspace
"""

import pandas as pd
import os
from sqlalchemy import create_engine
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoldLayerExporter:
    def __init__(self):
        self.postgres_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'poverty_mapping',
            'user': 'postgres',
            'password': 'postgres123'
        }
        
        # Create gold folder in workspace
        self.workspace_path = r'C:\TUBESABD'
        self.gold_folder = os.path.join(self.workspace_path, 'gold')
        
        # Ensure gold folder exists
        os.makedirs(self.gold_folder, exist_ok=True)
        
    def print_header(self):
        print("=" * 70)
        print("📤 EXPORTING GOLD LAYER DATA TO LOCAL FILES")
        print("📊 Kelompok 18 - Poverty Mapping Pipeline")
        print(f"💾 Output folder: {self.gold_folder}")
        print("=" * 70)
        
    def connect_database(self):
        """Create database connection"""
        try:
            connection_string = f"postgresql://{self.postgres_config['user']}:{self.postgres_config['password']}@{self.postgres_config['host']}:{self.postgres_config['port']}/{self.postgres_config['database']}"
            engine = create_engine(connection_string)
            logger.info("✅ Database connection established")
            return engine
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return None
    
    def export_table_to_csv(self, engine, table_name, description):
        """Export a table/view to CSV file"""
        try:
            logger.info(f"📤 Exporting {table_name}...")
            
            # Read data from database
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, engine)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{table_name}_{timestamp}.csv"
            filepath = os.path.join(self.gold_folder, filename)
            
            # Export to CSV
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            print(f"✅ {description}")
            print(f"   📁 File: {filename}")
            print(f"   📊 Records: {len(df)}")
            print(f"   💾 Size: {os.path.getsize(filepath):,} bytes")
            print(f"   📂 Path: {filepath}")
            
            # Show sample data
            if len(df) > 0:
                print(f"   📋 Sample data:")
                print(f"      Columns: {', '.join(df.columns.tolist())}")
                if len(df) <= 5:
                    for _, row in df.iterrows():
                        print(f"      • {dict(row)}")
                else:
                    print(f"      • First row: {dict(df.iloc[0])}")
            print()
            
            return filepath, len(df)
            
        except Exception as e:
            logger.error(f"❌ Failed to export {table_name}: {e}")
            return None, 0
    
    def export_all_gold_data(self):
        """Export all Gold layer tables and views"""
        engine = self.connect_database()
        if not engine:
            return False
        
        # Tables and views to export
        exports = [
            {
                'table': 'gold_province_poverty_summary',
                'description': 'Gold Province Poverty Summary (Main Gold Table)'
            },
            {
                'table': 'gold_poverty_statistics', 
                'description': 'Gold Poverty Statistics (Aggregated Stats)'
            },
            {
                'table': 'v_gold_provincial_dashboard',
                'description': 'Provincial Dashboard View (Enhanced for Superset)'
            },
            {
                'table': 'v_gold_poverty_hotspots',
                'description': 'Poverty Hotspots View (High Risk Areas)'
            },
            {
                'table': 'v_gold_summary_stats',
                'description': 'Summary Statistics View (KPI Metrics)'
            }
        ]
        
        exported_files = []
        total_records = 0
        
        for export_config in exports:
            filepath, record_count = self.export_table_to_csv(
                engine, 
                export_config['table'], 
                export_config['description']
            )
            
            if filepath:
                exported_files.append({
                    'file': filepath,
                    'table': export_config['table'],
                    'records': record_count
                })
                total_records += record_count
        
        # Create export summary
        self.create_export_summary(exported_files, total_records)
        
        return len(exported_files) > 0
    
    def create_export_summary(self, exported_files, total_records):
        """Create summary of exported files"""
        summary_file = os.path.join(self.gold_folder, 'EXPORT_SUMMARY.md')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary_content = f"""# Gold Layer Export Summary
Generated: {timestamp}
Kelompok 18 - Poverty Mapping Pipeline

## Export Location
📂 Folder: {self.gold_folder}

## Exported Files
"""
        
        for file_info in exported_files:
            filename = os.path.basename(file_info['file'])
            summary_content += f"""
### {file_info['table']}
- 📄 **File**: `{filename}`
- 📊 **Records**: {file_info['records']:,}
- 📂 **Full Path**: `{file_info['file']}`
"""
        
        summary_content += f"""
## Summary Statistics
- 📁 **Total Files**: {len(exported_files)}
- 📊 **Total Records**: {total_records:,}
- 💾 **Export Date**: {timestamp}

## Data Description
The exported data contains:
1. **gold_province_poverty_summary**: Main Gold layer with 3 Sumatera provinces
2. **gold_poverty_statistics**: Aggregated statistics and KPIs
3. **v_gold_provincial_dashboard**: Enhanced view for Superset dashboards
4. **v_gold_poverty_hotspots**: High-risk area analysis
5. **v_gold_summary_stats**: Summary metrics for executive reporting

## Usage
These CSV files can be used for:
- 📊 External analysis tools (Excel, Power BI, Tableau)
- 🔄 Data backup and archival
- 📈 Offline dashboard creation
- 🔍 Data validation and quality checks
- 📤 Data sharing with stakeholders

## Data Source
- **Source Database**: PostgreSQL (poverty_mapping)
- **Architecture**: Medallion (Bronze → Silver → Gold)
- **Real Data**: 3 Sumatera provinces from Profil_Kemiskinan_Sumatera.csv
"""
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"📋 Export summary created: {summary_file}")
    
    def create_gold_folder_structure(self):
        """Create organized folder structure in gold directory"""
        subdirs = ['tables', 'views', 'backups']
        
        for subdir in subdirs:
            subdir_path = os.path.join(self.gold_folder, subdir)
            os.makedirs(subdir_path, exist_ok=True)
        
        print(f"📁 Created folder structure in {self.gold_folder}")
        for subdir in subdirs:
            print(f"   📂 {subdir}/")
    
    def run_export(self):
        """Run the complete export process"""
        self.print_header()
        
        # Create folder structure
        self.create_gold_folder_structure()
        
        # Export all data
        if self.export_all_gold_data():
            print("=" * 70)
            print("🎉 GOLD LAYER DATA EXPORT COMPLETED!")
            print(f"📂 All files saved to: {self.gold_folder}")
            print("📋 Check EXPORT_SUMMARY.md for details")
            print("=" * 70)
            
            # Show folder contents
            print("\n📁 EXPORTED FILES:")
            for item in os.listdir(self.gold_folder):
                item_path = os.path.join(self.gold_folder, item)
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    print(f"   📄 {item} ({size:,} bytes)")
                else:
                    print(f"   📂 {item}/")
            
            return True
        else:
            print("❌ Export failed")
            return False

def main():
    """Main execution function"""
    try:
        exporter = GoldLayerExporter()
        success = exporter.run_export()
        
        if not success:
            print("\n❌ Export process failed")
            return 1
        
        print("\n💡 NEXT STEPS:")
        print("1. 📂 Navigate to C:\\TUBESABD\\gold\\")
        print("2. 📊 Open CSV files in Excel/tools of choice")
        print("3. 📈 Use data for external analysis")
        print("4. 🔄 Files can be imported to other systems")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Export cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
