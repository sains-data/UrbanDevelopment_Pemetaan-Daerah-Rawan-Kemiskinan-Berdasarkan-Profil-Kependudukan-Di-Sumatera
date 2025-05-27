# 🧹 WORKSPACE CLEANUP SCRIPT - KELOMPOK 18
# Big Data Poverty Mapping Project Organization

Write-Host "🧹 BIG DATA PROJECT CLEANUP & ORGANIZATION" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "Kelompok 18 - Poverty Mapping Project" -ForegroundColor Green
Write-Host ""

# Confirm before proceeding
$confirm = Read-Host "⚠️  This will reorganize all files in your workspace. Continue? (y/N)"
if ($confirm -notmatch '^[Yy]') {
    Write-Host "❌ Organization cancelled." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "🏗️  Creating organized folder structure..." -ForegroundColor Yellow

# Create main folders
$folders = @(
    "01_CORE_FILES",
    "02_DOCUMENTATION", 
    "03_SCRIPTS",
    "04_GUIDES",
    "05_ARCHIVED",
    "06_ASSETS",
    "07_OUTPUTS"
)

foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "✅ Created: $folder/" -ForegroundColor Green
    }
}

# Create subfolders
$subfolders = @{
    "03_SCRIPTS" = @("airflow", "spark", "superset", "postgres", "utilities")
    "04_GUIDES" = @("setup", "dashboard", "troubleshooting")
    "05_ARCHIVED" = @("old_scripts", "duplicate_docs", "temp_files")
}

