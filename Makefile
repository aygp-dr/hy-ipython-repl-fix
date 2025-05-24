.PHONY: help install test test-integration test-specific apply-fix diff reproduce-issue clean

help:
	@echo "Available targets:"
	@echo "  install          - Install requirements"
	@echo "  test             - Run all tests"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-specific    - Run specific test (use TEST=path::class::method)"
	@echo "  apply-fix        - Apply the fix to Hy REPL"
	@echo "  diff             - Show diff without applying fix"
	@echo "  reproduce-issue  - Reproduce the original issue"
	@echo "  clean            - Remove generated files and caches"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/

test-integration:
	python -m pytest tests/test_repl_integration.py

test-specific:
	@if [ -z "$(TEST)" ]; then \
		echo "Usage: make test-specific TEST=tests/test_repl_integration.py::HyReplIntegrationTests::test_ipython"; \
		exit 1; \
	fi
	python -m pytest $(TEST)

apply-fix:
	python scripts/apply_fix.py

diff:
	python scripts/apply_fix.py --diff

reproduce-issue:
	python worktrees/reproduce-issue/reproduce_issue.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	rm -rf .pytest_cache/