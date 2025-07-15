#!/usr/bin/env python3
"""
🚀 Global News Digest AI - Backend Server Runner

This script starts the FastAPI backend server for the Global News Digest AI application.

Features:
- 📰 News aggregation from multiple sources
- 🤖 AI-powered article summarization  
- 🔥 Trending topics analysis
- 🌍 Multi-region support
- 🎯 Advanced filtering and search
- 📊 Real-time statistics

Usage:
    python run_server.py

Environment Variables:
    NEWS_API_KEY: Your NewsAPI key (get from https://newsapi.org)
    OPENAI_API_KEY: Your OpenAI API key
    PORT: Server port (default: 8000)
    DEBUG: Enable debug mode (default: True)

API Endpoints:
    GET  /                     - API information
    GET  /health              - Health check
    GET  /docs                - Interactive API documentation
    GET  /api/news/articles   - Get filtered news articles
    GET  /api/news/trending   - Get trending topics
    GET  /api/news/stats      - Get news statistics
    POST /api/ai/summarize    - Generate AI summaries
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import openai
        import sqlalchemy
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("📦 Installing requirements...")
        
        # Install requirements
        requirements_file = Path(__file__).parent / "requirements.txt"
        if requirements_file.exists():
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
            print("✅ Requirements installed successfully")
            return True
        else:
            print("❌ requirements.txt not found")
            return False

def setup_environment():
    """Setup environment variables with defaults"""
    env_vars = {
        "NEWS_API_KEY": "your_newsapi_key_here",
        "OPENAI_API_KEY": "your_openai_key_here", 
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "DEBUG": "True"
    }
    
    print("🔧 Environment Setup:")
    for key, default_value in env_vars.items():
        current_value = os.getenv(key, default_value)
        os.environ[key] = current_value
        
        if key.endswith("_KEY") and current_value.startswith("your_"):
            print(f"⚠️  {key}: Using placeholder (set your real API key)")
        else:
            print(f"✅ {key}: {current_value}")

def main():
    """Main function to start the server"""
    print("=" * 60)
    print("🌟 GLOBAL NEWS DIGEST AI - BACKEND API")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("❌ Failed to install requirements")
        return
    
    # Setup environment
    setup_environment()
    
    print("\n🚀 Starting server...")
    print("📍 Server URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔥 Interactive API: http://localhost:8000/redoc")
    print("\n💡 Tips:")
    print("   - Set NEWS_API_KEY environment variable for real news data")
    print("   - Set OPENAI_API_KEY environment variable for AI summaries")
    print("   - Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Import and run the main app
    try:
        from main import app
        import uvicorn
        
        uvicorn.run(
            app,
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", 8000)),
            reload=os.getenv("DEBUG", "True").lower() == "true",
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
