# 🎨 PANDUAN LENGKAP DASHBOARD SUPERSET
## Kelompok 18 - Pemetaan Kemiskinan Sumatera

---

## 🚀 AKSES SUPERSET
**URL**: http://localhost:8089  
**Username**: `admin`  
**Password**: `admin`

---

## 📊 LANGKAH 1: KONEKSI DATABASE

### 1.1 Tambah Database Connection
1. Login ke Superset di http://localhost:8089
2. Klik **Settings** → **Database Connections**
3. Klik **+ DATABASE**
4. Pilih **SQLite**
5. Isi form:
   - **Database Name**: `poverty_mapping`
   - **SQLAlchemy URI**: `sqlite:///C:/TUBESABD/superset_data/poverty_mapping.db`
6. Klik **CONNECT**
7. Klik **FINISH**

### 1.2 Verifikasi Koneksi
- Pastikan status database menunjukkan "Connected"
- Test koneksi dengan klik "Test Connection"

---

## 📈 LANGKAH 2: BUAT DATASETS

### 2.1 Dataset Utama: poverty_data
1. Pergi ke **Data** → **Datasets**
2. Klik **+ DATASET**
3. Pilih:
   - **Database**: `poverty_mapping`
   - **Schema**: (kosongkan)
   - **Table**: `poverty_data`
4. Klik **CREATE DATASET AND CREATE CHART**

### 2.2 Dataset Ringkasan: province_summary
1. Ulangi langkah di atas untuk table `province_summary`
2. Dan untuk table `poverty_distribution`

---

## 🎯 LANGKAH 3: BUAT CHARTS

### 📊 Chart 1: Tingkat Kemiskinan per Provinsi
**Jenis**: Bar Chart
1. **Dataset**: poverty_data
2. **Query**:
   - **Dimensions**: Provinsi
   - **Metrics**: AVG(Persentase_Kemiskinan_Pct)
3. **Customize**:
   - **Chart Title**: "Rata-rata Tingkat Kemiskinan per Provinsi"
   - **X Axis Label**: "Provinsi"
   - **Y Axis Label**: "Persentase Kemiskinan (%)"
   - **Color Scheme**: Reds (untuk menunjukkan tingkat kemiskinan)
4. Klik **SAVE** → Beri nama "Poverty_Rate_by_Province"

### 🥧 Chart 2: Distribusi Kategori Kemiskinan
**Jenis**: Pie Chart
1. **Dataset**: poverty_distribution
2. **Query**:
   - **Dimensions**: Category
   - **Metrics**: Count
3. **Customize**:
   - **Chart Title**: "Distribusi Kategori Kemiskinan Sumatera"
   - **Show Labels**: Yes
   - **Show Percentages**: Yes
4. Klik **SAVE** → Beri nama "Poverty_Category_Distribution"

### 📈 Chart 3: Korelasi Pengangguran vs Kemiskinan
**Jenis**: Scatter Plot
1. **Dataset**: poverty_data
2. **Query**:
   - **X Axis**: Tingkat_Pengangguran_Pct
   - **Y Axis**: Persentase_Kemiskinan_Pct
   - **Series**: Provinsi (optional, untuk grouping)
3. **Customize**:
   - **Chart Title**: "Korelasi Tingkat Pengangguran vs Kemiskinan"
   - **X Axis Label**: "Tingkat Pengangguran (%)"
   - **Y Axis Label**: "Tingkat Kemiskinan (%)"
4. Klik **SAVE** → Beri nama "Unemployment_vs_Poverty"

### 📋 Chart 4: Tabel Ringkasan Provinsi
**Jenis**: Table
1. **Dataset**: province_summary
2. **Query**:
   - **Columns**: Provinsi, Total_Areas, Avg_Poverty_Rate, Avg_Unemployment_Rate, Total_Population
3. **Customize**:
   - **Chart Title**: "Ringkasan Statistik per Provinsi"
   - **Page Length**: 15
   - **Sort**: Avg_Poverty_Rate (descending)
4. Klik **SAVE** → Beri nama "Province_Summary_Table"

### 📊 Chart 5: Skor Kesehatan Ekonomi
**Jenis**: Bar Chart
1. **Dataset**: province_summary
2. **Query**:
   - **Dimensions**: Provinsi
   - **Metrics**: Avg_Economic_Health_Score
3. **Customize**:
   - **Chart Title**: "Skor Kesehatan Ekonomi per Provinsi"
   - **Color Scheme**: Greens (hijau untuk kesehatan ekonomi)
   - **Sort Bars**: Yes (descending)
4. Klik **SAVE** → Beri nama "Economic_Health_Score"

### 📉 Chart 6: Area Kemiskinan Tertinggi
**Jenis**: Table
1. **Dataset**: poverty_data
2. **Query**:
   - **Columns**: Provinsi, Komoditas, Persentase_Kemiskinan_Pct, Tingkat_Pengangguran_Pct
   - **Filters**: None
   - **Sort**: Persentase_Kemiskinan_Pct (descending)
   - **Row Limit**: 20
3. **Customize**:
   - **Chart Title**: "20 Area dengan Kemiskinan Tertinggi"
4. Klik **SAVE** → Beri nama "Top_Poverty_Areas"

---

## 🏠 LANGKAH 4: BUAT DASHBOARD

