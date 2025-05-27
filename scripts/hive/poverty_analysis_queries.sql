-- Hive SQL Queries for Poverty Analysis
-- Kelompok 18 - Pemetaan Kemiskinan Sumatera

-- Create database
CREATE DATABASE IF NOT EXISTS kemiskinan_db;
USE kemiskinan_db;

-- 1. Province Poverty Ranking Query
-- Shows provinces ranked by poverty rate with key indicators
CREATE VIEW province_poverty_ranking AS
SELECT 
    provinsi,
    ROUND(avg_poverty_rate, 2) as poverty_rate_pct,
    province_poverty_classification as risk_level,
    total_population,
    ROUND(clean_water_access_pct, 2) as water_access_pct,
    ROUND(good_education_access_pct, 2) as education_access_pct,
    ROUND(adequate_health_facilities_pct, 2) as health_access_pct,
    RANK() OVER (ORDER BY avg_poverty_rate DESC) as poverty_rank
FROM province_poverty_summary
ORDER BY avg_poverty_rate DESC;

-- 2. Expenditure vs Poverty Analysis
-- Analyzes relationship between expenditure groups and poverty
CREATE VIEW expenditure_poverty_analysis AS
SELECT 
    expenditure_group_clean,
    provinsi,
    ROUND(avg_poverty_rate, 2) as poverty_rate,
    ROUND(avg_consumption, 2) as avg_weekly_consumption,
    total_population,
    most_common_poverty_level,
    CASE 
        WHEN avg_poverty_rate <= 10 THEN 'Low Risk'
        WHEN avg_poverty_rate <= 20 THEN 'Medium Risk'
        ELSE 'High Risk'
    END as expenditure_risk_category
FROM expenditure_analysis
ORDER BY provinsi, avg_poverty_rate DESC;

-- 3. Regional Comparison Dashboard Query
-- Provides summary statistics for dashboard visualization
CREATE VIEW regional_comparison AS
SELECT 
    'Sumatera Barat' as region,
    AVG(avg_poverty_rate) as avg_poverty,
    COUNT(*) as data_points,
    AVG(clean_water_access_pct) as avg_water_access,
    AVG(good_education_access_pct) as avg_education_access
FROM province_poverty_summary
WHERE provinsi = 'Sumatera Barat'

UNION ALL

SELECT 
    'Sumatera Utara' as region,
    AVG(avg_poverty_rate) as avg_poverty,
    COUNT(*) as data_points,
    AVG(clean_water_access_pct) as avg_water_access,
    AVG(good_education_access_pct) as avg_education_access
FROM province_poverty_summary
WHERE provinsi = 'Sumatera Utara'

UNION ALL

SELECT 
    'Sumatera Selatan' as region,
    AVG(avg_poverty_rate) as avg_poverty,
    COUNT(*) as data_points,
    AVG(clean_water_access_pct) as avg_water_access,
    AVG(good_education_access_pct) as avg_education_access
FROM province_poverty_summary
WHERE provinsi = 'Sumatera Selatan';

-- 4. High-Risk Areas Identification
-- Identifies areas requiring immediate intervention
CREATE VIEW high_risk_areas AS
SELECT 
    provinsi,
    avg_poverty_rate,
    total_population,
    (avg_poverty_rate * total_population / 100) as estimated_poor_population,
    clean_water_access_pct,
    good_education_access_pct,
    adequate_health_facilities_pct,
    CASE 
        WHEN clean_water_access_pct < 50 AND good_education_access_pct < 50 THEN 'Critical'
        WHEN clean_water_access_pct < 70 OR good_education_access_pct < 70 THEN 'High Priority'
        ELSE 'Monitor'
    END as intervention_priority
FROM province_poverty_summary
WHERE province_poverty_classification = 'High'
ORDER BY avg_poverty_rate DESC;

-- 5. Model Performance Summary
-- Shows ML model performance metrics
CREATE VIEW model_performance AS
SELECT 
    metric,
    ROUND(value, 4) as performance_value,
    model_type,
    training_timestamp
FROM model_metrics
ORDER BY metric;

-- 6. Top Contributing Factors
-- Shows most important features for poverty prediction
CREATE VIEW poverty_factors AS
SELECT 
    feature,
    ROUND(importance, 4) as importance_score,
    RANK() OVER (ORDER BY importance DESC) as importance_rank,
    CASE 
        WHEN importance >= 0.15 THEN 'High Impact'
        WHEN importance >= 0.10 THEN 'Medium Impact'
        ELSE 'Low Impact'
    END as impact_level
FROM feature_importance
ORDER BY importance DESC;

-- 7. Temporal Analysis (if time series data available)
-- Currently using aggregation timestamp as proxy
CREATE VIEW pipeline_execution_history AS
SELECT 
    DATE(aggregation_timestamp) as execution_date,
    COUNT(DISTINCT provinsi) as provinces_processed,
    AVG(avg_poverty_rate) as national_avg_poverty,
    MAX(avg_poverty_rate) as highest_provincial_poverty,
    MIN(avg_poverty_rate) as lowest_provincial_poverty
FROM province_poverty_summary
GROUP BY DATE(aggregation_timestamp)
ORDER BY execution_date DESC;

-- 8. Comprehensive Poverty Dashboard Query
-- Main query for dashboard creation
CREATE VIEW poverty_dashboard AS
SELECT 
    p.provinsi,
    p.avg_poverty_rate as poverty_rate,
    p.province_poverty_classification as risk_level,
    p.total_population,
    p.clean_water_access_pct,
    p.good_education_access_pct,
    p.adequate_health_facilities_pct,
    ROUND((p.avg_poverty_rate * p.total_population / 100), 0) as estimated_poor_count,
    
    -- Correlations
    c.poverty_unemployment_corr,
    c.poverty_consumption_corr,
    
    -- Model predictions accuracy for this province
    COALESCE(
        (SELECT COUNT(*) FROM poverty_predictions pp 
         WHERE pp.province = p.provinsi AND pp.poverty_category = pp.prediction), 0
    ) as correct_predictions,
    
    -- Overall statistics context
    s.national_avg_poverty,
    s.total_sumatra_population,
    
    -- Intervention recommendations
    CASE 
        WHEN p.avg_poverty_rate > 25 AND p.clean_water_access_pct < 60 THEN 'Infrastructure + Water Access'
        WHEN p.avg_poverty_rate > 20 AND p.good_education_access_pct < 50 THEN 'Education Programs'
        WHEN p.avg_poverty_rate > 15 AND p.adequate_health_facilities_pct < 60 THEN 'Healthcare Infrastructure'
        WHEN p.avg_poverty_rate > 10 THEN 'Economic Development'
        ELSE 'Monitoring and Maintenance'
    END as recommended_intervention

FROM province_poverty_summary p
CROSS JOIN poverty_statistics s
CROSS JOIN poverty_correlations c
ORDER BY p.avg_poverty_rate DESC;

-- Show all views created
SHOW TABLES;
