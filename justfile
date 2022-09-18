test:
    poetry run pytest

format:
    poetry run black connectapi
    poetry run isort connectapi
    poetry run black tests
    poetry run isort tests

docs-build:
    rm -rf docs/_build
    # poetry run jupyter nbconvert --to notebook --execute docs/index.ipynb
    poetry run jupyter-book config sphinx docs
    poetry run jupyter-book build docs
    # open docs/_build/html/index.html