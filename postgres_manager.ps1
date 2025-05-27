#!/usr/bin/env powershell
<#
.SYNOPSIS
PostgreSQL Container Manager untuk Big Data Poverty Mapping Pipeline
Kelompok 18 - Sumatra

.DESCRIPTION
Script untuk mengelola container PostgreSQL dan mengekspos port ke jaringan lokal
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop", "restart", "status", "connect", "init", "help")]
    [string]$Action = "status"
)

# Colors for output
$GREEN = "Green"
$RED = "Red"
$YELLOW = "Yellow"
$BLUE = "Cyan"

function Write-ColorOutput {
    param($Message, $Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-Header {
    Write-Host "=" * 60 -ForegroundColor Blue
    Write-ColorOutput "🐘 PostgreSQL Container Manager" $BLUE
    Write-ColorOutput "📊 Big Data Poverty Mapping - Kelompok 18" $BLUE
    Write-Host "=" * 60 -ForegroundColor Blue
}

function Show-PostgreSQLStatus {
    Write-ColorOutput "📋 Checking PostgreSQL Container Status..." $YELLOW
    
    # Check if container exists and is running
    $containerStatus = docker ps --filter "name=postgres-local" --format "{{.Status}}" 2>$null
    
    if ($containerStatus) {
        Write-ColorOutput "✅ Container Status: $containerStatus" $GREEN
        
        # Check if PostgreSQL is ready
        $pgReady = docker exec postgres-local pg_isready -U postgres 2>$null
        if ($pgReady -match "accepting connections") {
            Write-ColorOutput "✅ PostgreSQL: Ready to accept connections" $GREEN
        } else {
            Write-ColorOutput "⚠️  PostgreSQL: Not ready" $YELLOW
        }
        
        # Show connection info
        Write-ColorOutput "`n🔗 Connection Information:" $BLUE
        Write-Host "   Host: localhost (or your machine's IP)"
        Write-Host "   Port: 5432"
        Write-Host "   Database: poverty_mapping"
        Write-Host "   Username: postgres"
        Write-Host "   Password: postgres123"
        
    } else {
        Write-ColorOutput "❌ PostgreSQL container is not running" $RED
        Write-ColorOutput "💡 Run: ./postgres_manager.ps1 start" $YELLOW
    }
}

function Start-PostgreSQL {
    Write-ColorOutput "🚀 Starting PostgreSQL container..." $YELLOW
    
    try {
        docker-compose up -d postgres
        Start-Sleep 10
        
        $pgReady = docker exec postgres-local pg_isready -U postgres 2>$null
        if ($pgReady -match "accepting connections") {
            Write-ColorOutput "✅ PostgreSQL started successfully!" $GREEN
            Show-PostgreSQLStatus
        } else {
            Write-ColorOutput "⚠️  PostgreSQL starting... please wait" $YELLOW
        }
    } catch {
        Write-ColorOutput "❌ Failed to start PostgreSQL: $_" $RED
    }
}

function Stop-PostgreSQL {
    Write-ColorOutput "🛑 Stopping PostgreSQL container..." $YELLOW
    
    try {
        docker-compose stop postgres
        Write-ColorOutput "✅ PostgreSQL stopped successfully!" $GREEN
    } catch {
        Write-ColorOutput "❌ Failed to stop PostgreSQL: $_" $RED
    }
}

function Restart-PostgreSQL {
    Write-ColorOutput "🔄 Restarting PostgreSQL container..." $YELLOW
    Stop-PostgreSQL
    Start-Sleep 5
    Start-PostgreSQL
}

function Connect-PostgreSQL {
    Write-ColorOutput "🔌 Connecting to PostgreSQL..." $YELLOW
    
    try {
        # Test connection first
        $pgReady = docker exec postgres-local pg_isready -U postgres 2>$null
        if ($pgReady -match "accepting connections") {
            Write-ColorOutput "✅ Opening PostgreSQL shell..." $GREEN
            docker exec -it postgres-local psql -U postgres -d poverty_mapping
        } else {
            Write-ColorOutput "❌ PostgreSQL is not ready. Please start it first." $RED
        }
    } catch {
        Write-ColorOutput "❌ Failed to connect: $_" $RED
    }
}

function Initialize-Database {
    Write-ColorOutput "🏗️  Initializing poverty mapping database..." $YELLOW
    
    $sql = @"
-- Create database if not exists
SELECT 'CREATE DATABASE poverty_mapping' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'poverty_mapping');

-- Create tables for poverty mapping
CREATE TABLE IF NOT EXISTS poverty_data (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100),
    regency VARCHAR(100),
    district VARCHAR(100),
    village VARCHAR(100),
    poverty_percentage DECIMAL(5,2),
    population INTEGER,
    poor_population INTEGER,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS province_summary (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100) UNIQUE,
    total_regencies INTEGER,
    avg_poverty_rate DECIMAL(5,2),
    total_population INTEGER,
    total_poor_population INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_poverty_province ON poverty_data(province);
CREATE INDEX IF NOT EXISTS idx_poverty_coordinates ON poverty_data(latitude, longitude);

-- Insert sample data check
INSERT INTO poverty_data (province, regency, district, village, poverty_percentage, population, poor_population, latitude, longitude)
VALUES ('Sumatera Utara', 'Medan', 'Medan Kota', 'Kampung Baru', 12.5, 50000, 6250, 3.5952, 98.6722)
ON CONFLICT DO NOTHING;

SELECT 'Database initialized successfully!' as message;
"@

    try {
        $sql | docker exec -i postgres-local psql -U postgres -d poverty_mapping
        Write-ColorOutput "✅ Database initialized successfully!" $GREEN
    } catch {
        Write-ColorOutput "❌ Failed to initialize database: $_" $RED
    }
}

function Test-NetworkConnection {
    Write-ColorOutput "🌐 Testing network connectivity..." $YELLOW
    
    # Get machine IP
    $machineIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"})[0].IPAddress
    
    Write-ColorOutput "🖥️  Machine IP: $machineIP" $BLUE
    Write-ColorOutput "🔗 PostgreSQL is accessible from:" $BLUE
    Write-Host "   • localhost:5432"
    Write-Host "   • 127.0.0.1:5432"
    Write-Host "   • ${machineIP}:5432"
    
    Write-ColorOutput "`n📱 Connection strings:" $BLUE
    Write-Host "   • JDBC: jdbc:postgresql://localhost:5432/poverty_mapping"
    Write-Host "   • Python: postgresql://postgres:postgres123@localhost:5432/poverty_mapping"
    Write-Host "   • .NET: Host=localhost;Port=5432;Database=poverty_mapping;Username=postgres;Password=postgres123"
}

function Show-Help {
    Write-ColorOutput "`n📖 PostgreSQL Manager - Usage:" $BLUE
    Write-Host "   ./postgres_manager.ps1 start     - Start PostgreSQL container"
    Write-Host "   ./postgres_manager.ps1 stop      - Stop PostgreSQL container"
    Write-Host "   ./postgres_manager.ps1 restart   - Restart PostgreSQL container"
    Write-Host "   ./postgres_manager.ps1 status    - Show container status"
    Write-Host "   ./postgres_manager.ps1 connect   - Connect to PostgreSQL shell"
    Write-Host "   ./postgres_manager.ps1 init      - Initialize poverty mapping database"
    Write-Host "   ./postgres_manager.ps1 help      - Show this help"
    
    Write-ColorOutput "`n🔧 Examples:" $YELLOW
    Write-Host "   # Start PostgreSQL and initialize database"
    Write-Host "   ./postgres_manager.ps1 start"
    Write-Host "   ./postgres_manager.ps1 init"
    Write-Host ""
    Write-Host "   # Connect from external application"
    Write-Host "   psql -h localhost -p 5432 -U postgres -d poverty_mapping"
}

# Main execution
Show-Header

switch ($Action.ToLower()) {
    "start" { 
        Start-PostgreSQL
        Test-NetworkConnection
    }
    "stop" { Stop-PostgreSQL }
    "restart" { Restart-PostgreSQL }
    "status" { 
        Show-PostgreSQLStatus
        Test-NetworkConnection
    }
    "connect" { Connect-PostgreSQL }
    "init" { Initialize-Database }
    "help" { Show-Help }
    default { 
        Show-PostgreSQLStatus
        Test-NetworkConnection
    }
}

Write-ColorOutput "`n✨ PostgreSQL Manager completed!" $GREEN
