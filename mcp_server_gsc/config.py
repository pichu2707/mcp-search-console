"""Configuration for the Google Search Console MCP server."""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration for the Google Search Console MCP server."""

    google_credentials_path: Optional[str] = Field(
        default=None,
        description="Path to the Google Cloud credentials file. If not provided, "
        "the GOOGLE_APPLICATION_CREDENTIALS environment variable will be used.",
    )

    @property
    def google_credentials(self) -> Optional[Path]:
        """Get the path to the Google Cloud credentials file."""
        if self.google_credentials_path:
            return Path(self.google_credentials_path)
        
        env_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if env_creds:
            return Path(env_creds)
        
        return None 