# Contributing to iris-mcp

Thank you for your interest in contributing! We welcome bug reports, feature requests, and code contributions.

## Development Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/iris-mcp.git
    cd iris-mcp
    ```

2.  **Install `uv`**:
    We use [uv](https://github.com/astral-sh/uv) for dependency management.
    ```bash
    # On macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Install dependencies**:
    ```bash
    uv sync
    ```

## Running Tests

We use `pytest` for testing.

```bash
uv run pytest
```

To run with coverage:

```bash
uv run pytest --cov=iris_mcp
```

## Code Quality

Please ensure your code passes linting and type checking before submitting a PR.

```bash
# Linting
uv run ruff check .

# Type checking
uv run mypy .
```

## Submitting Pull Requests

1.  Fork the repository.
2.  Create a new branch for your feature or fix.
3.  Implement your changes with tests.
4.  Ensure all checks pass (`pytest`, `ruff`, `mypy`).
5.  Submit a Pull Request with a clear description of your changes.
