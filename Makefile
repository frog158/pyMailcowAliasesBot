run:
	poetry run start
build:
	poetry build
install:
	poetry install
ipython:
	poetry run ipython
lint:
	poetry run flake8 .
test:
	poetry run pytest -vv