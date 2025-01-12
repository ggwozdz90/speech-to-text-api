# FastAPI Project Template Setup

This document describes how to clone the repository and start working on a new project that is pre-configured for code quality, clean architecture, Copilot automatizations, conventional commits, and GitHub workflows. It also explains how to merge changes from this template into an existing repository.

## Cloning the Repository

1. Clone the repository using the following command:

    ```bash
    git clone https://github.com/your-username/fastapi-project-template.git
    cd fastapi-project-template
    ```

2. Create a new repository on GitHub for your project.

3. Change the remote URL to point to your new repository:

    ```bash
    git remote set-url origin https://github.com/your-username/your-new-repo.git
    ```

## Initial Setup on the New Repository

1. Search and replace the following strings in all files downloaded from the repository:
    - `{{{PROJECT-NAME}}}` -> e.g. "speech-to-text-api" (use hyphens to separate words, e.g., "my-new-project")
    - `{{{PROJECT-DESCRIPTION}}}` -> e.g. "A FastAPI project integrating speech to text and translation services."
    - `{{{PROJECT-TITLE}}}` -> e.g. "Speech to text API" (same as `{{{PROJECT-NAME}}}` but with spaces instead of hyphens)
    - If you cloned the repository from a user other than the author `ggwozdz90`, replace all occurrences of `ggwozdz90` with your GitHub and DockerHub username.

2. Optionally, you can remove the TEMPLATE_SETUP.md file:

    ```bash
    rm docs/TEMPLATE_SETUP.md
    ```

3. Enable push trigger in the `.github/workflows/checks.yml` file by uncommenting the following lines:

    ```yaml
    on:
    #  push: <-- Uncomment this line>
      workflow_dispatch:
    ```

4. Push the initial commit to your new repository:

    ```bash
    git add .
    git commit -m "feat: Initial version from template"
    git push origin develop
    ```

## Initial Setup on the Existing Repository

1. Add the template repository as a remote:

    ```bash
    git remote add template https://github.com/ggwozdz90/fastapi-project-template
    ```

2. Fetch the template repository:

    ```bash
    git fetch template
    ```

3. Create a new branch from before merging the template repository:

    ```bash
    git checkout -b chore/template_sync
    ```

4. Merge the template repository into the new branch:

    ```bash
    git merge template/develop --allow-unrelated-histories
    ```

5. Resolve any conflicts that may arise during the merge.
6. Push the new branch to the remote repository:

    ```bash
    git push origin chore/template_sync
    ```

7. Create a pull request to merge the `chore/template_sync` branch into the `develop` branch.

## GitHub Configuration

1. In your GitHub repository, navigate to `Settings` -> `Secrets and variables` -> `Actions` and add the following variables:
    - `DOCKERHUB_USERNAME` - variable - your DockerHub username
    - `DOCKERHUB_TOKEN` - secret - DockerHub PAT with read, write, delete permissions required to update image overview automatically
    - `REPOSITORY_TOKEN` - secret - GitHub token with access to commit changes

2. Grant workflow permissions:
    - Go to `Settings` -> `Actions` -> `General`
    - Under `Workflow permissions`, select `Read and write permissions`

## Development

You are now ready to start developing your new project based on this template. Any changes made to this template will be reflected in other implementations of your projects.
