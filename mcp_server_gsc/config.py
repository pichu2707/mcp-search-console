"""Configuration for the Google Search Console MCP server."""

import os
import logging

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

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
            creds_path = Path(self.google_credentials_path)
            if not creds_path.exists():
                logger.error(f"Credentials file not found at {creds_path}")
                return None
            return creds_path
        
        env_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if env_creds:
            creds_path = Path(env_creds)
            if not creds_path.exists():
                logger.error(f"Credentials file not found at {creds_path}")
                return None
            logger.info(f"Using credentials from environment variable: {creds_path}")
            return creds_path
        
        logger.error("No Google credentials path provided and no environment variable set.")
        return None
        
        
        #Si no hay path configurado, intent
        # if self.google_credentials_path:
        #     return Path(self.google_credentials_path)
        
        # env_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        # if env_creds:
        #     return Path(env_creds)
        
        # return None 