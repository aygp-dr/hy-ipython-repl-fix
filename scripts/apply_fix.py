#!/usr/bin/env python3
"""
Script to apply the IPython REPL fix to a Hy repository.
"""

import os
import sys
import shutil
import argparse
import difflib
import tempfile
import subprocess

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Apply the IPython REPL fix to Hy")
    parser.add_argument(
        "--hy-repo", 
        default="../hy-repo", 
        help="Path to the Hy repository"
    )
    parser.add_argument(
        "--fix-path", 
        default="../hy-repo-fix/hy/repl.py", 
        help="Path to the fixed repl.py file"
    )
    parser.add_argument(
        "--backup", 
        action="store_true", 
        help="Create a backup of the original file"
    )
    parser.add_argument(
        "--diff", 
        action="store_true", 
        help="Show diff instead of applying"
    )
    return parser.parse_args()

def show_diff(original_path, fixed_path):
    """Show diff between original and fixed file."""
    with open(original_path, 'r') as f1, open(fixed_path, 'r') as f2:
        original = f1.readlines()
        fixed = f2.readlines()
    
    diff = difflib.unified_diff(
        original, 
        fixed,
        fromfile=original_path,
        tofile=fixed_path
    )
    
    for line in diff:
        sys.stdout.write(line)

def apply_fix(args):
    """Apply the fix to the repository."""
    # Resolve paths
    hy_repo = os.path.abspath(args.hy_repo)
    fix_path = os.path.abspath(args.fix_path)
    target_path = os.path.join(hy_repo, "hy", "repl.py")
    
    # Check if files exist
    if not os.path.exists(fix_path):
        print(f"Error: Fix file not found at {fix_path}")
        return 1
    
    if not os.path.exists(target_path):
        print(f"Error: Target file not found at {target_path}")
        return 1
    
    # Show diff if requested
    if args.diff:
        show_diff(target_path, fix_path)
        return 0
    
    # Create backup if requested
    if args.backup:
        backup_path = f"{target_path}.bak"
        print(f"Creating backup at {backup_path}")
        shutil.copy2(target_path, backup_path)
    
    # Apply the fix
    print(f"Applying fix to {target_path}")
    shutil.copy2(fix_path, target_path)
    
    # Run tests if available
    test_dir = os.path.join(hy_repo, "tests")
    if os.path.exists(test_dir):
        print("Running Hy tests to verify fix...")
        os.chdir(hy_repo)
        subprocess.run([sys.executable, "-m", "pytest", "tests/"], check=False)
    
    print("Fix applied successfully!")
    return 0

def main():
    """Main entry point."""
    args = parse_args()
    return apply_fix(args)

if __name__ == "__main__":
    sys.exit(main())