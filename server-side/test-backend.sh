#!/bin/bash

# 🧪 Backend Testing Script
echo "🧪 Testing Global News Digest AI Backend"
echo "========================================"

# Check if backend is running
echo "1️⃣ Checking if backend server is running..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend server is running"
else
    echo "❌ Backend server is not running"
    echo "💡 Start the backend with: python run_server.py"
    exit 1
fi

# Test health endpoint
echo ""
echo "2️⃣ Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo "✅ Health check passed"
    echo "   Response: $HEALTH_RESPONSE"
else
    echo "❌ Health check failed"
    echo "   Response: $HEALTH_RESPONSE"
fi

# Test articles endpoint
echo ""
echo "3️⃣ Testing articles endpoint..."
ARTICLES_RESPONSE=$(curl -s "http://localhost:8000/api/news/articles?limit=3")
if [[ $ARTICLES_RESPONSE == *"["* ]]; then
    echo "✅ Articles endpoint working"
    ARTICLE_COUNT=$(echo $ARTICLES_RESPONSE | jq '. | length' 2>/dev/null || echo "unknown")
    echo "   Retrieved $ARTICLE_COUNT articles"
else
    echo "❌ Articles endpoint failed"
    echo "   Response: $ARTICLES_RESPONSE"
fi

# Test AI summarization
echo ""
echo "4️⃣ Testing AI summarization..."
SUMMARY_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/ai/summarize" \
    -H "Content-Type: application/json" \
    -d '{"title": "Test Article", "content": "This is a test article about technology and AI."}')

if [[ $SUMMARY_RESPONSE == *"summary"* ]]; then
    echo "✅ AI summarization working"
    echo "   Summary generated successfully"
else
    echo "❌ AI summarization failed"
    echo "   Response: $SUMMARY_RESPONSE"
fi

# Test trending topics
echo ""
echo "5️⃣ Testing trending topics..."
TRENDING_RESPONSE=$(curl -s "http://localhost:8000/api/news/trending")
if [[ $TRENDING_RESPONSE == *"["* ]]; then
    echo "✅ Trending topics working"
    TRENDING_COUNT=$(echo $TRENDING_RESPONSE | jq '. | length' 2>/dev/null || echo "unknown")
    echo "   Retrieved $TRENDING_COUNT trending topics"
else
    echo "❌ Trending topics failed"
    echo "   Response: $TRENDING_RESPONSE"
fi

# Test database connection
echo ""
echo "6️⃣ Testing database connection..."
DB_RESPONSE=$(curl -s "http://localhost:8000/api/news/stats")
if [[ $DB_RESPONSE == *"total_articles"* ]]; then
    echo "✅ Database connection working"
    echo "   Statistics retrieved successfully"
else
    echo "❌ Database connection failed"
    echo "   Response: $DB_RESPONSE"
fi

echo ""
echo "🎉 Backend testing completed!"
echo "💡 If any tests failed, check the backend logs and configuration"
