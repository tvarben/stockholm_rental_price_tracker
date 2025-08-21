#!/bin/bash
# Navigate to project root
cd "$(dirname "$0")/.."

# Create virtual environment if it doesn't exist
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements from install/ folder
pip install -r install/requirements.txt

# Install Playwright dependencies and browsers
venv/bin/playwright install-deps  # Linux only
venv/bin/playwright install
