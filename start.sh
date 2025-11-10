#!/bin/bash
# EcoSnake Game - One-Click Launcher (macOS/Linux)

clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐍  EcoSnake Game Launcher"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found!"
    echo ""
    echo "Please install Python: https://python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 First time setup..."
    echo ""
    
    # Create virtual environment
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
    
    # Activate
    source .venv/bin/activate
    
    # Install Pygame
    echo "📥 Installing Pygame..."
    pip install --quiet --upgrade pip
    pip install --quiet pygame
    
    if [ $? -eq 0 ]; then
        echo "✅ Setup completed!"
        echo ""
    else
        echo "❌ Setup failed!"
        exit 1
    fi
else
    # Activate virtual environment
    source .venv/bin/activate
fi

# Start the game
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎮 Starting game..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 EcoSnake.py
