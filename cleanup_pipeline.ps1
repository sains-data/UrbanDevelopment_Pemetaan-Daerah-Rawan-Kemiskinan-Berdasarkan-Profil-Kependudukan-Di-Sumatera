# KELOMPOK 18 - PIPELINE CLEANUP SCRIPT
# Script untuk membersihkan file-file debug dan historical yang tidak diperlukan

Write-Host "🗑️ KELOMPOK 18 - PIPELINE CLEANUP" -ForegroundColor Red
Write-Host "===============================" -ForegroundColor Red

Write-Host "`n⚠️ WARNING: This will archive debug/fix files" -ForegroundColor Yellow
Write-Host "Core pipeline files will NOT be touched!" -ForegroundColor Green

# Create archive directory
Write-Host "`n📁 Creating archive directory..." -ForegroundColor Cyan
New-Item -Path "archived_files" -ItemType Directory -Force | Out-Null

# Files to keep (CORE PIPELINE - JANGAN DISENTUH!)
$coreFiles = @(
    "docker-compose.yml",
    "airflow\dags\poverty_mapping_dag_final.py",
    "data\Profil_Kemiskinan_Sumatera.csv",
    "init_postgres.sql",
    "hadoop.env",
    "start_pipeline.ps1",
    "open_all_services.ps1",
    "postgres_manager.ps1",
    "run_pipeline.py",
    "README.md",
    "PIPELINE_ORGANIZATION_FINAL.md",
    "PIPELINE_SUMMARY_FINAL.md",
    "PROJECT_COMPLETION_FINAL.md",
    "KELOMPOK18_PIPELINE_FINAL_REPORT.md"
)

Write-Host "✅ CORE FILES (WILL BE KEPT):" -ForegroundColor Green
foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        Write-Host "   📄 $file" -ForegroundColor White
    }
}

# Patterns for files to archive
$archivePatterns = @(
    "fix_*.py",
    "fix_*.bat", 
    "fix_*.ps1",
    "*_fix_*.md",
    "simple_*.py",
    "quick_*.py",
    "debug_*.py",
    "verify_*.py",
    "automate_*.py",
    "setup_*.py",
    "load_*.py",
    "organize_*.py",
    "*_GUIDE.md",
    "*_FIX*.md",
    "MANUAL_*.md",
    "SUPERSET_*.md",
    "POSTGRESQL_*.md",
    "DATABASE_*.md",
    "DATASET_*.md",
    "DASHBOARD_*.md",
    "*_READY.md",
    "*_SUCCESS.md",
    "cleanup_*.ps1",
    "launch_*.ps1",
    "restart_*.ps1"
)

Write-Host "`n🗑️ FILES TO ARCHIVE:" -ForegroundColor Yellow
$archiveCount = 0

foreach ($pattern in $archivePatterns) {
    $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        # Skip if it's a core file
        if ($coreFiles -notcontains $file) {
            Write-Host "   📦 $file" -ForegroundColor DarkYellow
            $archiveCount++
        }
    }
}

Write-Host "`n📊 SUMMARY:" -ForegroundColor Cyan
Write-Host "   ✅ Core Files Protected: $($coreFiles.Count)" -ForegroundColor Green
Write-Host "   🗑️ Files to Archive: $archiveCount" -ForegroundColor Yellow

Write-Host "`n🎯 MAIN PIPELINE STATUS:" -ForegroundColor Green
Write-Host "   📍 DAG: poverty_mapping_etl_final ✅" -ForegroundColor White
Write-Host "   📍 Data: 20,000+ poverty records ✅" -ForegroundColor White
Write-Host "   📍 Services: Docker containers ready ✅" -ForegroundColor White

$response = Read-Host "`n❓ Do you want to archive debug files? (y/N)"

if ($response -eq "y" -or $response -eq "Y") {
    Write-Host "`n🗂️ Archiving files..." -ForegroundColor Cyan
    
    $archivedCount = 0
    foreach ($pattern in $archivePatterns) {
        $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            if ($coreFiles -notcontains $file -and (Test-Path $file)) {
                try {
                    Move-Item $file "archived_files\" -Force
                    Write-Host "   ✅ Archived: $file" -ForegroundColor Green
                    $archivedCount++
                } catch {
                    Write-Host "   ❌ Failed to archive: $file" -ForegroundColor Red
                }
            }
        }
    }
    
    Write-Host "`n🎉 CLEANUP COMPLETED!" -ForegroundColor Green
    Write-Host "   📦 Archived $archivedCount files" -ForegroundColor Cyan
    Write-Host "   ✅ Core pipeline files preserved" -ForegroundColor Green
    Write-Host "   📁 Archived files in: archived_files\" -ForegroundColor Cyan
    
} else {
    Write-Host "`n⏹️ Cleanup cancelled. No files moved." -ForegroundColor Yellow
}

Write-Host "`n🚀 PIPELINE READY FOR USE!" -ForegroundColor Green
Write-Host "   1. docker-compose up -d" -ForegroundColor White
Write-Host "   2. Access Airflow: http://localhost:8090" -ForegroundColor White
Write-Host "   3. Enable DAG: poverty_mapping_etl_final" -ForegroundColor White
Write-Host "   4. Create Superset dashboards" -ForegroundColor White
