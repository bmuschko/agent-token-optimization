.PHONY: help install test task verify clean

help:
	@echo "make install    create the environment and install test tooling"
	@echo "make test       run the regression suite (must stay green)"
	@echo "make task T=t1  run the acceptance tests for one task"
	@echo "make verify     check this machine is set up correctly"

install:
	uv sync

test:
	uv run pytest

task:
	@test -n "$(T)" || (echo "usage: make task T=t1" && exit 1)
	uv run pytest tests/tasks/test_$(T)_*.py -v

verify:
	uv run python scripts/verify_setup.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache
