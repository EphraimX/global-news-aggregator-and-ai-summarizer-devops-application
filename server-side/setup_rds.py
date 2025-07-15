#!/usr/bin/env python3
"""
🚀 Amazon RDS Setup Script for Global News Digest AI

This script helps you set up and configure your Amazon RDS database.
It includes connection testing, table creation, and sample data insertion.
"""

import asyncio
import sys
import os
from pathlib import Path
import logging

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from config import settings
from database import init_database, close_database, check_database_health
from services.database_service import db_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_connection():
    """Test connection to Amazon RDS"""
    print("🔌 Testing Amazon RDS connection...")
    print(f"📍 Host: {settings.DB_HOST}")
    print(f"🔢 Port: {settings.DB_PORT}")
    print(f"🗄️ Database: {settings.DB_NAME}")
    print(f"👤 User: {settings.DB_USER}")
    print(f"🔧 Type: {settings.DB_TYPE}")
    
    try:
        await init_database()
        health = await check_database_health()
        
        if health["status"] == "healthy":
            print("✅ Connection successful!")
            return True
        else:
            print(f"❌ Connection failed: {health.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

async def setup_database():
    """Complete database setup"""
    print("\n🛠️ Setting up database...")
    
    try:
        # Initialize database service
        await db_service.init_db()
        
        # Create sample data
        print("📝 Creating sample data...")
        
        # You can add sample articles here if needed
        sample_articles = []  # Add sample Article objects here
        
        if sample_articles:
            success = await db_service.save_articles(sample_articles)
            if success:
                print("✅ Sample data created successfully!")
            else:
                print("⚠️ Failed to create sample data")
        
        print("✅ Database setup completed!")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        raise

async def show_statistics():
    """Show database statistics"""
    print("\n📊 Database Statistics:")
    
    try:
        stats = await db_service.get_statistics()
        print(f"📰 Total Articles: {stats['total_articles']}")
        
        if stats['articles_by_topic']:
            print("\n📂 Articles by Topic:")
            for topic, count in stats['articles_by_topic'].items():
                print(f"   {topic}: {count}")
        
        if stats['articles_by_source']:
            print("\n📡 Articles by Source:")
            for source, count in list(stats['articles_by_source'].items())[:5]:
                print(f"   {source}: {count}")
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")

async def main():
    """Main setup function"""
    print("=" * 60)
    print("🌟 AMAZON RDS SETUP - GLOBAL NEWS DIGEST AI")
    print("=" * 60)
    
    # Test connection
    if not await test_connection():
        print("\n❌ Setup failed - cannot connect to database")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check your RDS endpoint and port")
        print("   2. Verify security group allows connections")
        print("   3. Ensure database credentials are correct")
        print("   4. Check if RDS instance is running")
        return
    
    # Setup database
    await setup_database()
    
    # Show statistics
    await show_statistics()
    
    # Close connection
    await close_database()
    
    print("\n" + "=" * 60)
    print("🎉 RDS SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n🚀 You can now start the API server:")
    print("   python run_server.py")
    print("\n📚 API Documentation will be available at:")
    print("   http://localhost:8000/docs")

if __name__ == "__main__":
    asyncio.run(main())
