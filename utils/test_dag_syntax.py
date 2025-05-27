#!/usr/bin/env python3
"""
Test script to validate DAG syntax without Airflow installation
"""

def test_dag_syntax():
    """Test if the DAG file has valid Python syntax"""
    import ast
    import sys
    
    dag_file = "airflow/dags/poverty_mapping_dag.py"
    
    try:
        with open(dag_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(content)
        print("✅ DAG syntax is valid!")
        
        # Check for potential Jinja template issues
        if '&&' in content:
            print("⚠️  Warning: Found '&&' in bash commands - make sure they're properly escaped")
        
        if '$(date)' in content:
            print("⚠️  Warning: Found '$(date)' in bash commands - this might cause Jinja issues")
            
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in DAG file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading DAG file: {e}")
        return False

if __name__ == "__main__":
    test_dag_syntax()
