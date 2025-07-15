#!/bin/bash

# 🛠️ Useful Commands for Global News Digest AI
echo "🛠️ Global News Digest AI - Useful Commands"
echo "==========================================="

cat << 'EOF'

## 🚀 Development Commands

### Backend Commands
```bash
# Start backend server
python run_server.py

# Run database migrations
python migrations/create_tables.py

# Test API endpoints
python test_api.py

# Setup RDS database
python setup_rds.py

# Install backend dependencies
pip install -r requirements.txt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
