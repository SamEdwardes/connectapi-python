FROM python:3.9

# Install poetry
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN poetry config virtualenvs.create false

# Install depdencies
COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock
RUN poetry install --no-root

WORKDIR /connectapi
