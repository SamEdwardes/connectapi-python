test:
    poetry run pytest

format:
    poetry run black connectapi
    poetry run isort connectapi
    poetry run black tests
    poetry run isort tests

docs-open:
    open docs/_build/html/index.html

docs-clear-output:
    poetry run jupyter nbconvert --clear-output --inplace docs/**/*.ipynb

docs-build:
    rm -rf docs/_build
    poetry run jupyter nbconvert --clear-output --inplace docs/**/*.ipynb
    docker build -t connectapi .
    docker run -it --rm \
        -v $(pwd):/connectapi \
        -e CONNECT_SERVER=$CONNECT_SERVER \
        -e CONNECT_API_KEY=$CONNECT_API_KEY \
        connectapi \
        /bin/bash \
        -c "poetry install && jupyter-book build docs"
    open docs/_build/html/index.html

docker-build:
    docker build -t connectapi .

docker-run:
    docker run -it --rm \
        -v $(pwd):/connectapi \
        -e CONNECT_SERVER=$CONNECT_SERVER \
        -e CONNECT_API_KEY=$CONNECT_API_KEY \
        connectapi /bin/bash
