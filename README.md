# 👁️ DFIR-Iris MCP Server

**Connect your AI agents to [DFIR Iris](https://dfir-iris.org/) for automated incident response.**

This Model Context Protocol (MCP) server enables LLMs to managing cases, tracks evidence, and record timeline events directly within your DFIR workflow.

## 🚀 Quick Start

The easiest way to run this server is with [uv](https://github.com/astral-sh/uv).

### 1. Zero-Setup Run
If you have the repository cloned, you can run the server directly without manual virtualenv creation. The script handles its own dependencies!

```bash
# Make sure you have the repository cloned
git clone https://github.com/srozb/iris-mcp.git
cd iris-mcp

# Run directly (stdio mode)
./iris_mcp.py

# Run in HTTP mode (for Gemini/debug)
./iris_mcp.py --http
```

*Note: Requires `uv` to be installed.*

### 2. Configure Credentials
The server needs access to your DFIR Iris instance. Set these environment variables:

- `IRIS_API_KEY`: Your API key.
- `IRIS_HOST`: URL of your instance (e.g., `https://iris.example.com`).
- `IRIS_VERIFY_SSL`: `true` or `false` (default: `true`).

You can also create a `.env` file in the root directory:
```bash
IRIS_API_KEY=your_key
IRIS_HOST=https://iris.example.com
```

### 3. Gemini (HTTP Mode)
To run the server in HTTP mode (listening on port 9000):

```bash
uv run iris-mcp --http
```

Then add it to Gemini:
```bash
gemini mcp add iris http://127.0.0.1:9000/mcp
```

## 🔌 Connect to Claude Desktop

The server uses Standard Input/Output (stdio) by default, which is what Claude Desktop expects.

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dfir-iris": {
      "command": "uv",
      "args": [
        "run",
        "--with", "dfir-iris-client>=2.0.4",
        "--with", "fastmcp>=2.13.2",
        "https://raw.githubusercontent.com/srozb/iris-mcp/master/iris_mcp.py"
      ],
      "env": {
        "IRIS_API_KEY": "your_api_key",
        "IRIS_HOST": "https://your-iris-instance.com"
      }
    }
  }
}
```
*Tip: You can point `args` to a local path if you prefer running from source.*

## ✨ Features

- **Case Management**: Create, list, search, and update cases.
- **Evidence & IOCs**: Add malicious IPs, domains, and file artifacts.
- **Notes & Timeline**: Maintain a chronological record of the investigation.
- **Tasks**: manage analyst tasks.

## 🛠️ Development

This project uses `uv` for all lifecycle management.

```bash
# Run tests
uv run pytest

# Lint & Format
uv run ruff check .
uv run mypy .
```

## License

[MIT](LICENSE)
