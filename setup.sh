#!/bin/bash

echo "🔧 Setting up Python virtual environment..."

# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install package (editable) and dev tools
echo "📦 Installing package and dev extras..."
pip install -e .[dev]

echo "✅ Setup complete. To activate later, run: source venv/bin/activate"
