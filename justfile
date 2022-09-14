test:
    poetry run pytest

format:
    poetry run black connectapi
    poetry run isort connectapi
    poetry run black tests
    poetry run isort tests

readme-render:
    poetry run quarto render README.qmd --to gfm --output README.md

docs-build:
    rm -rf docs/_build
    poetry run jupyter-book config sphinx docs
    poetry run jupyter-book build docs
    open docs/_build/html/index.html