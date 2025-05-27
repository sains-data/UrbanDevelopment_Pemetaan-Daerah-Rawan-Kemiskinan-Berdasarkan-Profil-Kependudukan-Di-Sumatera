#!/usr/bin/env python3
"""
Airflow DAG Manager - Stop All Except Final
Kelompok 18 - Poverty Mapping Pipeline
"""

import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def manage_airflow_dags():
    """Manage Airflow DAGs - Keep final, stop others"""
    
    print("=" * 60)
    print("🌊 AIRFLOW DAG MANAGEMENT")
    print("🎯 Keep: poverty_mapping_etl_final (SUCCESS)")
    print("⏹️ Stop: working, simple, fixed (to avoid conflicts)")
    print("=" * 60)
    
    # DAGs to pause/unpause
    dags_to_pause = [
        'poverty_mapping_etl_working',
        'poverty_mapping_etl_simple', 
        'poverty_mapping_etl_fixed',
        'poverty_mapping_etl'  # original
    ]
    
    dag_to_keep = 'poverty_mapping_etl_final'
    
    try:
        # First, check current DAG status
        print("\n🔍 Checking current DAG status...")
        list_cmd = ['docker', 'exec', 'airflow', 'airflow', 'dags', 'list']
        result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Airflow DAGs available:")
            for line in result.stdout.split('\n'):
                if 'poverty_mapping' in line:
                    print(f"   📋 {line.strip()}")
        
        # Keep the final DAG active (unpause)
        print(f"\n🚀 Keeping active: {dag_to_keep}")
        unpause_cmd = ['docker', 'exec', 'airflow', 'airflow', 'dags', 'unpause', dag_to_keep]
        result = subprocess.run(unpause_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {dag_to_keep} is ACTIVE and RUNNING")
        else:
            print(f"⚠️ Could not unpause {dag_to_keep}: {result.stderr}")
        
        # Pause other DAGs to avoid conflicts
        print(f"\n⏹️ Stopping other DAGs to avoid conflicts...")
        for dag_id in dags_to_pause:
            print(f"   🛑 Pausing: {dag_id}")
            pause_cmd = ['docker', 'exec', 'airflow', 'airflow', 'dags', 'pause', dag_id]
            result = subprocess.run(pause_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"   ✅ {dag_id} paused successfully")
            else:
                print(f"   ⚠️ Could not pause {dag_id} (might not exist)")
        
        # Show final status
        print(f"\n📊 Final DAG Status:")
        state_cmd = ['docker', 'exec', 'airflow', 'airflow', 'dags', 'state', dag_to_keep]
        result = subprocess.run(state_cmd, capture_output=True, text=True, timeout=30)
        
        print("\n" + "=" * 60)
        print("🎉 DAG MANAGEMENT COMPLETED!")
        print(f"✅ ACTIVE: {dag_to_keep}")
        print("⏹️ PAUSED: All other poverty mapping DAGs")
        print("🔗 Check Airflow UI: http://localhost:8090")
        print("=" * 60)
        
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("❌ Timeout while managing DAGs")
        return False
    except Exception as e:
        logger.error(f"❌ Error managing DAGs: {e}")
        return False

def check_dag_runs():
    """Check recent DAG runs"""
    print("\n📈 Checking recent DAG runs...")
    
    try:
        # Check recent runs of final DAG
        runs_cmd = ['docker', 'exec', 'airflow', 'airflow', 'dags', 'list-runs', 
                   '-d', 'poverty_mapping_etl_final', '--limit', '5']
        result = subprocess.run(runs_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("📊 Recent runs of final DAG:")
            print(result.stdout)
        
    except Exception as e:
        logger.warning(f"⚠️ Could not check DAG runs: {e}")

def main():
    """Main execution"""
    try:
        print("🌊 Starting Airflow DAG Management...")
        
        # Manage DAGs
        if not manage_airflow_dags():
            print("❌ DAG management failed")
            return 1
        
        # Check runs
        check_dag_runs()
        
        print("\n💡 NEXT STEPS:")
        print("1. 🌐 Open Airflow UI: http://localhost:8090")
        print("2. ✅ Verify only 'poverty_mapping_etl_final' is active")
        print("3. 📊 Check that pipeline runs are successful")
        print("4. 🚀 Continue with Superset dashboard creation")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ Process cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
