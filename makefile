uv:
	pip install -r requirements.txt
	python -m build

all: test

lint:
	uv run --with pylint==2.17.5 pylint .

format:
	uv run --with black==24.1.0 black .

test:
	python3 -m pytest -q

upload:
	python3 -m build
	python3 -m twine upload dist/*

clean:
	rm -rf .pytest_cache __pycache__ build dist *.egg-info */__pycache__
