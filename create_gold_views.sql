-- Gold Layer Views for Superset Dashboard
-- Kelompok 18 - Big Data Poverty Mapping

-- Provincial Dashboard View - Main view for comprehensive poverty analysis
CREATE OR REPLACE VIEW v_gold_provincial_dashboard AS
SELECT 
    province_name,
    poverty_rate,
    population,
    poor_population,
    ROUND((poor_population::FLOAT / population * 100), 2) as poverty_percentage,
    poverty_depth_index,
    poverty_severity_index,
    avg_consumption_per_capita,
    risk_category,
    data_year,
    CASE 
        WHEN poverty_rate >= 12 THEN 'High Risk'
        WHEN poverty_rate >= 8 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_level_detailed,
    CASE 
        WHEN avg_consumption_per_capita >= 1100000 THEN 'High Income'
        WHEN avg_consumption_per_capita >= 900000 THEN 'Medium Income'
        ELSE 'Low Income'
    END as income_category
FROM gold_province_poverty_summary
ORDER BY poverty_rate DESC;

-- Poverty Hotspots View - Focus on high-risk areas
CREATE OR REPLACE VIEW v_gold_poverty_hotspots AS
SELECT 
    province_name,
    poverty_rate,
    poor_population,
    risk_category,
    poverty_depth_index,
    'Needs Immediate Attention' as priority
FROM gold_province_poverty_summary
WHERE poverty_rate >= 12
UNION ALL
SELECT 
    province_name,
    poverty_rate,
    poor_population,
    risk_category,
    poverty_depth_index,
    'Monitor Closely' as priority
FROM gold_province_poverty_summary
WHERE poverty_rate >= 8 AND poverty_rate < 12
ORDER BY poverty_rate DESC;

-- Summary Statistics View - High-level metrics for KPI dashboards
CREATE OR REPLACE VIEW v_gold_summary_stats AS
SELECT 
    COUNT(*) as total_provinces,
    ROUND(AVG(poverty_rate), 2) as avg_poverty_rate,
    ROUND(SUM(poor_population), 0) as total_poor_population,
    ROUND(SUM(population), 0) as total_population,
    ROUND(AVG(avg_consumption_per_capita), 0) as avg_consumption,
    COUNT(CASE WHEN poverty_rate >= 12 THEN 1 END) as high_risk_provinces,
    COUNT(CASE WHEN poverty_rate < 8 THEN 1 END) as low_risk_provinces
FROM gold_province_poverty_summary;

-- Regional Comparison View - For comparative analysis
CREATE OR REPLACE VIEW v_gold_regional_comparison AS
SELECT 
    province_name,
    poverty_rate,
    avg_consumption_per_capita,
    poverty_depth_index,
    poverty_severity_index,
    CASE 
        WHEN poverty_rate <= 5 THEN 'Very Low'
        WHEN poverty_rate <= 8 THEN 'Low' 
        WHEN poverty_rate <= 12 THEN 'Medium'
        WHEN poverty_rate <= 15 THEN 'High'
        ELSE 'Very High'
    END as poverty_level,
    RANK() OVER (ORDER BY poverty_rate DESC) as poverty_rank,
    RANK() OVER (ORDER BY avg_consumption_per_capita DESC) as consumption_rank
FROM gold_province_poverty_summary
ORDER BY poverty_rate DESC;

-- Economic Indicators View - Focus on consumption and economic factors
CREATE OR REPLACE VIEW v_gold_economic_indicators AS
SELECT 
    province_name,
    avg_consumption_per_capita,
    population,
    poor_population,
    ROUND((avg_consumption_per_capita * population), 0) as total_consumption_estimate,
    ROUND((poor_population::FLOAT / population * 100), 2) as poverty_percentage,
    CASE 
        WHEN avg_consumption_per_capita >= 1200000 THEN 'Developed'
        WHEN avg_consumption_per_capita >= 1000000 THEN 'Developing'
        WHEN avg_consumption_per_capita >= 800000 THEN 'Emerging'
        ELSE 'Underdeveloped'
    END as economic_status,
    data_year
FROM gold_province_poverty_summary
ORDER BY avg_consumption_per_capita DESC;
