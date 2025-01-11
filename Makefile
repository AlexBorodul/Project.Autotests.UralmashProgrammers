install:
		pip install poetry && \
		poetry install


start:
		poetry run python project/main.py