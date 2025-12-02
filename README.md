# cat-facts-mcp

An MCP (Model Context Protocol) server that provides random cat facts from the [meowfacts API](https://meowfacts.herokuapp.com/).

## Features

- **get_cat_fact**: Fetches a random cat fact from the meowfacts API

## Installation

```bash
pip install -e .
```

## Usage

### With VSCode

1. Install the MCP extension for VSCode
2. Add the configuration from `.vscode-settings.example.json` to your VSCode settings (`.vscode/settings.json` or user settings)
3. Update the `cwd` path to point to your installation directory if needed
4. Restart VSCode or reload the MCP servers
5. You can now use the `get_cat_fact` tool from the MCP server

### Running the Server Manually

```bash
python -m cat_facts_mcp.server
```

The server communicates via stdio and expects MCP protocol messages.

## API

The server provides one tool:

- **get_cat_fact**: Takes no parameters and returns a random cat fact as text.

## Example Response

The meowfacts API returns data in the following format:
```json
{
  "data": ["Cats have individual preferences for scratching surfaces and angles. Some are horizontal scratchers while others exercise their claws vertically."]
}
```

The MCP server extracts the fact and returns it as plain text.

## Requirements

- Python 3.10+
- mcp >= 0.9.0
- httpx >= 0.27.0

## License

See LICENSE file for details.
