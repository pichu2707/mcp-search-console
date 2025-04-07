#!/usr/bin/env python
"""Script to update version number"""

import re
import sys
from pathlib import Path


def bump_version(version_type):
    """
    Updates the version in pyproject.toml.
    
    version_type must be one of 'major', 'minor', or 'patch'.
    """
    if version_type not in ['major', 'minor', 'patch']:
        print(f"Error: Version type must be one of 'major', 'minor', or 'patch'.")
        sys.exit(1)
    
    # Load pyproject.toml
    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found.")
        sys.exit(1)
    
    content = pyproject_path.read_text()
    
    # Extract current version
    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not version_match:
        print("Error: Could not extract version from pyproject.toml.")
        sys.exit(1)
    
    current_version = version_match.group(1)
    print(f"Current version: {current_version}")
    
    # Break down version number
    try:
        major, minor, patch = map(int, current_version.split('.'))
    except ValueError:
        print(f"Error: Version number '{current_version}' is not in x.y.z format.")
        sys.exit(1)
    
    # Increment version based on specified type
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    
    new_version = f"{major}.{minor}.{patch}"
    print(f"New version: {new_version}")
    
    # Update the file
    new_content = re.sub(r'(version\s*=\s*)"[^"]+"', r'\1"' + new_version + '"', content)
    pyproject_path.write_text(new_content)
    
    print(f"Updated version in pyproject.toml to {new_version}.")
    print(f"Run the following commands to push to GitHub and create a release:")
    print(f"  git add pyproject.toml")
    print(f"  git commit -m 'Bump version to {new_version}'")
    print(f"  git tag v{new_version}")
    print(f"  git push origin main v{new_version}")
    print(f"Then create a release on the GitHub repository page.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch]")
        sys.exit(1)
    
    bump_version(sys.argv[1]) 