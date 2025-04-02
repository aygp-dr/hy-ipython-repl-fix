# Testing the Fix

This document explains how to test the Hy IPython REPL fix in different environments.

## Prerequisites

- Python 3.8 or higher
- Hy (version 0.26.0 recommended)
- IPython (version 8.14.0 recommended)
- pytest

Install requirements:

```bash
pip install -r requirements.txt
```

## Testing with the Test Suite

Run the automated tests:

```bash
python -m pytest tests/
```

This runs tests for both standard Python and IPython environments.

To run a specific test:

```bash
python -m pytest tests/test_repl_compatibility.py::HyReplCompatibilityTests::test_ipython
```

## Manual Testing

### Testing Hy REPL in Standard Python

```python
import hy
hy.REPL(locals=locals()).run()
```

### Testing Hy REPL in IPython

Start IPython:

```bash
ipython
```

Then in the IPython session:

```python
import hy
hy.REPL(locals=locals()).run()
```

### Expected Results

Both environments should start the Hy REPL successfully without any AttributeError.

## Applying the Fix

If you want to apply the fix to your Hy installation:

```bash
python scripts/fix_hy_repl.py
```

To see the changes without applying them:

```bash
python scripts/fix_hy_repl.py --diff-only
```

To create a backup of the original file:

```bash
python scripts/fix_hy_repl.py --backup
```