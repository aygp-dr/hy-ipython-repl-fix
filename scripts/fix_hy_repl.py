#!/usr/bin/env python3
"""
This script applies a fix to the Hy REPL to handle missing quit/exit builtins in IPython.

The fix modifies how the REPL handles the builtins.quit and builtins.exit attributes,
making it compatible with both standard Python and IPython environments.
"""

import os
import sys
import argparse
import shutil
import difflib


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fix Hy REPL to handle missing quit/exit builtins in IPython"
    )
    parser.add_argument(
        "--hy-path", 
        help="Path to the Hy installation directory"
    )
    parser.add_argument(
        "--diff-only", 
        action="store_true", 
        help="Just show the diff without applying changes"
    )
    parser.add_argument(
        "--backup", 
        action="store_true", 
        help="Create a backup of the original file"
    )
    return parser.parse_args()


def find_hy_installation():
    """Find the Hy installation directory in site-packages."""
    try:
        import hy
        return os.path.dirname(hy.__file__)
    except ImportError:
        print("Error: Hy package is not installed. Please install it first:")
        print("pip install hy")
        sys.exit(1)


def load_patched_repl():
    """Load the patched version of the REPL code."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    patch_file = os.path.join(current_dir, "..", "hy-repo-fix", "hy", "repl.py")
    
    if os.path.exists(patch_file):
        with open(patch_file, 'r') as f:
            return f.read()
    else:
        print(f"Error: Patch file not found at {patch_file}")
        print("You need to have the fixed repl.py file in hy-repo-fix/hy/repl.py")
        sys.exit(1)


def patch_repl_file(hy_path, patched_content, diff_only=False, backup=False):
    """Apply the patch to the repl.py file."""
    repl_path = os.path.join(hy_path, "repl.py")
    
    if not os.path.exists(repl_path):
        print(f"Error: repl.py not found at {repl_path}")
        sys.exit(1)
    
    # Read the original file
    with open(repl_path, 'r') as f:
        original_content = f.read()
    
    # Create the diff
    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        patched_content.splitlines(keepends=True),
        fromfile=f"{repl_path} (original)",
        tofile=f"{repl_path} (patched)"
    )
    
    diff_text = ''.join(diff)
    
    # If diff-only mode, just print the diff and exit
    if diff_only:
        if diff_text:
            print(diff_text)
        else:
            print("No changes needed, files are identical.")
        return
    
    # Create backup if requested
    if backup and diff_text:
        backup_path = f"{repl_path}.bak"
        print(f"Creating backup at {backup_path}")
        shutil.copy2(repl_path, backup_path)
    
    # Apply the patch
    if diff_text:
        with open(repl_path, 'w') as f:
            f.write(patched_content)
        print(f"Successfully patched {repl_path}")
    else:
        print("No changes needed, files are identical.")


def main():
    """Main function."""
    args = parse_args()
    
    # Find Hy installation if not provided
    hy_path = args.hy_path or find_hy_installation()
    print(f"Hy installation found at: {hy_path}")
    
    # Load the patched REPL code
    patched_content = load_patched_repl()
    
    # Apply the patch
    patch_repl_file(hy_path, patched_content, args.diff_only, args.backup)
    
    # Verify the fix if we applied it
    if not args.diff_only:
        print("\nVerifying the fix...")
        print("Running tests with pytest. Make sure pytest is installed.")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(current_dir, "..", "tests")
        
        if os.path.exists(test_dir):
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_dir, "-v"],
                capture_output=True,
                text=True
            )
            
            print("\nTest Results:")
            print(result.stdout)
            
            if result.returncode == 0:
                print("\nFix verified successfully!")
            else:
                print("\nTests failed. The fix might not be working correctly.")
        else:
            print(f"Warning: Test directory not found at {test_dir}")


if __name__ == "__main__":
    main()