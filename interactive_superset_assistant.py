#!/usr/bin/env python3
"""
Interactive Superset Dashboard Creation Assistant
Membantu langkah demi langkah pembuatan dashboard poverty mapping
"""

import requests
import time
import psycopg2
from psycopg2 import sql
import sys

class SupersetDashboardAssistant:
    def __init__(self):
        self.superset_url = "http://localhost:8088"
        self.postgres_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'poverty_mapping',
            'user': 'postgres',
            'password': 'password'
        }
        
    def check_services(self):
        """Check if required services are running"""
        print("🔍 Checking Services Status...")
        
        # Check Superset
        try:
            response = requests.get(self.superset_url, timeout=5)
            superset_status = "✅ RUNNING" if response.status_code == 200 else "❌ ERROR"
        except:
            superset_status = "❌ NOT ACCESSIBLE"
            
        # Check PostgreSQL
        try:
            conn = psycopg2.connect(**self.postgres_config)
            conn.close()
            postgres_status = "✅ RUNNING"
        except:
            postgres_status = "❌ NOT ACCESSIBLE"
            
        print(f"""
📊 SERVICE STATUS:
├── Superset: {superset_status}
├── PostgreSQL: {postgres_status}
└── URL: {self.superset_url}
        """)
        
        return "✅" in superset_status and "✅" in postgres_status
    
    def verify_gold_data(self):
        """Verify Gold layer data exists"""
        print("🔍 Verifying Gold Layer Data...")
        
        try:
            conn = psycopg2.connect(**self.postgres_config)
            cursor = conn.cursor()
            
            # Check views exist
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.views 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'v_gold%'
            """)
            views = cursor.fetchall()
            
            print("📋 GOLD VIEWS FOUND:")
            for view in views:
                cursor.execute(f"SELECT COUNT(*) FROM {view[0]}")
                count = cursor.fetchone()[0]
                print(f"├── {view[0]}: {count} rows")
                
            # Check specific data
            cursor.execute("SELECT * FROM v_gold_provincial_dashboard LIMIT 3")
            sample_data = cursor.fetchall()
            
            print("\n📊 SAMPLE DATA:")
            for row in sample_data:
                print(f"├── {row[1]}: {row[2]:.2f}%")  # province_name, poverty_rate
                
            conn.close()
            return len(views) >= 3
            
        except Exception as e:
            print(f"❌ Error checking data: {e}")
            return False
    
    def display_step_guide(self, step_number, title, instructions):
        """Display formatted step guide"""
        print(f"""
{'='*60}
📋 LANGKAH {step_number}: {title}
{'='*60}

{instructions}

{'='*60}
        """)
        
        input("⏳ Tekan ENTER setelah menyelesaikan langkah ini...")
    
    def run_interactive_guide(self):
        """Main interactive guide"""
        print("""
🚀 SUPERSET DASHBOARD CREATION ASSISTANT
=======================================
Membantu Anda membuat dashboard poverty mapping step-by-step
        """)
        
        # Step 0: Check services
        if not self.check_services():
            print("❌ Services tidak berjalan! Jalankan Docker containers terlebih dahulu.")
            return
            
        if not self.verify_gold_data():
            print("❌ Gold layer data tidak ditemukan! Jalankan ETL pipeline terlebih dahulu.")
            return
            
        print("✅ Semua prerequisite sudah siap!")
        input("📍 Tekan ENTER untuk memulai...")
        
        # Step 1: Database Connection
        self.display_step_guide(1, "MEMBUAT DATABASE CONNECTION", """
🎯 TUJUAN: Menghubungkan Superset ke PostgreSQL

📍 LOKASI UI:
1. Buka browser: http://localhost:8088
2. Login: admin/admin
3. Klik "Settings" (⚙️ pojok kanan atas)
4. Pilih "Database Connections"
5. Klik "+ DATABASE" (tombol biru)

📝 ISI FORM:
- SUPPORTED DATABASES: PostgreSQL
- DATABASE NAME: poverty_mapping_db
- SQLALCHEMY URI: postgresql://postgres:password@host.docker.internal:5432/poverty_mapping

🔧 TESTING:
1. Klik "TEST CONNECTION"
2. Tunggu "Connection looks good!"
3. Klik "CONNECT"
        """)
        
        # Step 2: Create Datasets
        self.display_step_guide(2, "MEMBUAT DATASETS", """
🎯 TUJUAN: Membuat 3 dataset dari Gold layer views

📍 LOKASI UI:
1. Klik "Data" (menu bar atas)
2. Pilih "Datasets"
3. Klik "+ DATASET"

📊 DATASET 1: Provincial Dashboard
- DATABASE: poverty_mapping_db
- SCHEMA: public
- TABLE: v_gold_provincial_dashboard
- Klik "CREATE DATASET AND CREATE CHART"

📊 DATASET 2: Poverty Hotspots
- DATABASE: poverty_mapping_db
- SCHEMA: public  
- TABLE: v_gold_poverty_hotspots
- Klik "CREATE DATASET AND CREATE CHART"

📊 DATASET 3: Summary Statistics
- DATABASE: poverty_mapping_db
- SCHEMA: public
- TABLE: v_gold_summary_stats
- Klik "CREATE DATASET AND CREATE CHART"
        """)
        
        # Step 3: Create Charts
        self.display_step_guide(3, "MEMBUAT CHART 1: KPI CARDS", """
