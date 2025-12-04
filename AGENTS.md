# DFIR Iris MCP Server Agent

## Overview
This agent is designed to act as a bridge between an AI assistant and a DFIR Iris instance. It allows the AI to perform actions within DFIR Iris, such as managing cases, creating alerts, and retrieving information, to assist DFIR analysts.

## Configuration
The agent is configured using environment variables:
- `IRIS_API_KEY`: The API key for authentication with the DFIR Iris instance.
- `IRIS_HOST`: The URL of the DFIR Iris instance (e.g., `https://iris.example.com`).
- `IRIS_VERIFY_SSL`: (Optional) Whether to verify SSL certificates (default: `true`).

## Dependencies
- `fastmcp`: For building the MCP server with minimal boilerplate.
- `dfir-iris-client`: The official Python client for DFIR Iris.
- `uv`: For project management and dependency resolution.

## Capabilities
The agent will support the following capabilities (extensible):
- **Case Management**: List, create, and update cases.
- **Alert Management**: Create and manage alerts.
- **Search**: Perform global searches within DFIR Iris.
- **Notes**: Add notes to cases.

The project is a modern Python application managed by `uv`.
It uses `fastmcp` to define tools and resources.

## Critical Development Notes

### Environment & Live Testing
- The `.env` file is populated with working values for a live DFIR Iris instance.
- **Agents MUST use these values** to interact with the running instance.
- Real data interaction is required to create proper `pytest` cases and evaluate the project.
- **Test Case**: Use **Case ID 16** for all testing purposes. Data in this case (notes, evidence, etc.) may be freely modified, created, or deleted.

### Documentation & References
- **`docs/index.md`**: This is the **primary resource** for understanding the client library. Read this first.
- **`vendor/iris-client`**: Contains the source code of the `dfir-iris-client` library. Use `ripgrep` or other tools to study the library's implementation and underlying structures when documentation is insufficient.

### Code Quality & Tooling
- The project enforces strict code quality standards using `ruff`, `mypy`, and `pytest`.
- Pre-commit hooks are configured to ensure all checks pass before committing.
- Ensure you run the full suite of tests and linters before submitting changes.
