@echo off
echo =================================
echo SUPERSET DATASET CREATION FIX
echo Kelompok 18 - Poverty Mapping
echo =================================

echo.
echo 1. Restarting containers...
docker-compose restart superset postgres

echo.
echo 2. Waiting for services to be ready...
timeout /t 30 /nobreak

echo.
echo 3. Checking container status...
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr -E "superset|postgres"

echo.
echo 4. Testing PostgreSQL connection...
docker exec postgres-local psql -U postgres -d poverty_mapping -c "SELECT COUNT(*) FROM poverty_data;" 2>nul
if %errorlevel% == 0 (
    echo ✅ PostgreSQL: OK
) else (
    echo ❌ PostgreSQL: ERROR
)

echo.
echo =================================
echo NEXT STEPS:
echo =================================
echo 1. Open Superset: http://localhost:8089
echo 2. Login: admin/admin
echo 3. Follow guide: SUPERSET_DATASET_ERROR_FIX.md
echo 4. Create database connection with these details:
echo    Host: postgres-local
echo    Port: 5432
echo    Database: poverty_mapping
echo    Username: postgres
echo    Password: postgres123
echo.
echo 5. Test in SQL Lab first before creating dataset
echo =================================

pause
