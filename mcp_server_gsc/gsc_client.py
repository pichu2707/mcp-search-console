"""Google Search Console API client."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from google.oauth2 import service_account
from googleapiclient.discovery import build


class GSCClient:
    """Client for the Google Search Console API."""

    def __init__(self, credentials_path: Path):
        """Initialize the Google Search Console API client.

        Args:
            credentials_path: Path to the Google Cloud credentials file.
        """
        self.credentials_path = credentials_path
        self.credentials = self._get_credentials()
        self.service = build(
            "searchconsole", "v1", credentials=self.credentials, cache_discovery=False
        )

    def _get_credentials(self):
        """Get the credentials for the Google Search Console API."""
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Credentials file not found: {self.credentials_path}"
            )
        
        return service_account.Credentials.from_service_account_file(
            str(self.credentials_path)
        )

    async def list_sites(self) -> Dict[str, Any]:
        """List all sites in the Google Search Console account.

        Returns:
            A dictionary containing the list of sites.
        """
        try:
            response = self.service.sites().list().execute()
            
            sites = response.get('siteEntry', [])
            formatted_sites = []
            
            for site in sites:
                site_info = {
                    'siteUrl': site.get('siteUrl', ''),
                    'permissionLevel': site.get('permissionLevel', ''),
                }
                formatted_sites.append(site_info)
            
            return {
                'sites': formatted_sites,
                'total_sites': len(formatted_sites)
            }
            
        except Exception as e:
            raise Exception(f"Error listing sites: {str(e)}")

    async def get_search_analytics(
        self,
        site_url: str,
        start_date: str,
        end_date: str,
        dimensions: Optional[List[str]] = None,
        search_type: Optional[str] = None,
        aggregation_type: Optional[str] = None,
        row_limit: int = 1000,
    ) -> Dict[str, Any]:
        """Get search analytics data from Google Search Console.

        Args:
            site_url: The URL of the site to get data for.
            start_date: The start date for the data (YYYY-MM-DD).
            end_date: The end date for the data (YYYY-MM-DD).
            dimensions: The dimensions to group the data by.
            search_type: The type of search (web, image, video, news).
            aggregation_type: The type of aggregation to use.
            row_limit: The maximum number of rows to return.

        Returns:
            The search analytics data.
        """
        # Validate dates
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in the format YYYY-MM-DD")

        # Create request body
        request_body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions or [],
            "rowLimit": row_limit,
        }

        # Add optional fields if provided
        if search_type:
            valid_types = ["web", "image", "video", "news", "discover", "googleNews"]
            if search_type not in valid_types:
                raise ValueError(f"Invalid search type: {search_type}. Must be one of {valid_types}")
            request_body["searchType"] = search_type

        if aggregation_type:
            valid_types = ["auto", "byPage", "byProperty", "byNewsShowcasePanel"]
            if aggregation_type not in valid_types:
                raise ValueError(f"Invalid aggregation type: {aggregation_type}. Must be one of {valid_types}")
            request_body["aggregationType"] = aggregation_type

        # Execute request
        response = self.service.searchanalytics().query(
            siteUrl=site_url, body=request_body
        ).execute()

        # Format the response
        formatted_response = self._format_search_analytics(response, dimensions or [])
        
        return formatted_response

    def _format_search_analytics(
        self, response: Dict[str, Any], dimensions: List[str]
    ) -> Dict[str, Any]:
        """Format the search analytics response.

        Args:
            response: The response from the Google Search Console API.
            dimensions: The dimensions used in the request.

        Returns:
            The formatted response.
        """
        rows = response.get("rows", [])
        formatted_rows = []

        for row in rows:
            formatted_row = {}
            
            # Add dimensions
            for i, dim in enumerate(dimensions):
                if i < len(row.get("keys", [])):
                    formatted_row[dim] = row["keys"][i]
            
            # Add metrics
            formatted_row["clicks"] = row.get("clicks", 0)
            formatted_row["impressions"] = row.get("impressions", 0)
            formatted_row["ctr"] = row.get("ctr", 0)
            formatted_row["position"] = row.get("position", 0)
            
            formatted_rows.append(formatted_row)
        
        return {
            "rows": formatted_rows,
            "responseAggregationType": response.get("responseAggregationType", ""),
        }