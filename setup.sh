#!/bin/bash

echo "🔧 Setting up Python virtual environment..."

# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f requirements.txt ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️ No requirements.txt found. Skipping pip install."
fi

echo "✅ Setup complete. To activate later, run: source venv/bin/activate"

