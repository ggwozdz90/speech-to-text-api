# Speech to Text API

This project provides an API for transcribing text from uploaded audio/video files using the OpenAI Whisper model. Additionally, it offers text translation using Facebook/Meta's mBART and Seamless models. A key aspect of this project is memory optimization; models are loaded in separate processes and terminated after a configurable idle timeout to conserve RAM. The application can also be run in a Docker container.

## Docker Image Tags

The Docker images for this project are built and tagged with specific identifiers to indicate the type of dependencies included. Below are the types of images and their corresponding tags:

- **CUDA 12.4 Dependencies**: These images include dependencies for CUDA 12.4, allowing the application to leverage GPU acceleration for improved performance. The tag format is `version-cuda124`.
- **CPU Dependencies**: These images include dependencies for CPU execution, suitable for environments without GPU support. The tag format is `version-cpu`.

The `latest` tag always points to the most recent CUDA version image.

## Getting Started

You have four options for running the project:

- **Using Docker-Compose**:

  ```yaml
  services:
    api:
      image: ggwozdz/speech-to-text-api
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
        - ./volume/uploaded_files:/app/uploaded_files
  ```

- **Using Docker**:

  ```sh
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
      ggwozdz/speech-to-text-api
  ```

## Usage

Once the Docker container is running, you can access the FastAPI documentation at `http://localhost:8000/docs`.

### Transcribe Audio to Text

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

### Generate Subtitles in SRT Format

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

## Source Code

The source code for this project can be found at [GitHub](https://github.com/ggwozdz90/speech-to-text-api)