### 4.1 Buat Dashboard Baru
1. Pergi ke **Dashboards**
2. Klik **+ DASHBOARD**
3. **Dashboard Title**: "Pemetaan Kemiskinan Sumatera - Kelompok 18"
4. **Slug**: `poverty-mapping-sumatra`

### 4.2 Tambah Charts ke Dashboard
1. Klik **EDIT DASHBOARD**
2. Drag dan drop charts dari panel sebelah kiri:
   - **Baris 1**: "Poverty_Rate_by_Province" (lebar penuh)
   - **Baris 2**: "Poverty_Category_Distribution" (1/3) + "Economic_Health_Score" (2/3)
   - **Baris 3**: "Unemployment_vs_Poverty" (1/2) + "Province_Summary_Table" (1/2)
   - **Baris 4**: "Top_Poverty_Areas" (lebar penuh)

### 4.3 Tambah Filters
1. Klik **+** → **Filter**
2. Tambah filter untuk:
   - **Provinsi** (dari dataset poverty_data)
   - **Poverty_Category** (dari dataset poverty_data)
3. Set filter sebagai "Scoped to all charts"

### 4.4 Tambah Text Box (Optional)
1. Klik **+** → **Markdown**
2. Tambah text header:
```markdown
# 📊 Pemetaan Kemiskinan Sumatera
**Kelompok 18** | Dashboard analisis kemiskinan dan pengangguran di provinsi Sumatera

## Key Insights:
- Analisis tingkat kemiskinan per provinsi
- Korelasi antara pengangguran dan kemiskinan  
- Distribusi kategori kemiskinan
- Skor kesehatan ekonomi regional
```

### 4.5 Finalisasi Dashboard
1. Arrange ulang layout sesuai keinginan
2. Klik **SAVE** untuk menyimpan dashboard
3. Klik **PUBLISH** untuk membuat dashboard publik

---

## 🎨 LANGKAH 5: KUSTOMISASI LANJUTAN

### 5.1 Color Schemes yang Disarankan
- **Kemiskinan**: `Reds` atau `Oranges` (merah = tinggi)
- **Kesehatan Ekonomi**: `Greens` atau `Blues` (hijau/biru = baik)  
- **Netral**: `Viridis` atau `Cool`

### 5.2 Tambahan Charts (Optional)
- **Heatmap**: Korelasi antar variabel
- **Line Chart**: Trend analysis (jika ada data time series)
- **Box Plot**: Distribusi kemiskinan per provinsi
- **Histogram**: Distribusi frekuensi tingkat kemiskinan

### 5.3 Export dan Sharing
- **PDF Export**: Dashboard → Actions → Export to PDF
- **PNG Export**: Individual charts → Actions → Download as Image
- **CSV Export**: Table charts → Actions → Export to CSV

---

## 📊 EXPECTED DASHBOARD RESULT

Setelah selesai, dashboard Anda akan menampilkan:

### 📈 **Visualisasi Utama**
- **Bar Chart**: Ranking kemiskinan per provinsi
- **Pie Chart**: Proporsi kategori kemiskinan
- **Scatter Plot**: Korelasi pengangguran-kemiskinan
- **Table**: Detail statistik per provinsi

### 🎯 **Insights yang Dihasilkan**
- Provinsi mana yang memiliki tingkat kemiskinan tertinggi
- Bagaimana distribusi kategori kemiskinan di Sumatera
- Korelasi antara tingkat pengangguran dan kemiskinan
- Area-area prioritas untuk intervensi kebijakan

### 🔍 **Fitur Interaktif**
- Filter berdasarkan provinsi dan kategori kemiskinan
- Drill-down ke level detail yang lebih spesifik
- Export data untuk analisis lebih lanjut
- Dashboard yang responsif untuk berbagai device

---

## 🛠️ TROUBLESHOOTING

### Masalah Umum dan Solusi:

**1. Database Connection Error**
- Pastikan path database benar: `C:/TUBESABD/superset_data/poverty_mapping.db`
- Cek apakah file database exists
- Restart Superset container jika perlu

**2. Charts Tidak Muncul Data**
- Verifikasi dataset connection
- Cek apakah ada data di table dengan SQL Lab
- Refresh browser dan clear cache

**3. Permission Issues**
- Login dengan admin/admin
- Cek role permissions di Security settings
- Pastikan dataset accessible

**4. Performance Issues**
- Gunakan aggregated tables untuk charts besar
- Limit row count untuk table charts
- Cache charts untuk performa lebih baik

---

## 🎯 LANGKAH SELANJUTNYA

Setelah dashboard selesai:

1. **Analisis Data**: Gunakan dashboard untuk mengidentifikasi insights
2. **Policy Recommendations**: Buat rekomendasi berdasarkan visualisasi
3. **Regular Updates**: Update data secara berkala
4. **Advanced Analytics**: Tambah ML predictions ke dashboard
5. **Stakeholder Sharing**: Share dashboard dengan stakeholders

---

**🏆 Dashboard Superset untuk Pemetaan Kemiskinan Sumatera - Kelompok 18**  
**🔗 Access**: http://localhost:8089  
**📊 Database**: poverty_mapping.db (20,000+ records)  
**📅 Last Updated**: May 25, 2025
