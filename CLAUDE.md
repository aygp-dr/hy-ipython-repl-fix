# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Test Commands
- Install requirements: `pip install -r requirements.txt`
- Run all tests: `python -m pytest tests/`
- Run a specific test: `python -m pytest tests/test_repl_integration.py::HyReplIntegrationTests::test_ipython`
- Apply the fix: `python scripts/apply_fix.py`
- Show diff without applying: `python scripts/apply_fix.py --diff`
- Reproduce the issue: `python worktrees/reproduce-issue/reproduce_issue.py`

## Git Commit Conventions
- Use conventional commit format: `<type>(<scope>): <description>`
- Types: feat, fix, docs, style, refactor, test, chore
- Add Co-authored-by as a trailer, not in commit body:
  ```
  git commit -m "fix(repl): handle missing quit/exit in builtins" --trailer "Co-Authored-By: Claude <noreply@anthropic.com>"
  ```
- Always use `--no-gpg-sign` for commits

## Code Style Guidelines
- Follow PEP 8 for Python code formatting
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Import order: standard library, third-party, local packages
- Type hints are encouraged for function signatures
- Error handling should use try/except with specific exceptions
- Variable naming: snake_case for variables/functions, PascalCase for classes

## Project Structure
- Do not directly modify code in the submodules (cpython-repo, hy-repo, ipython-repo)
- Use scripts/ for utility scripts to apply/test fixes
- Keep documentation in docs/ with .org format
- Place standalone test cases in tests/ directory