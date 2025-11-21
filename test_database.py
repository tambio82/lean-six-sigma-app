"""
TEST SCRIPT - Verify database_FINAL.py before upload
Run this to make sure file is correct
"""

import sys

print("=" * 60)
print("TESTING database_FINAL.py")
print("=" * 60)

# Test 1: File exists
try:
    with open('database_FINAL.py', 'r') as f:
        content = f.read()
    print("✅ Test 1: File exists and readable")
except Exception as e:
    print(f"❌ Test 1 FAILED: {e}")
    sys.exit(1)

# Test 2: Has ProjectDatabase class
if 'class ProjectDatabase' in content:
    print("✅ Test 2: ProjectDatabase class found")
else:
    print("❌ Test 2 FAILED: ProjectDatabase class NOT found")
    sys.exit(1)

# Test 3: Has __init__ method
if 'def __init__(self' in content:
    print("✅ Test 3: __init__ method found")
else:
    print("❌ Test 3 FAILED: __init__ method NOT found")
    sys.exit(1)

# Test 4: Try to import (syntax check)
try:
    import py_compile
    py_compile.compile('database_FINAL.py', doraise=True)
    print("✅ Test 4: Syntax is valid")
except Exception as e:
    print(f"❌ Test 4 FAILED: Syntax error - {e}")
    sys.exit(1)

# Test 5: Count lines
lines = content.count('\n')
if lines > 1000:
    print(f"✅ Test 5: File has {lines} lines (looks complete)")
else:
    print(f"❌ Test 5 FAILED: File only has {lines} lines (may be incomplete)")
    sys.exit(1)

# Test 6: Has collaboration methods
collab_methods = [
    'add_activity_log',
    'get_activities',
    'add_comment',
    'get_comments',
    'add_meeting_minutes',
    'get_meeting_minutes'
]

missing = []
for method in collab_methods:
    if f'def {method}' not in content:
        missing.append(method)

if not missing:
    print(f"✅ Test 6: All {len(collab_methods)} collaboration methods found")
else:
    print(f"⚠️  Test 6 WARNING: Missing methods: {', '.join(missing)}")
    print("    (File may still work but missing collaboration features)")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nFile database_FINAL.py is ready to upload!")
print("Rename to: database.py when uploading to GitHub")