🎯 TUJUAN: Membuat KPI card untuk tingkat kemiskinan

📍 LOKASI UI:
1. Charts → + (Create New Chart)
2. Choose Chart Type: "Big Number"
3. Choose Dataset: v_gold_provincial_dashboard

⚙️ SETTINGS:
QUERY:
- Metric: poverty_rate
- Row limit: 3

CUSTOMIZE:
- Header Text: "Tingkat Kemiskinan (%)"
- Subheader: "Data Provinsi Sumatera"

💾 SAVE:
- Chart Name: "KPI - Tingkat Kemiskinan"
- Add to Dashboard: [Create New] "Dashboard Poverty Mapping"
        """)
        
        self.display_step_guide(4, "MEMBUAT CHART 2: BAR CHART", """
🎯 TUJUAN: Membuat bar chart kemiskinan per provinsi

📍 LOKASI UI:
1. Charts → + (Create New Chart)  
2. Choose Chart Type: "Bar Chart"
3. Choose Dataset: v_gold_provincial_dashboard

⚙️ SETTINGS:
QUERY:
- X-axis: province_name
- Metric: poverty_rate
- Row limit: 10

CUSTOMIZE:
- Chart Title: "Tingkat Kemiskinan per Provinsi"
- X Axis Label: "Provinsi"
- Y Axis Label: "Tingkat Kemiskinan (%)"

💾 SAVE:
- Chart Name: "Bar Chart - Kemiskinan per Provinsi"
- Add to Dashboard: "Dashboard Poverty Mapping"
        """)
        
        self.display_step_guide(5, "MEMBUAT CHART 3: PIE CHART", """
🎯 TUJUAN: Membuat pie chart distribusi populasi

📍 LOKASI UI:
1. Charts → + (Create New Chart)
2. Choose Chart Type: "Pie Chart"  
3. Choose Dataset: v_gold_provincial_dashboard

⚙️ SETTINGS:
QUERY:
- Dimension: province_name
- Metric: total_population
- Row limit: 10

CUSTOMIZE:
- Chart Title: "Distribusi Populasi Provinsi"
- Show Labels: ✓
- Show Legend: ✓

💾 SAVE:
- Chart Name: "Pie Chart - Distribusi Populasi"
- Add to Dashboard: "Dashboard Poverty Mapping"
        """)
        
        self.display_step_guide(6, "MEMBUAT CHART 4: TABLE", """
🎯 TUJUAN: Membuat table statistik detail

📍 LOKASI UI:
1. Charts → + (Create New Chart)
2. Choose Chart Type: "Table"
3. Choose Dataset: v_gold_summary_stats

⚙️ SETTINGS:
QUERY:
- Columns: total_provinces, avg_poverty_rate, total_population, total_poor_population
- Row limit: 10

CUSTOMIZE:
- Table Title: "Statistik Kemiskinan Sumatera"
- Show Totals: ✓

💾 SAVE:
- Chart Name: "Table - Statistik Detail"
- Add to Dashboard: "Dashboard Poverty Mapping"
        """)
        
        # Step 7: Dashboard Layout
        self.display_step_guide(7, "MENGATUR DASHBOARD LAYOUT", """
🎯 TUJUAN: Menata layout dashboard yang professional

📍 LOKASI UI:
1. Dashboards → "Dashboard Poverty Mapping"
2. Klik "EDIT DASHBOARD" (pojok kanan atas)

🎨 LAYOUT ARRANGEMENT:
Row 1 (Top):
[KPI - Tingkat Kemiskinan] [Table - Statistik Detail]

Row 2 (Middle):  
[Bar Chart - Kemiskinan per Provinsi] (Full Width)

Row 3 (Bottom):
[Pie Chart - Distribusi Populasi] (Full Width)

📏 SIZING:
- KPI Card: 1/3 lebar layar
- Table: 2/3 lebar layar
- Bar Chart: Full width
- Pie Chart: Full width

💾 SAVE:
Klik "SAVE CHANGES" (pojok kanan atas)
        """)
        
        # Final Step
        print(f"""
🎉 SELAMAT! DASHBOARD BERHASIL DIBUAT!
=====================================

📊 DASHBOARD URL: http://localhost:8088/superset/dashboard/1/

✅ YANG SUDAH DIBUAT:
├── ✅ Database Connection
├── ✅ 3 Datasets (Gold layer views)
├── ✅ 4 Charts (KPI, Bar, Pie, Table)
└── ✅ Professional Dashboard Layout

📋 FITUR DASHBOARD:
├── 📊 KPI Cards: Tingkat kemiskinan real-time
├── 📈 Bar Chart: Perbandingan antar provinsi
├── 🥧 Pie Chart: Distribusi populasi
└── 📋 Table: Statistik detail lengkap

🔍 DATA YANG DITAMPILKAN:
├── Sumatera Barat: 17.66%
├── Sumatera Selatan: 17.53%
└── Sumatera Utara: 17.32%

🚀 NEXT STEPS:
1. Explore dashboard interactivity
2. Add filters jika diperlukan  
3. Share dengan stakeholders
4. Schedule data refresh via Airflow

Terima kasih telah menggunakan assistant! 🙏
        """)

def main():
    assistant = SupersetDashboardAssistant()
    assistant.run_interactive_guide()

if __name__ == "__main__":
    main()
