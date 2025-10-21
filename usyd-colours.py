#!/usr/bin/env python3

"""
University of Sydney Official Colors MCP Server
Provides access to official USYD color palettes for staff and students
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# University of Sydney Official Colors Database
USYD_COLORS = {
    # Official Primary/Masterbrand Colors (from style guide)
    "official_primary": {
        "ochre": {"name": "Ochre", "rgb": [231, 71, 38], "hex": "#E74726", "official": True},
        "white": {"name": "White", "rgb": [255, 255, 255], "hex": "#FFFFFF", "official": True},
        "black": {"name": "Black", "rgb": [0, 0, 0], "hex": "#000000", "official": True},
        "lightGrey": {"name": "Light Grey", "rgb": [230, 231, 233], "hex": "#E6E7E9", "official": True},
        "charcoal": {"name": "Charcoal", "rgb": [66, 65, 67], "hex": "#424143", "official": True},
    },
    
    # Official Secondary Color (from style guide)
    "official_secondary": {
        "sandstone": {"name": "Sandstone", "rgb": [251, 238, 226], "hex": "#FBEEE2", "official": True},
    },
    
    # Official Tertiary/Heritage Colors (from style guide)
    "official_tertiary": {
        "heritageRose": {"name": "Heritage Rose", "rgb": [218, 168, 162], "hex": "#DAA8A2", "official": True},
        "jacaranda": {"name": "Jacaranda", "rgb": [143, 158, 200], "hex": "#8F9EC8", "official": True},
        "navy": {"name": "Navy", "rgb": [27, 53, 94], "hex": "#1B355E", "official": True},
        "eucalypt": {"name": "Eucalypt", "rgb": [113, 164, 153], "hex": "#71A499", "official": True},
    },
    
    # Extended/Complementary Colors (additional colors that complement the official palette)
    "extended_neutrals": {
        "accentGrey": {"name": "Accent Grey", "rgb": [241, 241, 241], "hex": "#F1F1F1", "official": False},
        "neutralGrey": {"name": "Neutral Grey", "rgb": [224, 224, 224], "hex": "#E0E0E0", "official": False},
        "masterbrandCharcoal": {"name": "Masterbrand Charcoal", "rgb": [66, 66, 66], "hex": "#424242", "official": False},
    },
    
    "extended_warm": {
        "lightOchre": {"name": "Light Ochre", "rgb": [255, 173, 140], "hex": "#FFAD8C", "official": False},
        "updatedOchre": {"name": "Updated Ochre", "rgb": [231, 71, 38], "hex": "#E74726", "official": False},
        "beige": {"name": "Beige", "rgb": [253, 202, 144], "hex": "#FDCA90", "official": False},
        "ivory": {"name": "Ivory", "rgb": [248, 239, 221], "hex": "#F8EFDD", "official": False},
        "peach": {"name": "Peach", "rgb": [247, 156, 114], "hex": "#F79C72", "official": False},
        "orange": {"name": "Orange", "rgb": [249, 161, 52], "hex": "#F9A134", "official": False},
        "maroon": {"name": "Maroon", "rgb": [122, 32, 0], "hex": "#7A2000", "official": False},
    },
    
    "extended_cool": {
        "accentBlue": {"name": "Accent Blue", "rgb": [1, 72, 164], "hex": "#0148A4", "official": False},
        "lightBlue": {"name": "Light Blue", "rgb": [145, 189, 229], "hex": "#91BDE5", "official": False},
        "secondaryBlue": {"name": "Secondary Blue", "rgb": [78, 152, 211], "hex": "#4E98D3", "official": False},
        "darkEucalypt": {"name": "Dark Eucalypt", "rgb": [37, 88, 77], "hex": "#25584D", "official": False},
        "lightSeafoam": {"name": "Light Seafoam", "rgb": [104, 198, 182], "hex": "#68C6B6", "official": False},
        "darkSeafoam": {"name": "Dark Seafoam", "rgb": [0, 164, 133], "hex": "#00A485", "official": False},
    },
    
    "extended_vibrant": {
        "accentYellow": {"name": "Accent Yellow", "rgb": [255, 184, 0], "hex": "#FFB800", "official": False},
        "lemon": {"name": "Lemon", "rgb": [251, 243, 141], "hex": "#FBF38D", "official": False},
        "lightGreen": {"name": "Light Green", "rgb": [189, 220, 150], "hex": "#BDDC96", "official": False},
        "darkGreen": {"name": "Dark Green", "rgb": [0, 126, 59], "hex": "#007E3B", "official": False},
        "lilac": {"name": "Lilac", "rgb": [184, 150, 198], "hex": "#B896C6", "official": False},
        "purple": {"name": "Purple", "rgb": [127, 63, 152], "hex": "#7F3F98", "official": False},
        "lightPink": {"name": "Light Pink", "rgb": [248, 185, 204], "hex": "#F8B9CC", "official": False},
        "pink": {"name": "Pink", "rgb": [214, 81, 157], "hex": "#D6519D", "official": False},
    },
}


def format_color_info(color_data: Dict[str, Any], category: str, key: str) -> Dict[str, Any]:
    """Format color information for output."""
    return {
        "name": color_data["name"],
        "category": category,
        "key": key,
        "hex": color_data["hex"],
        "rgb": {
            "r": color_data["rgb"][0],
            "g": color_data["rgb"][1],
            "b": color_data["rgb"][2],
            "string": f"rgb({', '.join(map(str, color_data['rgb']))})",
        },
        "css": {
            "hex": color_data["hex"],
            "rgb": f"rgb({', '.join(map(str, color_data['rgb']))})",
        },
        "official": color_data["official"],
    }


def get_colors_by_category(category: str) -> Optional[List[Dict[str, Any]]]:
    """Get all colors in a category."""
    category_data = USYD_COLORS.get(category)
    if not category_data:
        return None
    
    return [
        format_color_info(color, category, key)
        for key, color in category_data.items()
    ]


def get_official_colors() -> Dict[str, List[Dict[str, Any]]]:
    """Get only official colors."""
    return {
        "primary": get_colors_by_category("official_primary"),
        "secondary": get_colors_by_category("official_secondary"),
        "tertiary": get_colors_by_category("official_tertiary"),
    }


def get_extended_colors() -> Dict[str, List[Dict[str, Any]]]:
    """Get all extended colors."""
    return {
        "neutrals": get_colors_by_category("extended_neutrals"),
        "warm": get_colors_by_category("extended_warm"),
        "cool": get_colors_by_category("extended_cool"),
        "vibrant": get_colors_by_category("extended_vibrant"),
    }


def search_color(query: str, official_only: bool = False) -> List[Dict[str, Any]]:
    """Search for a color by name or hex code."""
    results = []
    lower_query = query.lower()
    
    for category, colors in USYD_COLORS.items():
        for key, color in colors.items():
            if official_only and not color["official"]:
                continue
            
            if (
                lower_query in color["name"].lower()
                or lower_query in key.lower()
                or lower_query in color["hex"].lower()
            ):
                results.append(format_color_info(color, category, key))
    
    return results


def generate_palette(palette_type: str) -> Optional[List[Dict[str, Any]]]:
    """Generate color palette by type."""
    palette_type = palette_type.lower()
    
    if palette_type in ["official", "primary"]:
        return get_colors_by_category("official_primary")
    elif palette_type == "secondary":
        return get_colors_by_category("official_secondary")
    elif palette_type in ["tertiary", "heritage"]:
        return get_colors_by_category("official_tertiary")
    elif palette_type == "official_all":
        return (
            get_colors_by_category("official_primary")
            + get_colors_by_category("official_secondary")
            + get_colors_by_category("official_tertiary")
        )
    elif palette_type == "extended":
        return (
            get_colors_by_category("extended_neutrals")
            + get_colors_by_category("extended_warm")
            + get_colors_by_category("extended_cool")
            + get_colors_by_category("extended_vibrant")
        )
    
    return None


def generate_css(include_extended: bool = False) -> str:
    """Generate CSS custom properties for USYD colors."""
    css_vars = ":root {\n  /* University of Sydney Official Colors */\n"
    
    def add_colors_to_css(colors: List[Dict[str, Any]], prefix: str, is_official: bool = False):
        nonlocal css_vars
        label = "Official" if is_official else "Extended"
        css_vars += f"\n  /* {prefix.capitalize()} Colors ({label}) */\n"
        
        for color in colors:
            var_name = f"--usyd-{prefix}-{color['key']}"
            css_vars += f"  {var_name}: {color['hex']};\n"
            css_vars += f"  {var_name}-rgb: {color['rgb']['r']}, {color['rgb']['g']}, {color['rgb']['b']};\n"
    
    # Always include official colors
    add_colors_to_css(get_colors_by_category("official_primary"), "primary", True)
    add_colors_to_css(get_colors_by_category("official_secondary"), "secondary", True)
    add_colors_to_css(get_colors_by_category("official_tertiary"), "tertiary", True)
    
    # Optionally include extended colors
    if include_extended:
        add_colors_to_css(get_colors_by_category("extended_neutrals"), "neutral", False)
        add_colors_to_css(get_colors_by_category("extended_warm"), "warm", False)
        add_colors_to_css(get_colors_by_category("extended_cool"), "cool", False)
        add_colors_to_css(get_colors_by_category("extended_vibrant"), "vibrant", False)
    
    css_vars += "}\n"
    return css_vars


def get_branding_guidelines() -> str:
    """Get color usage guidelines."""
    return """# University of Sydney Color Usage Guidelines

