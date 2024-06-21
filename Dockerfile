# syntax=docker/dockerfile:1

FROM python:3.10-slim-bookworm

ENV POETRY_VERSION=1.6 \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry and clean up
RUN pip install "poetry==$POETRY_VERSION" && \
    rm -rf /root/.cache/pip

# Set work directory
WORKDIR /code

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /code/

# Install project dependencies and clean up
RUN poetry install --no-interaction --no-ansi --no-root --no-dev && \
    rm -rf /root/.cache/pip

# Copy Python code to the Docker image
COPY pypi_scout /code/pypi_scout/

# Make empty data directory
RUN mkdir -p /code/data

ENV PYTHONPATH=/code

# Use the script as the entrypoint
CMD ["uvicorn", "pypi_scout.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
