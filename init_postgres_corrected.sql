-- Initialize PostgreSQL Database for Poverty Mapping
-- Kelompok 18 - Big Data Pipeline Project
-- Only 3 Sumatra Provinces: Sumatera Barat, Sumatera Selatan, Sumatera Utara

-- Create main poverty data table
CREATE TABLE IF NOT EXISTS poverty_data (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100),
    regency VARCHAR(100),
    district VARCHAR(100),
    village VARCHAR(100),
    poverty_percentage DECIMAL(5,2),
    population INTEGER,
    unemployment_rate DECIMAL(5,2),
    consumption_per_capita DECIMAL(10,2),
    education_access VARCHAR(50),
    health_facility VARCHAR(50),
    water_access VARCHAR(20),
    poverty_category VARCHAR(20),
    commodity VARCHAR(100),
    expenditure_group VARCHAR(100),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data from actual Sumatra provinces only
INSERT INTO poverty_data (province, regency, district, village, poverty_percentage, population, unemployment_rate, consumption_per_capita, education_access, health_facility, water_access, poverty_category, commodity, expenditure_group, latitude, longitude) VALUES
-- Sumatera Barat
('Sumatera Barat', 'Padang', 'Padang Utara', 'Lolong', 16.48, 1360, 12.03, 3.03, 'sedang', 'memadai', 'tidak', 'sedang', 'Jagung basah degan kulit', '200 000- 299 999', -0.9471, 100.4172),
('Sumatera Barat', 'Bukittinggi', 'Guguk Panjang', 'Campago', 9.81, 966, 8.08, 1.82, 'sedang', 'memadai', 'ya', 'rendah', 'Jagung basah degan kulit', '750 000- 999 999', -0.3074, 100.3815),
('Sumatera Barat', 'Agam', 'Lubuk Basung', 'Basung', 25.47, 4926, 7.35, 1.14, 'sedang', 'memadai', 'ya', 'tinggi', 'Jagung basah degan kulit', '1 000 000- 1 499 999', -0.2985, 100.0892),
('Sumatera Barat', 'Tanah Datar', 'Batusangkar', 'Limo Kaum', 14.08, 3944, 16.53, 1.83, 'baik', 'memadai', 'ya', 'tinggi', 'Jagung basah degan kulit', '> 1 500 000', -0.4522, 100.6213),
('Sumatera Barat', 'Solok', 'Kubung', 'Selayo', 10.36, 630, 3.01, 2.84, 'buruk', 'memadai', 'tidak', 'rendah', 'Jagung basah degan kulit', '300 000- 499 999', -0.7896, 100.6555),
('Sumatera Barat', 'Sijunjung', 'Kamang Baru', 'Tanjung Gadang', 24.99, 2891, 19.27, 1.23, 'sedang', 'memadai', 'ya', 'tinggi', 'Jagung basah degan kulit', '1 000 000- 1 499 999', -0.6789, 101.0234),
('Sumatera Barat', 'Dharmasraya', 'Pulau Punjung', 'Koto Salak', 5.60, 3404, 10.45, 1.56, 'buruk', 'tidak memadai', 'tidak', 'rendah', 'Jagung basah degan kulit', '500 000- 749 999', -1.1456, 101.3456),
('Sumatera Barat', 'Lima Puluh Kota', 'Harau', 'Tarantang', 13.64, 974, 11.45, 0.70, 'sedang', 'memadai', 'ya', 'rendah', 'Jagung basah degan kulit', '750 000- 999 999', -0.1123, 100.6789),

-- Sumatera Selatan
('Sumatera Selatan', 'Palembang', 'Ilir Timur I', 'Talang Semut', 21.47, 4272, 13.07, 1.75, 'buruk', 'tidak memadai', 'ya', 'sedang', 'Jagung basah degan kulit', '300 000- 499 999', -2.9761, 104.7754),
('Sumatera Selatan', 'Prabumulih', 'Prabumulih Timur', 'Gunung Ibul', 9.86, 3671, 15.22, 4.78, 'baik', 'tidak memadai', 'ya', 'tinggi', 'Jagung basah degan kulit', '150 000- 199 999', -3.4292, 104.2394),
('Sumatera Selatan', 'Lubuklinggau', 'Lubuklinggau Timur I', 'Karang Jaya', 14.13, 3419, 6.84, 4.51, 'buruk', 'memadai', 'tidak', 'rendah', 'Jagung basah degan kulit', '200 000- 299 999', -3.3139, 102.8578),
('Sumatera Selatan', 'Muara Enim', 'Belimbing', 'Tanjung Enim', 17.99, 2185, 14.32, 2.22, 'baik', 'tidak memadai', 'ya', 'sedang', 'Jagung basah degan kulit', '500 000- 749 999', -3.7851, 103.8131),
('Sumatera Selatan', 'Lahat', 'Lahat', 'Bandar Agung', 21.71, 1269, 5.67, 2.26, 'sedang', 'memadai', 'tidak', 'sedang', 'Jagung basah degan kulit', '750 000- 999 999', -3.7974, 103.5319),
('Sumatera Selatan', 'Musi Rawas', 'Muara Beliti', 'Beliti Ulu', 10.69, 2933, 13.27, 0.75, 'baik', 'tidak memadai', 'ya', 'rendah', 'Jagung basah degan kulit', '> 1 500 000', -3.0794, 103.0886),
('Sumatera Selatan', 'OKU Timur', 'Belitang', 'Belitang Jaya', 9.17, 1684, 17.44, 4.32, 'buruk', 'memadai', 'ya', 'tinggi', 'Jagung basah degan kulit', '150 000- 199 999', -3.4167, 104.1833),
('Sumatera Selatan', 'Banyuasin', 'Betung', 'Sumber Mulya', 5.49, 3885, 16.70, 1.57, 'baik', 'tidak memadai', 'ya', 'tinggi', 'Jagung basah degan kulit', '200 000- 299 999', -2.7500, 104.7500),
('Sumatera Selatan', 'OKU Selatan', 'Muaradua', 'Muaradua Kisam', 10.70, 4617, 12.48, 4.11, 'buruk', 'tidak memadai', 'tidak', 'rendah', 'Jagung basah degan kulit', '300 000- 499 999', -4.0789, 103.8456),
('Sumatera Selatan', 'Empat Lawang', 'Tebing Tinggi', 'Air Kuti', 8.64, 1582, 16.65, 0.67, 'buruk', 'memadai', 'ya', 'tinggi', 'Jagung basah degan kulit', '1 000 000- 1 499 999', -3.9167, 103.1833),

