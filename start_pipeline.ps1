# Big Data Pipeline Executor - Sumatra Poverty Mapping
# Kelompok 18 - Quick Start Script

param(
    [switch]$CheckOnly,
    [switch]$StartServices,
    [switch]$RunPipeline,
    [switch]$ViewDashboard
)

Write-Host "🚀 BIG DATA PIPELINE - SUMATRA POVERTY MAPPING" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host "Kelompok 18 - Automated ETL Pipeline" -ForegroundColor Cyan
Write-Host ""

# Function to check service status
function Check-Services {
    Write-Host "🔍 Checking Docker services..." -ForegroundColor Yellow
    
    $services = @(
        @{Name="namenode"; Port="9870"; Description="Hadoop NameNode"},
        @{Name="spark-master"; Port="8080"; Description="Spark Master"},
        @{Name="airflow-webserver"; Port="8090"; Description="Airflow WebServer"},
        @{Name="superset"; Port="8089"; Description="Apache Superset"},
        @{Name="jupyter"; Port="8888"; Description="Jupyter Notebook"}
    )
    
    foreach ($service in $services) {
        try {
            $result = docker ps --filter "name=$($service.Name)" --format "{{.Status}}"
            if ($result -like "*Up*") {
                Write-Host "  ✅ $($service.Description): http://localhost:$($service.Port)" -ForegroundColor Green
            } else {
                Write-Host "  ❌ $($service.Description): Not running" -ForegroundColor Red
            }
        } catch {
            Write-Host "  ❌ $($service.Description): Error checking status" -ForegroundColor Red
        }
    }
    Write-Host ""
}

# Function to start Docker services
function Start-Services {
    Write-Host "🚀 Starting Docker services..." -ForegroundColor Yellow
    
    try {
        docker-compose up -d
        Write-Host "✅ Docker services started" -ForegroundColor Green
        Write-Host "⏳ Waiting 30 seconds for services to initialize..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        Check-Services
    } catch {
        Write-Host "❌ Failed to start services: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Function to run the complete pipeline
function Run-Pipeline {
    Write-Host "🔄 Executing complete data pipeline..." -ForegroundColor Yellow
    
    try {
        python run_pipeline.py
        Write-Host "✅ Pipeline execution completed" -ForegroundColor Green
    } catch {
        Write-Host "❌ Pipeline execution failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Function to open dashboards
function Open-Dashboards {
    Write-Host "🌐 Opening dashboards..." -ForegroundColor Yellow
    
    $urls = @(
        "http://localhost:8090",  # Airflow
        "http://localhost:8089",  # Superset  
        "http://localhost:8080",  # Spark
        "http://localhost:9870"   # HDFS
    )
    
    foreach ($url in $urls) {
        try {
            Start-Process $url
            Write-Host "  ✅ Opened: $url" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Failed to open: $url" -ForegroundColor Red
        }
    }
}

# Main execution logic
if ($CheckOnly) {
    Check-Services
} elseif ($StartServices) {
    Start-Services
} elseif ($RunPipeline) {
    Check-Services
    if ((Read-Host "Continue with pipeline execution? (y/n)") -eq 'y') {
        Run-Pipeline
    }
} elseif ($ViewDashboard) {
    Open-Dashboards
} else {
    # Default: Interactive menu
    Write-Host "Select an option:" -ForegroundColor Cyan
    Write-Host "1. Check service status" -ForegroundColor White
    Write-Host "2. Start Docker services" -ForegroundColor White  
    Write-Host "3. Run complete pipeline" -ForegroundColor White
    Write-Host "4. Open dashboards" -ForegroundColor White
    Write-Host "5. Exit" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-5)"
    
    switch ($choice) {
        "1" { Check-Services }
        "2" { Start-Services }
        "3" { 
            Check-Services
            if ((Read-Host "Continue with pipeline execution? (y/n)") -eq 'y') {
                Run-Pipeline
            }
        }
        "4" { Open-Dashboards }
        "5" { 
            Write-Host "👋 Goodbye!" -ForegroundColor Green
            exit 
        }
        default {
            Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "📊 QUICK ACCESS URLS:" -ForegroundColor Cyan
Write-Host "  - Airflow: http://localhost:8090 (admin/admin)" -ForegroundColor White
Write-Host "  - Superset: http://localhost:8089 (admin/admin)" -ForegroundColor White
Write-Host "  - Spark UI: http://localhost:8080" -ForegroundColor White
Write-Host "  - HDFS: http://localhost:9870" -ForegroundColor White
Write-Host "  - Jupyter: http://localhost:8888" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Usage Examples:" -ForegroundColor Cyan
Write-Host "  .\start_pipeline.ps1 -CheckOnly" -ForegroundColor Gray
Write-Host "  .\start_pipeline.ps1 -StartServices" -ForegroundColor Gray
Write-Host "  .\start_pipeline.ps1 -RunPipeline" -ForegroundColor Gray
Write-Host "  .\start_pipeline.ps1 -ViewDashboard" -ForegroundColor Gray
