# Project Overview

This project integrates OpenAI's Whisper model in Python and runs within a Docker container. It provides a FastAPI endpoint that processes an uploaded file and returns the extracted text.

## Features

- **OpenAI Whisper Integration**: Utilizes Whisper for advanced speech-to-text capabilities.
- **Dockerized**: The application runs in a Docker container for easy deployment.
- **FastAPI**: Exposes a RESTful API endpoint for file uploads and text extraction.
- **Configurable**: The repository includes a `.env` file that defines configurable environment variables.
- **Clean Architecture**: The project structure follows the principles of Clean Architecture, ensuring separation of concerns and maintainability.
- **Pre-commit Hooks**: Ensures code quality and formatting with checks for JSON, TOML, YAML, mixed line endings, trailing whitespace, Black, Flake8, isort, mypy, Bandit, and Vulture.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.12
- Poetry
- ffmpeg

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/ggwozdz90/speach-to-text-api
    ```

2. You have two options for installing dependencies:

    - **Using Docker**:
        - Build and run the Docker container, which will handle the installation of dependencies:

            ```sh
            docker-compose up --build
            ```

    - **Locally using Poetry**:
        - Install dependencies locally using Poetry:

            ```sh
            poetry install
            ```

        - Run the application

            ```sh
            poetry run start
            ```

### Usage

Once the Docker container is running, you can access the FastAPI documentation at `http://localhost:8000/docs`.

To transcribe an audio file, use the `/transcribe` endpoint. This endpoint accepts the following parameters:

- `file`: The audio file to be transcribed.
- `language`: The language of the audio file (e.g., `en` for English).

### Example

```sh
curl -X POST "http://localhost:8000/transcribe" -F "file=@path/to/your/file" -F "language=en"
```

## Configuration

The application uses a `.env` file or Docker Compose to define configurable environment variables. Below are the available configuration options:

- `FILE_UPLOAD_PATH`: Path where uploaded files will be stored. Default is `uploaded_files`.
- `DELETE_FILES_AFTER_TRANSCRIPTION`: Whether to delete files after transcription. Set to `true` or `false`. Default is `true`.
- `FASTAPI_HOST`: Host for the FastAPI server. Default is `127.0.0.1`.
- `FASTAPI_PORT`: Port for the FastAPI server. Default is `8000`.
- `WHISPER_MODEL_NAME`: Name of the Whisper model to use. Supported models are `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large`, and `turbo`. Default is `turbo`.
- `WHISPER_MODEL_DOWNLOAD_PATH`: Path where Whisper models are downloaded. Default is `downloaded_whisper_models`.

## Table of Contents

- [Project Overview](#project-overview)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Example](#example)
  - [Configuration](#configuration)
  - [Table of Contents](#table-of-contents)
