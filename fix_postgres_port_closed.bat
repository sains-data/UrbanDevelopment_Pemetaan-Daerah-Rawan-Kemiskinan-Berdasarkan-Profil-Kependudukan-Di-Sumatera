@echo off
echo ==========================================
echo FIX POSTGRESQL PORT CLOSED ERROR
echo Kelompok 18 - Big Data Poverty Mapping
echo ==========================================

echo.
echo [STEP 1] Checking current container status...
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo [STEP 2] Stopping all containers...
docker-compose down

echo.
echo [STEP 3] Starting PostgreSQL container...
docker-compose up -d postgres

echo.
echo [STEP 4] Waiting for PostgreSQL to be ready...
timeout /t 15 /nobreak

echo.
echo [STEP 5] Starting Superset container...
docker-compose up -d superset

echo.
echo [STEP 6] Waiting for all services...
timeout /t 30 /nobreak

echo.
echo [STEP 7] Checking final status...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo [STEP 8] Testing PostgreSQL connection...
docker exec postgres-local psql -U postgres -d poverty_mapping -c "SELECT COUNT(*) FROM poverty_data;" 2>nul
if %errorlevel% == 0 (
    echo ✅ PostgreSQL: WORKING - Port 5432 OPEN
) else (
    echo ❌ PostgreSQL: STILL NOT WORKING
)

echo.
echo ==========================================
echo SOLUTION FOR SUPERSET DATABASE CONNECTION:
echo ==========================================
echo.
echo Use these connection details in Superset:
echo.
echo Host: localhost
echo Port: 5432  
echo Database name: poverty_mapping
echo Username: postgres
echo Password: postgres123
echo.
echo OR use SQLAlchemy URI:
echo postgresql://postgres:postgres123@localhost:5432/poverty_mapping
echo.
echo ==========================================
echo Next: Open Superset at http://localhost:8089
echo ==========================================

pause
