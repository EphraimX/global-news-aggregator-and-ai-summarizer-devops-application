#!/bin/bash

# 🔍 Debug Script for Global News Digest AI
echo "🔍 Global News Digest AI - Debug Information"
echo "============================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# System Information
echo -e "${BLUE}📊 System Information${NC}"
echo "OS: $(uname -s)"
echo "Architecture: $(uname -m)"
echo "Python Version: $(python3 --version 2>/dev/null || echo 'Not installed')"
echo "Node Version: $(node --version 2>/dev/null || echo 'Not installed')"
echo "Docker Version: $(docker --version 2>/dev/null || echo 'Not installed')"
echo ""

# Environment Variables
echo -e "${BLUE}🔧 Environment Variables${NC}"
echo "DB_HOST: ${DB_HOST:-'Not set'}"
echo "DB_PORT: ${DB_PORT:-'Not set'}"
echo "DB_NAME: ${DB_NAME:-'Not set'}"
echo "DB_USER: ${DB_USER:-'Not set'}"
echo "NEWS_API_KEY: ${NEWS_API_KEY:0:10}... (${#NEWS_API_KEY} chars)"
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}... (${#OPENAI_API_KEY} chars)"
echo "NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-'Not set'}"
echo ""

# Backend Status
echo -e "${BLUE}🖥️ Backend Status${NC}"
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is running${NC}"
    
    # API Endpoints Test
    echo "Testing API endpoints..."
    
    # Health check
    HEALTH=$(curl -s http://localhost:8000/health)
    echo "Health: $HEALTH"
    
    # Articles count
    ARTICLES=$(curl -s "http://localhost:8000/api/news/articles?limit=1" | jq '. | length' 2>/dev/null || echo "Error")
    echo "Articles endpoint: $ARTICLES"
    
    # Database connection
    STATS=$(curl -s http://localhost:8000/api/news/stats | jq '.total_articles' 2>/dev/null || echo "Error")
    echo "Database articles: $STATS"
    
else
    echo -e "${RED}❌ Backend is not running${NC}"
    echo "Try starting with: python run_server.py"
fi
echo ""

# Frontend Status
echo -e "${BLUE}🎨 Frontend Status${NC}"
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${RED}❌ Frontend is not running${NC}"
    echo "Try starting with: npm run dev"
fi
echo ""

# Database Connection
echo -e "${BLUE}🗃️ Database Connection${NC}"
if [ -n "$DB_HOST" ] && [ -n "$DB_USER" ]; then
    if command -v psql &> /dev/null; then
        if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1;" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Database connection successful${NC}"
            
            # Table information
            TABLE_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs)
            echo "Tables in database: $TABLE_COUNT"
            
            ARTICLE_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM articles;" 2>/dev/null | xargs)
            echo "Articles in database: $ARTICLE_COUNT"
        else
            echo -e "${RED}❌ Database connection failed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ psql not installed, cannot test database connection${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Database credentials not set${NC}"
fi
echo ""

# Docker Status
echo -e "${BLUE}🐳 Docker Status${NC}"
if command -v docker &> /dev/null; then
    echo "Docker containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(global-news|NAMES)"
    
    echo ""
    echo "Docker images:"
    docker images | grep -E "(global-news|REPOSITORY)"
else
    echo -e "${YELLOW}⚠️ Docker not installed${NC}"
fi
echo ""

# Log Files
echo -e "${BLUE}📝 Recent Log Entries${NC}"
if [ -f "backend.log" ]; then
    echo "Backend logs (last 5 lines):"
    tail -5 backend.log
else
    echo "No backend log file found"
fi

if [ -f "frontend.log" ]; then
    echo "Frontend logs (last 5 lines):"
    tail -5 frontend.log
else
    echo "No frontend log file found"
fi
echo ""

# Network Connectivity
echo -e "${BLUE}🌐 Network Connectivity${NC}"
echo "Testing external APIs..."

# NewsAPI
if curl -s "https://newsapi.org/v2/top-headlines?country=us&apiKey=${NEWS_API_KEY}&pageSize=1" | grep -q "articles"; then
    echo -e "${GREEN}✅ NewsAPI connection successful${NC}"
else
    echo -e "${RED}❌ NewsAPI connection failed${NC}"
fi

# OpenAI API (basic connectivity test)
if curl -s -H "Authorization: Bearer ${OPENAI_API_KEY}" "https://api.openai.com/v1/models" | grep -q "data"; then
    echo -e "${GREEN}✅ OpenAI API connection successful${NC}"
else
    echo -e "${RED}❌ OpenAI API connection failed${NC}"
fi
echo ""

# Disk Space
echo -e "${BLUE}💾 Disk Space${NC}"
df -h . | head -2
echo ""

# Memory Usage
echo -e "${BLUE}🧠 Memory Usage${NC}"
free -h 2>/dev/null || echo "Memory info not available"
echo ""

# Process Information
echo -e "${BLUE}⚙️ Related Processes${NC}"
ps aux | grep -E "(python|node|nginx)" | grep -v grep | head -10
echo ""

echo -e "${GREEN}🎉 Debug information collection completed!${NC}"
echo "If you're experiencing issues, check the items marked with ❌ above."
