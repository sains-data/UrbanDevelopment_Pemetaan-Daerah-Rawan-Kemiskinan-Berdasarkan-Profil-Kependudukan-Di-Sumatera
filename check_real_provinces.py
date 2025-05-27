import pandas as pd

# Load CSV and check provinces
df = pd.read_csv(r'C:\TUBESABD\data\Profil_Kemiskinan_Sumatera.csv')

print("Provinsi yang ada dalam CSV:")
provinces = df['Provinsi'].unique()
for i, prov in enumerate(provinces, 1):
    print(f"{i}. {prov}")

print(f"\nJumlah provinsi: {df['Provinsi'].nunique()}")
print(f"Total rows: {len(df)}")

# Show sample data for each province
print("\nSample data per provinsi:")
for prov in provinces:
    prov_data = df[df['Provinsi'] == prov]
    avg_poverty = prov_data['Persentase Kemiskinan (%)'].mean()
    total_pop = prov_data['Jumlah Penduduk (jiwa)'].sum()
    print(f"• {prov}: {avg_poverty:.2f}% poverty, {total_pop:,} population")
