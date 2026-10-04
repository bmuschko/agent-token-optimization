.PHONY: help install test task coverage verify clean

help:
	@echo "make install    install dependencies"
	@echo "make test       run the regression suite (must stay green)"
	@echo "make task T=t1  run the acceptance tests for one task"
	@echo "make coverage   check coverage of currency.py (task T6)"
	@echo "make verify     check this machine is set up correctly"

install:
	pip install -r requirements.txt

test:
	python3 -m pytest

task:
	@test -n "$(T)" || (echo "usage: make task T=t1" && exit 1)
	python3 -m pytest tests/tasks/test_$(T)_*.py -v

coverage:
	python3 -m pytest --cov=orderly.pricing.currency --cov-report=term-missing \
		--cov-fail-under=95 tests/

verify:
	python3 scripts/verify_setup.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .coverage
