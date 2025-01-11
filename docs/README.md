# {{{PROJECT-TITLE}}}

This project is a template for FastAPI projects.

## Features

- **RESTful API**: Exposes RESTful API endpoints
- **Configuration**: The repository includes a `.env` file that defines configurable environment variables.

## Available Distributions

### Docker Images

Available versions:

- `latest`: Provides the latest version of the application

### Windows Executable

Download the executable from [GitHub Releases](https://github.com/ggwozdz90/{{{PROJECT-NAME}}}/releases).

## Quick Start

### Prerequisites

Choose your preferred distribution:

- **Windows Executable**:
  - Windows 10 or later

- **Docker Images**:
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

### Using Windows Executable

1. Download from GitHub Releases
2. Run `{{{PROJECT-NAME}}}.exe`

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

Developer guide is available in [docs/DEVELOPER.md](DEVELOPER.md).

## Table of Contents

- [{{{PROJECT-TITLE}}}](#{{{PROJECT-NAME}}})
  - [Features](#features)
  - [Available Distributions](#available-distributions)
    - [Docker Images](#docker-images)
    - [Windows Executable](#windows-executable)
  - [Quick Start](#quick-start)
    - [Prerequisites](#prerequisites)
    - [Using Docker](#using-docker)
    - [Using Docker Compose](#using-docker-compose)
    - [Using Windows Executable](#using-windows-executable)
  - [API Features](#api-features)
    - [Health Check](#health-check)
  - [Configuration](#configuration)
  - [Developer Guide](#developer-guide)
  - [Table of Contents](#table-of-contents)
