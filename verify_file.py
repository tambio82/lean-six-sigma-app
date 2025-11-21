#!/usr/bin/env python3
"""
VERIFICATION SCRIPT - Check comments_manager.py before upload
Run this to make sure you have the CORRECT file!
"""

import sys
import os

print("=" * 70)
print("  VERIFYING: comments_manager.py")
print("=" * 70)

# Test 1: File exists
print("\n[Test 1] Checking if file exists...")
if not os.path.exists('comments_manager.py'):
    print("  ❌ FAILED: comments_manager.py not found!")
    print("  → Make sure file is in same directory as this script")
    sys.exit(1)
print("  ✅ PASSED: File exists")

# Test 2: Read file
print("\n[Test 2] Reading file...")
try:
    with open('comments_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"  ✅ PASSED: File readable ({len(content)} characters)")
except Exception as e:
    print(f"  ❌ FAILED: Cannot read file - {e}")
    sys.exit(1)

# Test 3: Check for DataFrame conversion
print("\n[Test 3] Checking for DataFrame conversion...")
if "comments.to_dict('records')" in content:
    print("  ✅ PASSED: DataFrame conversion code found")
else:
    print("  ❌ FAILED: DataFrame conversion code NOT found!")
    print("  → This is the WRONG file!")
    print("  → Download the correct file from Claude")
    sys.exit(1)

# Test 4: Check line count
print("\n[Test 4] Checking line count...")
lines = content.count('\n')
if 370 <= lines <= 390:
    print(f"  ✅ PASSED: File has {lines} lines (expected ~382)")
else:
    print(f"  ⚠️  WARNING: File has {lines} lines (expected ~382)")
    print("  → File may be incomplete")

# Test 5: Check critical method
print("\n[Test 5] Checking get_comments method...")
if "def get_comments(self, project_id: int) -> List[Dict]:" in content:
    print("  ✅ PASSED: get_comments method signature found")
else:
    print("  ❌ FAILED: get_comments method signature not found!")
    sys.exit(1)

# Test 6: Check for the fix
print("\n[Test 6] Checking for the actual fix...")
if "# Convert DataFrame to list of dicts" in content:
    print("  ✅ PASSED: Fix comment found")
    
    # Check if conversion is right after comment
    if "if comments is not None and not comments.empty:" in content:
        print("  ✅ PASSED: DataFrame empty check found")
        
        if "return comments.to_dict('records')" in content:
            print("  ✅ PASSED: Conversion to dict found")
        else:
            print("  ❌ FAILED: Conversion missing!")
            sys.exit(1)
    else:
        print("  ❌ FAILED: Empty check missing!")
        sys.exit(1)
else:
    print("  ❌ FAILED: Fix comment not found!")
    print("  → This is the OLD file!")
    sys.exit(1)

# Test 7: Syntax check
print("\n[Test 7] Checking Python syntax...")
try:
    compile(content, 'comments_manager.py', 'exec')
    print("  ✅ PASSED: No syntax errors")
except SyntaxError as e:
    print(f"  ❌ FAILED: Syntax error - {e}")
    sys.exit(1)

# Test 8: Check for to_dict occurrences
print("\n[Test 8] Counting to_dict occurrences...")
count = content.count("to_dict('records')")
if count >= 1:
    print(f"  ✅ PASSED: Found {count} occurrence(s) of to_dict('records')")
else:
    print("  ❌ FAILED: No to_dict conversion found!")
    sys.exit(1)

# All tests passed!
print("\n" + "=" * 70)
print("  🎉 ALL TESTS PASSED!")
print("=" * 70)
print("\n✅ This file is CORRECT and ready to upload!")
print("✅ You can safely upload this to GitHub")
print("\nNext steps:")
print("1. Go to: https://github.com/tambio82/lean-six-sigma-app")
print("2. Replace comments_manager.py with this file")
print("3. Commit changes")
print("4. Wait for Streamlit to redeploy")
print("\n" + "=" * 70)
