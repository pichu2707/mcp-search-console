#!/bin/bash
set -e

# Cleanup
rm -rf dist/
rm -rf build/

# Build package
python -m build

# Upload to PyPI
python -m twine upload dist/*

echo "Package published successfully!" 