#!/bin/bash

# Contract Pricing Intelligence Prototype - Startup Script

echo "🚀 Starting Contract Pricing Intelligence Prototype..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Load sample data if not already loaded
echo "Loading sample data..."
python manage.py load_sample_data

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting development server..."
echo "📍 Server running at: http://localhost:8000"
echo "📊 Admin panel at: http://localhost:8000/admin (admin/admin123)"
echo "📡 API at: http://localhost:8000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
