import pandas as pd

print("🔍 ANALYSIS DATA ASLI DARI CSV")
print("=" * 40)

# Load CSV
df = pd.read_csv(r'C:\TUBESABD\data\Profil_Kemiskinan_Sumatera.csv')
print(f"Total rows: {len(df)}")

# Get unique provinces
provinces = df['Provinsi'].unique()
print(f"\nProvinsi yang benar dalam CSV:")
for i, prov in enumerate(provinces, 1):
    print(f"{i}. {prov}")

print(f"\nJumlah provinsi: {len(provinces)}")

# Analyze each province
print("\n📊 ANALYSIS PER PROVINSI:")
print("=" * 40)

for prov in provinces:
    prov_data = df[df['Provinsi'] == prov]
    
    # Convert to numeric
    pov_rates = pd.to_numeric(prov_data['Persentase Kemiskinan (%)'], errors='coerce')
    populations = pd.to_numeric(prov_data['Jumlah Penduduk (jiwa)'], errors='coerce')
    consumption = pd.to_numeric(prov_data['Konsumsi (per kapita per minggu)'], errors='coerce')
    
    # Clean data
    clean_pov = pov_rates.dropna()
    clean_pop = populations.dropna()
    clean_cons = consumption.dropna()
    
    if len(clean_pov) > 0 and len(clean_pop) > 0:
        avg_pov = clean_pov.mean()
        total_pop = clean_pop.sum()
        avg_cons = clean_cons.mean() if len(clean_cons) > 0 else 0
        poor_pop = int(total_pop * avg_pov / 100)
        
        # Risk category
        risk = 'High' if avg_pov >= 15 else ('Medium' if avg_pov >= 10 else 'Low')
        
        print(f"\n🏛️ {prov}:")
        print(f"   • Poverty Rate: {avg_pov:.2f}%")
        print(f"   • Population: {total_pop:,}")
        print(f"   • Poor Population: {poor_pop:,}")
        print(f"   • Avg Consumption: {avg_cons:.2f} per week")
        print(f"   • Risk Category: {risk}")
        print(f"   • Records: {len(prov_data)}")

print("\n" + "=" * 40)
print("✅ ANALYSIS COMPLETED")
