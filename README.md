# Implementasi Ekosistem Hadoop untuk Pemetaan Daerah Rawan Kemiskinan di Sumatera

![Arsitektur Pipeline](Arsitektur%20Pipeline.png)

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk memetakan daerah rawan kemiskinan di Sumatera dengan pendekatan berbasis Big Data. Dengan memanfaatkan ekosistem Hadoop, tim mengimplementasikan arsitektur pipeline yang mampu menangani data kependudukan dalam skala besar, mulai dari ingestion hingga visualisasi analitik interaktif.

Teknologi yang digunakan mencakup HDFS, Apache Spark, Hive, PostgreSQL, Superset, dan Airflow, yang semuanya diorkestrasi melalui Docker.

## 🗺️ Arsitektur Sistem

Pipeline ini dibangun dalam tiga lapisan utama sesuai pendekatan *Medallion Architecture*:
- **Bronze Layer:** Menyimpan data mentah dari file CSV (20.000+ record)
- **Silver Layer:** Data dibersihkan, tervalidasi, dan distandardisasi menggunakan Apache Spark
- **Gold Layer:** Data teragregasi dan siap dianalisis dengan Hive dan PostgreSQL

Visualisasi dilakukan menggunakan Superset Dashboard dengan analisis lanjutan di Jupyter Notebooks.

## 🧱 Stack Teknologi

- **Containerization:** Docker, Docker Compose
- **Big Data Processing:** Apache Hadoop (HDFS), Apache Spark
- **Data Warehouse:** Apache Hive, PostgreSQL
- **Workflow Management:** Apache Airflow
- **Visualisasi & BI:** Apache Superset, Jupyter Notebooks, PySpark

## ⚙️ Komponen Fungsional

### Infrastructure Layer
- Docker containerization
- Jaringan internal (`bigdata-network`)
- Volume persistence

### Data Layer
- Penyimpanan: HDFS
- Metadata dan hasil: PostgreSQL
- Dataset mentah: Profil_Kemiskinan_Sumatera.csv

### Processing Layer
- Spark cluster (2 workers)
- Airflow DAG: `poverty_mapping_dag_etl_final`
- Hive untuk query analitik

### Presentation Layer
- Dashboard Superset interaktif
- Analisis statistik dan eksplorasi data di Jupyter

## 🔁 Workflow ETL (via Airflow DAG)

1. `extract_csv_data`
2. `validate_and_clean`
3. `spark_transform_daa`
4. `load_to_postgres_hive`
5. `create_analysis_view`

## 📊 Visualisasi Dashboard

- Peta interaktif kemiskinan
- Korelasi indikator ekonomi
- Distribusi penduduk miskin
- KPI Cards, Pie Chart, Gauge Chart
- Tabel perbandingan dan statistik antar provinsi

## 🔌 Arsitektur Docker & Port

| Komponen              | Port Lokal        |
|----------------------|-------------------|
| Superset Dashboard   | `localhost:8089`  |
| Airflow UI           | `localhost:8090`  |
| Spark Master UI      | `localhost:8080`  |
| Jupyter Notebook     | `localhost:8888`  |
| Hive Server2         | `localhost:10000` |
| PostgreSQL           | `localhost:5432`  |

## 📁 Struktur Folder

```
├── airflow/dags/            # ETL workflows (DAGs)
├── data/                    # Dataset CSV
├── notebooks/               # Jupyter analysis
├── docker-compose.yml       # Docker stack definition
├── Arsitektur Pipeline.png  # Gambar arsitektur
├── Laporan Akhir Tugas ABD_Kelompok 18 RB.pdf  # Dokumentasi proyek
└── README.md                # Dokumentasi proyek
```

## 🧪 Hasil Analisis

- Tingkat kemiskinan rerata: **17.5%**
- Sumatera Barat menunjukkan **kedalaman kemiskinan tertinggi**
- Tiga provinsi memiliki jumlah penduduk miskin yang **relatif setara**
- **Distribusi risiko kemiskinan** menunjukkan urgensi intervensi sosial terintegrasi

## 📚 Referensi

1. Dataset utama dari Badan Pusat Statistik (2018–2022)
2. Teknologi Big Data dan arsitektur pipeline mengacu pada praktik industri modern

## 📄 Dokumentasi Lengkap

Untuk detail lengkap mengenai implementasi dan hasil analisis, silakan baca laporan tugas akhir berikut:

📥 [Unduh / Lihat Laporan Tugas Akhir (PDF)](./Laporan%20Akhir%20Tugas%20ABD_Kelompok%2018%20RB.pdf)


---

## ✨ Kontributor

- Try Yani Rizki Nur Rohmah
- Nabiilah Putri Karnaia
- Priska Silvia Ferantiana
- Naufal Fakhri

Proyek ini merupakan tugas akhir mata kuliah **Analisis Big Data**, Program Studi Sains Data, Institut Teknologi Sumatera.
