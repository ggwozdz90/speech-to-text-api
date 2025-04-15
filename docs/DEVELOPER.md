# Speech to Text API - Developer Guide

## Features & Technical Highlights

### Core Capabilities

- **Speech-to-Text Model Integration**: Utilizes OpenAI Whisper model for transcription
- **Translation Model Integration**: Translates detected text using translation models like Facebook/Meta's mBART and Seamless
- **Memory Optimization**: Models are loaded in separate processes and terminated after a configurable idle timeout to conserve RAM

### Technical Architecture

- **Clean Architecture**: Project structure follows clean architecture principles, ensuring separation of concerns and maintainability
- **FastAPI Implementation**: Exposes RESTful API endpoints for file uploads, text extraction, and subtitle generation
- **Comprehensive Configuration**: Uses `.env` file for flexible environment configuration
- **Logging System**: Detailed operation logging for traceability and debugging
- **Conventional Commits**: Follows conventional commit messages for automated versioning and changelog generation

### Deployment Options

- **Docker Support**: Application runs in a Docker container for easy deployment:
  - `cpu`: CPU-only version (fully tested and stable)
  - `cuda128`: NVIDIA CUDA 12.8 support for RTX 50XX GPU acceleration (tested and stable)
  - `cuda124`: NVIDIA CUDA 12.4 support for GPU acceleration (not tested)*
  - `rocm62`: AMD ROCm 6.2 support for GPU acceleration (proof-of-concept implementation, requires build from source code)*
- **Windows Executable**: Provides a standalone Windows executable for local use (CPU version, fully tested)

### Quality Assurance

- **Pre-commit Hooks**: Ensures code quality with automated checks:
  - Formatting: Black, isort, add-trailing-comma
  - Linting: Flake8, flake8-pyproject, flake8-clean-block, tryceratops, flake8-simplify, flake8-fastapi
  - Type checking: mypy
  - Security: Bandit, Vulture
  - General: Mixed line endings, trailing whitespace, end-of-file fixer, JSON/TOML/YAML validation
  - Spelling: Codespell
- **Test Coverage**: Maintains 90% code coverage requirement

### Copilot Customizations

- **Commit Message**: Custom guidelines and tools for generating standardized commit messages to ensure consistency and clarity. Used when `Generate Commit Message with Copilot` button is clicked.
- **Test**: Custom guidelines and tools for writing and running tests to improve code quality and development speed. Used when copilot command `/test` is invoked.

### Template Synchronization

