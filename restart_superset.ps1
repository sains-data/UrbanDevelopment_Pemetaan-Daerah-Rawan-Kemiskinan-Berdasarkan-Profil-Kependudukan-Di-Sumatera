# Restart Superset untuk fix database name conflict error
Write-Host "🔄 Restarting Superset untuk membersihkan cache dan error state..." -ForegroundColor Yellow

# Stop Superset container
Write-Host "1. Stopping Superset container..." -ForegroundColor Cyan
docker stop superset

# Wait a moment
Write-Host "2. Waiting 5 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Start Superset container
Write-Host "3. Starting Superset container..." -ForegroundColor Cyan
docker start superset

# Wait for Superset to be ready
Write-Host "4. Waiting for Superset to be ready (30 seconds)..." -ForegroundColor Cyan
Start-Sleep -Seconds 30

# Check status
Write-Host "5. Checking Superset status..." -ForegroundColor Cyan
$supersetStatus = docker ps --filter "name=superset" --format "table {{.Names}}\t{{.Status}}"
Write-Host $supersetStatus -ForegroundColor Green

Write-Host "`n✅ Superset restart completed!" -ForegroundColor Green
Write-Host "🌐 Superset UI: http://localhost:8089" -ForegroundColor Yellow
Write-Host "🔑 Login: admin / admin" -ForegroundColor Yellow

Write-Host "`n🎯 Sekarang coba lagi di Superset UI:" -ForegroundColor Cyan
Write-Host "1. Settings → Database Connections → + DATABASE" -ForegroundColor White
Write-Host "2. Pilih PostgreSQL" -ForegroundColor White
Write-Host "3. Database Name: poverty_kelompok18_fresh" -ForegroundColor White
Write-Host "4. Host: postgres-local" -ForegroundColor White
Write-Host "5. Port: 5432" -ForegroundColor White
Write-Host "6. Database: poverty_mapping" -ForegroundColor White
Write-Host "7. Username: postgres" -ForegroundColor White
Write-Host "8. Password: postgres123" -ForegroundColor White
Write-Host "9. Test Connection → Connect" -ForegroundColor White

Write-Host "`n💡 Jika masih error, coba gunakan nama database yang berbeda:" -ForegroundColor Magenta
Write-Host "   - kelompok18_poverty" -ForegroundColor White
Write-Host "   - sumatera_poverty_db" -ForegroundColor White
Write-Host "   - poverty_data_final" -ForegroundColor White
