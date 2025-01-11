# Stage 1: Dockerfile for building the {{{PROJECT-NAME}}} image
FROM python:3.12-slim-bookworm AS builder

# ARG POETRY_INSTALL_ARGS is used to pass the 'extras' parameter to poetry install.
ARG POETRY_INSTALL_ARGS=""

# Setup Poetry
RUN pip install --no-cache-dir poetry==2.0.0
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy dependency files and source code
COPY pyproject.toml ./
COPY src ./src

# Install dependencies and clean up Poetry cache
RUN poetry install ${POETRY_INSTALL_ARGS} --without dev --no-root \
    && rm -rf "$POETRY_CACHE_DIR"


# Stage 2: Dockerfile for running the {{{PROJECT-NAME}}} image
FROM python:3.12-slim-bookworm AS runtime

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src

# Install updates and create a non-root user
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir -p /home/appuser && chown -R appuser:appuser /home/appuser

# Switch to the non-root user
USER appuser

WORKDIR /app

# Copy the virtual environment and source code from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY src ./src

# Expose the application port
EXPOSE 8000

# Set the entry point for the container
ENTRYPOINT ["python", "-m", "src.main"]