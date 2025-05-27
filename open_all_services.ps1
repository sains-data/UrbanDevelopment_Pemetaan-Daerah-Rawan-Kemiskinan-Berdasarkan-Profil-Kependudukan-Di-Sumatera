# Open All Services - Big Data Poverty Mapping Pipeline
# Kelompok 18 - Sumatra

Write-Host "=" * 60 -ForegroundColor Blue
Write-Host "🚀 OPENING ALL BIG DATA SERVICES" -ForegroundColor Cyan
Write-Host "📊 Kelompok 18 - Poverty Mapping Pipeline" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Blue

# Check container status first
Write-Host "`n🔍 Checking container status..." -ForegroundColor Yellow

$containers = @(
    @{Name="postgres-local"; Port="5432"; Service="PostgreSQL Database"},
    @{Name="superset"; Port="8089"; Service="Superset Dashboard"}, 
    @{Name="airflow"; Port="8090"; Service="Airflow Workflow"},
    @{Name="spark-master"; Port="8080"; Service="Spark Master UI"},
    @{Name="namenode"; Port="9870"; Service="Hadoop HDFS UI"},
    @{Name="jupyter"; Port="8888"; Service="Jupyter Notebooks"}
)

$runningServices = @()

foreach ($container in $containers) {
    $status = docker ps --filter "name=$($container.Name)" --format "{{.Status}}" 2>$null
    if ($status) {
        Write-Host "  ✅ $($container.Service): Running" -ForegroundColor Green
        $runningServices += $container
    } else {
        Write-Host "  ❌ $($container.Service): Not running" -ForegroundColor Red
    }
}

if ($runningServices.Count -eq 0) {
    Write-Host "`n⚠️  No services are running!" -ForegroundColor Yellow
    Write-Host "💡 Start services with: docker-compose up -d" -ForegroundColor Yellow
    exit
}

# Open running services
Write-Host "`n🌐 Opening web interfaces..." -ForegroundColor Yellow

foreach ($service in $runningServices) {
    $url = "http://localhost:$($service.Port)"
    Write-Host "  🔗 Opening $($service.Service): $url" -ForegroundColor Cyan
    
    try {
        Start-Process $url
        Start-Sleep 2
    } catch {
        Write-Host "  ⚠️  Could not auto-open $url" -ForegroundColor Yellow
    }
}

# Display service information
Write-Host "`n📋 SERVICE OVERVIEW:" -ForegroundColor Blue
Write-Host "=" * 60 -ForegroundColor Blue

Write-Host "`n🗄️  DATABASE SERVICES:" -ForegroundColor Green
Write-Host "   • PostgreSQL: localhost:5432" 
Write-Host "     └─ Database: poverty_mapping"
Write-Host "     └─ User: postgres / Password: postgres123"
Write-Host "     └─ Data: 20 poverty records, 9 provinces"

Write-Host "`n📊 DASHBOARD & ANALYTICS:" -ForegroundColor Green  
Write-Host "   • Superset Dashboard: http://localhost:8089"
Write-Host "     └─ Login: admin / admin"
Write-Host "     └─ Create poverty mapping dashboards"
Write-Host "   • Jupyter Notebooks: http://localhost:8888"
Write-Host "     └─ Data analysis and ML models"

Write-Host "`n🔄 WORKFLOW & PROCESSING:" -ForegroundColor Green
Write-Host "   • Airflow: http://localhost:8090" 
Write-Host "     └─ Login: admin / admin"
Write-Host "     └─ ETL pipeline orchestration"
Write-Host "   • Spark UI: http://localhost:8080"
Write-Host "     └─ Job monitoring and cluster status"

Write-Host "`n💾 BIG DATA STORAGE:" -ForegroundColor Green
Write-Host "   • Hadoop HDFS: http://localhost:9870"
Write-Host "     └─ Distributed file system"
Write-Host "     └─ Bronze/Silver/Gold data layers"

Write-Host "`n🎯 SUPERSET QUICK START:" -ForegroundColor Yellow
Write-Host "1. Open: http://localhost:8089"
Write-Host "2. Login: admin/admin"  
Write-Host "3. Add Database: Data > Databases > + DATABASE"
Write-Host "4. Connection URI: postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping"
Write-Host "5. Create datasets from tables: poverty_data, province_summary"
Write-Host "6. Build amazing poverty mapping dashboards!"

Write-Host "`n📊 AVAILABLE DATA TABLES:" -ForegroundColor Yellow
Write-Host "   • poverty_data - Main poverty mapping data (20 records)"
Write-Host "   • province_summary - Province statistics (9 provinces)" 
Write-Host "   • regency_summary - Regency level data"
Write-Host "   • v_poverty_hotspots - High poverty areas (>13%)"
Write-Host "   • v_poverty_by_province - Province comparison view"

Write-Host "`n✨ DASHBOARD IDEAS:" -ForegroundColor Cyan
Write-Host "   🗺️  Geographic poverty mapping (using lat/lng)"
Write-Host "   📈 Province poverty rate comparison"
Write-Host "   🔥 Poverty hotspots identification"  
Write-Host "   👥 Population vs poverty correlation"
Write-Host "   📊 Multi-level drill-down (Province→Regency→District)"

Write-Host "`n" + "=" * 60 -ForegroundColor Blue
Write-Host "🎉 ALL SERVICES OPENED!" -ForegroundColor Green
Write-Host "📊 Ready to create amazing poverty mapping dashboards!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Blue

# Keep window open
Write-Host "`nPress any key to close..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
