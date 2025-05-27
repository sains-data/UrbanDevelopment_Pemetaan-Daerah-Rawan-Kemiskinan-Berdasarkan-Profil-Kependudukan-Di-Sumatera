@echo off
echo 🔄 Fixing "Database with same name already exists" error
echo =====================================================

echo.
echo 1. Stopping Superset container...
docker stop superset

echo.
echo 2. Waiting 5 seconds...
timeout /t 5 /nobreak

echo.
echo 3. Starting Superset container...
docker start superset

echo.
echo 4. Waiting 30 seconds for Superset to be ready...
timeout /t 30 /nobreak

echo.
echo ✅ Superset restarted successfully!
echo.
echo 🎯 SEKARANG COBA LAGI DI SUPERSET:
echo 1. Buka: http://localhost:8089
echo 2. Login: admin / admin
echo 3. Settings → Database Connections → + DATABASE
echo 4. PostgreSQL
echo 5. GUNAKAN NAMA DATABASE YANG BERBEDA:
echo.
echo    Database Name: KELOMPOK18_POVERTY_FINAL
echo    Host: postgres-local
echo    Port: 5432
echo    Database: poverty_mapping
echo    Username: postgres
echo    Password: postgres123
echo.
echo 💡 PENTING: Gunakan nama database yang UNIK!
echo    Contoh nama lain:
echo    - sumatera_poverty_db
echo    - poverty_kelompok18_2025
echo    - bigdata_poverty_final
echo.
echo 🔧 ALTERNATIF JIKA MASIH ERROR:
echo 1. Cek Settings → Database Connections dulu
echo 2. Kalau ada koneksi PostgreSQL, PAKAI yang sudah ada
echo 3. Jangan buat baru kalau sudah ada
echo.
pause
