test:
    poetry run pytest

format:
    poetry run black connectapi
    poetry run isort connectapi
    poetry run black tests
    poetry run isort tests