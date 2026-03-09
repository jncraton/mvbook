uv:
	pip install -r requirements.txt
	python -m build

all: test

lint:
	uvx black@24.1.0 --check .

format:
	uvx black@24.1.0 .

test:
	uvx pytest@9.0.2

upload:
	python3 -m build
	python3 -m twine upload dist/*

clean:
	rm -rf .pytest_cache __pycache__ build dist *.egg-info */__pycache__ uv.lock
