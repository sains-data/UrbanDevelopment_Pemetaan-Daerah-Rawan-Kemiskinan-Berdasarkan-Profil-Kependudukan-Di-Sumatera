import pandas as pd
import numpy as np

print("🚀 BIG DATA PIPELINE EXECUTION")
print("=" * 50)

# Load data
df = pd.read_csv('data/Profil_Kemiskinan_Sumatera.csv')
print(f"✅ Data loaded: {len(df)} records")
print(f"📊 Columns: {len(df.columns)}")
print(f"🏛️ Provinces: {df['Provinsi'].nunique()}")

# Basic analysis
print("\n📊 BASIC ANALYSIS:")
print(f"Average poverty rate: {df['Persentase Kemiskinan (%)'].mean():.2f}%")
print(f"Average unemployment: {df['Tingkat Pengangguran (%)'].mean():.2f}%")

# Provincial breakdown
print("\n🏛️ PROVINCIAL ANALYSIS:")
for province in df['Provinsi'].unique():
    province_data = df[df['Provinsi'] == province]
    avg_poverty = province_data['Persentase Kemiskinan (%)'].mean()
    print(f"• {province}: {avg_poverty:.2f}% poverty rate")

print("\n✅ PIPELINE EXECUTION COMPLETED!")
print("🎯 Ready for advanced analytics in Jupyter!")
