#!/usr/bin/env python3
"""
Quick Verification Script for Superset-PostgreSQL Connection
Kelompok 18 - Big Data Poverty Mapping Pipeline
"""

import subprocess
import json
import sys

def print_header():
    print("=" * 60)
    print("🔍 SUPERSET-POSTGRESQL CONNECTION VERIFIER")
    print("📊 Kelompok 18 - Big Data Poverty Mapping Pipeline")
    print("=" * 60)

def check_containers():
    """Check if containers are running"""
    print("\n📋 Checking Container Status...")
    
    containers = ["postgres-local", "superset"]
    all_running = True
    
    for container in containers:
        try:
            result = subprocess.run([
                "docker", "ps", "--filter", f"name={container}", 
                "--format", "{{.Names}}: {{.Status}}"
            ], capture_output=True, text=True, timeout=10)
            
            if result.stdout.strip():
                print(f"  ✅ {result.stdout.strip()}")
            else:
                print(f"  ❌ {container}: Not running")
                all_running = False
                
        except Exception as e:
            print(f"  ❌ {container}: Error checking - {e}")
            all_running = False
    
    return all_running

def check_postgresql_data():
    """Check PostgreSQL data availability"""
    print("\n📊 Checking PostgreSQL Data...")
    
    queries = [
        ("Total poverty records", "SELECT COUNT(*) FROM poverty_data;"),
        ("Provinces count", "SELECT COUNT(*) FROM province_summary;"),
        ("Sample province data", "SELECT province, avg_poverty_rate FROM province_summary LIMIT 3;"),
        ("Poverty hotspots", "SELECT COUNT(*) FROM v_poverty_hotspots;")
    ]
    
    for desc, query in queries:
        try:
            result = subprocess.run([
                "docker", "exec", "postgres-local", 
                "psql", "-U", "postgres", "-d", "poverty_mapping", 
                "-t", "-c", query
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"  ✅ {desc}: {output}")
            else:
                print(f"  ❌ {desc}: Query failed")
                
        except Exception as e:
            print(f"  ❌ {desc}: Error - {e}")

def check_network_connectivity():
    """Check network connectivity between containers"""
    print("\n🌐 Testing Network Connectivity...")
    
    try:
        # Test if Superset can reach PostgreSQL
        result = subprocess.run([
            "docker", "exec", "superset", 
            "nc", "-z", "postgres-local", "5432"
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("  ✅ Superset can reach PostgreSQL")
        else:
            print("  ❌ Network connectivity issue")
            
    except Exception as e:
        print(f"  ❌ Network test error: {e}")

def show_connection_info():
    """Display connection information"""
    print("\n🔗 CONNECTION INFORMATION:")
    print("  📍 Superset URL: http://localhost:8089")
    print("  🔑 Login: admin / admin")
    print("  🗄️  Database URI: postgresql://postgres:postgres123@postgres-local:5432/poverty_mapping")
    print("  🌐 External PostgreSQL: localhost:5432")

def show_quick_actions():
    """Show quick actions user can take"""
    print("\n🚀 QUICK ACTIONS:")
    print("  1. Open Superset: http://localhost:8089")
    print("  2. Add database connection with URI above")
    print("  3. Create datasets from tables:")
    print("     • poverty_data")
    print("     • province_summary") 
    print("     • v_poverty_by_province")
    print("     • v_poverty_hotspots")
    print("  4. Build amazing dashboards!")

def main():
    """Main verification process"""
    print_header()
    
    # Run all checks
    containers_ok = check_containers()
    
    if containers_ok:
        check_postgresql_data()
        check_network_connectivity()
        show_connection_info()
        show_quick_actions()
        
        print("\n✅ VERIFICATION COMPLETE!")
        print("🎯 Ready to create awesome poverty mapping dashboards!")
    else:
        print("\n❌ Some containers are not running.")
        print("💡 Try: docker-compose up -d")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
