"""
Test script để kiểm tra app có chạy được không
"""
import sys
import traceback

print("=" * 60)
print("Testing Lean Six Sigma App")
print("=" * 60)

# Test 1: Import modules
print("\n1. Testing module imports...")
try:
    from database import ProjectDatabase
    print("   ✓ database module")
except Exception as e:
    print(f"   ✗ database module: {e}")
    sys.exit(1)

try:
    from gantt_chart import create_gantt_chart
    print("   ✓ gantt_chart module")
except Exception as e:
    print(f"   ✗ gantt_chart module: {e}")
    sys.exit(1)

try:
    from dashboard import create_status_chart
    print("   ✓ dashboard module")
except Exception as e:
    print(f"   ✗ dashboard module: {e}")
    sys.exit(1)

try:
    from export_pdf import create_project_pdf
    print("   ✓ export_pdf module")
except Exception as e:
    print(f"   ✗ export_pdf module: {e}")
    sys.exit(1)

# Test 2: Database initialization
print("\n2. Testing database initialization...")
try:
    db = ProjectDatabase("test_lean.db")
    print("   ✓ Database created")
    
    # Test basic operations
    projects = db.get_all_projects()
    print(f"   ✓ Query projects: {len(projects)} records")
    
    stats = db.get_statistics()
    print(f"   ✓ Get statistics: {stats['total_projects']} projects")
    
    departments = db.get_departments()
    print(f"   ✓ Query departments: {len(departments)} records")
    
except Exception as e:
    print(f"   ✗ Database error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Import streamlit
print("\n3. Testing Streamlit...")
try:
    import streamlit as st
    print(f"   ✓ Streamlit version: {st.__version__}")
except Exception as e:
    print(f"   ✗ Streamlit import error: {e}")
    sys.exit(1)

# Test 4: Check app.py syntax
print("\n4. Testing app.py syntax...")
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        code = f.read()
    compile(code, 'app.py', 'exec')
    print("   ✓ app.py syntax is valid")
except SyntaxError as e:
    print(f"   ✗ Syntax error in app.py: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ Error reading app.py: {e}")
    sys.exit(1)

# Cleanup
import os
if os.path.exists("test_lean.db"):
    os.remove("test_lean.db")

print("\n" + "=" * 60)
print("✅ All tests passed! App is ready to run.")
print("=" * 60)
print("\nTo start the app, run:")
print("  streamlit run app.py")
print("\nOr use the run script:")
print("  ./run.sh")
print("=" * 60)
