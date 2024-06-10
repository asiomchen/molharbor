# Contributing to Molharbor

Thank you for considering contributing to Molharbor! This guide outlines the process for contributing to the project, including setting up the development environment and running tests.

## Getting Started

To get started with contributing to Molharbor, follow these steps:

1. Fork the Molharbor repository on GitHub.
2. Clone your forked repository to your local machine:

```bash
 git clone https://github.com/asiomchen/molharbor.git
```
3. Navigate to the project directory:

4. Install dependencies using Poetry:

```bash
poetry install
```



## Making Changes

Once you have the project set up, you can make changes to the code. Here are some guidelines to follow:

- **Branching**: Create a new branch for each feature or bug fix. Name your branch descriptively, such as `feature/new-feature` or `bugfix/issue-123`.
- **Coding Style**: Follow PEP 8 guidelines for Python code. Make sure your code is well-formatted and documented.
- **Commits**: Make small, focused commits with clear messages. Use imperative language (e.g., "Add feature" rather than "Added feature").

## Testing

Molharbor uses pytest for testing. Before submitting your changes, make sure all tests pass. To run tests, execute the following command:
    
```bash
poetry run pytest
```

## Formatting and Linting

Molharbor uses ruff for formatting and linting. Also it highly recommended to use pre-commit hooks to ensure that your code is formatted correctly and passes linting checks before committing. To install pre-commit hooks, run the following command:

```bash
pre-commit install
```

## Submitting Changes

Once you have made your changes and ensured that all tests pass, you can submit a pull request to the main Molharbor repository. Make sure to include a detailed description of your changes and any relevant information for reviewers.


