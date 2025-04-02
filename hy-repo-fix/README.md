# Fixed Hy REPL Implementation

This directory contains a fixed version of Hy's REPL implementation that is compatible with IPython.

## The Fix

The key fix is in `hy/repl.py`, which modifies how Hy's REPL handles `builtins.quit` and `builtins.exit` attributes.

Original code in Hy's REPL:

```python
saved_values = (
    getattr(sys, "ps1", sentinel),
    getattr(sys, "ps2", sentinel),
    builtins.quit,  # <- This fails in IPython
    builtins.exit,  # <- This fails in IPython
    builtins.help,
)
```

Fixed code:

```python
saved_values = (
    getattr(sys, "ps1", sentinel),
    getattr(sys, "ps2", sentinel),
    getattr(builtins, "quit", None),  # <- Use getattr with default value
    getattr(builtins, "exit", None),  # <- Use getattr with default value
    getattr(builtins, "help", None),  # <- Use getattr with default value
)
```

The fix also handles proper restoration of these attributes in the `finally` block.

## Applying the Fix

Use the script at `../scripts/fix_hy_repl.py` to apply this fix to a Hy installation.