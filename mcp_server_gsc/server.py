"""MCP server implementation for Google Search Console."""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

from mcp import MCPServer, types
from mcp.server import LogLevel

from .config import Config
from .gsc_client import GSCClient


class GSCMCPServer(MCPServer):
    """MCP server implementation for Google Search Console."""

    def __init__(self, config: Config):
        """Initialize the MCP server.

        Args:
            config: The server configuration.
        """
        super().__init__()
        self.config = config
        self.gsc_client: Optional[GSCClient] = None

        # Initialize the GSC client if credentials are available
        if self.config.google_credentials:
            self.gsc_client = GSCClient(self.config.google_credentials)
        
        # Configure the server capabilities
        self.capabilities = types.ServerCapabilities(
            tools=types.ToolsCapabilities(
                list=True,
                listChanged=True,
            ),
            logging=types.LoggingCapabilities(),
        )

    async def initialize(self, params: types.InitializeParams) -> types.InitializeResult:
        """Initialize the MCP server.

        Args:
            params: The initialization parameters.

        Returns:
            The initialization result.
        """
        if not self.gsc_client:
            await self.log(
                LogLevel.ERROR,
                "Google Search Console credentials not found. "
                "Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.",
            )
            return types.InitializeResult(
                capabilities=self.capabilities,
                serverInfo=types.ServerInfo(
                    name="google-search-console",
                    version="0.1.0",
                    description="MCP server for Google Search Console",
                ),
            )

        try:
            # Test the GSC client to ensure it's working
            # Just accessing the service is enough to validate the credentials
            _ = self.gsc_client.service
            await self.log(LogLevel.INFO, "Google Search Console client initialized")
        except Exception as e:
            await self.log(
                LogLevel.ERROR,
                f"Failed to initialize Google Search Console client: {e}",
            )

        return types.InitializeResult(
            capabilities=self.capabilities,
            serverInfo=types.ServerInfo(
                name="google-search-console",
                version="0.1.0",
                description="MCP server for Google Search Console",
            ),
        )

    async def list_tools(self) -> types.ListToolsResult:
        """List the available tools.

        Returns:
            The list of available tools.
        """
        tools = [
            types.Tool(
                name="search_analytics",
                description="Get search analytics data from Google Search Console",
                schema={
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
        return types.ListToolsResult(tools=tools)

    async def call_tool(
        self, params: types.CallToolParams
    ) -> types.CallToolResult:
        """Call a tool.

        Args:
            params: The tool call parameters.

        Returns:
            The tool call result.
        """
        if not self.gsc_client:
            return types.CallToolResult(
                status="error",
                error="Google Search Console client not initialized",
            )

        if params.name == "search_analytics":
            try:
                # Extract and validate parameters
                site_url = params.arguments.get("siteUrl")
                start_date = params.arguments.get("startDate")
                end_date = params.arguments.get("endDate")
                
                if not site_url or not start_date or not end_date:
                    return types.CallToolResult(
                        status="error",
                        error="Missing required parameters: siteUrl, startDate, endDate",
                    )
                
                # Extract optional parameters
                dimensions_str = params.arguments.get("dimensions", "")
                dimensions = [dim.strip() for dim in dimensions_str.split(",") if dim.strip()] if dimensions_str else None
                search_type = params.arguments.get("type")
                aggregation_type = params.arguments.get("aggregationType")
                row_limit = params.arguments.get("rowLimit", 1000)
                
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
                
                return types.CallToolResult(
                    status="success",
                    result=result,
                )
            except Exception as e:
                await self.log(LogLevel.ERROR, f"Error calling search_analytics: {e}")
                return types.CallToolResult(
                    status="error",
                    error=str(e),
                )
        
        return types.CallToolResult(
            status="error",
            error=f"Unknown tool: {params.name}",
        ) 