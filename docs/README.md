# Speech to Text API

This project provides an API for transcribing and translating audio/video content using state-of-the-art AI models. Convert speech to text using OpenAI's Whisper model and translate using Facebook/Meta's mBART or Seamless models.

## Features

- **RESTful API**: Exposes RESTful API endpoints
- **Transcription**: Utilizes OpenAI Whisper model for transcription
- **Translation**: Translates detected text using translation models like Facebook/Meta's mBART and Seamless
- **Configuration**: The repository includes a `.env` file that defines configurable environment variables.
- **Memory Optimization**: Models are loaded in separate processes and terminated after a configurable idle timeout to conserve RAM

## Available Distributions

### Docker Images

Available on [Docker Hub](https://hub.docker.com/r/ggwozdz/speech-to-text-api):

- `version-cpu`: CPU-only version (fully tested and stable)
- `version-cuda124`: NVIDIA CUDA 12.4 support for GPU acceleration (proof-of-concept implementation)*
- `version-rocm62`: AMD ROCm 6.2 support for GPU acceleration (proof-of-concept implementation, requires build from source code)*
- `latest`: Points to latest CPU version

*Note on GPU Support: The current implementations of CUDA and ROCm support are provided as proof-of-concept solutions. While these implementations handle basic scenarios effectively, they haven't undergone comprehensive testing across all use cases. Users planning to utilize GPU acceleration may need to modify the Docker images to include additional environment-specific GPU support software. I recommend using the CPU version, which has been thoroughly tested and validated. The GPU implementations serve as a foundation for future development of more sophisticated functionality.

### Windows Executable

Download the CPU version executable from [GitHub Releases](https://github.com/ggwozdz90/speech-to-text-api/releases).

## Quick Start

### Prerequisites

Choose your preferred distribution:

- **Windows Executable**:
  - [ffmpeg](https://www.ffmpeg.org/download.html)

- **Docker Images**:
  - [Docker](https://www.docker.com/get-started/)

### Using Docker

- Run the following command to start the API server:

    ```bash
    docker run -d -p 8000:8000 \
      -e LOG_LEVEL=INFO \
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
      -v ./volume/downloaded_speech_to_text_models:/app/downloaded_speech_to_text_models \
      -v ./volume/downloaded_translation_models:/app/downloaded_translation_models \
      -v ./volume/uploaded_files:/app/uploaded_files \
      ggwozdz/speech-to-text-api:latest
    ```

### Using Docker Compose

- Create a `docker-compose.yml` file with the following content and run `docker-compose up`:

    ```yaml
    services:
      api:
        image: ggwozdz/speech-to-text-api:latest
        environment:
          - LOG_LEVEL=INFO
          - DEVICE=cpu
          - FILE_UPLOAD_PATH=uploaded_files
          - DELETE_FILES_AFTER_TRANSCRIPTION=true
          - FASTAPI_HOST=0.0.0.0
          - FASTAPI_PORT=8000
          - MODEL_IDLE_TIMEOUT=60
          - SPEECH_TO_TEXT_MODEL_NAME=openai/whisper
          - SPEECH_TO_TEXT_MODEL_TYPE=turbo
          - SPEECH_TO_TEXT_MODEL_DOWNLOAD_PATH=downloaded_speech_to_text_models
          - TRANSLATION_MODEL_NAME=facebook/mbart-large-50-many-to-many-mmt
          - TRANSLATION_MODEL_DOWNLOAD_PATH=downloaded_translation_models
        ports:
          - "8000:8000"
        volumes:
          - ./volume/downloaded_speech_to_text_models:/app/downloaded_speech_to_text_models
          - ./volume/downloaded_translation_models:/app/downloaded_translation_models
          - ./volume/uploaded_files:/app/uploaded_files
    ```

### Using Windows Executable

1. Download from GitHub Releases
2. Run `speech-to-text-api.exe`

## API Features

### Transcribe Audio/Video

- Request:

    ```bash
    curl -X POST "http://localhost:8000/transcribe" \
        -F "file=@video.mp4" \
        -F "source_language=en_US"
    ```

- Response:

    ```json
    {
      "filename": "your_file_name",
      "content": "transcribed text"
    }
    ```

### Transcribe Audio/Video with Translation

- Request:

    ```bash
    curl -X POST "http://localhost:8000/transcribe" \
        -F "file=@video.mp4" \
        -F "source_language=en_US"
        -F "target_language=pl_PL"
    ```

- Response:

    ```json
    {
      "filename": "your_file_name",
      "content": "transkrypcja tekstu"
    }
    ```

### Generate Subtitles

- Request:

    ```bash
    curl -X POST "http://localhost:8000/transcribe/srt" \
         -F "file=@video.mp4" \
         -F "source_language=en_US"
    ```

- Response:

    ```plaintext
    1
    00:00:00,000 --> 00:00:05,000
    Hello, world!
    2
    00:00:05,000 --> 00:00:10,000
    This is a subtitle.
    ```

### Generate Subtitles with Translation

- Request:

    ```bash
    curl -X POST "http://localhost:8000/transcribe/srt" \
        -F "file=@video.mp4" \
        -F "source_language=en_US"
        -F "target_language=pl_PL"
    ```

- Response:

    ```plaintext
    1
    00:00:00,000 --> 00:00:05,000
    Cześć, świat!
    2
    00:00:05,000 --> 00:00:10,000
    To jest napis.
    ```

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

Refer to mapping files in source code for supported languages:

- Whisper: [whisper_mapping.json](../src/assets/mappings/whisper_mapping.json)
- mBART: [mbart_mapping.json](../src/assets/mappings/mbart_mapping.json)
- Seamless: [seamless_mapping.json](../src/assets/mappings/seamless_mapping.json)

## Developer Guide

Developer guide is available in [docs/DEVELOPER.md](DEVELOPER.md).

## Table of Contents

- [Speech to Text API](#speech-to-text-api)
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
    - [Transcribe Audio/Video](#transcribe-audiovideo)
    - [Transcribe Audio/Video with Translation](#transcribe-audiovideo-with-translation)
    - [Generate Subtitles](#generate-subtitles)
    - [Generate Subtitles with Translation](#generate-subtitles-with-translation)
    - [Health Check](#health-check)
  - [Configuration](#configuration)
  - [Supported Languages](#supported-languages)
  - [Developer Guide](#developer-guide)
  - [Table of Contents](#table-of-contents)
