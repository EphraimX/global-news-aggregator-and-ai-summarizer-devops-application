from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from databases import Database
from datetime import datetime
import uuid
import asyncio
import logging

from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup with connection pooling for RDS
engine = create_engine(
    settings.SYNC_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,  # Validate connections before use
    echo=settings.DEBUG,
    connect_args={
        "sslmode": settings.DB_SSL_MODE,
        "connect_timeout": 10,
    } if settings.DB_TYPE == "postgresql" else {
        "connect_timeout": 10,
    }
)

# Async database connection
database = Database(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ArticleDB(Base):
    __tablename__ = "articles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False, index=True)
    source_name = Column(String(100), nullable=False, index=True)
    source_favicon = Column(String(10), default="📰")
    source_color = Column(String(100), default="from-blue-500 to-purple-500")
    original_excerpt = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=False, index=True)
    topic = Column(String(50), nullable=False, index=True)
    url = Column(String(1000), nullable=False)
    image_url = Column(String(1000), nullable=True)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    is_trending = Column(Boolean, default=False, index=True)
    region = Column(String(20), default="Global", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Add indexes for better query performance
    __table_args__ = (
        Index('idx_topic_published', 'topic', 'published_at'),
        Index('idx_source_published', 'source_name', 'published_at'),
        Index('idx_region_topic', 'region', 'topic'),
        Index('idx_trending_published', 'is_trending', 'published_at'),
    )

class UserInteractionDB(Base):
    __tablename__ = "user_interactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    article_id = Column(String(36), nullable=False, index=True)
    interaction_type = Column(String(20), nullable=False)  # 'view', 'like', 'share'
    user_ip = Column(String(45), nullable=True)  # For anonymous tracking
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class TrendingTopicDB(Base):
    __tablename__ = "trending_topics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_name = Column(String(50), nullable=False, index=True)
    count = Column(Integer, default=0)
    trend_type = Column(String(20), default="rising")  # 'hot', 'trending', 'rising'
    emoji = Column(String(10), default="📰")
    region = Column(String(20), default="Global", index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)

async def init_database():
    """Initialize database connection and create tables"""
    try:
        # Connect to database
        await database.connect()
        logger.info("✅ Connected to Amazon RDS database")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

async def close_database():
    """Close database connection"""
    try:
        await database.disconnect()
        logger.info("✅ Database connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

async def get_async_db():
    """Get async database connection"""
    return database

# Health check for database
async def check_database_health():
    """Check if database is healthy"""
    try:
        query = "SELECT 1"
        result = await database.fetch_one(query)
        return {"status": "healthy", "connection": "active"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

# Database utility functions
async def execute_query(query: str, values: dict = None):
    """Execute a query with error handling"""
    try:
        if values:
            return await database.fetch_all(query, values)
        else:
            return await database.fetch_all(query)
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise

async def execute_single_query(query: str, values: dict = None):
    """Execute a query that returns a single result"""
    try:
        if values:
            return await database.fetch_one(query, values)
        else:
            return await database.fetch_one(query)
    except Exception as e:
        logger.error(f"Single query execution failed: {e}")
        raise
