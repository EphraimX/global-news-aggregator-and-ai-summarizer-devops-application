#!/usr/bin/env python3
"""
🗃️ Database Migration Script for Amazon RDS

This script creates all necessary tables in your Amazon RDS instance.
Run this script after setting up your RDS database.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from database import Base, engine, init_database
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_tables():
    """Create all database tables"""
    try:
        print("🗃️ Creating database tables in Amazon RDS...")
        print(f"📍 Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
        print(f"🔧 Database Type: {settings.DB_TYPE}")
        
        # Initialize database connection
        await init_database()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ All tables created successfully!")
        print("\n📋 Created tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"   - {table_name}")
        
        print("\n🎉 Database migration completed!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        logger.error(f"Migration error: {e}")
        sys.exit(1)

async def verify_tables():
    """Verify that all tables were created"""
    try:
        from database import database
        
        # Check if tables exist
        tables_to_check = ['articles', 'user_interactions', 'trending_topics']
        
        for table in tables_to_check:
            query = f"SELECT COUNT(*) as count FROM {table}"
            result = await database.fetch_one(query)
            print(f"✅ Table '{table}': {result['count']} records")
        
    except Exception as e:
        print(f"⚠️ Table verification failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🌟 GLOBAL NEWS DIGEST AI - DATABASE MIGRATION")
    print("=" * 60)
    
    # Run migration
    asyncio.run(create_tables())
    
    # Verify tables
    print("\n🔍 Verifying tables...")
    asyncio.run(verify_tables())
