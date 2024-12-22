# Speech to Text API

This project integrates OpenAI's Whisper model in Python and runs within a Docker container. It provides FastAPI endpoints for processing uploaded audio files to extract text and generate subtitles in SRT format. The detected text can also be translated using the mBART model.

## Features

- **OpenAI Whisper Integration**: Utilizes Whisper for advanced speech-to-text capabilities.
- **mBART Translation**: Translates detected text using the mBART model.
- **Dockerized**: The application runs in a Docker container for easy deployment.
- **FastAPI**: Exposes RESTful API endpoints for file uploads, text extraction, and subtitle generation.
- **Configurable**: The repository includes a `.env` file that defines configurable environment variables.
- **Clean Architecture**: The project structure follows the principles of Clean Architecture, ensuring separation of concerns and maintainability.
- **Pre-commit Hooks**: Ensures code quality and formatting with checks for JSON, TOML, YAML, mixed line endings, trailing whitespace, Black, Flake8, isort, mypy, Bandit, and Vulture.
- **Logging**: Detailed logging of operations for better traceability and debugging.

## Docker Image

The Docker image for this project is available on Docker Hub: [ggwozdz/speach-to-text-api](https://hub.docker.com/r/ggwozdz/speach-to-text-api)

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

#### Transcribe Audio to Text

To transcribe an audio file, use the `/transcribe` endpoint. This endpoint accepts the following parameters:

- `file`: The audio file to be transcribed.
- `source_language`: The language of the audio file (e.g., `en_XX` for English).
- `target_language`: (Optional) The target language for translation(e.g., `pl_PL` for Polish).

Request:

```sh
curl -X POST "http://localhost:8000/transcribe" \
     -F "file=@/home/user/video.mp4" \
     -F "source_language=en_XX" \
     -F "target_language=pl_PL"
```

Response:

```json
{
  "filename": "your_file_name",
  "content": "transcribed text"
}
```

#### Generate Subtitles in SRT Format

To generate subtitles in SRT format from an audio file, use the `/transcribe/srt` endpoint. This endpoint accepts the following parameters:

- `file`: The audio file to be transcribed.
- `source_language`: The language of the audio file (e.g., `en_XX` for English).
- `target_language`: (Optional) The target language for translation(e.g., `pl_PL` for Polish).

Request:

```sh
curl -X POST "http://localhost:8000/transcribe/srt" \
     -F "file=@/home/user/video.mp4" \
     -F "source_language=en_XX" \
     -F "target_language=pl_PL"
```

Response:

```plaintext
1
00:00:00,000 --> 00:00:05,000
Hello, world!

2
00:00:05,000 --> 00:00:10,000
This is a subtitle.
```

## Configuration

The application uses a `.env` file or Docker Compose to define configurable environment variables. Below are the available configuration options:

- `DEVICE`: Device to run the models on (`cpu` or `cuda`). Default is `cpu`.
- `FILE_UPLOAD_PATH`: Path where uploaded files will be stored. Default is `uploaded_files`.
- `DELETE_FILES_AFTER_TRANSCRIPTION`: Whether to delete files after transcription. Set to `true` or `false`. Default is `true`.
- `FASTAPI_HOST`: Host for the FastAPI server. Default is `127.0.0.1`.
- `FASTAPI_PORT`: Port for the FastAPI server. Default is `8000`.
- `WHISPER_MODEL_NAME`: Name of the Whisper model to use. Supported models are `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large`, and `turbo`. Default is `turbo`.
- `WHISPER_MODEL_DOWNLOAD_PATH`: Path where Whisper models are downloaded. Default is `downloaded_whisper_models`.
- `TRANSLATION_MODEL_NAME`: Name of the translation model to use. Default is `facebook/mbart-large-50-many-to-many-mmt`.
- `TRANSLATION_MODEL_DOWNLOAD_PATH`: Path where translation models are downloaded. Default is `downloaded_translation_models`.
- `MODEL_IDLE_TIMEOUT`: Time in seconds after which the model will be unloaded if not used. Default is `120`.

## Table of Contents

- [Speech to Text API](#speech-to-text-api)
  - [Features](#features)
  - [Docker Image](#docker-image)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
      - [Transcribe Audio to Text](#transcribe-audio-to-text)
      - [Generate Subtitles in SRT Format](#generate-subtitles-in-srt-format)
  - [Configuration](#configuration)
  - [Table of Contents](#table-of-contents)
