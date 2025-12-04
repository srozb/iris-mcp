# DFIR-Iris MCP Server

A Model Context Protocol (MCP) server that enables AI agents to interact with [DFIR Iris](https://dfir-iris.org/), a collaborative incident response platform.

This server allows LLMs to assist analysts by:
- Managing cases (create, read, update)
- Recording evidence, IOCs, and notes
- Tracking timeline events
- Managing alerts

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Access to a running DFIR Iris instance

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd iris-mcp
    ```

2.  **Install dependencies**:
    Using `uv`:
    ```bash
    uv sync
    ```
    Or using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the project root with your DFIR Iris credentials:

```bash
IRIS_API_KEY=your_api_key_here
IRIS_HOST=https://your-iris-instance.com
IRIS_VERIFY_SSL=true  # Set to false for self-signed certs
```

## Usage

### Running the Server

You can run the MCP server using `uv`:

```bash
uv run iris-mcp
```

Or directly with Python if installed in your environment:

```bash
python iris_mcp.py
```

### Connecting an Agent

Configure your MCP client (e.g., Claude Desktop, an IDE extension, or a custom agent) to use this server.

**Example Claude Desktop Config (`claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "dfir-iris": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/iris-mcp",
        "run",
        "iris-mcp"
      ],
      "env": {
        "IRIS_API_KEY": "your_api_key",
        "IRIS_HOST": "https://your-iris-instance.com"
      }
    }
  }
}
```

## Development

### Running Tests

```bash
uv run pytest
```

### Code Quality

Run linting and type checking:

```bash
uv run ruff check .
uv run mypy .
```

## License

[MIT](LICENSE)