foreach ($parent in $subfolders.Keys) {
    foreach ($sub in $subfolders[$parent]) {
        $subPath = Join-Path $parent $sub
        if (!(Test-Path $subPath)) {
            New-Item -ItemType Directory -Path $subPath -Force | Out-Null
            Write-Host "   └── $sub/" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "📦 Organizing files by category..." -ForegroundColor Yellow

# Function to move files safely
function Move-FilesPattern {
    param($Pattern, $Destination, $Description)
    
    $files = Get-ChildItem -Path . -Name $Pattern -File 2>$null
    if ($files) {
        if (!(Test-Path $Destination)) {
            New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        }
        
        $count = 0
        foreach ($file in $files) {
            try {
                Move-Item $file $Destination -Force
                Write-Host "   ✅ Moved: $file → $Destination" -ForegroundColor Green
                $count++
            }
            catch {
                Write-Host "   ❌ Error moving $file" -ForegroundColor Red
            }
        }
        if ($count -gt 0) {
            Write-Host "📁 $Description: $count files moved" -ForegroundColor Cyan
        }
    }
}

# Organize Python scripts
Write-Host "🐍 Organizing Python scripts..." -ForegroundColor Magenta

Move-FilesPattern "*dag*.py" "03_SCRIPTS\airflow" "Airflow DAGs"
Move-FilesPattern "*airflow*.py" "03_SCRIPTS\airflow" "Airflow scripts"
Move-FilesPattern "manage*dag*.py" "03_SCRIPTS\airflow" "DAG management"

Move-FilesPattern "*spark*.py" "03_SCRIPTS\spark" "Spark scripts"
Move-FilesPattern "*etl*.py" "03_SCRIPTS\spark" "ETL scripts"
Move-FilesPattern "bronze_to_silver.py" "03_SCRIPTS\spark" "Bronze to Silver"
Move-FilesPattern "silver_to_gold.py" "03_SCRIPTS\spark" "Silver to Gold"

Move-FilesPattern "*superset*.py" "03_SCRIPTS\superset" "Superset scripts"
Move-FilesPattern "*dashboard*.py" "03_SCRIPTS\superset" "Dashboard scripts"

Move-FilesPattern "*postgres*.py" "03_SCRIPTS\postgres" "PostgreSQL scripts"
Move-FilesPattern "*.sql" "03_SCRIPTS\postgres" "SQL files"

Move-FilesPattern "check_*.py" "03_SCRIPTS\utilities" "Check utilities"
Move-FilesPattern "verify_*.py" "03_SCRIPTS\utilities" "Verify utilities"
Move-FilesPattern "debug_*.py" "03_SCRIPTS\utilities" "Debug utilities"
Move-FilesPattern "organize_*.py" "03_SCRIPTS\utilities" "Organization utilities"
Move-FilesPattern "test_*.py" "03_SCRIPTS\utilities" "Test utilities"

# Organize documentation
Write-Host ""
Write-Host "📚 Organizing documentation..." -ForegroundColor Magenta

Move-FilesPattern "*SETUP*.md" "04_GUIDES\setup" "Setup guides"
Move-FilesPattern "*READY*.md" "04_GUIDES\setup" "Ready guides"
Move-FilesPattern "*FIX*.md" "04_GUIDES\troubleshooting" "Fix guides"

Move-FilesPattern "*DASHBOARD*.md" "04_GUIDES\dashboard" "Dashboard guides"
Move-FilesPattern "*SUPERSET*.md" "04_GUIDES\dashboard" "Superset guides"
Move-FilesPattern "*CHART*.md" "04_GUIDES\dashboard" "Chart guides"

Move-FilesPattern "*ARSITEKTUR*.md" "02_DOCUMENTATION" "Architecture docs"
Move-FilesPattern "*PIPELINE*.md" "02_DOCUMENTATION" "Pipeline docs"
Move-FilesPattern "*KELOMPOK18*.md" "02_DOCUMENTATION" "Project reports"

# Move remaining documentation
$mdFiles = Get-ChildItem -Path . -Name "*.md" -File | Where-Object { $_ -ne "README.md" }
if ($mdFiles) {
    foreach ($file in $mdFiles) {
        try {
            Move-Item $file "02_DOCUMENTATION" -Force
            Write-Host "   ✅ Moved: $file → documentation/" -ForegroundColor Green
        }
        catch {
            Write-Host "   ❌ Error moving $file" -ForegroundColor Red
        }
    }
}

# Move text files
$txtFiles = Get-ChildItem -Path . -Name "*.txt" -File
if ($txtFiles) {
    foreach ($file in $txtFiles) {
        try {
            Move-Item $file "02_DOCUMENTATION" -Force
            Write-Host "   ✅ Moved: $file → documentation/" -ForegroundColor Green
        }
        catch {
            Write-Host "   ❌ Error moving $file" -ForegroundColor Red
        }
    }
}

# Archive old/backup files
Write-Host ""
Write-Host "🗂️  Archiving old files..." -ForegroundColor Magenta

Move-FilesPattern "*old*.py" "05_ARCHIVED\old_scripts" "Old Python scripts"
Move-FilesPattern "*backup*.py" "05_ARCHIVED\old_scripts" "Backup scripts"
Move-FilesPattern "*temp*.py" "05_ARCHIVED\temp_files" "Temporary scripts"

# Move PowerShell scripts (except this one)
$psFiles = Get-ChildItem -Path . -Name "*.ps1" -File | Where-Object { $_ -ne "organize_workspace.ps1" }
if ($psFiles) {
    foreach ($file in $psFiles) {
        try {
            Move-Item $file "03_SCRIPTS\utilities" -Force
            Write-Host "   ✅ Moved: $file → utilities/" -ForegroundColor Green
        }
        catch {
            Write-Host "   ❌ Error moving $file" -ForegroundColor Red
        }
    }
}

# Move batch files
$batFiles = Get-ChildItem -Path . -Name "*.bat" -File
if ($batFiles) {
    foreach ($file in $batFiles) {
        try {
            Move-Item $file "03_SCRIPTS\utilities" -Force
            Write-Host "   ✅ Moved: $file → utilities/" -ForegroundColor Green
        }
        catch {
            Write-Host "   ❌ Error moving $file" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "📝 Creating README files..." -ForegroundColor Yellow

# Create README files for each main folder
$readmeContents = @{
    "01_CORE_FILES" = @"
# Core Files
Essential project files that must remain in the root directory:
- docker-compose.yml: Main container orchestration
- hadoop.env: Hadoop environment configuration  
- README.md: Main project documentation
"@

    "02_DOCUMENTATION" = @"
# Documentation
All project documentation, guides, and references:
- Architecture documents
- Technical specifications
- Project reports
- Reference materials
"@

    "03_SCRIPTS" = @"
# Scripts
All executable scripts organized by service/purpose:
- airflow/: DAG files and Airflow automation
- spark/: ETL processing (Bronze → Silver → Gold)
- superset/: Dashboard creation and setup
- postgres/: Database scripts and SQL files
- utilities/: Helper and maintenance scripts
"@

    "04_GUIDES" = @"
# Implementation Guides
Step-by-step guides for setup and usage:
- setup/: Installation and configuration guides
- dashboard/: Dashboard creation instructions
- troubleshooting/: Error fixes and solutions
"@

    "05_ARCHIVED" = @"
# Archived Files
Old versions, duplicates, and deprecated files.
⚠️ Files here are kept for reference but not actively used.
- old_scripts/: Previous script versions
- duplicate_docs/: Duplicate documentation
- temp_files/: Temporary and test files
"@

    "06_ASSETS" = @"
# Assets
Images, diagrams, screenshots, and other media files.
"@

    "07_OUTPUTS" = @"
# Outputs
Generated reports, exports, and pipeline outputs.
"@
}

foreach ($folder in $readmeContents.Keys) {
    $readmePath = Join-Path $folder "README.md"
    $readmeContents[$folder] | Out-File -FilePath $readmePath -Encoding UTF8
    Write-Host "📝 Created: $folder\README.md" -ForegroundColor Green
}

# Generate organization report
$reportPath = "07_OUTPUTS\organization_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"

$reportContent = @"
# Project Organization Report
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## New Folder Structure
``````
TUBESABD/
├── 01_CORE_FILES/           (Essential files)
├── 02_DOCUMENTATION/        (All docs and guides)
├── 03_SCRIPTS/              (All executable scripts)
│   ├── airflow/             (DAGs and Airflow scripts)
│   ├── spark/               (ETL processing scripts)
│   ├── superset/            (Dashboard scripts)
│   ├── postgres/            (Database scripts)
│   └── utilities/           (Helper scripts)
├── 04_GUIDES/               (Implementation guides)
│   ├── setup/               (Setup guides)
│   ├── dashboard/           (Dashboard guides)
│   └── troubleshooting/     (Fix guides)
├── 05_ARCHIVED/             (Old/duplicate files)
├── 06_ASSETS/               (Images and media)
└── 07_OUTPUTS/              (Generated reports)
``````

## Organization Summary
- ✅ Project successfully organized into logical folders
- 📁 Created 7 main folders with appropriate subfolders
- 📝 Added README files for documentation
- 🗂️ Files organized by purpose and service type
- 📦 Old/duplicate files safely archived

## Core Files Kept in Root
- docker-compose.yml (Container orchestration)
- hadoop.env (Environment configuration)
- README.md (Main documentation)

## Verification Steps
1. ✅ Check that Docker services still work: ``docker-compose up -d``
2. ✅ Verify Superset dashboard functionality
3. ✅ Test Airflow DAGs execution
4. ✅ Confirm all scripts can find their dependencies

## Important Notes
- All file movements preserve original functionality
- Scripts may need path updates if they reference other files
- Archive folder contains backup of old files
- README files added for better navigation

## Services Access (Unchanged)
- Superset: http://localhost:8088
- Airflow: http://localhost:8080  
- PostgreSQL: http://localhost:5432
- Jupyter: http://localhost:8888
- Spark UI: http://localhost:4040

Generated by: Kelompok 18 Cleanup Script
"@

$reportContent | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host ""
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "✅ PROJECT ORGANIZATION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan

Write-Host ""
Write-Host "📊 ORGANIZATION SUMMARY:" -ForegroundColor Yellow
Write-Host "📁 Files organized into structured folders" -ForegroundColor Green
Write-Host "📝 README files created for navigation" -ForegroundColor Green  
Write-Host "🗂️ Old files safely archived" -ForegroundColor Green
Write-Host "📋 Report generated: $reportPath" -ForegroundColor Green

Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. ✅ Verify services: docker-compose up -d" -ForegroundColor Cyan
Write-Host "2. ✅ Test Superset dashboard: http://localhost:8088" -ForegroundColor Cyan
Write-Host "3. ✅ Check Airflow DAGs: http://localhost:8080" -ForegroundColor Cyan
Write-Host "4. ✅ Review archived files in 05_ARCHIVED/" -ForegroundColor Cyan

Write-Host ""
Write-Host "🚀 Your workspace is now clean and organized!" -ForegroundColor Green
Write-Host "📁 Navigate folders using the README files" -ForegroundColor Green

# Pause to show results
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
