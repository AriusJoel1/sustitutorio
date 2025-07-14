.PHONY: deps lint test report clean all

deps:
	pip install -r requirements.txt

lint:
	black --check src
	flake8 --max-complexity=10 src scripts
	markdownlint readme.md

test:
	pytest --maxfail=1 --disable-warnings --cov=src --cov-fail-under=90

report:
	scripts/make_report.sh

clean:
	rm -rf .pytest_cache .coverage metrics.json report.md

all: deps lint test report
