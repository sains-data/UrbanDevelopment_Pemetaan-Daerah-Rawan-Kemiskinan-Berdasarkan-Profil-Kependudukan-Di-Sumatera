#!/usr/bin/env python3
"""
ETL Pipeline Execution Script for Poverty Mapping
Kelompok 18 - Pemetaan Kemiskinan Sumatera

This script executes the complete ETL pipeline:
1. Bronze to Silver transformation
2. Silver to Gold aggregation
3. Machine Learning pipeline
4. Data quality validation
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

print("🚀 Starting ETL Pipeline Execution...")
print("=" * 60)

# Step 1: Load data from Bronze layer (simulating HDFS read)
print("📥 Step 1: Loading data from Bronze layer...")

try:
    # Read the source data
    df_bronze = pd.read_csv('/data/Profil_Kemiskinan_Sumatera.csv')
    print(f"✅ Bronze layer data loaded: {len(df_bronze)} records")
    print(f"📊 Columns: {list(df_bronze.columns)}")
except Exception as e:
    print(f"❌ Error loading Bronze data: {e}")
    exit(1)

# Step 2: Bronze to Silver transformation
print("\n🔄 Step 2: Bronze to Silver Transformation...")
print("-" * 40)

def clean_data(df):
    """Clean and standardize data for Silver layer"""
    df_clean = df.copy()
    
    # Clean numeric columns
    numeric_cols = ['Konsumsi (per kapita per minggu)', 'Jumlah Penduduk (jiwa)', 
                   'Persentase Kemiskinan (%)', 'Tingkat Pengangguran (%)']
    
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Standardize categorical values
    categorical_mappings = {
        'Akses Pendidikan': {'baik': 3, 'sedang': 2, 'buruk': 1},
        'Fasilitas Kesehatan': {'memadai': 1, 'tidak memadai': 0},
        'Akses Air Bersih': {'ya': 1, 'tidak': 0},
        'Kategori Kemiskinan': {'rendah': 1, 'sedang': 2, 'tinggi': 3}
    }
    
    for col, mapping in categorical_mappings.items():
        if col in df_clean.columns:
            df_clean[f"{col}_encoded"] = df_clean[col].map(mapping)
    
    # Add derived features
    df_clean['Konsumsi_per_Penduduk'] = df_clean['Konsumsi (per kapita per minggu)'] / df_clean['Jumlah Penduduk (jiwa)']
    df_clean['Indeks_Kesejahteraan'] = (
        df_clean['Akses Pendidikan_encoded'] + 
        df_clean['Fasilitas Kesehatan_encoded'] + 
        df_clean['Akses Air Bersih_encoded']
    ) / 3
    
    # Remove rows with missing critical data
    df_clean = df_clean.dropna(subset=['Persentase Kemiskinan (%)', 'Tingkat Pengangguran (%)'])
    
    return df_clean

df_silver = clean_data(df_bronze)
print(f"✅ Silver layer data created: {len(df_silver)} records")
print(f"📊 New features added: Konsumsi_per_Penduduk, Indeks_Kesejahteraan")

# Save Silver layer data
try:
    df_silver.to_csv('/data/silver/kemiskinan_cleaned.csv', index=False)
    print(f"💾 Silver layer data saved to /data/silver/kemiskinan_cleaned.csv")
except Exception as e:
    print(f"⚠️  Could not save to /data/silver/ directory: {e}")

# Step 3: Silver to Gold aggregation
print("\n📊 Step 3: Silver to Gold Aggregation...")
print("-" * 40)

def create_gold_aggregations(df):
    """Create aggregated views for Gold layer"""
    
    # Provincial-level aggregations
    gold_province = df.groupby('Provinsi').agg({
        'Persentase Kemiskinan (%)': ['mean', 'std', 'min', 'max'],
        'Tingkat Pengangguran (%)': ['mean', 'std'],
        'Jumlah Penduduk (jiwa)': 'sum',
        'Indeks_Kesejahteraan': 'mean',
        'Konsumsi_per_Penduduk': 'mean'
    }).round(2)
    
    gold_province.columns = ['_'.join(col).strip() for col in gold_province.columns]
    gold_province = gold_province.reset_index()
    
    # Commodity analysis
    gold_commodity = df.groupby('Komoditas').agg({
        'Persentase Kemiskinan (%)': 'mean',
        'Konsumsi (per kapita per minggu)': 'mean',
        'Jumlah Penduduk (jiwa)': 'sum'
    }).round(2).reset_index()
    
    # Income group analysis
    gold_income = df.groupby('Golongan Pengeluaran').agg({
        'Persentase Kemiskinan (%)': 'mean',
        'Tingkat Pengangguran (%)': 'mean',
        'Indeks_Kesejahteraan': 'mean'
    }).round(2).reset_index()
    
    return gold_province, gold_commodity, gold_income

gold_province, gold_commodity, gold_income = create_gold_aggregations(df_silver)

print(f"✅ Provincial aggregation: {len(gold_province)} provinces")
print(f"✅ Commodity analysis: {len(gold_commodity)} commodities")
print(f"✅ Income group analysis: {len(gold_income)} groups")

# Save Gold layer data
try:
    gold_province.to_csv('/data/gold/province_aggregation.csv', index=False)
    gold_commodity.to_csv('/data/gold/commodity_analysis.csv', index=False)
    gold_income.to_csv('/data/gold/income_group_analysis.csv', index=False)
    print(f"💾 Gold layer data saved to /data/gold/ directory")
except Exception as e:
    print(f"⚠️  Could not save to /data/gold/ directory: {e}")

# Step 4: Machine Learning Pipeline
print("\n🤖 Step 4: Machine Learning Pipeline...")
print("-" * 40)

def train_poverty_model(df):
    """Train poverty prediction model"""
    
    # Prepare features for ML
    feature_cols = [
        'Konsumsi (per kapita per minggu)',
        'Jumlah Penduduk (jiwa)',
        'Tingkat Pengangguran (%)',
        'Akses Pendidikan_encoded',
        'Fasilitas Kesehatan_encoded',
        'Akses Air Bersih_encoded',
        'Indeks_Kesejahteraan'
    ]
    
    # Filter data with required features
    ml_data = df[feature_cols + ['Kategori Kemiskinan_encoded']].dropna()
    
    X = ml_data[feature_cols]
    y = ml_data['Kategori Kemiskinan_encoded']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf_model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    return rf_model, accuracy, feature_importance, X_test, y_test, y_pred

rf_model, accuracy, feature_importance, X_test, y_test, y_pred = train_poverty_model(df_silver)

print(f"✅ Random Forest model trained")
print(f"📊 Model accuracy: {accuracy:.3f}")
print(f"🔝 Top 3 important features:")
for idx, row in feature_importance.head(3).iterrows():
    print(f"   {row['feature']}: {row['importance']:.3f}")

# Step 5: Data Quality Validation
print("\n🔍 Step 5: Data Quality Validation...")
print("-" * 40)

def validate_data_quality(df_bronze, df_silver, df_gold_province):
    """Validate data quality across layers"""
    
    quality_report = {
        'bronze_records': len(df_bronze),
        'silver_records': len(df_silver),
        'gold_province_records': len(df_gold_province),
        'bronze_completeness': df_bronze.isnull().sum().sum() / (len(df_bronze) * len(df_bronze.columns)),
        'silver_completeness': df_silver.isnull().sum().sum() / (len(df_silver) * len(df_silver.columns)),
        'data_loss_bronze_to_silver': (len(df_bronze) - len(df_silver)) / len(df_bronze) * 100
    }
    
    return quality_report

quality_report = validate_data_quality(df_bronze, df_silver, gold_province)

print(f"📈 Data Quality Report:")
print(f"   Bronze records: {quality_report['bronze_records']:,}")
print(f"   Silver records: {quality_report['silver_records']:,}")
print(f"   Gold province records: {quality_report['gold_province_records']:,}")
print(f"   Data loss (Bronze → Silver): {quality_report['data_loss_bronze_to_silver']:.1f}%")

# Step 6: Generate Summary Report
print("\n📋 Step 6: Pipeline Summary Report...")
print("-" * 40)

summary_stats = {
    'total_provinces': df_silver['Provinsi'].nunique(),
    'total_commodities': df_silver['Komoditas'].nunique(),
    'avg_poverty_rate': df_silver['Persentase Kemiskinan (%)'].mean(),
    'avg_unemployment_rate': df_silver['Tingkat Pengangguran (%)'].mean(),
    'highest_poverty_province': df_silver.loc[df_silver['Persentase Kemiskinan (%)'].idxmax(), 'Provinsi'],
    'lowest_poverty_province': df_silver.loc[df_silver['Persentase Kemiskinan (%)'].idxmin(), 'Provinsi']
}

print(f"📊 Pipeline Processing Summary:")
print(f"   Total Provinces: {summary_stats['total_provinces']}")
print(f"   Total Commodities: {summary_stats['total_commodities']}")
print(f"   Average Poverty Rate: {summary_stats['avg_poverty_rate']:.2f}%")
print(f"   Average Unemployment Rate: {summary_stats['avg_unemployment_rate']:.2f}%")
print(f"   Highest Poverty: {summary_stats['highest_poverty_province']}")
print(f"   Lowest Poverty: {summary_stats['lowest_poverty_province']}")

print("\n🎉 ETL Pipeline Execution Completed Successfully!")
print("=" * 60)
print("📌 Next Steps:")
print("   1. Access Jupyter notebooks for detailed analysis")
print("   2. Configure Superset dashboards for visualization")
print("   3. Set up Airflow for automated scheduling")
print("   4. Monitor data quality and model performance")
print("=" * 60)
