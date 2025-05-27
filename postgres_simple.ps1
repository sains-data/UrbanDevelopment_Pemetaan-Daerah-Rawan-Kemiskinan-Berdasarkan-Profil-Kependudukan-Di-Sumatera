# PostgreSQL Container Manager
# Kelompok 18 - Big Data Poverty Mapping Pipeline

param(
    [string]$Action = "status"
)

Write-Host "=" * 60 -ForegroundColor Blue
Write-Host "PostgreSQL Container Manager" -ForegroundColor Cyan
Write-Host "Big Data Poverty Mapping - Kelompok 18" -ForegroundColor Cyan  
Write-Host "=" * 60 -ForegroundColor Blue

function Show-Status {
    Write-Host "Checking PostgreSQL Container Status..." -ForegroundColor Yellow
    
    $containerStatus = docker ps --filter "name=postgres-local" --format "{{.Status}}" 2>$null
    
    if ($containerStatus) {
        Write-Host "✅ Container Status: $containerStatus" -ForegroundColor Green
        
        $pgReady = docker exec postgres-local pg_isready -U postgres 2>$null
        if ($pgReady -match "accepting connections") {
            Write-Host "✅ PostgreSQL: Ready to accept connections" -ForegroundColor Green
        } else {
            Write-Host "⚠️  PostgreSQL: Not ready" -ForegroundColor Yellow
        }
        
        Write-Host ""
        Write-Host "Connection Information:" -ForegroundColor Cyan
        Write-Host "   Host: localhost"
        Write-Host "   Port: 5432"
        Write-Host "   Database: poverty_mapping"
        Write-Host "   Username: postgres"
        Write-Host "   Password: postgres123"
        
        # Get machine IP
        try {
            $machineIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"})[0].IPAddress
            Write-Host ""
            Write-Host "Network Access:" -ForegroundColor Cyan
            Write-Host "   • localhost:5432"
            Write-Host "   • 127.0.0.1:5432" 
            Write-Host "   • ${machineIP}:5432"
        } catch {
            Write-Host "   • localhost:5432" 
        }
        
    } else {
        Write-Host "❌ PostgreSQL container is not running" -ForegroundColor Red
        Write-Host "💡 Run: docker-compose up -d postgres" -ForegroundColor Yellow
    }
}

function Start-Postgres {
    Write-Host "Starting PostgreSQL container..." -ForegroundColor Yellow
    docker-compose up -d postgres
    Start-Sleep 10
    Show-Status
}

function Stop-Postgres {
    Write-Host "Stopping PostgreSQL container..." -ForegroundColor Yellow
    docker-compose stop postgres
    Write-Host "✅ PostgreSQL stopped" -ForegroundColor Green
}

function Connect-Postgres {
    Write-Host "Connecting to PostgreSQL..." -ForegroundColor Yellow
    docker exec -it postgres-local psql -U postgres -d poverty_mapping
}

function Test-Connection {
    Write-Host "Testing PostgreSQL connection..." -ForegroundColor Yellow
    
    $result = docker exec postgres-local psql -U postgres -d poverty_mapping -c "\l" 2>$null
    if ($result) {
        Write-Host "✅ Connection successful!" -ForegroundColor Green
        Write-Host "Database list:" -ForegroundColor Cyan
        docker exec postgres-local psql -U postgres -c "\l"
    } else {
        Write-Host "❌ Connection failed" -ForegroundColor Red
    }
}

# Main execution
switch ($Action.ToLower()) {
    "start" { Start-Postgres }
    "stop" { Stop-Postgres }
    "connect" { Connect-Postgres }
    "test" { Test-Connection }
    default { Show-Status }
}

Write-Host ""
Write-Host "Available commands:" -ForegroundColor Yellow
Write-Host "   .\postgres_manager.ps1 start    - Start PostgreSQL"
Write-Host "   .\postgres_manager.ps1 stop     - Stop PostgreSQL"  
Write-Host "   .\postgres_manager.ps1 connect  - Connect to PostgreSQL"
Write-Host "   .\postgres_manager.ps1 test     - Test connection"
Write-Host "   .\postgres_manager.ps1 status   - Show status (default)"
