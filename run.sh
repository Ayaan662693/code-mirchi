#!/bin/bash
set -e

# Change to project root
cd "$(dirname "$0")"

# Setup virtual environment if missing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

# Run Flask server
echo "Starting CODE MIRCHI Backend..."
./venv/bin/python3 app.py
