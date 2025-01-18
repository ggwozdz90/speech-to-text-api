## 0.14.0 (2025-01-18)

### Feat

- add transcription and translation parameters to processing models

## 0.13.0 (2025-01-12)

### Feat

- initialize FastAPI application

### Refactor

- standardize logger naming and update build scripts

## 0.12.0 (2025-01-11)

### Feat

- add health check endpoint

## 0.11.0 (2025-01-11)

### Feat

- enhance SentenceModel with translation field and improve sentence processing

## 0.10.0 (2025-01-10)

### Feat

- update Dockerfile and GitHub Actions for improved deployment
- add ROCm 6.2 support in Docker workflow and dependencies
- add CudaChecker class for CUDA support verification

### Refactor

- update import paths for CudaChecker class
- update import path for CudaChecker class

## 0.9.0 (2025-01-08)

### Feat

- add support for CPU and CUDA 12.4 builds in Docker workflow

## 0.8.0 (2025-01-05)

### Feat

- add custom exception classes for error handling
- replace LanguageDTO with TranscribeDTO for language validation
- add log_level configuration to workers
- Introduced LOG_LEVEL environment variable for configurable logging levels
- enhance error handling and logging in application
- configure Uvicorn loggers for improved logging management
- implement global exception handler with structured error responses
- add logging to process time middleware

### Fix

- correct spelling errors in environment variable names

## 0.7.0 (2024-12-30)

### Feat

- add option to generate executable and include in GitHub release artifacts

## 0.6.0 (2024-12-28)

### Feat

- implement language mapping service for improved language handling
- update translation model and add seamless worker factory
- implement MBartWorker for translation processing
- implement whisper worker for asynchronous transcription

### Refactor

- rename and restructure translation and speech-to-text worker classes
- rename Whisper references to SpeechToText for consistency
- restructure WhisperWorker and introduce BaseWorker for improved extensibility

## 0.5.0 (2024-12-21)

### Feat

- add translation functionality

## 0.4.0 (2024-12-17)

### Feat

- add generate subtitles in srt format

## 0.3.0 (2024-12-17)

### Fix

- resolve internal server error for non-existent directories

## 0.2.0 (2024-12-16)

### Feat

- add speech-to-text API project using Whisper model

### Fix

- improve environment variable parsing in AppConfig