- **Template Repository Sync**: This repository is configured to  synchronize with the template repository [ggwozdz90/fastapi-project-template](https://github.com/ggwozdz90/fastapi-project-template). This ensures that boilerplate code is unified and accelerates the start of new projects.

## Getting Started

### Prerequisites

Choose your development environment:

- **Source Code Development**:
  - Python 3.12
  - Poetry
  - ffmpeg

- **Container Development**:
  - Python 3.12
  - Poetry
  - Docker

Choose your hardware acceleration:

- **CPU Version** (Recommended):
  - Thoroughly tested and validated for stability

- **CUDA Version** (12.8-nightly and 12.4):
  - NVIDIA GPU with CUDA support
  - NVIDIA Container Toolkit
  - Note: May require additional configuration and GPU support software
  - Current implementation handles basic scenarios but needs further testing

- **ROCm Version** (Proof of concept):
  - AMD GPU with ROCm support
  - Note: May require additional configuration and GPU support software
  - Current implementation handles basic scenarios but needs further testing

### Environment setup

1. Clone the repository:

    ```bash
    git clone https://github.com/ggwozdz90/speech-to-text-api
    cd speech-to-text-api
    ```

2. Install poetry:

    ```bash
    pip install poetry==2.0.0
    ```

3. Create virtual environment:

    ```bash
    python -m venv .venv
    ```

4. Select the appropriate Python environment in VSCode:

    - Open the Command Palette (`Ctrl+Shift+P`)
    - Select `Python: Select Interpreter`
    - Choose the `.venv` environment

5. Install dependencies:

    ```bash
    # speech-to-text processing on CPU
    poetry install --extras cpu
  
    # speech-to-text processing on GPU  (NVIDIA CUDA 12.8-nightly)
    poetry install --extras cuda128

    # speech-to-text processing on GPU  (NVIDIA CUDA 12.4)
    poetry install --extras cuda124

    # speech-to-text processing on GPU (AMD ROCm 6.2)
    poetry install --extras rocm62
    ```

6. Start the application:

    - Local development with VSCode using `F5` key (using `.vscode/launch.json` configuration)

    - Container Development:

      ```bash
      docker-compose up
      ```

7. Access the API documentation:

   - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser

## Development Workflow

### Code Quality

- Run all pre-commit checks:

    ```bash
    poetry run pre-commit run --all-files
    ```

### Testing

1. Run tests with coverage:

    ```bash
    poetry run coverage run -m pytest
    poetry run coverage report --fail-under=90
    ```

2. Generate VSCode coverage report for Coverage Gutters VSCode extension:

    ```bash
    poetry run coverage xml
    ```

### Building

#### Windows Executable

- Create a standalone Windows executable using PyInstaller:

    ```bash
    poetry run pyinstaller scripts/pyinstaller.spec
    ```

#### Docker Images

- Build Docker images for CPU, CUDA and ROCm:

    ```bash
    # CPU Version (2.19 GB image size) - Recommended
    docker build --build-arg POETRY_INSTALL_ARGS="--extras=cpu" -t speech-to-text-api:cpu .

    # CUDA 12.8-Nightly Version (11.86 GB image size) - Nvidia GPU 50XX support
    docker build --build-arg POETRY_INSTALL_ARGS="--extras=cuda128" -t speech-to-text-api:cuda128 .

    # CUDA 12.4 Version (6.16 GB image size) - Not tested
    docker build --build-arg POETRY_INSTALL_ARGS="--extras=cuda124" -t speech-to-text-api:cuda124 .

    # ROCm Version (19.16 GB image size) - Proof of concept implementation
    # Note: May require additional GPU support software
    docker build --build-arg POETRY_INSTALL_ARGS="--extras=rocm62" -t speech-to-text-api:rocm .
    ```

## CI/CD Pipeline

### GitHub Actions Workflows

The project implements automated pipelines for:

- **Code Quality**: Runs pre-commit checks and tests on every push to any branch
- **Release**: Creates a new release with version bump and changelog generation (using Conventional Commits). This workflow is triggered manually and automatically invokes the Docker and Windows build workflows.
- **Docker Build**: Builds and pushes Docker images to Docker Hub
- **Windows Executable**: Builds and uploads Windows executable to GitHub Releases

## Project Structure

```plaintext
src/
├── api/                   # API Layer
│   ├── dtos/               # Data Transfer Objects
│   ├── handlers/           # Request Handlers
│   ├── middlewares/        # API Middlewares
│   ├── routers/            # Route Definitions
│   └── server.py           # Server Configuration
├── application/           # Application Layer
│   └── usecases/           # Business Logic Use Cases
├── assets/                # Static Resources
│   └── mappings/           # Language Mappings
├── core/                  # Core Components
│   ├── config/             # Configuration Management
│   ├── logger/             # Logging Setup
│   ├── timer/              # Timing Utilities
│   └── cuda/               # CUDA Utilities
├── data/                  # Data Layer
│   ├── factories/          # Object Factories
│   ├── repositories/       # Data Access
│   └── workers/            # Background Workers
├── domain/                # Domain Layer
│   ├── exceptions/         # Custom Exceptions
│   ├── models/             # Domain Models
│   ├── repositories/       # Repository Interfaces
│   └── services/           # Domain Services
└── main.py                # Application Entry Point
```

## Table of Contents

- [Speech to Text API - Developer Guide](#speech-to-text-api---developer-guide)
  - [Features \& Technical Highlights](#features--technical-highlights)
    - [Core Capabilities](#core-capabilities)
    - [Technical Architecture](#technical-architecture)
    - [Deployment Options](#deployment-options)
    - [Quality Assurance](#quality-assurance)
    - [Copilot Customizations](#copilot-customizations)
    - [Template Synchronization](#template-synchronization)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Environment setup](#environment-setup)
  - [Development Workflow](#development-workflow)
    - [Code Quality](#code-quality)
    - [Testing](#testing)
    - [Building](#building)
      - [Windows Executable](#windows-executable)
      - [Docker Images](#docker-images)
  - [CI/CD Pipeline](#cicd-pipeline)
    - [GitHub Actions Workflows](#github-actions-workflows)
  - [Project Structure](#project-structure)
  - [Table of Contents](#table-of-contents)
