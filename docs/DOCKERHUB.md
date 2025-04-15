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

Available versions:

- `version-cpu`: CPU-only version (fully tested and stable)
- `version-cuda128`: NVIDIA CUDA 12.8 support for RTX 50XX GPU acceleration (tested and stable)
- `version-cuda124`: NVIDIA CUDA 12.4 support for GPU acceleration (not tested)*
- `version-rocm62`: AMD ROCm 6.2 support for GPU acceleration (proof-of-concept implementation, requires build from source code)*
- `latest`: Points to latest CPU version

*Note on GPU Support: The CUDA and ROCm implementations are currently in a proof-of-concept stage. While functional for basic use cases, they have not been comprehensively tested across all scenarios. Users may need to customize Docker images with additional GPU support software for their specific computing environments. I recommend the CPU version which has been thoroughly tested and validated. The GPU implementations serve as a foundation for future development of more advanced functionality.

## Quick Start

### Prerequisites

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

## API Features

### Transcribe Audio/Video

- Request:

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/transcribe' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@file.mp3;type=audio/mpeg' \
      -F 'source_language=en_US' \
      -F 'transcription_parameters={"num_beams": 5}'
    ```

- Response:

    ```json
    {
      "transcription": "transcribed text"
    }
    ```

### Transcribe Audio/Video with Translation

- Request:

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/transcribe' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@file.mp3;type=audio/mpeg' \
      -F 'source_language=en_US' \
      -F 'target_language=pl_PL' \
      -F 'transcription_parameters={"num_beams": 5}' \
      -F 'translation_parameters={"num_beams": 5}'
    ```

- Response:

    ```json
    {
      "transcription": "transkrypcja tekstu"
    }
    ```

### Generate Subtitles

- Request:

    ```bash
    curl -X POST "http://localhost:8000/transcribe/srt" \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@file.mp3;type=audio/mpeg' \
      -F 'source_language=en_US' \
      -F 'transcription_parameters={"num_beams": 5}'
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
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@file.mp3;type=audio/mpeg' \
      -F 'source_language=en_US' \
      -F 'target_language=pl_PL' \
      -F 'transcription_parameters={"num_beams": 5}' \
      -F 'translation_parameters={"num_beams": 5}'
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

#### Generation parameters

The `translation_parameters` and `transcription_parameters` field in the request allows you to specify the parameters which are described in the model documentation.

[For Seamless model](https://huggingface.co/docs/transformers/main/en/model_doc/seamless_m4t#transformers.SeamlessM4TForTextToText.generate), [for mBART model](https://huggingface.co/docs/transformers/main/en/model_doc/mbart#transformers.MBartForConditionalGeneration.generate) and [for Whisper model](https://github.com/openai/whisper/blob/main/whisper/transcribe.py).

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

- Whisper: [whisper_mapping.json](https://github.com/ggwozdz90/speech-to-text-api/blob/main/src/assets/mappings/whisper_mapping.json)
- mBART: [mbart_mapping.json](https://github.com/ggwozdz90/speech-to-text-api/blob/main/src/assets/mappings/mbart_mapping.json)
- Seamless: [seamless_mapping.json](https://github.com/ggwozdz90/speech-to-text-api/blob/main/src/assets/mappings/seamless_mapping.json)

## Developer Guide

Developer guide is available in [docs/DEVELOPER.md](https://github.com/ggwozdz90/speech-to-text-api/blob/main/docs/DEVELOPER.md).
