# 🚀 Quick Launch Script for Superset Dashboard Creation
# Kelompok 18 - Big Data Poverty Mapping Pipeline

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🚀 SUPERSET DASHBOARD QUICK LAUNCHER" -ForegroundColor Green
Write-Host "📊 Kelompok 18 - Poverty Mapping Pipeline" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Check container status
Write-Host "`n📋 Checking Container Status..." -ForegroundColor Yellow
$containers = @("postgres-local", "superset")

foreach ($container in $containers) {
    $status = docker ps --filter "name=$container" --format "{{.Names}}: {{.Status}}"
    if ($status) {
        Write-Host "  ✅ $status" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $container: Not running" -ForegroundColor Red
    }
}

# Quick data verification
Write-Host "`n📊 Quick Data Check..." -ForegroundColor Yellow
try {
    $recordCount = docker exec postgres-local psql -U postgres -d poverty_mapping -t -c "SELECT COUNT(*) FROM poverty_data;" 2>$null
    if ($recordCount) {
        Write-Host "  ✅ Poverty data records: $($recordCount.Trim())" -ForegroundColor Green
    }
    
    $provinceCount = docker exec postgres-local psql -U postgres -d poverty_mapping -t -c "SELECT COUNT(*) FROM province_summary;" 2>$null
    if ($provinceCount) {
        Write-Host "  ✅ Provinces: $($provinceCount.Trim())" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️ Could not verify data - containers may be starting" -ForegroundColor Yellow
}

# Launch services
Write-Host "`n🌐 Opening Services..." -ForegroundColor Yellow

# Open Superset
Write-Host "  🚀 Opening Superset Dashboard..." -ForegroundColor Cyan
Start-Process "http://localhost:8089"

# Wait a moment
Start-Sleep -Seconds 2

# Open guides
Write-Host "  📚 Opening Creation Guide..." -ForegroundColor Cyan
if (Test-Path "SUPERSET_DASHBOARD_CREATION_GUIDE.md") {
    Start-Process "SUPERSET_DASHBOARD_CREATION_GUIDE.md"
} else {
    Write-Host "    ⚠️ Guide not found in current directory" -ForegroundColor Yellow
}

# Display quick actions
Write-Host "`n🎯 QUICK ACTIONS:" -ForegroundColor Magenta
Write-Host "  1. Login to Superset: admin / admin" -ForegroundColor White
Write-Host "  2. Settings → Database Connections → + DATABASE" -ForegroundColor White
Write-Host "  3. Choose PostgreSQL" -ForegroundColor White
Write-Host "  4. URI: postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping" -ForegroundColor Gray
Write-Host "  5. Test Connection → Connect" -ForegroundColor White

Write-Host "`n📊 DATASETS TO CREATE:" -ForegroundColor Magenta
Write-Host "  • poverty_data (main records)" -ForegroundColor White
Write-Host "  • province_summary (aggregated)" -ForegroundColor White
Write-Host "  • v_poverty_hotspots (high poverty areas)" -ForegroundColor White

Write-Host "`n📈 CHART SUGGESTIONS:" -ForegroundColor Magenta
Write-Host "  • Bar Chart: Province poverty comparison" -ForegroundColor White
Write-Host "  • Pie Chart: Poverty distribution" -ForegroundColor White
Write-Host "  • Table: Detailed area data" -ForegroundColor White
Write-Host "  • Scatter Plot: Geographic visualization" -ForegroundColor White

Write-Host "`n🔧 TROUBLESHOOTING:" -ForegroundColor Magenta
Write-Host "  • Connection issues: docker restart postgres-local superset" -ForegroundColor White
Write-Host "  • Run automation: python automate_superset_setup.py" -ForegroundColor White
Write-Host "  • Verify setup: python verify_superset_setup.py" -ForegroundColor White

Write-Host "`n✅ ALL SERVICES LAUNCHED!" -ForegroundColor Green
Write-Host "🎨 Start creating your poverty mapping dashboards!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

# Optional: Run automation script
Write-Host "`n🤖 Run automation script? (y/n): " -ForegroundColor Yellow -NoNewline
$runAuto = Read-Host

if ($runAuto -eq "y" -or $runAuto -eq "Y") {
    Write-Host "`n🚀 Running automation script..." -ForegroundColor Cyan
    python automate_superset_setup.py
}
