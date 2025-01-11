# Commit Message Guidelines

Follow the Conventional Commits specification for your commit messages. This helps in automatically generating changelogs using tools like Commitizen.

## Commit Message Structure

Each commit message should consist of a header and an optional body. The header has a specific format that includes a type and a subject:

```text
<type>: <subject>
<BLANK LINE>
<body>
```

### Header

The header is mandatory and must conform to the following format:

- **type**: Describes the kind of change that this commit is introducing.
- **subject**: A brief description of the change.

### Body

The body is optional and should provide additional context or details about the change. It should be concise, focus on explaining the "why" behind the change, and be kept short.

### Types

- **feat**: A new feature.
- **fix**: A bug fix.
- **docs**: Documentation only changes.
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- **refactor**: A code change that neither fixes a bug nor adds a feature.
- **perf**: A code change that improves performance.
- **test**: Adding missing tests or correcting existing tests.
- **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm).
- **ci**: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs).
- **chore**: Other changes that don't modify src or test files.
- **revert**: Reverts a previous commit.

### Example

```text
docs: add commit message guidelines for the repository

- Established a standardized format for commit messages to enhance clarity and consistency.
- Included a link to the Docker Hub repository in README.md file.
```

### Reason of change
