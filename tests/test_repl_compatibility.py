#!/usr/bin/env python3
"""
Test script for checking the compatibility of Hy REPL in different Python environments.
This test verifies that the Hy REPL can run in both standard Python and IPython environments.
"""

import sys
import unittest
import subprocess


class HyReplCompatibilityTests(unittest.TestCase):
    """Test Hy REPL compatibility with different Python environments."""
    
    def test_standard_python(self):
        """Test that Hy REPL works in standard Python."""
        cmd = [
            sys.executable,
            "-c",
            "import hy; print('Starting Hy REPL...'); "
            "try: exit_code = hy.REPL(locals=locals()).run(); print('Success!'); sys.exit(exit_code)"
            "except Exception as e: print(f'Error: {e}'); sys.exit(1)"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Standard Python test failed: {result.stderr}")
        self.assertIn("Success!", result.stdout)
    
    def test_ipython(self):
        """Test that Hy REPL works in IPython."""
        try:
            import IPython
        except ImportError:
            self.skipTest("IPython not installed")
        
        cmd = [
            sys.executable,
            "-m", "IPython",
            "-c",
            "import sys; "
            "import hy; print('Starting Hy REPL...'); "
            "try: exit_code = hy.REPL(locals=locals()).run(); print('Success!'); sys.exit(exit_code)"
            "except Exception as e: print(f'Error: {e}'); sys.exit(1)"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"IPython test failed: {result.stderr}")
        self.assertIn("Success!", result.stdout)


if __name__ == "__main__":
    unittest.main()