# {{{PROJECT-TITLE}}}

This project is a template for FastAPI projects.

## Features

- **RESTful API**: Exposes RESTful API endpoints
- **Configuration**: The repository includes a `.env` file that defines configurable environment variables.

## Available Distributions

### Docker Images

Available versions:

- `latest`: Provides the latest version of the application

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started/)

### Using Docker

- Run the following command to start the API server:

    ```bash
    docker run -d -p 8000:8000 \
      -e LOG_LEVEL=INFO \
      -e FASTAPI_HOST=0.0.0.0 \
      -e FASTAPI_PORT=8000 \
      ggwozdz/{{{PROJECT-NAME}}}:latest
    ```

### Using Docker Compose

- Create a `docker-compose.yml` file with the following content and run `docker-compose up`:

    ```yaml
    services:
      api:
        image: ggwozdz/{{{PROJECT-NAME}}}:latest
        environment:
          - LOG_LEVEL=INFO
          - FASTAPI_HOST=0.0.0.0
          - FASTAPI_PORT=8000
        ports:
          - "8000:8000"
    ```

## API Features

### Health Check

- Request:

    ```bash
    curl -X GET "http://localhost:8000/healthcheck"
    ```

- Response:

    ```json
    {
      "status": "OK"
    }
    ```

## Configuration

The application uses a `.env` file or Docker Compose to define configurable environment variables. Below are the available configuration options:

- `LOG_LEVEL`: The logging level for the application. Supported levels are `NOTSET`, `DEBUG`, `INFO`, `WARN`, `WARNING`, `ERROR`, `FATAL`, and `CRITICAL`. The same log level will be applied to `uvicorn` and `uvicorn.access` loggers. Default is `INFO`.
- `FASTAPI_HOST`: Host for the FastAPI server. Default is `127.0.0.1`.
- `FASTAPI_PORT`: Port for the FastAPI server. Default is `8000`.

## Developer Guide

Developer guide is available in [docs/DEVELOPER.md](https://github.com/ggwozdz90/{{{PROJECT-NAME}}}/blob/main/docs/DEVELOPER.md).
