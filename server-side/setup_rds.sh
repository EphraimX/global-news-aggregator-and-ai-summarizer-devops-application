#!/bin/bash

# 🚀 Amazon RDS Setup Script for Global News Digest AI
# This script helps set up the RDS environment and dependencies

echo "🌟 Setting up Amazon RDS for Global News Digest AI"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Install required packages
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Packages installed successfully"
else
    echo "❌ Failed to install packages"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your RDS credentials"
    echo "   Required variables:"
    echo "   - DB_HOST (your RDS endpoint)"
    echo "   - DB_PASSWORD (your database password)"
    echo "   - NEWS_API_KEY (from newsapi.org)"
    echo "   - OPENAI_API_KEY (from openai.com)"
else
    echo "✅ .env file found"
fi

# Download RDS CA certificate
echo "🔐 Downloading RDS CA certificate..."
if [ ! -f "rds-ca-2019-root.pem" ]; then
    curl -o rds-ca-2019-root.pem https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem
    if [ $? -eq 0 ]; then
        echo "✅ RDS CA certificate downloaded"
    else
        echo "⚠️  Failed to download RDS CA certificate"
    fi
else
    echo "✅ RDS CA certificate already exists"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Edit .env file with your RDS credentials"
echo "2. Run: python3 setup_rds.py"
echo "3. Run: python3 run_server.py"
echo ""
echo "📚 Documentation: http://localhost:8000/docs"
