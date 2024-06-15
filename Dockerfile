# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV POETRY_VERSION=1.6 \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy Python code to the Docker image
COPY pypi_llm /code/pypi_llm/

ENV PYTHONPATH=/code

CMD [ "python", "pypi_llm/foo.py"]
