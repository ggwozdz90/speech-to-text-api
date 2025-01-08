# Speech to Text API

This project provides an API for transcribing text from uploaded audio/video files using the OpenAI Whisper model. Additionally, it offers text translation using Facebook/Meta's mBART and Seamless models. A key aspect of this project is memory optimization; models are loaded in separate processes and terminated after a configurable idle timeout to conserve RAM. The application can also be run in a Docker container.

## Features

- **Speech-to-Text Model Integration**: Utilizes advanced speech-to-text models like OpenAI Whisper for transcription.
- **Translation Model Integration**: Translates detected text using translation models like Facebook/Meta's mBART and Seamless.
- **Dockerized**: The application runs in a Docker container for easy deployment.
- **FastAPI**: Exposes RESTful API endpoints for file uploads, text extraction, and subtitle generation.
- **Configurable**: The repository includes a `.env` file that defines configurable environment variables.
- **Clean Architecture**: The project structure follows the principles of Clean Architecture, ensuring separation of concerns and maintainability.
- **Pre-commit Hooks**: Ensures code quality and formatting with checks for JSON, TOML, YAML, mixed line endings, trailing whitespace, Black, Flake8, isort, mypy, Bandit, and Vulture.
- **Logging**: Provides detailed logging of operations for better traceability and debugging.
- **Memory Optimization**: Models are loaded in separate processes and terminated after a configurable idle timeout to conserve RAM.

## Docker Image

The Docker image for this project is available on Docker Hub: [ggwozdz/speech-to-text-api](https://hub.docker.com/r/ggwozdz/speech-to-text-api)

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.12
- Poetry
- ffmpeg

### Running the Project

You have four options for running the project:

1. **Using Docker Compose**:
    - Build and run the Docker container using Docker Compose with the `docker-compose.yaml` file in the root directory:

        ```sh
        docker-compose up --build
        ```

2. **Using Docker**:
    - Run the Docker container directly from Docker Hub. You can choose between CPU and CUDA 12.4 dependencies by using the appropriate tag (`v0.0.0-cpu` or `v0.0.0-cuda124`). The `latest` tag corresponds to the CUDA version:

        ```sh
        docker run -d -p 8000:8000 \
            -e DEVICE=cpu \
            -e FILE_UPLOAD_PATH=uploaded_files \
            -e DELETE_FILES_AFTER_TRANSCRIPTION=true \
            -e FASTAPI_HOST=0.0.0.0 \
            -e FASTAPI_PORT=8000 \
            -e MODEL_IDLE_TIMEOUT=60 \
            -e SPEECH_TO_TEXT_MODEL_NAME=openai/whisper \
            -e SPEECH_TO_TEXT_MODEL_TYPE=turbo \
            -e SPEECH_TO_TEXT_MODEL_DOWNLOAD_PATH=downloaded_speech_to_text_models \
            -e TRANSLATION_MODEL_NAME=facebook/mbart-large-50-many-to-many-mmt \
            -e TRANSLATION_MODEL_DOWNLOAD_PATH=downloaded_translation_models \
            ggwozdz/speech-to-text-api:latest
        ```

3. **Locally using Poetry**:
    - Clone the repository:

        ```sh
        git clone https://github.com/ggwozdz90/speech-to-text-api
        cd speech-to-text-api
        ```

    - Install dependencies locally using Poetry:

        ```sh
        poetry install --extras cpu

        or

        poetry install --extras cuda124
        ```

    - Run the application

        ```sh
        poetry run start
        ```

4. **Using Executable File**:
    - Download the executable file from the [GitHub Releases](https://github.com/ggwozdz90/speech-to-text-api/releases) page.
    - Run the executable file:

        ```sh
        ./speech-to-text-api.exe
        ```

### Usage

Once the Docker container is running, you can access the FastAPI documentation at `http://localhost:8000/docs`.

#### Transcribe Audio to Text

To transcribe an audio file, use the `/transcribe` endpoint. This endpoint accepts the following parameters:

- `file`: The audio file to be transcribed.
- `source_language`: The language of the audio file (e.g., `en_US` for English).
- `target_language`: (Optional) The target language for translation(e.g., `pl_PL` for Polish).

Request:

```sh
curl -X POST "http://localhost:8000/transcribe" \
     -F "file=@/home/user/video.mp4" \
     -F "source_language=en_US" \
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
- `source_language`: The language of the audio file (e.g., `en_US` for English).
- `target_language`: (Optional) The target language for translation(e.g., `pl_PL` for Polish).

Request:

```sh
curl -X POST "http://localhost:8000/transcribe/srt" \
     -F "file=@/home/user/video.mp4" \
     -F "source_language=en_US" \
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

- `LOG_LEVEL`: The logging level for the application. Supported levels are `NOTSET`, `DEBUG`, `INFO`, `WARN`, `WARNING`, `ERROR`, `FATAL`, and `CRITICAL`. The same log level will be applied to `uvicorn` and `uvicorn.access` loggers. Default is `INFO`.
- `DEVICE`: Device to run the models on (`cpu` or `cuda`). Default is `cpu`.
- `FILE_UPLOAD_PATH`: Path where uploaded files will be stored. Default is `uploaded_files`.
- `DELETE_FILES_AFTER_TRANSCRIPTION`: Whether to delete files after transcription. Set to `true` or `false`. Default is `true`.
- `FASTAPI_HOST`: Host for the FastAPI server. Default is `127.0.0.1`.
- `FASTAPI_PORT`: Port for the FastAPI server. Default is `8000`.
- `SPEECH_TO_TEXT_MODEL_NAME`: Name of the speech-to-text model to use. Supported models are `openai/whisper`. Default is `openai/whisper`.
- `SPEECH_TO_TEXT_MODEL_TYPE`: Type of the speech-to-text model to use. Example types are `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large`, and `turbo`. Default is `turbo`.
- `SPEECH_TO_TEXT_MODEL_DOWNLOAD_PATH`: Path where speech-to-text models are downloaded. Default is `downloaded_speech_to_text_models`.
- `TRANSLATION_MODEL_NAME`: Name of the translation model to use. Supported models are `facebook/mbart-large-50-many-to-many-mmt` and `facebook/seamless-m4t-v2-large`. Default is `facebook/seamless-m4t-v2-large`.
- `TRANSLATION_MODEL_DOWNLOAD_PATH`: Path where translation models are downloaded. Default is `downloaded_translation_models`.
- `MODEL_IDLE_TIMEOUT`: Time in seconds after which the model will be unloaded if not used. Default is `60`.

## Supported Languages

The supported languages for each model can be found in the following files:

- Whisper: [whisper_mapping.json](src/assets/mappings/whisper_mapping.json)
- mBART: [mbart_mapping.json](src/assets/mappings/mbart_mapping.json)
- Seamless: [seamless_mapping.json](src/assets/mappings/seamless_mapping.json)

## Table of Contents

- [Speech to Text API](#speech-to-text-api)
  - [Features](#features)
  - [Docker Image](#docker-image)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Running the Project](#running-the-project)
    - [Usage](#usage)
      - [Transcribe Audio to Text](#transcribe-audio-to-text)
      - [Generate Subtitles in SRT Format](#generate-subtitles-in-srt-format)
  - [Configuration](#configuration)
  - [Supported Languages](#supported-languages)
  - [Table of Contents](#table-of-contents)
