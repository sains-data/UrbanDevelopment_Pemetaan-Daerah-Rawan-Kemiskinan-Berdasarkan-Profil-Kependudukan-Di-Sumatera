#!/usr/bin/env powershell
<#
.SYNOPSIS
Fix PostgreSQL Connection Issue in Superset

.DESCRIPTION
Script untuk mengatasi masalah "Port 5432 closed" saat menambahkan PostgreSQL connection di Superset.
Masalah disebabkan oleh missing psycopg2 driver di container Superset.
#>

Write-Host "=" * 60 -ForegroundColor Blue
Write-Host "🔧 FIXING POSTGRESQL CONNECTION IN SUPERSET" -ForegroundColor Cyan
Write-Host "📊 Kelompok 18 - Big Data Pipeline" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Blue

function Test-ContainerRunning {
    param($ContainerName)
    
    $status = docker ps --filter "name=$ContainerName" --format "{{.Status}}" 2>$null
    return $status -ne $null -and $status -ne ""
}

function Wait-ForContainer {
    param($ContainerName, $MaxWait = 60)
    
    Write-Host "⏳ Waiting for $ContainerName to be ready..." -ForegroundColor Yellow
    
    $waited = 0
    while ($waited -lt $MaxWait) {
        if (Test-ContainerRunning $ContainerName) {
            $health = docker ps --filter "name=$ContainerName" --format "{{.Status}}" 2>$null
            if ($health -match "healthy" -or $health -notmatch "starting") {
                Write-Host "✅ $ContainerName is ready!" -ForegroundColor Green
                return $true
            }
        }
        Start-Sleep 5
        $waited += 5
        Write-Host "  ⏳ Still waiting... ($waited/$MaxWait seconds)" -ForegroundColor Gray
    }
    
    Write-Host "❌ $ContainerName not ready after $MaxWait seconds" -ForegroundColor Red
    return $false
}

# Step 1: Check container status
Write-Host "`n🔍 Checking container status..." -ForegroundColor Yellow

if (-not (Test-ContainerRunning "postgres-local")) {
    Write-Host "❌ PostgreSQL container not running. Starting..." -ForegroundColor Red
    docker-compose up -d postgres
    if (-not (Wait-ForContainer "postgres-local")) {
        Write-Host "❌ Failed to start PostgreSQL container" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ PostgreSQL container: Running" -ForegroundColor Green
}

if (-not (Test-ContainerRunning "superset")) {
    Write-Host "❌ Superset container not running. Starting..." -ForegroundColor Red
    docker-compose up -d superset
    if (-not (Wait-ForContainer "superset")) {
        Write-Host "❌ Failed to start Superset container" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Superset container: Running" -ForegroundColor Green
}

# Step 2: Install PostgreSQL driver
Write-Host "`n🔧 Installing PostgreSQL driver in Superset..." -ForegroundColor Yellow

try {
    # Check if psycopg2 is already installed
    $checkResult = docker exec superset python -c "import psycopg2; print('already_installed')" 2>$null
    
    if ($checkResult -match "already_installed") {
        Write-Host "✅ PostgreSQL driver already installed" -ForegroundColor Green
    } else {
        Write-Host "📦 Installing psycopg2-binary..." -ForegroundColor Yellow
        docker exec superset pip install psycopg2-binary
        Write-Host "✅ PostgreSQL driver installed successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Failed to install PostgreSQL driver: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Test network connectivity
Write-Host "`n🌐 Testing network connectivity..." -ForegroundColor Yellow

try {
    $networkTest = docker exec superset python -c "import socket; sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); result = sock.connect_ex(('postgres-local', 5432)); print('OK' if result == 0 else 'FAILED'); sock.close()" 2>$null
    
    if ($networkTest -match "OK") {
        Write-Host "✅ Network connectivity: OK" -ForegroundColor Green
    } else {
        Write-Host "❌ Network connectivity: FAILED" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Network test failed: $_" -ForegroundColor Red
    exit 1
}

# Step 4: Test PostgreSQL connection
Write-Host "`n🗄️ Testing PostgreSQL connection..." -ForegroundColor Yellow

try {
    $connectionTest = docker exec superset python -c "import psycopg2; conn = psycopg2.connect(host='postgres-local', port=5432, database='poverty_mapping', user='postgres', password='postgres123'); print('SUCCESS'); conn.close()" 2>$null
    
    if ($connectionTest -match "SUCCESS") {
        Write-Host "✅ PostgreSQL connection: SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "❌ PostgreSQL connection: FAILED" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Connection test failed: $_" -ForegroundColor Red
    exit 1
}

# Step 5: Restart Superset to ensure changes take effect
Write-Host "`n🔄 Restarting Superset to apply changes..." -ForegroundColor Yellow

docker restart superset > $null
if (Wait-ForContainer "superset" 90) {
    Write-Host "✅ Superset restarted successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️ Superset may still be starting..." -ForegroundColor Yellow
}

# Step 6: Final verification
Write-Host "`n✅ FINAL VERIFICATION:" -ForegroundColor Green
Write-Host "=" * 40 -ForegroundColor Green

# Verify driver one more time
$finalCheck = docker exec superset python -c "import psycopg2; conn = psycopg2.connect(host='postgres-local', port=5432, database='poverty_mapping', user='postgres', password='postgres123'); print('READY'); conn.close()" 2>$null

if ($finalCheck -match "READY") {
    Write-Host "🎉 PostgreSQL connection is now READY!" -ForegroundColor Green
    
    Write-Host "`n📋 NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Open Superset: http://localhost:8089" 
    Write-Host "2. Login: admin / admin"
    Write-Host "3. Go to Data > Databases > + DATABASE"
    Write-Host "4. Select PostgreSQL"
    Write-Host "5. Use connection URI:"
    Write-Host "   postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping" -ForegroundColor Yellow
    Write-Host "6. Test connection (should work now!)"
    Write-Host "7. Create datasets and build dashboards"
    
    Write-Host "`n🎯 CONNECTION DETAILS:" -ForegroundColor Blue
    Write-Host "Host: postgres-local"
    Write-Host "Port: 5432"
    Write-Host "Database: poverty_mapping"
    Write-Host "Username: postgres"
    Write-Host "Password: postgres123"
    
} else {
    Write-Host "❌ Final verification failed" -ForegroundColor Red
    Write-Host "🔧 Try running this script again or check logs manually" -ForegroundColor Yellow
}

Write-Host "`n" + "=" * 60 -ForegroundColor Blue
Write-Host "🔧 PostgreSQL Connection Fix Complete!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Blue
