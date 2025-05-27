# 🏗️ ARSITEKTUR PIPELINE BIG DATA KELOMPOK 18
## Pemetaan Kemiskinan Sumatera - Complete Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           🏢 KELOMPOK 18 BIG DATA ARCHITECTURE                      │
│                         Pemetaan Kemiskinan Sumatera Pipeline                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  📊 DATA LAYER                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│   📂 Raw Data       │    │   🗄️ Data Storage    │    │   🧹 Clean Data      │
│                     │    │                      │    │                      │
│ • CSV Files         │───▶│ • HDFS Distributed   │───▶│ • PostgreSQL DB      │
│ • 20,000+ Records   │    │ • Hadoop NameNode    │    │ • poverty_clean view │
│ • Sumatera Data     │    │ • DataNode 1 & 2     │    │ • Filtered & Valid   │
│ • Poverty Stats     │    │ • Fault Tolerant     │    │ • Ready for Analysis │
└─────────────────────┘    └──────────────────────┘    └──────────────────────┘
        │                            │                            │
        │                            │                            │
        ▼                            ▼                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              🔄 PROCESSING LAYER                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  ⚙️ ETL Pipeline     │    │  🚀 Spark Processing │    │  📋 Orchestration    │
│                     │    │                      │    │                      │
│ • Extract CSV       │    │ • Spark Master       │    │ • Apache Airflow     │
│ • Transform Data    │───▶│ • Worker Nodes (2)    │───▶│ • DAG Management     │
│ • Load to DB        │    │ • Distributed Compute │    │ • Scheduling         │
│ • Data Validation   │    │ • In-Memory Process   │    │ • Monitoring         │
└─────────────────────┘    └──────────────────────┘    └──────────────────────┘
        │                            │                            │
        │                            │                            │
        ▼                            ▼                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            🎨 PRESENTATION LAYER                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  📊 Visualization   │    │  🔬 Analytics        │    │  📈 Business Intel   │
│                     │    │                      │    │                      │
│ • Apache Superset   │    │ • Jupyter Notebooks  │    │ • Interactive Dash   │
│ • Interactive Dash  │───▶│ • PySpark Analysis    │───▶│ • Poverty Mapping    │
│ • Charts & Maps     │    │ • Data Exploration   │    │ • Geographic Insights│
│ • Real-time Updates │    │ • Statistical Models │    │ • Decision Support   │
└─────────────────────┘    └──────────────────────┘    └──────────────────────┘
```

## 🔧 **INFRASTRUCTURE COMPONENTS**

### **💻 Container Infrastructure (Docker)**
```
┌─────────────────────────────────────────────────────────────────────┐
│                        🐳 DOCKER ECOSYSTEM                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📦 HADOOP CLUSTER          📦 SPARK CLUSTER         📦 DATABASES   │
│  ┌─────────────────┐       ┌─────────────────┐      ┌─────────────┐ │
│  │ namenode:9870   │       │ spark-master    │      │ postgres    │ │
│  │ datanode1:9864  │◄─────►│ :8080, :7077    │◄────►│ :5432       │ │
│  │ datanode2:9865  │       │ spark-worker-1  │      │ hive-meta   │ │
│  │ resourcemanager │       │ :8081           │      │ :5432       │ │
│  │ historyserver   │       │ spark-worker-2  │      │ airflow-db  │ │
│  └─────────────────┘       │ :8082           │      │ :5432       │ │
│                            └─────────────────┘      └─────────────┘ │
│                                                                     │
│  📦 WEB SERVICES            📦 ANALYTICS             📦 WORKFLOW    │
│  ┌─────────────────┐       ┌─────────────────┐      ┌─────────────┐ │
│  │ superset:8089   │       │ jupyter:8888    │      │ airflow     │ │
│  │ hive-server     │◄─────►│ pyspark-notebook│◄────►│ :8090       │ │
│  │ :10000          │       │ data-analysis   │      │ scheduler   │ │
│  └─────────────────┘       └─────────────────┘      │ webserver   │ │
│                                                     └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### **🌐 Network Architecture**
```
┌─────────────────────────────────────────────────────────────────────┐
│                       🌐 NETWORK TOPOLOGY                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  HOST MACHINE (Windows)                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  📁 c:\TUBESABD\                                            │   │
│  │  ├── 📊 data/ (CSV files)                                   │   │
│  │  ├── ⚙️ airflow/dags/ (ETL workflows)                       │   │
│  │  ├── 📓 notebooks/ (Analysis)                               │   │
│  │  ├── 🔧 scripts/ (Utilities)                                │   │
│  │  └── 🐳 docker-compose.yml                                  │   │
│  │                                                             │   │
│  │  💡 EXPOSED PORTS:                                          │   │
│  │  ├── 🌐 :8089 → Superset Dashboard                          │   │
│  │  ├── 🔄 :8090 → Airflow Web UI                              │   │
│  │  ├── ⚡ :8080 → Spark Master UI                             │   │
│  │  ├── 📊 :8888 → Jupyter Notebooks                          │   │
│  │  ├── 🗄️ :5432 → PostgreSQL                                 │   │
│  │  └── 📁 :9870 → Hadoop NameNode                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  DOCKER INTERNAL NETWORK: bigdata-network                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  🐳 Container Communication (Internal DNS)                  │   │
│  │  ├── namenode:9000 (HDFS)                                  │   │
│  │  ├── spark-master:7077 (Spark)                             │   │
│  │  ├── postgres-local:5432 (DB)                              │   │
│  │  └── superset:8088 (Internal)                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## 📊 **DATA FLOW ARCHITECTURE**

### **🔄 ETL Pipeline Flow**
```
┌─────────────────────────────────────────────────────────────────────┐
│                         📊 DATA PIPELINE FLOW                       │
└─────────────────────────────────────────────────────────────────────┘

