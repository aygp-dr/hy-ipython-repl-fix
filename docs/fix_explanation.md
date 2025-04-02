# Technical Explanation of the Fix

## The Issue

When using Hy's REPL inside IPython, an error occurs:

```
AttributeError: module 'builtins' has no attribute 'quit'
```

This happens because Hy's REPL implementation assumes that `builtins.quit` and `builtins.exit` always exist, which is true in standard Python but not in IPython.

## How Python and IPython Handle quit/exit Differently

### Standard Python
In standard Python, the `site` module adds `quit` and `exit` functions to the `builtins` module during interpreter initialization:

```python
# From site.py
__builtin__.quit = _sitebuiltins._Quitter('quit')
__builtin__.exit = _sitebuiltins._Quitter('exit')
```

These objects remain accessible throughout the Python session.

### IPython
IPython uses a different approach:

1. It removes the standard `quit` and `exit` functions from builtins using its `BuiltinTrap` mechanism
2. It provides its own implementations via the `ExitAutocall` class
3. These are accessible in the interactive namespace, not through the builtins module

## The Fix

The fix is simple but effective:

1. Use `getattr` with a default value when accessing `builtins.quit` and `builtins.exit`
2. Check if the attributes existed before setting them during cleanup

### Original Code
```python
saved_values = (
    getattr(sys, "ps1", sentinel),
    getattr(sys, "ps2", sentinel),
    builtins.quit,  # This fails in IPython
    builtins.exit,  # This fails in IPython
    builtins.help,
)

# Later in finally block:
sys.ps1, sys.ps2, builtins.quit, builtins.exit, builtins.help = saved_values
```

### Fixed Code
```python
saved_values = (
    getattr(sys, "ps1", sentinel),
    getattr(sys, "ps2", sentinel),
    getattr(builtins, "quit", None),  # Use getattr with default
    getattr(builtins, "exit", None),  # Use getattr with default
    getattr(builtins, "help", None),  # Use getattr with default
)

# Later in finally block:
sys.ps1, sys.ps2 = saved_values[0], saved_values[1]

# Restore original quit/exit/help or remove if they didn't exist
if saved_values[2] is not None:
    builtins.quit = saved_values[2]
elif hasattr(builtins, "quit"):
    delattr(builtins, "quit")
            
if saved_values[3] is not None:
    builtins.exit = saved_values[3]
elif hasattr(builtins, "exit"):
    delattr(builtins, "exit")
            
if saved_values[4] is not None:
    builtins.help = saved_values[4]
elif hasattr(builtins, "help"):
    delattr(builtins, "help")
```

This fix makes Hy's REPL compatible with both standard Python and IPython environments.