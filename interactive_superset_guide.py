#!/usr/bin/env python3
"""
Interactive Superset Chart Creation Guide
Kelompok 18 - Step-by-step dengan Wait Prompts
"""

import webbrowser
import time
import sys

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_user(message):
    input(f"\n⏸️ {message}\n🔄 Press Enter when ready to continue...")

def print_section_header(title):
    print("\n" + "=" * 60)
    print(f"📋 {title}")
    print("=" * 60)

def print_substep(step_num, description):
    print(f"\n🔸 Step {step_num}: {description}")

def main():
    clear_screen()
    
    print("🎯 INTERACTIVE SUPERSET DASHBOARD CREATION")
    print("📊 Kelompok 18 - Poverty Mapping Sumatera")
    print("🚀 Follow along step-by-step!")
    print("\n" + "=" * 60)
    
    # Step 1: Open Superset
    print_section_header("STEP 1: OPEN SUPERSET & LOGIN")
    print("🌐 Opening Superset in your browser...")
    
    try:
        webbrowser.open("http://localhost:8089")
        print("✅ Superset opened: http://localhost:8089")
    except:
        print("❌ Could not open browser automatically")
        print("📱 Please open manually: http://localhost:8089")
    
    print("\n🔑 LOGIN CREDENTIALS:")
    print("   Username: admin")
    print("   Password: admin")
    
    wait_for_user("Complete login and you see the Superset homepage")
    
    # Step 2: Database Connection  
    print_section_header("STEP 2: DATABASE CONNECTION")
    print("📝 EXACT PLACEMENT INSTRUCTIONS:")
    print_substep(1, "Look for ⚙️ Settings icon in TOP-RIGHT corner")
    print_substep(2, "Click Settings → Database Connections")
    print_substep(3, "Click + DATABASE button (blue button)")
    print_substep(4, "Select 'PostgreSQL' from dropdown")
    
    print("\n📋 COPY-PASTE THESE VALUES:")
    print("━" * 40)
    print("DISPLAY NAME:")
    print("Poverty Mapping DB")
    print("\nSQLALCHEMY URI:")
    print("postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping")
    print("━" * 40)
    
    print_substep(5, "Click TEST CONNECTION (must show success)")
    print_substep(6, "Click CONNECT to save")
    
    wait_for_user("Complete database connection setup")
    
    # Step 3: Dataset Creation
    print_section_header("STEP 3: CREATE DATASET")
    print_substep(1, "Click 'Data' in top menu bar")
    print_substep(2, "Select 'Datasets' from dropdown")
    print_substep(3, "Click + DATASET button")
    
    print("\n📝 FORM SELECTION:")
    print("   DATABASE: Poverty Mapping DB")
    print("   SCHEMA: public")
    print("   TABLE: v_gold_provincial_dashboard")
    
    print_substep(4, "Click CREATE DATASET AND CREATE CHART")
    
    wait_for_user("Complete dataset creation - you should see chart builder")
    
    # Step 4: First Chart - KPI Card
    print_section_header("STEP 4: CREATE KPI CARD #1")
    print("🎯 CREATING: Total Population KPI")
    
    print_substep(1, "Chart Type: Click dropdown → Select 'Big Number'")
    print_substep(2, "Metrics: Click + ADD METRIC → Select 'population' → Set to 'SUM'")
    print_substep(3, "Chart Title: Enter 'Total Population Sumatera'")
    print_substep(4, "Click UPDATE CHART (blue button bottom-left)")
    print_substep(5, "Click SAVE (green button top-right) → Name: 'KPI - Total Population'")
    
    wait_for_user("Complete first KPI chart creation")
    
    # Step 5: Bar Chart
    print_section_header("STEP 5: CREATE BAR CHART")
    print("📊 CREATING: Poverty Rate Comparison")
    
    print_substep(1, "Go to Charts → Click + CHART")
    print_substep(2, "Select dataset: v_gold_provincial_dashboard → CREATE CHART")
    print_substep(3, "Chart Type: Select 'Bar Chart'")
    print_substep(4, "X-AXIS: Drag 'province_name' to X-AXIS")
    print_substep(5, "Y-AXIS: Drag 'poverty_rate' to Y-AXIS (set to AVG)")
    print_substep(6, "Title: 'Poverty Rate by Province (%)'")
    print_substep(7, "UPDATE CHART → SAVE as 'Bar Chart - Poverty Rates'")
    
    wait_for_user("Complete bar chart creation")
    
    # Step 6: Dashboard Creation
    print_section_header("STEP 6: CREATE DASHBOARD")
    print_substep(1, "Click 'Dashboards' in top menu")
    print_substep(2, "Click + DASHBOARD")
    print_substep(3, "Title: 'Poverty Mapping Sumatera - Kelompok 18'")
    print_substep(4, "Click SAVE")
    print_substep(5, "Click EDIT DASHBOARD")
    print_substep(6, "Drag your charts from left panel to dashboard canvas")
    
    print("\n🎨 LAYOUT SUGGESTION:")
    print("   ROW 1: KPI cards (horizontal)")
    print("   ROW 2: Bar chart + Additional charts")
    print("   ROW 3: Table (full width)")
    
    wait_for_user("Complete dashboard creation and layout")
    
    # Final Steps
    print_section_header("COMPLETION & NEXT STEPS")
    print("🎉 CONGRATULATIONS! Your basic dashboard should be ready!")
    
    print("\n📊 WHAT YOU'VE CREATED:")
    print("   ✅ Database connection to PostgreSQL")
    print("   ✅ Dataset from Gold layer")
    print("   ✅ KPI card showing total population")
    print("   ✅ Bar chart comparing provinces")
    print("   ✅ Dashboard with professional layout")
    
    print("\n🚀 NEXT STEPS TO ENHANCE:")
    print("   1. Create more KPI cards (Avg Poverty, High Risk Count)")
    print("   2. Add Pie chart for population distribution")
    print("   3. Add detailed table with all statistics")
    print("   4. Customize colors and themes")
    print("   5. Add filters and interactivity")
    
    print("\n📚 REFERENCE FILES:")
    print("   📄 SUPERSET_PLACEMENT_GUIDE_DETAILED.md - Complete guide")
    print("   📄 CHART_RECOMMENDATIONS_POVERTY_MAPPING.md - Chart types")
    
    print("\n🎯 YOUR DASHBOARD URL:")
    print("   http://localhost:8089/dashboard/list/")
    
    print("\n" + "=" * 60)
    print("🏆 EXCELLENT WORK! You've successfully created your first Superset dashboard!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Process cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
