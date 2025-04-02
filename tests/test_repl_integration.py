"""
Integration tests for Hy REPL in different environments.
"""

import sys
import os
import subprocess
import unittest

class HyReplIntegrationTests(unittest.TestCase):
    """Test Hy REPL integration with different Python environments."""
    
    def test_standard_python(self):
        """Test Hy REPL in standard Python."""
        cmd = [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, '.'); import hy; print('Test successful if no error'); exit_code = hy.REPL(locals=locals()).run(); sys.exit(exit_code)"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Standard Python test failed: {result.stderr}")
        self.assertIn("Test successful if no error", result.stdout)
    
    def test_ipython(self):
        """Test Hy REPL in IPython."""
        try:
            import IPython
        except ImportError:
            self.skipTest("IPython not installed")
        
        cmd = [
            sys.executable,
            "-m", "IPython",
            "-c",
            "import sys; sys.path.insert(0, '.'); import hy; print('Test successful if no error'); exit_code = hy.REPL(locals=locals()).run(); sys.exit(exit_code)"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"IPython test failed: {result.stderr}")
        self.assertIn("Test successful if no error", result.stdout)


if __name__ == "__main__":
    unittest.main()