-- Sumatera Utara
('Sumatera Utara', 'Medan', 'Medan Kota', 'Kesawan', 13.87, 3592, 17.00, 4.31, 'buruk', 'memadai', 'tidak', 'tinggi', 'Jagung basah degan kulit', '500 000- 749 999', 3.5952, 98.6722),
('Sumatera Utara', 'Binjai', 'Binjai Kota', 'Rambung', 19.50, 3058, 13.89, 3.82, 'baik', 'memadai', 'tidak', 'sedang', 'Jagung basah degan kulit', '> 1 500 000', 3.6007, 98.4854),
('Sumatera Utara', 'Tebing Tinggi', 'Tebing Tinggi Kota', 'Padang Hilir', 15.20, 2456, 11.30, 2.85, 'sedang', 'memadai', 'ya', 'sedang', 'Jagung basah degan kulit', '400 000- 599 999', 3.3281, 99.1625),
('Sumatera Utara', 'Pematangsiantar', 'Siantar Timur', 'Toba', 12.40, 3789, 9.75, 3.45, 'baik', 'memadai', 'ya', 'rendah', 'Jagung basah degan kulit', '600 000- 899 999', 2.9592, 99.0681),
('Sumatera Utara', 'Toba Samosir', 'Balige', 'Sosor Ladang', 18.90, 1234, 14.50, 1.95, 'sedang', 'tidak memadai', 'tidak', 'tinggi', 'Jagung basah degan kulit', '250 000- 399 999', 2.3294, 99.0681),
('Sumatera Utara', 'Deli Serdang', 'Lubuk Pakam', 'Namo Rambe', 11.80, 4567, 8.90, 4.12, 'baik', 'memadai', 'ya', 'rendah', 'Jagung basah degan kulit', '700 000- 999 999', 3.5500, 98.8667),
('Sumatera Utara', 'Langkat', 'Stabat', 'Kwala Mencirim', 16.70, 2890, 15.60, 2.30, 'buruk', 'tidak memadai', 'tidak', 'tinggi', 'Jagung basah degan kulit', '300 000- 499 999', 3.7667, 98.4333),
('Sumatera Utara', 'Asahan', 'Kisaran', 'Kisaran Timur', 14.30, 3456, 12.80, 3.78, 'sedang', 'memadai', 'ya', 'sedang', 'Jagung basah degan kulit', '500 000- 749 999', 2.9833, 99.6167);

-- Create province summary table
CREATE TABLE province_summary AS
SELECT 
    province,
    COUNT(*) as total_areas,
    ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
    ROUND(MIN(poverty_percentage), 2) as min_poverty_rate,
    ROUND(MAX(poverty_percentage), 2) as max_poverty_rate,
    SUM(population) as total_population,
    ROUND(AVG(unemployment_rate), 2) as avg_unemployment_rate
FROM poverty_data 
GROUP BY province;

-- Create regency summary table
CREATE TABLE regency_summary AS
SELECT 
    province,
    regency,
    COUNT(*) as total_areas,
    ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
    SUM(population) as total_population,
    ROUND(AVG(unemployment_rate), 2) as avg_unemployment_rate
FROM poverty_data 
GROUP BY province, regency
ORDER BY province, avg_poverty_rate DESC;

-- Create poverty hotspots view (areas with poverty > 15%)
CREATE VIEW v_poverty_hotspots AS
SELECT 
    province,
    regency,
    district,
    village,
    poverty_percentage,
    population,
    unemployment_rate,
    'High Poverty' as risk_level
FROM poverty_data 
WHERE poverty_percentage > 15.0
ORDER BY poverty_percentage DESC;

-- Create province poverty view
CREATE VIEW v_poverty_by_province AS
SELECT 
    province,
    ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
    COUNT(*) as area_count,
    SUM(population) as total_population,
    CASE 
        WHEN AVG(poverty_percentage) > 20 THEN 'Very High'
        WHEN AVG(poverty_percentage) > 15 THEN 'High'
        WHEN AVG(poverty_percentage) > 10 THEN 'Medium'
        ELSE 'Low'
    END as poverty_level
FROM poverty_data 
GROUP BY province
ORDER BY avg_poverty_rate DESC;

-- Create indexes for better performance
CREATE INDEX idx_poverty_data_province ON poverty_data(province);
CREATE INDEX idx_poverty_data_poverty_pct ON poverty_data(poverty_percentage);
CREATE INDEX idx_poverty_data_population ON poverty_data(population);

-- Show summary
SELECT 'SUMMARY: Database initialized with 3 Sumatra provinces' as message;
SELECT province, COUNT(*) as record_count, ROUND(AVG(poverty_percentage), 2) as avg_poverty 
FROM poverty_data 
GROUP BY province 
ORDER BY province;
