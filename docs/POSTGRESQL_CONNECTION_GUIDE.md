# PostgreSQL Connection Guide
# Poverty Mapping Database - Kelompok 18

## 🗄️ PostgreSQL Database Information

### Database Details:
- **Host**: localhost
- **Port**: 5432
- **Main Database**: poverty_mapping
- **Username**: postgres
- **Password**: postgres123

### Additional Databases:
- **superset_db**: For Superset metadata
- **analytics_db**: For analytics results
- **airflow**: For Airflow metadata (separate container)

### Application User:
- **Username**: bigdata_user
- **Password**: bigdata123
- **Privileges**: Full access to all application databases

## 🔧 Connection Strings

### Python (psycopg2):
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="poverty_mapping",
    user="postgres",
    password="postgres123"
)
```

### SQLAlchemy:
```python
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/poverty_mapping"
```

### DBeaver/pgAdmin Connection:
- Host: localhost
- Port: 5432
- Database: poverty_mapping
- Username: postgres
- Password: postgres123

### Command Line (psql):
```bash
psql -h localhost -p 5432 -U postgres -d poverty_mapping
```

## 📊 Database Schema

### Schemas Created:
1. **poverty_data**: Raw and processed poverty statistics
2. **processed_data**: ETL processed data
3. **ml_models**: Machine learning model results

### Sample Tables (to be created):
- `poverty_data.sumatra_poverty`: Main poverty statistics
- `processed_data.provincial_summary`: Aggregated provincial data
- `ml_models.poverty_predictions`: ML prediction results

## 🚀 Quick Setup Commands

### 1. Start PostgreSQL Container:
```bash
cd c:\TUBESABD
docker-compose up -d postgres
```

### 2. Check Container Status:
```bash
docker ps | grep postgres-local
```

### 3. Connect to Database:
```bash
docker exec -it postgres-local psql -U postgres -d poverty_mapping
```

### 4. Initialize Database:
```bash
docker exec -it postgres-local bash /docker-entrypoint-initdb.d/data/../scripts/init_postgres.sh
```

## 🔍 Database Management

### View All Databases:
```sql
\l
```

### Connect to Specific Database:
```sql
\c poverty_mapping
```

### View All Tables:
```sql
\dt
```

### View All Schemas:
```sql
\dn
```

## 🛠️ Troubleshooting

### Container Not Starting:
```bash
docker logs postgres-local
```

### Connection Refused:
- Check if port 5432 is available: `netstat -an | findstr 5432`
- Ensure container is running: `docker ps`

### Password Authentication Failed:
- Use the correct credentials: postgres/postgres123
- For application user: bigdata_user/bigdata123

## 📈 Performance Settings

Current optimizations in docker-compose.yml:
- max_connections: 100
- shared_buffers: 128MB
- effective_cache_size: 256MB
- work_mem: 4MB
- maintenance_work_mem: 64MB

## 🔐 Security Notes

⚠️ **Development Only**: These credentials are for development purposes only.
For production deployment, use strong passwords and proper security configurations.

---

**Container Name**: postgres-local  
**Image**: postgres:15  
**Status**: Ready for connection at localhost:5432
