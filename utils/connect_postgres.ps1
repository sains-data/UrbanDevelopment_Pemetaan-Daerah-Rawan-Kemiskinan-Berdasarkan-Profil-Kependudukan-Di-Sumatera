# PostgreSQL Connection Script
# Quick connection to PostgreSQL database

Write-Host "=== PostgreSQL Database Connection ===" -ForegroundColor Green

# Database connection details
$host = "localhost"
$port = "5432"
$database = "poverty_mapping"
$username = "postgres"
$password = "postgres123"

Write-Host "`n📋 Connection Details:" -ForegroundColor Yellow
Write-Host "   Host: $host" -ForegroundColor Cyan
Write-Host "   Port: $port" -ForegroundColor Cyan
Write-Host "   Database: $database" -ForegroundColor Cyan
Write-Host "   Username: $username" -ForegroundColor Cyan
Write-Host "   Password: $password" -ForegroundColor Cyan

# Check if PostgreSQL container is running
Write-Host "`n🔍 Checking PostgreSQL Container..." -ForegroundColor Yellow
try {
    $containerStatus = docker ps --filter "name=postgres-local" --format "{{.Status}}"
    if ($containerStatus) {
        Write-Host "✅ PostgreSQL container is running: $containerStatus" -ForegroundColor Green
    } else {
        Write-Host "❌ PostgreSQL container is not running" -ForegroundColor Red
        Write-Host "💡 Starting PostgreSQL container..." -ForegroundColor Yellow
        docker-compose up -d postgres
        Start-Sleep -Seconds 10
    }
} catch {
    Write-Host "❌ Error checking container status" -ForegroundColor Red
}

# Test database connection
Write-Host "`n🔗 Testing Database Connection..." -ForegroundColor Yellow
try {
    $testQuery = "SELECT version();"
    $result = docker exec postgres-local psql -U $username -d $database -c $testQuery 2>$null
    if ($result) {
        Write-Host "✅ Database connection successful!" -ForegroundColor Green
        Write-Host "   PostgreSQL Version: $($result -split "`n" | Select-Object -Skip 2 -First 1)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Database connection failed" -ForegroundColor Red
}

# Show available databases
Write-Host "`n📊 Available Databases:" -ForegroundColor Yellow
try {
    $databases = docker exec postgres-local psql -U $username -c "\l" 2>$null
    if ($databases) {
        $databases -split "`n" | Select-Object -Skip 3 | ForEach-Object {
            if ($_ -and $_ -notmatch "^\s*$" -and $_ -notmatch "^\s*-") {
                Write-Host "   $_" -ForegroundColor Cyan
            }
        }
    }
} catch {
    Write-Host "   Unable to retrieve database list" -ForegroundColor Red
}

# Connection commands
Write-Host "`n🚀 Quick Connection Commands:" -ForegroundColor Yellow
Write-Host "   Command Line: psql -h $host -p $port -U $username -d $database" -ForegroundColor Cyan
Write-Host "   Docker Exec: docker exec -it postgres-local psql -U $username -d $database" -ForegroundColor Cyan

# DBeaver/pgAdmin connection string
Write-Host "`n🔧 GUI Tools Connection:" -ForegroundColor Yellow
Write-Host "   Host: $host" -ForegroundColor Cyan
Write-Host "   Port: $port" -ForegroundColor Cyan
Write-Host "   Database: $database" -ForegroundColor Cyan
Write-Host "   Username: $username" -ForegroundColor Cyan
Write-Host "   Password: $password" -ForegroundColor Cyan

# Python connection example
Write-Host "`n🐍 Python Connection Example:" -ForegroundColor Yellow
Write-Host "   import psycopg2" -ForegroundColor Cyan
Write-Host "   conn = psycopg2.connect(host='$host', port=$port, database='$database', user='$username', password='$password')" -ForegroundColor Cyan

Write-Host "`n✅ PostgreSQL is ready for connections!" -ForegroundColor Green
Write-Host "📖 For detailed guide, see: docs\POSTGRESQL_CONNECTION_GUIDE.md" -ForegroundColor Yellow
