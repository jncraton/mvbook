uv:
	pip install -r requirements.txt
	python -m build

all: test

lint:
	pipx run --spec black==24.1.0 black --check .

format:
	pipx run --spec black==24.1.0 black .

test:
	pipx run --spec pytest==9.0.2 pytest

upload:
	python3 -m build
	python3 -m twine upload dist/*

clean:
	rm -rf .pytest_cache __pycache__ build dist *.egg-info */__pycache__ uv.lock
