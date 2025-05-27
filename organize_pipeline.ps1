# KELOMPOK 18 - PIPELINE ORGANIZATION SCRIPT
# Pemetaan Kemiskinan Sumatera

Write-Host "🗂️ ORGANIZING KELOMPOK 18 PIPELINE" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Create organized folders
Write-Host "`n📁 Creating organized structure..." -ForegroundColor Yellow
New-Item -Path "organized" -ItemType Directory -Force | Out-Null
New-Item -Path "organized/core" -ItemType Directory -Force | Out-Null
New-Item -Path "organized/scripts" -ItemType Directory -Force | Out-Null
New-Item -Path "organized/docs" -ItemType Directory -Force | Out-Null
New-Item -Path "organized/archive" -ItemType Directory -Force | Out-Null

Write-Host "✅ Directories created" -ForegroundColor Green

# Show core pipeline files (ACTIVE - JANGAN DIHAPUS)
Write-Host "`n✅ CORE PIPELINE FILES (ACTIVE):" -ForegroundColor Green
$coreFiles = @(
    "docker-compose.yml",
    "airflow\dags\poverty_mapping_dag_final.py",
    "data\Profil_Kemiskinan_Sumatera.csv",
    "init_postgres.sql",
    "hadoop.env"
)

foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        Write-Host "   📄 $file" -ForegroundColor White
    }
}

# Show active scripts (KEEP)
Write-Host "`n🔧 ACTIVE SCRIPTS (KEEP):" -ForegroundColor Cyan
$activeScripts = @(
    "start_pipeline.ps1",
    "open_all_services.ps1",
    "postgres_manager.ps1",
    "run_pipeline.py"
)

foreach ($script in $activeScripts) {
    if (Test-Path $script) {
        Write-Host "   📜 $script" -ForegroundColor White
    }
}

# Show important docs (KEEP)
Write-Host "`n📚 IMPORTANT DOCS (KEEP):" -ForegroundColor Magenta
$importantDocs = @(
    "README.md",
    "PIPELINE_ORGANIZATION_FINAL.md",
    "PIPELINE_SUMMARY_FINAL.md",
    "PROJECT_COMPLETION_FINAL.md"
)

foreach ($doc in $importantDocs) {
    if (Test-Path $doc) {
        Write-Host "   📖 $doc" -ForegroundColor White
    }
}

# Count files to archive (debug/fix files)
Write-Host "`n🗑️ FILES TO ARCHIVE (Debug/Historical):" -ForegroundColor Yellow
$archivePatterns = @("fix_*.py", "fix_*.bat", "fix_*.ps1", "*_fix_*.md", "simple_*.py", "quick_*.py", "debug_*.py", "*_GUIDE.md", "*_FIX*.md", "MANUAL_*.md")
$archiveCount = 0

foreach ($pattern in $archivePatterns) {
    $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        Write-Host "   📦 $file" -ForegroundColor DarkYellow
        $archiveCount++
    }
}

Write-Host "`n📊 SUMMARY:" -ForegroundColor Cyan
Write-Host "   ✅ Core Pipeline Files: $($coreFiles.Count)" -ForegroundColor Green
Write-Host "   🔧 Active Scripts: $($activeScripts.Count)" -ForegroundColor Cyan
Write-Host "   📚 Important Docs: $($importantDocs.Count)" -ForegroundColor Magenta
Write-Host "   🗑️ Files to Archive: $archiveCount" -ForegroundColor Yellow

Write-Host "`n🎯 MAIN AIRFLOW DAG:" -ForegroundColor Green
Write-Host "   📍 File: poverty_mapping_dag_final.py" -ForegroundColor White
Write-Host "   📍 DAG ID: poverty_mapping_etl_final" -ForegroundColor White
Write-Host "   ⚠️  JANGAN DIUBAH NAMA DAG-nya!" -ForegroundColor Red

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✅ PIPELINE ORGANIZATION COMPLETED!" -ForegroundColor Green
Write-Host "`n🚀 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. docker-compose up -d" -ForegroundColor White
Write-Host "2. Access Airflow: http://localhost:8090" -ForegroundColor White
Write-Host "3. Enable DAG: poverty_mapping_etl_final" -ForegroundColor White
Write-Host "4. Create Superset dashboards: http://localhost:8089" -ForegroundColor White

Write-Host "`n🎯 STATUS: READY FOR DASHBOARD CREATION! ✅" -ForegroundColor Green
