#!/usr/bin/env python3
"""
🧪 API Testing Script for Global News Digest AI

This script tests all the API endpoints to ensure they're working correctly.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing Global News Digest AI API")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Health Check
        print("1️⃣ Testing Health Check...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
        
        print()
        
        # Test 2: Get Articles
        print("2️⃣ Testing Get Articles...")
        try:
            response = await client.get(f"{BASE_URL}/api/news/articles?limit=20")
            if response.status_code == 200:
                articles = response.json()
                print(f"✅ Got {len(articles)} articles")
                if articles:
                    print(f"   Sample title: {articles[0]['title'][:50]}...")
            else:
                print(f"❌ Get articles failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Get articles error: {e}")
        
        print()
        
        # Test 3: Get Trending Topics
        print("3️⃣ Testing Trending Topics...")
        try:
            response = await client.get(f"{BASE_URL}/api/news/trending")
            if response.status_code == 200:
                trending = response.json()
                print(f"✅ Got {len(trending)} trending topics")
                for topic in trending[:3]:
                    print(f"   {topic['emoji']} {topic['name']}: {topic['count']} articles ({topic['trend_type']})")
            else:
                print(f"❌ Trending topics failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Trending topics error: {e}")
        
        print()
        
        # Test 4: AI Summarization
        print("4️⃣ Testing AI Summarization...")
        try:
            test_data = {
                "title": "Test Article About Technology",
                "content": "This is a test article about the latest developments in artificial intelligence and machine learning. The technology is advancing rapidly and changing many industries."
            }
            response = await client.post(f"{BASE_URL}/api/ai/summarize", json=test_data)
            if response.status_code == 200:
                summary = response.json()
                print("✅ AI summarization working")
                print(f"   Summary: {summary['summary'][:100]}...")
            else:
                print(f"❌ AI summarization failed: {response.status_code}")
        except Exception as e:
            print(f"❌ AI summarization error: {e}")
        
        print()
        
        # Test 5: News Statistics
        print("5️⃣ Testing News Statistics...")
        try:
            response = await client.get(f"{BASE_URL}/api/news/stats")
            if response.status_code == 200:
                stats = response.json()
                print("✅ News statistics working")
                print(f"   Total articles: {stats['total_articles']}")
                print(f"   Topics: {list(stats['articles_by_topic'].keys())}")
            else:
                print(f"❌ News statistics failed: {response.status_code}")
        except Exception as e:
            print(f"❌ News statistics error: {e}")
        
        print()
        
        # Test 6: Filtered Articles
        print("6️⃣ Testing Filtered Articles...")
        try:
            params = {
                "topic": "Technology",
                "limit": 3,
                "search_query": "AI"
            }
            response = await client.get(f"{BASE_URL}/api/news/articles", params=params)
            if response.status_code == 200:
                articles = response.json()
                print(f"✅ Filtered articles working - got {len(articles)} articles")
            else:
                print(f"❌ Filtered articles failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Filtered articles error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("💡 If any tests failed, check that the server is running on localhost:8000")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
