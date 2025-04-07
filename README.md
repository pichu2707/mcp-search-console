# Google Search Console MCP Server

A tool for accessing Google Search Console using the Model Context Protocol (MCP) server.

## Features

* Retrieve search analytics data (with dimension support)
* Detailed data analysis with customizable reporting periods

## Prerequisites

* Python 3.10 or higher
* Google Cloud project with Search Console API enabled
* Service account credentials with access to Search Console

## Installation

```bash
pip install mcp-server-google-search-console
```

Or install from source:

```bash
git clone https://github.com/yourusername/mcp-server-google-search-console.git
cd mcp-server-google-search-console
pip install -e .
```

## Setting Up Development Environment (uv)

This project uses uv for faster package management and installation.

### Installing uv and uvx

First, install uv and uvx:

```bash
pip install uv uvx
```

### Creating and Managing Virtual Environments

To create a new virtual environment using uv:

```bash
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Installing Dependencies

After cloning the repository, install dependencies:

```bash
git clone https://github.com/yourusername/mcp-server-google-search-console.git
cd mcp-server-google-search-console
pip install -e .
```

To install the MCP package separately:

```bash
pip install "mcp[cli]"
```

### Installing Development Dependencies

To install additional tools needed for development, run:

```bash
pip install -e ".[dev]"
```

## Authentication Setup

To obtain Google Search Console API credentials:

1. Access the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the API:
   * Go to "APIs & Services" > "Library"
   * Search for and enable "Search Console API"
4. Create credentials:
   * Go to "APIs & Services" > "Credentials"
   * Click "Create Credentials" > "Service Account"
   * Enter service account details
   * Create a new key in JSON format
   * The credentials file (.json) will be automatically downloaded
5. Grant access:
   * Open Search Console
   * Add the service account email address (format: name@project.iam.gserviceaccount.com) as a property administrator

## Usage

Set an environment variable to specify the path to your Google Search Console credentials file:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### Starting the MCP Server

#### Standard Method

```bash
mcp-server-gsc
```

#### Using uvx

With uvx, you can automate virtual environment and package installation:

```bash
# Run directly without installation
uvx run mcp-server-gsc

# Run with a specific Python version
uvx --python=3.11 run mcp-server-gsc

# Run with specified environment variables
uvx run -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json mcp-server-gsc
```

### Configuration for Claude Desktop Application

#### Standard Configuration

```json
{
  "mcpServers": {
    "gsc": {
      "command": "mcp-server-gsc",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

#### Configuration Using uvx

```json
{
  "mcpServers": {
    "gsc": {
      "command": "uvx",
      "args": ["run", "mcp-server-gsc"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

## Available Tools

### search_analytics

Retrieve search performance data from Google Search Console:

**Required Parameters:**

* `siteUrl`: Site URL (format: `http://www.example.com/` or `sc-domain:example.com`)
* `startDate`: Start date (YYYY-MM-DD)
* `endDate`: End date (YYYY-MM-DD)

**Optional Parameters:**

* `dimensions`: Comma-separated list (`query,page,country,device,searchAppearance`)
* `type`: Search type (`web`, `image`, `video`, `news`)
* `aggregationType`: Aggregation method (`auto`, `byNewsShowcasePanel`, `byProperty`, `byPage`)
* `rowLimit`: Maximum number of rows to return (default: 1000)

Example usage:

```json
{
  "siteUrl": "https://example.com",
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": "query,country",
  "type": "web",
  "rowLimit": 500
}
```

## Release Procedure

This project is automatically published to PyPI when a GitHub release tag is created.

To release a new version:

1. Run the version update script:
   ```bash
   python scripts/bump_version.py [major|minor|patch]
   ```

2. Follow the displayed instructions to push to GitHub:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to x.y.z"
   git tag vx.y.z
   git push origin main vx.y.z
   ```

3. Create a release on the GitHub repository page:
   - Select tag: `vx.y.z`
   - Enter title: `vx.y.z`
   - Fill in release notes
   - Click "Publish"

4. GitHub Actions will be triggered and automatically publish the package to PyPI.

## License

MIT

## Contributions

Contributions are welcome! Please read the contribution guidelines before submitting a pull request.