.PHONY: clean clean-build clean-jupyter clean-pyc 

clean: clean-build clean-jupyter clean-pyc

check: black flake

nice: clean check

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-jupyter:
	find . -name '*.ipynb_checkpoints' -exec rm -rf {} +

install:
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install -r requirements.txt
	python -m pip install -e .

install-dev: install
	python -m pip install -r requirements-dev.txt

black:
	black openbudget/

flake:
	flake8 --ignore=E501 openbudget/