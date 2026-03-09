uv:
	pip install -r requirements.txt
	python -m build

all: test

lint:
	flake8 .

format:
	black .

test:
	python -m pytest -q

clean:
	rm -rf .pytest_cache __pycache__ build dist *.egg-info