🗂️ SOURCE DATA                🔄 PROCESSING               📊 DESTINATION
┌─────────────┐               ┌─────────────┐             ┌─────────────┐
│             │               │             │             │             │
│ 📁 CSV      │──── Extract ──▶│ 🚀 Spark    │──── Load ──▶│ 🗄️ PostgreSQL│
│ 20K+ Records│               │ Transforms  │             │ Clean Data  │
│             │               │             │             │             │
│ ├─Province  │               │ ├─Validate  │             │ ├─poverty_  │
│ ├─Regency   │               │ ├─Filter    │             │ │  clean    │
│ ├─Poverty % │               │ ├─Aggregate │             │ │  view     │
│ ├─Population│               │ └─Normalize │             │ └─20K clean │
│ └─Economics │               │             │             │   records   │
└─────────────┘               └─────────────┘             └─────────────┘
       │                             │                           │
       │                             │                           │
       ▼                             ▼                           ▼
┌─────────────┐               ┌─────────────┐             ┌─────────────┐
│ 📅 Schedule │               │ 🔍 Monitor  │             │ 🎨 Visualize│
│ Airflow DAG │               │ Job Status  │             │ Superset    │
│ Daily Runs  │               │ Error Handle│             │ Dashboard   │
└─────────────┘               └─────────────┘             └─────────────┘
```

### **📈 Analytics & Visualization Flow**
```
┌─────────────────────────────────────────────────────────────────────┐
│                    🎯 ANALYTICS ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────┘

📊 DATA SOURCE           🔬 ANALYSIS              🎨 VISUALIZATION
┌─────────────┐         ┌─────────────┐          ┌─────────────┐
│             │         │             │          │             │
│ 🗄️ PostgreSQL│────────▶│ 📓 Jupyter  │─────────▶│ 📊 Superset │
│ poverty_clean│         │ Notebooks   │          │ Dashboard   │
│             │         │             │          │             │
│ ├─Geographic │         │ ├─EDA       │          │ ├─Maps      │
│ ├─Economic   │         │ ├─Statistics│          │ ├─Charts    │
│ ├─Demographic│         │ ├─ML Models │          │ ├─Tables    │
│ └─Social     │         │ └─Insights  │          │ └─Filters   │
└─────────────┘         └─────────────┘          └─────────────┘
       │                       │                        │
       │                       │                        │
       ▼                       ▼                        ▼
┌─────────────┐         ┌─────────────┐          ┌─────────────┐
│ 🔍 Query    │         │ 🧮 Compute  │          │ 👥 Users    │
│ Real-time   │         │ Spark Cluster│          │ Interactive │
│ SQL Access  │         │ Distributed │          │ Exploration │
└─────────────┘         └─────────────┘          └─────────────┘
```

## 🎯 **FUNCTIONAL COMPONENTS**

### **📋 Core Components List**
```
🏗️ INFRASTRUCTURE LAYER
├── 🐳 Docker Containerization
├── 🌐 Network Management (bigdata-network)
├── 💾 Volume Persistence
└── 🔧 Service Orchestration

