# {{{PROJECT-TITLE}}} - Developer Guide

## Features & Technical Highlights

### Core Capabilities

- **Template Project**: Provides a starting point for new FastAPI projects with a focus on code quality and maintainability

### Technical Architecture

- **Clean Architecture**: Project structure follows clean architecture principles, ensuring separation of concerns and maintainability
- **FastAPI Implementation**: Exposes RESTful API endpoints
- **Comprehensive Configuration**: Uses `.env` file for flexible environment configuration
- **Logging System**: Detailed operation logging for traceability and debugging
- **Conventional Commits**: Follows conventional commit messages for automated versioning and changelog generation

### Deployment Options

- **Docker Support**: Application runs in a Docker container for easy deployment
- **Windows Executable**: Provides a standalone Windows executable for local use

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

- **Container Development**:
  - Python 3.12
  - Poetry
  - Docker

### Environment setup

1. Clone the repository:

    ```bash
    git clone https://github.com/ggwozdz90/{{{PROJECT-NAME}}}
    cd {{{PROJECT-NAME}}}
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
    poetry install
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
    docker build -t {{{PROJECT-NAME}}}:latest .
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
┣ api/                   # API Layer
┃ ┣ dtos/                 # Data Transfer Objects
┃ ┣ handlers/             # Request Handlers
┃ ┣ middlewares/          # API Middlewares
┃ ┣ routers/              # Route Definitions
┃ ┗ server.py             # Server Configuration
┣ core/                  # Core Components
┃ ┣ config/               # Configuration Management
┃ ┗ logger/               # Logging Setup
┗ main.py                # Application Entry Point
```

## Table of Contents

- [{{{PROJECT-TITLE}}} - Developer Guide](#{{{PROJECT-NAME}}}---developer-guide)
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
