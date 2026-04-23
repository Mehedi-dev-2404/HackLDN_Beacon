#!/bin/bash

# Aura AI Student OS - Startup Script

echo "🚀 Starting Aura AI Student OS..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📝 Please copy .env.example to .env and add your API keys:"
    echo "   cp .env.example .env"
    exit 1
fi

# Check if in virtual environment (recommended)
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Recommended: python -m venv venv && source venv/bin/activate"
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

# Run tests
echo ""
echo "🧪 Running system tests..."
python test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
    echo "🌐 Starting FastAPI server on http://localhost:8000"
    echo "📚 API docs available at http://localhost:8000/docs"
    echo ""
    
    cd backend
    python main.py
else
    echo ""
    echo "❌ Tests failed. Please fix the issues above."
    exit 1
fi
