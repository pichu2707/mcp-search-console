"""MCP server implementation for Google Search Console."""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from .config import Config
from .gsc_client import GSCClient


class GSCMCPServer:
    """MCP server implementation for Google Search Console."""

    def __init__(self, config: Config):
        """Initialize the MCP server.

        Args:
            config: The server configuration.
        """
        self.config = config
        self.gsc_client: Optional[GSCClient] = None
        self.server = Server("google-search-console")

        # Initialize the GSC client if credentials are available
        if self.config.google_credentials:
            self.gsc_client = GSCClient(self.config.google_credentials)
        
        # Set up handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up the MCP server handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List the available tools."""
            tools = [
                types.Tool(
                    name="list_sites",
                    description="List all sites configured in Google Search Console",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                    },
                ),
                types.Tool(
                    name="search_analytics",
                    description="Get search analytics data from Google Search Console",
                    inputSchema={
                        "type": "object",
                        "required": ["siteUrl", "startDate", "endDate"],
                        "properties": {
                            "siteUrl": {
                                "type": "string",
                                "description": "The URL of the site to get data for.",
                            },
                            "startDate": {
                                "type": "string",
                                "description": "The start date for the data (YYYY-MM-DD).",
                            },
                            "endDate": {
                                "type": "string",
                                "description": "The end date for the data (YYYY-MM-DD).",
                            },
                            "dimensions": {
                                "type": "string",
                                "description": "Comma-separated list of dimensions to group by (query,page,country,device,searchAppearance).",
                            },
                            "type": {
                                "type": "string",
                                "description": "The type of search (web, image, video, news, discover, googleNews).",
                            },
                            "aggregationType": {
                                "type": "string",
                                "description": "The type of aggregation (auto, byPage, byProperty, byNewsShowcasePanel).",
                            },
                            "rowLimit": {
                                "type": "integer",
                                "description": "The maximum number of rows to return (default: 1000).",
                            },
                        },
                    },
                ),
            ]
            return tools

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Call a tool."""
            if not self.gsc_client:
                raise RuntimeError("Google Search Console client not initialized")

            if name == "list_sites":
                try:
                    result = await self.gsc_client.list_sites()
                    return [
                        types.TextContent(
                            type="text",
                            text=json.dumps(result, indent=2)
                        )
                    ]
                except Exception as e:
                    raise RuntimeError(f"Error calling list_sites: {e}")

            elif name == "search_analytics":
                try:
                    if not arguments:
                        raise ValueError("No arguments provided")
                    
                    # Extract and validate parameters
                    site_url = arguments.get("siteUrl")
                    start_date = arguments.get("startDate")
                    end_date = arguments.get("endDate")
                    
                    if not site_url or not start_date or not end_date:
                        raise ValueError("Missing required parameters: siteUrl, startDate, endDate")
                    
                    # Extract optional parameters
                    dimensions_str = arguments.get("dimensions", "")
                    dimensions = [dim.strip() for dim in dimensions_str.split(",") if dim.strip()] if dimensions_str else None
                    search_type = arguments.get("type")
                    aggregation_type = arguments.get("aggregationType")
                    row_limit = arguments.get("rowLimit", 1000)
                    
                    # Call the GSC client
                    result = await self.gsc_client.get_search_analytics(
                        site_url=site_url,
                        start_date=start_date,
                        end_date=end_date,
                        dimensions=dimensions,
                        search_type=search_type,
                        aggregation_type=aggregation_type,
                        row_limit=row_limit,
                    )
                    
                    return [
                        types.TextContent(
                            type="text",
                            text=json.dumps(result, indent=2)
                        )
                    ]
                except Exception as e:
                    raise RuntimeError(f"Error calling search_analytics: {e}")
            
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """Run the MCP server."""
        if not self.gsc_client:
            print("Error: Google Search Console credentials not found.", file=sys.stderr)
            return
        
        # Test the GSC client to ensure it's working
        try:
            _ = self.gsc_client.service
            print("Google Search Console client initialized", file=sys.stderr)
        except Exception as e:
            print(f"Failed to initialize Google Search Console client: {e}", file=sys.stderr)
            return

        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="google-search-console",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )