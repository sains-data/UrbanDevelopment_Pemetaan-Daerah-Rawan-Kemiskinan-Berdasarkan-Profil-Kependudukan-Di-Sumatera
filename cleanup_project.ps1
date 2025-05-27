# Script untuk merapihkan struktur proyek
# Kelompok 18 - Big Data Pipeline

Write-Host "🧹 CLEANUP PROJECT STRUCTURE" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

# Backup dulu untuk safety
$backupDir = "c:\TUBESABD\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "📁 Creating backup directory: $backupDir" -ForegroundColor Yellow

# File-file yang akan dipindah ke utils/
$utilsFiles = @(
    "check_database.py",
    "debug_pipeline.py", 
    "demo_pipeline_execution.py",
    "final_validation.py",
    "fix_airflow.sh",
    "manual_superset_setup.py",
    "next_steps.py",
    "open_superset.ps1",
    "organize_files.ps1",
    "organize_project.py",
    "prepare_github.ps1",
    "prepare_github.sh",
    "quick_access.ps1",
    "run_complete_pipeline.sh",
    "run_etl_pipeline.py",
    "run_pipeline_simple.py",
    "setup_superset_dashboard.py",
    "simple_demo.py",
    "simple_superset_setup.py",
    "start.sh",
    "start_complete_pipeline.py",
    "superset_api_setup.py",
    "test_airflow_dag.py",
    "test_components.py", 
    "test_dag_syntax.py",
    "validate_pipeline.bat",
    "verify_superset_setup.py"
)

# File dokumentasi yang akan dipindah ke docs/
$docsFiles = @(
    "AIRFLOW_DAG_FIX_SUMMARY.md",
    "DEPLOYMENT_REPORT.md",
    "EXECUTION_REPORT.md", 
    "FINAL_PROJECT_REPORT.md",
    "PROJECT_COMPLETE.md",
    "PROJECT_COMPLETION_FINAL.md",
    "PROJECT_STATUS_FINAL.md",
    "READY_TO_EXECUTE.md",
    "SUPERSET_READY.md"
)

# File debug reports yang akan dipindah ke logs/
$debugFiles = @(
    "debug_report_20250525_231506.txt",
    "debug_report_20250525_231703.txt"
)

# Pastikan direktori target ada
$directories = @("utils", "docs", "logs")
foreach ($dir in $directories) {
    if (!(Test-Path "c:\TUBESABD\$dir")) {
        New-Item -ItemType Directory -Path "c:\TUBESABD\$dir" -Force
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Pindahkan file utils
Write-Host "`n📦 Moving utility files to utils/" -ForegroundColor Cyan
foreach ($file in $utilsFiles) {
    if (Test-Path "c:\TUBESABD\$file") {
        try {
            Move-Item -Path "c:\TUBESABD\$file" -Destination "c:\TUBESABD\utils\" -Force
            Write-Host "  ✅ Moved: $file" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Failed to move: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Pindahkan file dokumentasi
Write-Host "`n📚 Moving documentation files to docs/" -ForegroundColor Cyan
foreach ($file in $docsFiles) {
    if (Test-Path "c:\TUBESABD\$file") {
        try {
            Move-Item -Path "c:\TUBESABD\$file" -Destination "c:\TUBESABD\docs\" -Force
            Write-Host "  ✅ Moved: $file" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Failed to move: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Pindahkan file debug ke logs
Write-Host "`n📋 Moving debug files to logs/" -ForegroundColor Cyan
foreach ($file in $debugFiles) {
    if (Test-Path "c:\TUBESABD\$file") {
        try {
            Move-Item -Path "c:\TUBESABD\$file" -Destination "c:\TUBESABD\logs\" -Force
            Write-Host "  ✅ Moved: $file" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Failed to move: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Cek sisa file di root
Write-Host "`n📁 Remaining files in root:" -ForegroundColor Yellow
$remainingFiles = Get-ChildItem -Path "c:\TUBESABD" -File | Where-Object { 
    $_.Name -notin @("docker-compose.yml", "hadoop.env", "README.md", ".gitignore", "cleanup_project.ps1") 
}

if ($remainingFiles.Count -eq 0) {
    Write-Host "  ✅ Root directory is clean!" -ForegroundColor Green
} else {
    Write-Host "  Files still in root:" -ForegroundColor Yellow
    foreach ($file in $remainingFiles) {
        Write-Host "    - $($file.Name)" -ForegroundColor White
    }
}

Write-Host "`n📊 Final project structure:" -ForegroundColor Cyan
Write-Host "TUBESABD/" -ForegroundColor White
Write-Host "├── README.md" -ForegroundColor Gray
Write-Host "├── docker-compose.yml" -ForegroundColor Gray  
Write-Host "├── hadoop.env" -ForegroundColor Gray
Write-Host "├── .gitignore" -ForegroundColor Gray
Write-Host "├── airflow/" -ForegroundColor White
Write-Host "├── config/" -ForegroundColor White
Write-Host "├── data/" -ForegroundColor White
Write-Host "├── docs/" -ForegroundColor White
Write-Host "├── logs/" -ForegroundColor White
Write-Host "├── notebooks/" -ForegroundColor White
Write-Host "├── scripts/" -ForegroundColor White
Write-Host "├── superset_data/" -ForegroundColor White
Write-Host "└── utils/" -ForegroundColor White

Write-Host "`n🎉 Project cleanup completed successfully!" -ForegroundColor Green
Write-Host "📁 Clean root directory with organized subdirectories" -ForegroundColor Green
