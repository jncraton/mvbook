uv:
	pip install -r requirements.txt
	python -m build

all: test

lint:
	flake8 .

format:
	black .

test:
	python3 -m pytest -q

clean:
	rm -rf .pytest_cache __pycache__ build dist *.egg-info */__pycache__