## Official Brand Colors

### Primary Colors (Official)
The primary colors are the foundation of the USYD brand identity and should be used prominently:
- **Ochre (#E74726)**: The signature USYD color, use prominently in all branding materials
- **White (#FFFFFF)**: Clean, professional backgrounds
- **Black (#000000)**: Text and strong contrast elements
- **Light Grey (#E6E7E9)**: Subtle backgrounds and dividers
- **Charcoal (#424143)**: Secondary text and UI elements

### Secondary Color (Official)
- **Sandstone (#FBEEE2)**: Warm, accessible secondary background color

### Tertiary/Heritage Colors (Official)
Colors that evoke the university's heritage and campus environment:
- **Heritage Rose (#DAA8A2)**: Warm, historic tone
- **Jacaranda (#8F9EC8)**: Inspired by campus jacaranda trees
- **Navy (#1B355E)**: Deep, authoritative blue
- **Eucalypt (#71A499)**: Natural, calming green-blue

## Extended/Complementary Colors

The extended palette provides additional colors that complement the official brand colors. These are organized into:
- **Neutrals**: Additional grey tones for subtle variations
- **Warm tones**: Oranges, peaches, and earth tones that pair with Ochre
- **Cool tones**: Blues, teals, and greens for variety
- **Vibrant accents**: Bright colors for highlights and special applications

## Best Practices

1. **Always prioritize official colors**: Use the official primary, secondary, and tertiary colors as your foundation
2. **Use extended colors sparingly**: Extended colors should complement, not dominate your design
3. **Ochre is paramount**: Always feature Ochre prominently as the primary brand identifier
4. **Ensure accessibility**: Maintain WCAG AA contrast ratios (minimum 4.5:1 for text)
5. **Test across media**: Colors may appear differently in print vs digital - always test
6. **Consistency is key**: Use the same color codes across all university materials
7. **Official colors for official materials**: Use only official colors for formal university communications

## Usage Examples

- **Marketing materials**: Primary colors + 1-2 tertiary colors
- **Web design**: Primary colors with extended neutrals for UI elements
- **Reports & documents**: Official colors only for formal consistency
- **Presentations**: Mix of official and extended colors for visual interest
- **Social media**: More flexibility with extended palette while keeping Ochre prominent

## Resources
- R Package with color palettes: https://github.com/Sydney-Informatics-Hub/usydColours
- Official Brand Guidelines: Contact Marketing & Communications
- This MCP server provides programmatic access to all color specifications
"""


# Create the server instance
app = Server("usyd-colors")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_color",
            description="Get detailed information about a specific USYD color by name or hex code",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Color name (e.g., 'ochre', 'sandstone') or hex code (e.g., '#E74726')",
                    },
                    "official_only": {
                        "type": "boolean",
                        "description": "If true, only search within official brand colors",
                        "default": False,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_official_colors",
            description="Get all official USYD brand colors (primary, secondary, and tertiary palettes from style guide)",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_extended_colors",
            description="Get extended/complementary colors that work with the official USYD palette",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Optional: specific extended category (neutrals, warm, cool, vibrant)",
                        "enum": ["neutrals", "warm", "cool", "vibrant"],
                    },
                },
            },
        ),
        Tool(
            name="get_palette",
            description="Get a specific color palette",
            inputSchema={
                "type": "object",
                "properties": {
                    "palette_type": {
                        "type": "string",
                        "description": "Type of palette: 'official' (primary colors), 'secondary', 'tertiary', 'official_all' (all official colors), or 'extended' (complementary colors)",
                        "enum": ["official", "primary", "secondary", "tertiary", "heritage", "official_all", "extended"],
                    },
                },
                "required": ["palette_type"],
            },
        ),
        Tool(
            name="list_all_colors",
            description="List all available colors (both official and extended) organized by category",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="generate_css",
            description="Generate CSS custom properties (variables) for USYD colors",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_extended": {
                        "type": "boolean",
                        "description": "Whether to include extended/complementary colors in addition to official colors",
                        "default": False,
                    },
                },
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls."""
    
    if name == "get_color":
        query = arguments.get("query")
        official_only = arguments.get("official_only", False)
        results = search_color(query, official_only)
        
        if not results:
            text = f"No colors found matching \"{query}\""
            if official_only:
                text += " in official colors"
            text += ". Try searching by name (e.g., 'ochre', 'sandstone') or hex code."
            return [TextContent(type="text", text=text)]
        
        return [TextContent(type="text", text=json.dumps(results, indent=2))]
    
    elif name == "get_official_colors":
        official_colors = get_official_colors()
        return [TextContent(type="text", text=json.dumps(official_colors, indent=2))]
    
    elif name == "get_extended_colors":
        category = arguments.get("category")
        
        if category:
            category_key = f"extended_{category}"
            colors = get_colors_by_category(category_key)
            
            if not colors:
                return [TextContent(
                    type="text",
                    text=f"Invalid category \"{category}\". Available categories: neutrals, warm, cool, vibrant"
                )]
            
            return [TextContent(type="text", text=json.dumps({"category": category, "colors": colors}, indent=2))]
        
        extended_colors = get_extended_colors()
        return [TextContent(type="text", text=json.dumps(extended_colors, indent=2))]
    
    elif name == "get_palette":
        palette_type = arguments.get("palette_type")
        palette = generate_palette(palette_type)
        
        if not palette:
            return [TextContent(
                type="text",
                text=f"Invalid palette type \"{palette_type}\". Available types: official, primary, secondary, tertiary, official_all, extended"
            )]
        
        return [TextContent(type="text", text=json.dumps({"palette": palette_type, "colors": palette}, indent=2))]
    
    elif name == "list_all_colors":
        all_colors = {
            "official": get_official_colors(),
            "extended": get_extended_colors(),
        }
        return [TextContent(type="text", text=json.dumps(all_colors, indent=2))]
    
    elif name == "generate_css":
        include_extended = arguments.get("include_extended", False)
        css = generate_css(include_extended)
        return [TextContent(type="text", text=css)]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="usyd://colors/official",
            name="Official USYD Brand Colors",
            mimeType="application/json",
            description="Official University of Sydney brand colors from the style guide (Primary, Secondary, Tertiary)",
        ),
        Resource(
            uri="usyd://colors/extended",
            name="Extended/Complementary Colors",
            mimeType="application/json",
            description="Extended color palette that complements the official USYD colors",
        ),
        Resource(
            uri="usyd://colors/all",
            name="All USYD Colors",
            mimeType="application/json",
            description="Complete database including both official and extended colors",
        ),
        Resource(
            uri="usyd://colors/primary",
            name="Primary Color Palette (Official)",
            mimeType="application/json",
            description="Official USYD primary colors: Ochre, White, Black, Light Grey, Charcoal",
        ),
        Resource(
            uri="usyd://colors/secondary",
            name="Secondary Color (Official)",
            mimeType="application/json",
            description="Official secondary color: Sandstone",
        ),
        Resource(
            uri="usyd://colors/tertiary",
            name="Tertiary/Heritage Colors (Official)",
            mimeType="application/json",
            description="Official heritage colors: Heritage Rose, Jacaranda, Navy, Eucalypt",
        ),
        Resource(
            uri="usyd://branding/guidelines",
            name="Color Usage Guidelines",
            mimeType="text/markdown",
            description="Best practices for using USYD colors in branding",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content."""
    
    if uri == "usyd://colors/official":
        return json.dumps(get_official_colors(), indent=2)
    
    elif uri == "usyd://colors/extended":
        return json.dumps(get_extended_colors(), indent=2)
    
    elif uri == "usyd://colors/all":
        all_colors = {
            "official": get_official_colors(),
            "extended": get_extended_colors(),
        }
        return json.dumps(all_colors, indent=2)
    
    elif uri == "usyd://colors/primary":
        return json.dumps(get_colors_by_category("official_primary"), indent=2)
    
    elif uri == "usyd://colors/secondary":
        return json.dumps(get_colors_by_category("official_secondary"), indent=2)
    
    elif uri == "usyd://colors/tertiary":
        return json.dumps(get_colors_by_category("official_tertiary"), indent=2)
    
    elif uri == "usyd://branding/guidelines":
        return get_branding_guidelines()
    
    else:
        return f"Resource not found: {uri}"


async def main():
    """Run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())