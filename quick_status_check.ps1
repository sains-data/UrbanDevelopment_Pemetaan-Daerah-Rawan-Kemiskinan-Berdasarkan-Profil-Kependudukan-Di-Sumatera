# Quick Status Check for Kelompok 18 Pipeline
Write-Host "🔍 Checking Kelompok 18 Big Data Pipeline Status..." -ForegroundColor Cyan
Write-Host "=" * 50

# Check Docker containers
Write-Host "`n📦 Docker Services:" -ForegroundColor Yellow
try {
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}" | Select-Object -First 10
    $containers | ForEach-Object { Write-Host "   $_" }
    $runningCount = (docker ps --quiet | Measure-Object).Count
    Write-Host "   ✅ Total running containers: $runningCount" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Docker not accessible" -ForegroundColor Red
}

# Check PostgreSQL data
Write-Host "`n🗄️ PostgreSQL Data:" -ForegroundColor Yellow
try {
    $dataCount = docker exec tubesabd_postgres-local_1 psql -U postgres -d poverty_mapping -t -c "SELECT COUNT(*) FROM poverty_clean;" 2>$null
    if ($dataCount) {
        Write-Host "   ✅ poverty_clean view: $($dataCount.Trim()) records" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Could not verify data count" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ PostgreSQL not accessible" -ForegroundColor Red
}

# Check web services
Write-Host "`n🌐 Web Services:" -ForegroundColor Yellow
$services = @(
    @{Name="Superset"; URL="http://localhost:8089"; Port=8089},
    @{Name="Airflow"; URL="http://localhost:8080"; Port=8080}
)

foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri $service.URL -TimeoutSec 5 -UseBasicParsing 2>$null
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ $($service.Name): Available at $($service.URL)" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ❌ $($service.Name): Not accessible at $($service.URL)" -ForegroundColor Red
    }
}

Write-Host "`n" + "=" * 50
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Open Superset: http://localhost:8089" -ForegroundColor White
Write-Host "2. Login: admin / admin" -ForegroundColor White
Write-Host "3. Create dataset from poverty_clean view" -ForegroundColor White
Write-Host "4. Build dashboard for poverty mapping" -ForegroundColor White
