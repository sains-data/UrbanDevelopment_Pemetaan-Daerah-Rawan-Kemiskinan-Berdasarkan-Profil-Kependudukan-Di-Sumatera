# Superset Configuration
import os

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:////app/superset_home/superset.db'

# Security Configuration
SECRET_KEY = 'superset_secret_key_change_in_production'

# Hive Connection
DATABASES = {
    'hive': {
        'type': 'hive',
        'driver': 'pyhive',
        'host': 'hive-server',
        'port': 10000,
        'database': 'kemiskinan_db',
        'username': 'hive',
        'password': '',
    }
}

# Cache Configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/app/superset_home/cache'
}

# Feature Flags
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
}

# CSV Upload
CSV_TO_HIVE_UPLOAD_S3_BUCKET = None
UPLOAD_FOLDER = '/app/superset_home/uploads'

# Webdriver Configuration
WEBDRIVER_BASEURL = 'http://superset:8088'
