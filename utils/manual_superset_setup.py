"""
Manual Superset Dashboard Setup - Step by Step Guide
Kelompok 18 - Big Data Pipeline for Poverty Mapping in Sumatra
Complete manual setup instructions for creating comprehensive dashboards
"""

import sqlite3
import os
from datetime import datetime

def verify_database():
    """Verify our database is ready for Superset"""
    print("🔍 VERIFYING DATABASE FOR SUPERSET")
    print("=" * 60)
    
    db_path = 'superset_data/poverty_mapping.db'
    abs_path = os.path.abspath(db_path)
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {abs_path}")
        return False
    
    # Connect and verify
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    print(f"✅ Database found: {abs_path}")
    print(f"📊 File size: {os.path.getsize(db_path):,} bytes")
    print(f"📋 Tables available: {', '.join(tables)}")
    
    # Check main table
    cursor.execute("SELECT COUNT(*) FROM poverty_data")
    main_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM province_summary") 
    summary_count = cursor.fetchone()[0]
    
    print(f"📈 Main data records: {main_count:,}")
    print(f"📊 Summary records: {summary_count}")
    
    # Show sample data
    print(f"\n📋 SAMPLE DATA:")
    cursor.execute("SELECT Provinsi, Kabupaten_Kota, Poverty_Rate, Unemployment_Rate FROM poverty_data LIMIT 3")
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"   {i}. {row[0]} - {row[1]}: {row[2]}% poverty, {row[3]}% unemployment")
    
    conn.close()
    return True

def generate_setup_instructions():
    """Generate complete setup instructions"""
    print(f"\n🎯 MANUAL DASHBOARD SETUP INSTRUCTIONS")
    print("=" * 60)
    
    instructions = f"""
    
STEP 1: ACCESS SUPERSET
📍 Open your browser and go to: http://localhost:8089
👤 Login with:
   Username: admin
   Password: admin

STEP 2: CREATE DATABASE CONNECTION
🗄️ Go to Settings > Database Connections
➕ Click "+ DATABASE"
📝 Fill in the details:
   Database Name: Poverty_Mapping_Sumatra
   SQLAlchemy URI: sqlite:///{os.path.abspath('superset_data/poverty_mapping.db').replace(chr(92), '/')}
   
✅ Test Connection
💾 Save

STEP 3: CREATE DATASETS
📊 Go to Data > Datasets
➕ Click "+ DATASET"
🔗 Select database: Poverty_Mapping_Sumatra
📋 Choose tables:
   - poverty_data (main dataset)
   - province_summary (summary data)
   - poverty_distribution (distribution data)
💾 Save each dataset

STEP 4: CREATE CHARTS
📈 Go to Charts > + (Create new chart)

CHART 1: Poverty Rate by Province (Bar Chart)
   Dataset: poverty_data
   Chart Type: Bar Chart
   X-axis: Provinsi
   Metric: AVG(Poverty_Rate)
   Title: "Average Poverty Rate by Province"

CHART 2: Unemployment vs Poverty (Scatter Plot)
   Dataset: poverty_data  
   Chart Type: Scatter Plot
   X-axis: Unemployment_Rate
   Y-axis: Poverty_Rate
   Size: Population
   Title: "Unemployment vs Poverty Relationship"

CHART 3: Economic Health Distribution (Pie Chart)
   Dataset: poverty_data
   Chart Type: Pie Chart
   Dimension: Poverty_Category
   Metric: COUNT(*)
   Title: "Economic Health Category Distribution"

CHART 4: Regional Summary Table
   Dataset: poverty_data
   Chart Type: Table
   Columns: Provinsi, Kabupaten_Kota, Poverty_Rate, Unemployment_Rate, Population
   Title: "Regional Poverty Statistics"

CHART 5: Provincial Summary (Big Number)
   Dataset: province_summary
   Chart Type: Big Number with Trendline
   Metric: AVG(Avg_Poverty_Rate)
   Title: "Overall Poverty Rate"

CHART 6: Geographic Heatmap
   Dataset: poverty_data
   Chart Type: Heatmap
   X-axis: Provinsi
   Y-axis: Kabupaten_Kota
   Metric: AVG(Poverty_Rate)
   Title: "Poverty Intensity Heatmap"

STEP 5: CREATE DASHBOARD
🎨 Go to Dashboards > + (Create new dashboard)
📝 Title: "Poverty Mapping Dashboard - Sumatra"
🖱️ Drag and drop your charts
📐 Arrange in a 2x3 grid layout
🎨 Apply filters and formatting
💾 Save and Publish

STEP 6: ADD FILTERS
🔍 Add dashboard filters:
   - Province filter (Provinsi)
   - Year filter (Tahun)
   - Poverty Category filter (Poverty_Category)

STEP 7: FINAL CONFIGURATION
⚙️ Dashboard Settings:
   - Auto-refresh: 5 minutes
   - Color scheme: Superset default
   - Enable cross-filtering
   - Add descriptions for each chart

    """
    
    print(instructions)

