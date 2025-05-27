#!/usr/bin/env python3
"""
Big Data Pipeline Execution Demo
Kelompok 18 - Pemetaan Kemiskinan Sumatera
Demonstrasi lengkap ETL pipeline dan machine learning
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set style untuk visualisasi
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("🚀 BIG DATA PIPELINE EXECUTION DEMO")
print("=" * 70)
print("Kelompok 18 - Pemetaan Kemiskinan Sumatera")
print("Medallion Architecture: Bronze → Silver → Gold")
print("=" * 70)

# ============================================================================
# BRONZE LAYER - Data Ingestion
# ============================================================================
print("\n📥 BRONZE LAYER: Data Ingestion")
print("-" * 50)

try:
    # Load raw data
    df_bronze = pd.read_csv('data/Profil_Kemiskinan_Sumatera.csv')
    print(f"✅ Data berhasil dimuat dari Bronze layer")
    print(f"📊 Total records: {len(df_bronze):,}")
    print(f"📋 Kolom data: {len(df_bronze.columns)}")
    print(f"🗂️ Provinsi: {df_bronze['Provinsi'].nunique()}")
    print(f"🥬 Komoditas: {df_bronze['Komoditas'].nunique()}")
    
    # Data overview
    print(f"\n📊 Overview Data Bronze:")
    print(f"   • Rentang kemiskinan: {df_bronze['Persentase Kemiskinan (%)'].min():.1f}% - {df_bronze['Persentase Kemiskinan (%)'].max():.1f}%")
    print(f"   • Rata-rata pengangguran: {df_bronze['Tingkat Pengangguran (%)'].mean():.1f}%")
    print(f"   • Total populasi: {df_bronze['Jumlah Penduduk (jiwa)'].sum():,} jiwa")
    
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)

# ============================================================================
# SILVER LAYER - Data Cleaning & Transformation
# ============================================================================
print("\n🔄 SILVER LAYER: Data Cleaning & Transformation")
print("-" * 50)

def transform_bronze_to_silver(df):
    """Transform Bronze data to Silver layer"""
    df_silver = df.copy()
    
    # 1. Clean numeric columns
    numeric_cols = ['Konsumsi (per kapita per minggu)', 'Jumlah Penduduk (jiwa)', 
                   'Persentase Kemiskinan (%)', 'Tingkat Pengangguran (%)']
    
    for col in numeric_cols:
        df_silver[col] = pd.to_numeric(df_silver[col], errors='coerce')
    
    # 2. Encode categorical variables
    categorical_mappings = {
        'Akses Pendidikan': {'baik': 3, 'sedang': 2, 'buruk': 1},
        'Fasilitas Kesehatan': {'memadai': 1, 'tidak memadai': 0},
        'Akses Air Bersih': {'ya': 1, 'tidak': 0}
    }
    
    for col, mapping in categorical_mappings.items():
        df_silver[f"{col}_encoded"] = df_silver[col].map(mapping)
    
    # 3. Create poverty category encoding
    poverty_mapping = {'rendah': 1, 'sedang': 2, 'tinggi': 3}
    df_silver['Kategori_Kemiskinan_encoded'] = df_silver['Kategori Kemiskinan'].map(poverty_mapping)
    
    # 4. Feature engineering
    df_silver['Konsumsi_per_Penduduk'] = (
        df_silver['Konsumsi (per kapita per minggu)'] / 
        (df_silver['Jumlah Penduduk (jiwa)'] + 1)  # +1 to avoid division by zero
    )
    
    df_silver['Indeks_Kesejahteraan'] = (
        df_silver['Akses Pendidikan_encoded'] + 
        df_silver['Fasilitas Kesehatan_encoded'] + 
        df_silver['Akses Air Bersih_encoded']
    ) / 3
    
    # 5. Clean missing values
    df_silver = df_silver.dropna(subset=['Persentase Kemiskinan (%)', 'Tingkat Pengangguran (%)'])
    
    return df_silver

# Transform data
df_silver = transform_bronze_to_silver(df_bronze)

print(f"✅ Data transformation completed")
print(f"📊 Silver records: {len(df_silver):,}")
print(f"🧹 Data cleaning loss: {((len(df_bronze) - len(df_silver)) / len(df_bronze) * 100):.1f}%")
print(f"🔧 New features created: Konsumsi_per_Penduduk, Indeks_Kesejahteraan")

# ============================================================================
# GOLD LAYER - Data Aggregation & Analytics
# ============================================================================
print("\n📊 GOLD LAYER: Data Aggregation & Analytics")
print("-" * 50)

def create_gold_aggregations(df):
    """Create Gold layer aggregations"""
    
    # 1. Provincial analysis
    gold_province = df.groupby('Provinsi').agg({
        'Persentase Kemiskinan (%)': ['mean', 'std', 'min', 'max'],
        'Tingkat Pengangguran (%)': ['mean', 'std'],
        'Jumlah Penduduk (jiwa)': 'sum',
        'Indeks_Kesejahteraan': 'mean',
        'Konsumsi_per_Penduduk': 'mean'
    }).round(2)
    
    gold_province.columns = ['_'.join(col).strip() for col in gold_province.columns]
    gold_province = gold_province.reset_index()
    
    # 2. Poverty category distribution
    poverty_dist = df['Kategori Kemiskinan'].value_counts()
    
    # 3. Infrastructure analysis
    infra_analysis = df.groupby(['Akses Pendidikan', 'Fasilitas Kesehatan', 'Akses Air Bersih']).agg({
        'Persentase Kemiskinan (%)': 'mean',
        'Jumlah Penduduk (jiwa)': 'sum'
    }).round(2)
    
    return gold_province, poverty_dist, infra_analysis

gold_province, poverty_dist, infra_analysis = create_gold_aggregations(df_silver)

print("✅ Gold layer aggregations created:")
print(f"🏛️ Provincial analysis: {len(gold_province)} provinces")
print(f"📈 Poverty distribution: {len(poverty_dist)} categories")
print(f"🏗️ Infrastructure combinations: {len(infra_analysis)} scenarios")

# Display provincial insights
print(f"\n🏛️ Provincial Poverty Analysis:")
for _, row in gold_province.iterrows():
    print(f"   • {row['Provinsi']}: {row['Persentase Kemiskinan (%)_mean']:.1f}% poverty rate")

# ============================================================================
# MACHINE LEARNING PIPELINE
# ============================================================================
print("\n🤖 MACHINE LEARNING PIPELINE")
print("-" * 50)

def train_poverty_models(df):
    """Train multiple ML models for poverty prediction"""
    
    # Prepare features
    feature_cols = [
        'Konsumsi (per kapita per minggu)',
        'Jumlah Penduduk (jiwa)',
        'Tingkat Pengangguran (%)',
        'Akses Pendidikan_encoded',
        'Fasilitas Kesehatan_encoded',
        'Akses Air Bersih_encoded',
        'Indeks_Kesejahteraan'
    ]
    
    # Filter complete cases
    ml_data = df[feature_cols + ['Kategori_Kemiskinan_encoded']].dropna()
    
    X = ml_data[feature_cols]
    y = ml_data['Kategori_Kemiskinan_encoded']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models
    models = {}
    
    # 1. Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    models['Random Forest'] = {
        'model': rf_model,
        'predictions': rf_pred,
        'accuracy': accuracy_score(y_test, rf_pred),
        'feature_importance': pd.DataFrame({
            'feature': feature_cols,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
    }
    
    # 2. Logistic Regression
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train_scaled, y_train)
    lr_pred = lr_model.predict(X_test_scaled)
    models['Logistic Regression'] = {
        'model': lr_model,
        'predictions': lr_pred,
        'accuracy': accuracy_score(y_test, lr_pred)
    }
    
    return models, X_test, y_test

# Train models
models, X_test, y_test = train_poverty_models(df_silver)

print("✅ Machine Learning models trained:")
for model_name, model_info in models.items():
    print(f"   • {model_name}: {model_info['accuracy']:.3f} accuracy")

# Feature importance analysis
print(f"\n🔝 Top 5 Important Features (Random Forest):")
for idx, row in models['Random Forest']['feature_importance'].head(5).iterrows():
    print(f"   {idx+1}. {row['feature']}: {row['importance']:.3f}")

# ============================================================================
# BUSINESS INSIGHTS & PREDICTIONS
# ============================================================================
print("\n🎯 BUSINESS INSIGHTS & PREDICTIONS")
print("-" * 50)

# 1. Poverty hotspots
poverty_hotspots = df_silver.groupby('Provinsi')['Persentase Kemiskinan (%)'].mean().sort_values(ascending=False)
print(f"🔴 Poverty Hotspots:")
for province, rate in poverty_hotspots.items():
    print(f"   • {province}: {rate:.1f}%")

# 2. Infrastructure impact
print(f"\n🏗️ Infrastructure Impact on Poverty:")
infra_impact = df_silver.groupby(['Akses Pendidikan', 'Fasilitas Kesehatan', 'Akses Air Bersih'])['Persentase Kemiskinan (%)'].mean().sort_values()
print(f"   • Best infrastructure combo: {infra_impact.iloc[-1]:.1f}% poverty")
print(f"   • Worst infrastructure combo: {infra_impact.iloc[0]:.1f}% poverty")

# 3. Prediction scenarios
print(f"\n🔮 Prediction Scenarios:")
scenarios = [
    [2000, 1000, 15, 3, 1, 1, 1.67],  # Good scenario
    [1000, 2000, 25, 1, 0, 0, 0.33],  # Poor scenario
    [1500, 1500, 20, 2, 1, 1, 1.33],  # Average scenario
]

scenario_names = ['Optimistic', 'Pessimistic', 'Moderate']
rf_model = models['Random Forest']['model']

for i, scenario in enumerate(scenarios):
    prediction = rf_model.predict([scenario])[0]
    poverty_levels = {1: 'Rendah', 2: 'Sedang', 3: 'Tinggi'}
    print(f"   • {scenario_names[i]} scenario: {poverty_levels[prediction]} poverty level")

# ============================================================================
# DATA QUALITY REPORT
# ============================================================================
print("\n🔍 DATA QUALITY REPORT")
print("-" * 50)

quality_metrics = {
    'Total Bronze Records': len(df_bronze),
    'Total Silver Records': len(df_silver),
    'Data Completeness': f"{(1 - df_silver.isnull().sum().sum() / (len(df_silver) * len(df_silver.columns))):.1%}",
    'Missing Value Rate': f"{(df_bronze.isnull().sum().sum() / (len(df_bronze) * len(df_bronze.columns))):.1%}",
    'Duplicate Records': len(df_bronze) - len(df_bronze.drop_duplicates()),
    'Data Loss (Bronze→Silver)': f"{((len(df_bronze) - len(df_silver)) / len(df_bronze) * 100):.1f}%"
}

for metric, value in quality_metrics.items():
    print(f"   • {metric}: {value}")

# ============================================================================
# PIPELINE SUMMARY
# ============================================================================
print("\n📋 PIPELINE EXECUTION SUMMARY")
print("=" * 70)

summary_stats = {
    'Execution Status': '✅ SUCCESSFUL',
    'Data Processing': f'{len(df_bronze):,} → {len(df_silver):,} records',
    'ML Model Accuracy': f"RF: {models['Random Forest']['accuracy']:.3f}, LR: {models['Logistic Regression']['accuracy']:.3f}",
    'Provinces Analyzed': df_silver['Provinsi'].nunique(),
    'Commodities Tracked': df_silver['Komoditas'].nunique(),
    'Key Insights Generated': '5+ business insights',
    'Prediction Models': '2 trained models ready'
}

for metric, value in summary_stats.items():
    print(f"📊 {metric}: {value}")

print("\n🎉 BIG DATA PIPELINE EXECUTION COMPLETED!")
print("=" * 70)
print("🔗 Access Points:")
print("   • Jupyter Notebooks: http://localhost:8888")
print("   • Hadoop NameNode: http://localhost:9870")
print("   • Spark Master: http://localhost:8080")
print("   • Apache Airflow: http://localhost:8090")
print("=" * 70)
print("💡 Next Steps: Access Jupyter for interactive analysis!")
