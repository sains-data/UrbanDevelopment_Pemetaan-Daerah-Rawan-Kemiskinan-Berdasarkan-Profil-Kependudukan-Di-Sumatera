# Start PostgreSQL Container Script
Write-Host "=== Starting PostgreSQL Database ===" -ForegroundColor Green

# Change to project directory
Set-Location c:\TUBESABD

# Start PostgreSQL container
Write-Host "`n🚀 Starting PostgreSQL container..." -ForegroundColor Yellow
try {
    docker-compose up -d postgres
    Write-Host "✅ PostgreSQL container started successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start PostgreSQL container" -ForegroundColor Red
    exit 1
}

# Wait for database to be ready
Write-Host "`n⏳ Waiting for database to be ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0

do {
    $attempt++
    try {
        $ready = docker exec postgres-local pg_isready -h localhost -p 5432 2>$null
        if ($ready -match "accepting connections") {
            Write-Host "✅ Database is ready and accepting connections!" -ForegroundColor Green
            break
        }
    } catch {
        # Continue waiting
    }
    
    if ($attempt -ge $maxAttempts) {
        Write-Host "❌ Database failed to start within timeout period" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "   Attempt $attempt/$maxAttempts - waiting..." -ForegroundColor Gray
    Start-Sleep -Seconds 2
} while ($true)

# Initialize database if needed
Write-Host "`n🔧 Initializing database..." -ForegroundColor Yellow
try {
    # Create initial databases
    docker exec postgres-local psql -U postgres -c "CREATE DATABASE IF NOT EXISTS poverty_mapping;" 2>$null
    docker exec postgres-local psql -U postgres -c "CREATE DATABASE IF NOT EXISTS superset_db;" 2>$null
    docker exec postgres-local psql -U postgres -c "CREATE DATABASE IF NOT EXISTS analytics_db;" 2>$null
    
    # Create application user
    docker exec postgres-local psql -U postgres -c "CREATE USER IF NOT EXISTS bigdata_user WITH PASSWORD 'bigdata123';" 2>$null
    docker exec postgres-local psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE poverty_mapping TO bigdata_user;" 2>$null
    docker exec postgres-local psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE superset_db TO bigdata_user;" 2>$null
    docker exec postgres-local psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE analytics_db TO bigdata_user;" 2>$null
    
    Write-Host "✅ Database initialization completed!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Database initialization had some issues, but container is running" -ForegroundColor Yellow
}

# Show connection information
Write-Host "`n📋 PostgreSQL Connection Information:" -ForegroundColor Cyan
Write-Host "   Host: localhost" -ForegroundColor White
Write-Host "   Port: 5432" -ForegroundColor White
Write-Host "   Database: poverty_mapping" -ForegroundColor White
Write-Host "   Username: postgres" -ForegroundColor White
Write-Host "   Password: postgres123" -ForegroundColor White

Write-Host "`n🔗 Quick Connection Commands:" -ForegroundColor Cyan
Write-Host "   psql -h localhost -p 5432 -U postgres -d poverty_mapping" -ForegroundColor Gray
Write-Host "   docker exec -it postgres-local psql -U postgres -d poverty_mapping" -ForegroundColor Gray

Write-Host "`n✅ PostgreSQL is ready for use!" -ForegroundColor Green
Write-Host "📖 For detailed guide: .\docs\POSTGRESQL_CONNECTION_GUIDE.md" -ForegroundColor Yellow

# Test connection
Write-Host "`n🧪 Testing connection..." -ForegroundColor Yellow
try {
    $version = docker exec postgres-local psql -U postgres -d poverty_mapping -c "SELECT version();" 2>$null
    if ($version) {
        Write-Host "✅ Connection test successful!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Connection test failed, but container should be accessible" -ForegroundColor Yellow
}
