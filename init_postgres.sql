-- Initialize Poverty Mapping Database
-- Kelompok 18 - Big Data Poverty Mapping Pipeline Sumatra

-- Create main poverty data table
CREATE TABLE IF NOT EXISTS poverty_data (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100) NOT NULL,
    regency VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    village VARCHAR(100),
    poverty_percentage DECIMAL(5,2),
    population INTEGER,
    poor_population INTEGER,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    year INTEGER DEFAULT 2023,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create province summary table
CREATE TABLE IF NOT EXISTS province_summary (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100) UNIQUE NOT NULL,
    total_regencies INTEGER,
    avg_poverty_rate DECIMAL(5,2),
    total_population INTEGER,
    total_poor_population INTEGER,
    min_poverty_rate DECIMAL(5,2),
    max_poverty_rate DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create regency summary table
CREATE TABLE IF NOT EXISTS regency_summary (
    id SERIAL PRIMARY KEY,
    province VARCHAR(100) NOT NULL,
    regency VARCHAR(100) NOT NULL,
    total_districts INTEGER,
    avg_poverty_rate DECIMAL(5,2),
    total_population INTEGER,
    total_poor_population INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(province, regency)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_poverty_province ON poverty_data(province);
CREATE INDEX IF NOT EXISTS idx_poverty_regency ON poverty_data(regency);
CREATE INDEX IF NOT EXISTS idx_poverty_coordinates ON poverty_data(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_poverty_rate ON poverty_data(poverty_percentage);

-- Insert sample data for Sumatra provinces
INSERT INTO poverty_data (province, regency, district, village, poverty_percentage, population, poor_population, latitude, longitude) VALUES
('Sumatera Utara', 'Medan', 'Medan Kota', 'Kampung Baru', 12.5, 50000, 6250, 3.5952, 98.6722),
('Sumatera Utara', 'Deli Serdang', 'Lubuk Pakam', 'Tanjung Morawa', 15.2, 35000, 5320, 3.6148, 98.8756),
('Sumatera Barat', 'Padang', 'Padang Barat', 'Air Tawar', 10.8, 45000, 4860, -0.9471, 100.4172),
('Sumatera Selatan', 'Palembang', 'Ilir Timur I', 'Bukit Baru', 13.7, 38000, 5206, -2.9761, 104.7754),
('Riau', 'Pekanbaru', 'Sukajadi', 'Kampung Tengah', 11.3, 42000, 4746, 0.5071, 101.4478),
('Jambi', 'Jambi', 'Kota Baru', 'Simpang III Sipin', 14.9, 28000, 4172, -1.6101, 103.6131),
('Bengkulu', 'Bengkulu', 'Selebar', 'Pagar Dewa', 16.8, 25000, 4200, -3.8007, 102.2655),
('Lampung', 'Bandar Lampung', 'Tanjung Karang Pusat', 'Durian Payung', 12.1, 55000, 6655, -5.3971, 105.2946),
('Bangka Belitung', 'Pangkal Pinang', 'Bukit Intan', 'Air Itam', 9.5, 18000, 1710, -2.1316, 106.1068),
('Kepulauan Riau', 'Batam', 'Batu Aji', 'Kibing', 8.2, 32000, 2624, 1.0456, 104.0305);

-- Update province summary based on data
INSERT INTO province_summary (province, total_regencies, avg_poverty_rate, total_population, total_poor_population)
SELECT 
    province,
    COUNT(DISTINCT regency) as total_regencies,
    ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
    SUM(population) as total_population,
    SUM(poor_population) as total_poor_population
FROM poverty_data 
GROUP BY province
ON CONFLICT (province) DO UPDATE SET
    total_regencies = EXCLUDED.total_regencies,
    avg_poverty_rate = EXCLUDED.avg_poverty_rate,
    total_population = EXCLUDED.total_population,
    total_poor_population = EXCLUDED.total_poor_population;

-- Update regency summary
INSERT INTO regency_summary (province, regency, total_districts, avg_poverty_rate, total_population, total_poor_population)
SELECT 
    province,
    regency,
    COUNT(DISTINCT district) as total_districts,
    ROUND(AVG(poverty_percentage), 2) as avg_poverty_rate,
    SUM(population) as total_population,
    SUM(poor_population) as total_poor_population
FROM poverty_data 
GROUP BY province, regency
ON CONFLICT (province, regency) DO UPDATE SET
    total_districts = EXCLUDED.total_districts,
    avg_poverty_rate = EXCLUDED.avg_poverty_rate,
    total_population = EXCLUDED.total_population,
    total_poor_population = EXCLUDED.total_poor_population;

-- Create views for easier data access
CREATE OR REPLACE VIEW v_poverty_by_province AS
SELECT 
    province,
    total_regencies,
    avg_poverty_rate,
    total_population,
    total_poor_population,
    ROUND((total_poor_population::decimal / total_population * 100), 2) as calculated_poverty_rate
FROM province_summary
ORDER BY avg_poverty_rate DESC;

CREATE OR REPLACE VIEW v_poverty_hotspots AS
SELECT 
    province,
    regency,
    district,
    village,
    poverty_percentage,
    population,
    poor_population,
    latitude,
    longitude
FROM poverty_data
WHERE poverty_percentage > 13.0
ORDER BY poverty_percentage DESC;

-- Show results
SELECT 'Database initialized successfully!' as status;
SELECT 'Tables created: poverty_data, province_summary, regency_summary' as info;
SELECT COUNT(*) as sample_records FROM poverty_data;
SELECT COUNT(*) as provinces FROM province_summary;
