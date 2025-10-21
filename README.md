# University of Sydney Colours MCP Server

A Model Context Protocol (MCP) server that provides programmatic access to the University of Sydney's official colour palettes for staff and students.

## Features

- **Official Brand Colours**: Access to USYD's official primary, secondary, and tertiary colour palettes
- **Extended Colours**: Complementary colours that work harmoniously with the official palette
- **Multiple Output Formats**: Get colours in HEX, RGB, and CSS formats
- **Smart Search**: Search colours by name or hex colour
- **CSS Generation**: Automatically generate CSS custom properties
- **Usage Guidelines**: Built-in branding and accessibility guidelines

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv

If you don't have `uv` installed:

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup the Server

1. **Clone or download this repository**:
```bash
mkdir -p ~/Documents/projects/usyd-colours-mcp
cd ~/Documents/projects/usyd-colours-mcp
```

2. **Create the project files**:

Save `usyd-colours.py` (the server code) to this directory.

3. **Create `pyproject.toml`**:
```toml
[project]
name = "usyd-colours-mcp"
version = "1.0.0"
description = "MCP server for University of Sydney official colours"
dependencies = [
    "mcp>=0.9.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

4. **Install dependencies**:
```bash
uv sync
```

## Configuration

### Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "usyd-colours": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/Documents/projects/usyd-colours-mcp",
        "run",
        "usyd-colours.py"
      ]
    }
  }
}
```

**Important**: Replace `YOUR_USERNAME` with your actual username!

To find your `uv` path:
```bash
which uv
```

### Other MCP Clients

The server uses stdio transport and can be used with any MCP-compatible client. Configure according to your client's documentation.

## Usage

Once configured, you can interact with the server through your MCP client (like Claude Desktop). Here are some example queries:

### Search for Colours

```
"What's the hex code for USYD ochre?"
"Show me the Heritage Rose colour"
"Find colours matching '#E74726'"
```

### Get Colour Palettes

```
"Show me the official USYD primary colours"
"What are the tertiary/heritage colours?"
"Give me all the official brand colours"
"What extended warm colours are available?"
```

### Generate CSS

```
"Generate CSS variables for the official USYD colours"
"Create CSS custom properties including extended colours"
```

### Get Guidelines

```
"Show me the colour usage guidelines"
"How should I use USYD colours in my design?"
```

## Available Tools

The server provides these tools:

- **get_colour**: Search for specific colours by name or hex code
- **get_official_colours**: Get all official USYD brand colours
- **get_extended_colours**: Get complementary/extended colours
- **get_palette**: Get specific palette types (primary, secondary, tertiary, etc.)
- **list_all_colours**: List all available colours
- **generate_css**: Generate CSS custom properties

## Colour Categories

### Official Colours

**Primary Colours** (from official style guide):
- Ochre (#E74726) - The signature USYD colour
- White (#FFFFFF)
- Black (#000000)
- Light Grey (#E6E7E9)
- Charcoal (#424143)

**Secondary Colour**:
- Sandstone (#FBEEE2)

**Tertiary/Heritage Colours**:
- Heritage Rose (#DAA8A2)
- Jacaranda (#8F9EC8)
- Navy (#1B355E)
- Eucalypt (#71A499)

### Extended Colours

Complementary colours organized into:
- **Neutrals**: Additional grey tones
- **Warm**: Oranges, peaches, earth tones
- **Cool**: Blues, teals, greens
- **Vibrant**: Bright accent colours

## Development

### Project Structure

```
usyd-colours-mcp/
├── usyd-colours.py      # Main server code
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

### Testing

You can test the server directly:

```bash
cd ~/Documents/projects/usyd-colours-mcp
uv run usyd-colours.py
```

The server should start and wait for MCP protocol messages on stdin.

### Debugging

If the server isn't working:

1. **Check the logs** in Claude Desktop (Help > View Logs)
2. **Verify uv path**:
   ```bash
   which uv
   ```
3. **Test Python script directly**:
   ```bash
   python3 usyd-colours.py
   ```
4. **Check dependencies**:
   ```bash
   uv sync
   ```

## Resources

- [Official USYD Brand Guidelines](https://intranet.sydney.edu.au/services/marketing-communications/our-brand.html) - Contact Marketing & Communications
- [usydColours R Package](https://github.com/Sydney-Informatics-Hub/usydColours) - R implementation
- [MCP Documentation](https://modelcontextprotocol.io/docs)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## License

This server is provided for use by University of Sydney staff and students. The colour specifications are property of the University of Sydney.

## Contributing

For issues or improvements, please contact the Sydney Informatics Hub or create an issue in the repository.

## Acknowledgments

- Sydney Informatics Hub for the original R package
- University of Sydney Marketing & Communications for the official colour specifications
- Anthropic for the Model Context Protocol

---

**Maintained by**: ICT 
**Last Updated**: 21 October 2025

