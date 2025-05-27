# Airflow DAG Management Script
# Kelompok 18 - Keep Final DAG Active, Pause Others

Write-Host "=" * 60
Write-Host "🌊 AIRFLOW DAG MANAGEMENT" -ForegroundColor Cyan
Write-Host "🎯 Keep: poverty_mapping_etl_final (SUCCESS)" -ForegroundColor Green
Write-Host "⏹️ Stop: working, simple, fixed (to avoid conflicts)" -ForegroundColor Yellow
Write-Host "=" * 60

# Ensure final DAG is active
Write-Host "`n🚀 Keeping FINAL DAG active..." -ForegroundColor Green
docker exec airflow airflow dags unpause poverty_mapping_etl_final

# Pause other DAGs
Write-Host "`n⏹️ Pausing other DAGs to avoid conflicts..." -ForegroundColor Yellow

$other_dags = @(
    "poverty_mapping_etl_working",
    "poverty_mapping_etl_simple", 
    "poverty_mapping_etl_fixed",
    "poverty_mapping_etl"
)

foreach ($dag in $other_dags) {
    Write-Host "   🛑 Pausing: $dag" -ForegroundColor Red
    docker exec airflow airflow dags pause $dag
}

# Check status
Write-Host "`n📊 Checking DAG status..." -ForegroundColor Cyan
docker exec airflow airflow dags list | Select-String "poverty"

Write-Host "`n" + "=" * 60
Write-Host "🎉 DAG MANAGEMENT COMPLETED!" -ForegroundColor Green
Write-Host "✅ ACTIVE: poverty_mapping_etl_final" -ForegroundColor Green
Write-Host "⏹️ PAUSED: All other poverty mapping DAGs" -ForegroundColor Yellow
Write-Host "🔗 Check Airflow UI: http://localhost:8090" -ForegroundColor Cyan
Write-Host "=" * 60

Write-Host "`n💡 NEXT STEPS:" -ForegroundColor Magenta
Write-Host "1. 🌐 Open Airflow UI: http://localhost:8090"
Write-Host "2. ✅ Verify only 'poverty_mapping_etl_final' is active"
Write-Host "3. 📊 Check that pipeline runs are successful"
Write-Host "4. 🚀 Continue with Superset dashboard creation"