def create_access_shortcuts():
    """Create quick access files"""
    print(f"\n🚀 CREATING ACCESS SHORTCUTS")
    print("=" * 60)
    
    # PowerShell script
    ps_content = f"""# Superset Quick Access - Kelompok 18
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Write-Host "🎨 SUPERSET DASHBOARD ACCESS" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

Write-Host "🔗 Opening Superset Dashboard..." -ForegroundColor Green
Start-Process "http://localhost:8089"

Write-Host "👤 Login Credentials:" -ForegroundColor Yellow
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin" -ForegroundColor White

Write-Host "🗄️ Database Connection URI:" -ForegroundColor Yellow
Write-Host "   sqlite:///{os.path.abspath('superset_data/poverty_mapping.db').replace(chr(92), '/')}" -ForegroundColor White

Write-Host "📊 Available Tables:" -ForegroundColor Yellow
Write-Host "   - poverty_data (20,000 records)" -ForegroundColor White
Write-Host "   - province_summary (3 provinces)" -ForegroundColor White
Write-Host "   - poverty_distribution (categories)" -ForegroundColor White

Write-Host "📖 Setup Guide: superset_data/PANDUAN_DASHBOARD_LENGKAP.md" -ForegroundColor Magenta
Write-Host "✨ Ready to create amazing dashboards!" -ForegroundColor Green
"""
    
    with open('superset_quick_access.ps1', 'w') as f:
        f.write(ps_content)
    
    # HTML quick reference
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Superset Dashboard Setup - Kelompok 18</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-left: 4px solid #3498db; padding-left: 15px; }}
        .info-box {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .success {{ background: #d4edda; border: 1px solid #c3e6cb; }}
        .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; }}
        .code {{ background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 5px; font-family: monospace; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Superset Dashboard Setup</h1>
        <p><strong>Kelompok 18 - Big Data Pipeline for Poverty Mapping in Sumatra</strong></p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="info-box success">
            <h2>🚀 Quick Access</h2>
            <p><strong>Superset URL:</strong> <a href="http://localhost:8089" target="_blank">http://localhost:8089</a></p>
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> admin</p>
        </div>
        
        <div class="info-box warning">
            <h2>🗄️ Database Connection</h2>
            <p><strong>Database Name:</strong> Poverty_Mapping_Sumatra</p>
            <div class="code">sqlite:///{os.path.abspath('superset_data/poverty_mapping.db').replace(chr(92), '/')}</div>
        </div>
        
        <h2>📊 Available Data</h2>
        <ul>
            <li><strong>poverty_data:</strong> 20,000 records of poverty statistics</li>
            <li><strong>province_summary:</strong> 3 provinces summary</li>
            <li><strong>poverty_distribution:</strong> Category distributions</li>
        </ul>
        
        <h2>📈 Recommended Charts</h2>
        <ol>
            <li><strong>Bar Chart:</strong> Poverty Rate by Province</li>
            <li><strong>Scatter Plot:</strong> Unemployment vs Poverty</li>
            <li><strong>Pie Chart:</strong> Economic Health Distribution</li>
            <li><strong>Table:</strong> Regional Summary Statistics</li>
            <li><strong>Big Number:</strong> Overall Poverty Rate</li>
            <li><strong>Heatmap:</strong> Geographic Poverty Intensity</li>
        </ol>
        
        <div class="info-box">
            <h2>📖 Documentation</h2>
            <p>Complete setup guide: <code>superset_data/PANDUAN_DASHBOARD_LENGKAP.md</code></p>
            <p>Database file: <code>superset_data/poverty_mapping.db</code></p>
        </div>
        
        <div class="info-box success">
            <h2>✨ Next Steps</h2>
            <ol>
                <li>Open Superset at <a href="http://localhost:8089">localhost:8089</a></li>
                <li>Login with admin/admin</li>
                <li>Create database connection</li>
                <li>Import datasets</li>
                <li>Create charts</li>
                <li>Build dashboard</li>
                <li>Generate insights!</li>
            </ol>
        </div>
    </div>
</body>
</html>"""
    
    with open('superset_setup_guide.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Created: superset_quick_access.ps1")
    print("✅ Created: superset_setup_guide.html")

def main():
    """Main execution"""
    print("🎨 SUPERSET MANUAL SETUP PREPARATION")
    print("=" * 60)
    print("📋 Kelompok 18 - Big Data Pipeline for Poverty Mapping")
    print(f"🗓️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Verify database
    if not verify_database():
        print("❌ Database verification failed!")
        return
    
    # Generate instructions
    generate_setup_instructions()
    
    # Create shortcuts
    create_access_shortcuts()
    
    print(f"\n🎉 PREPARATION COMPLETED!")
    print("=" * 60)
    print("🔗 Next steps:")
    print("   1. Run: .\\superset_quick_access.ps1")
    print("   2. Open: superset_setup_guide.html")
    print("   3. Follow manual setup instructions")
    print("   4. Create amazing dashboards!")
    
    print(f"\n📖 All documentation ready in:")
    print("   📋 superset_data/PANDUAN_DASHBOARD_LENGKAP.md")
    print("   🌐 superset_setup_guide.html")
    print("   ⚡ superset_quick_access.ps1")

if __name__ == "__main__":
    main()