📊 DATA LAYER  
├── 📁 Raw Data Storage (CSV)
├── 🗄️ HDFS Distributed Storage
├── 🏪 PostgreSQL Data Warehouse
└── 🧹 Data Quality Management

⚙️ PROCESSING LAYER
├── 🚀 Apache Spark (Master + 2 Workers)
├── 🔄 Apache Airflow (ETL Orchestration)
├── 🐝 Apache Hive (Data Warehouse)
└── 📊 Hadoop Ecosystem

🎨 PRESENTATION LAYER
├── 📊 Apache Superset (BI Dashboard)
├── 📓 Jupyter Notebooks (Analysis)
├── 🌐 Web Interfaces
└── 📈 Interactive Visualizations
```

### **🔄 Workflow Components**
```
📅 AIRFLOW DAG: poverty_mapping_etl_final
├── 🔄 extract_csv_data
├── 🧹 validate_and_clean
├── 🚀 spark_transform_data
├── 📊 load_to_postgresql
└── ✅ create_analysis_view

🎨 SUPERSET DASHBOARD: Pemetaan Kemiskinan Sumatera
├── 🗺️ Geographic Poverty Map
├── 📊 Top Critical Areas Chart
├── 📈 Economic Correlation Analysis
├── 📋 Province Comparison Table
├── 📊 Distribution Histogram
└── 🔍 Interactive Filters
```

## 💡 **TECHNOLOGY STACK**

### **🛠️ Technologies Used**
```
📦 CONTAINERIZATION
├── Docker 🐳
└── Docker Compose

🗄️ BIG DATA STORAGE
├── Apache Hadoop (HDFS)
├── PostgreSQL
└── Apache Hive

⚡ PROCESSING ENGINES
├── Apache Spark
├── PySpark
└── Spark SQL

🔄 WORKFLOW MANAGEMENT
├── Apache Airflow
└── Python DAGs

🎨 VISUALIZATION & BI
├── Apache Superset
├── Jupyter Notebooks
└── PySpark Analysis

🌐 WEB INTERFACES
├── Airflow Web UI (Port 8090)
├── Superset Dashboard (Port 8089)
├── Spark Master UI (Port 8080)
├── Hadoop NameNode (Port 9870)
└── Jupyter Lab (Port 8888)
```

## 🎯 **PROJECT OBJECTIVES & OUTCOMES**

### **🎯 Business Goals**
```
📍 PRIMARY OBJECTIVES:
├── 🗺️ Map poverty distribution across Sumatera
├── 📊 Identify high-poverty areas needing intervention
├── 📈 Analyze economic correlations
├── 📋 Generate actionable insights
└── 🎨 Create interactive visualizations

📊 DATA OUTCOMES:
├── ✅ 20,000+ poverty data points processed
├── ✅ 6 Sumatera provinces analyzed
├── ✅ Real-time dashboard available
├── ✅ Geographic insights generated
└── ✅ Decision support system ready
```

### **🏆 Technical Achievements**
```
✅ COMPLETED IMPLEMENTATIONS:
├── 🐳 Full Docker containerization (17 services)
├── 🔄 End-to-end ETL pipeline with Airflow
├── 🚀 Distributed processing with Spark cluster
├── 🗄️ Scalable data storage with HDFS + PostgreSQL
├── 📊 Interactive BI dashboard with Superset
├── 📓 Analysis environment with Jupyter
├── 🌐 Web-based management interfaces
└── 📈 Real-time poverty mapping visualization
```

## 🚀 **DEPLOYMENT & ACCESS**

### **🌐 Service Access Points**
```
🎯 PRODUCTION SERVICES:
├── 📊 Superset Dashboard: http://localhost:8089
├── 🔄 Airflow Management: http://localhost:8090
├── ⚡ Spark Monitoring: http://localhost:8080
├── 📓 Jupyter Analysis: http://localhost:8888
├── 🗄️ Hadoop Management: http://localhost:9870
└── 🐝 Hive Server: http://localhost:10000

🔐 CREDENTIALS:
├── Superset: admin / admin
├── PostgreSQL: postgres / postgres123
├── Database: poverty_mapping
└── Airflow: admin / admin
```

---

**🎓 KELOMPOK 18 BIG DATA PIPELINE**  
**📊 Pemetaan Kemiskinan Sumatera**  
**🗓️ Implemented: May 26, 2025**  
**✅ Status: Production Ready with 20,000+ Records**
