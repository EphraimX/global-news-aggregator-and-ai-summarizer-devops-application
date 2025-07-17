import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_newsapi_key_here")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_openai_key_here")
    
    # Amazon RDS Database Configuration
    DB_HOST = os.getenv("DB_HOST", "your-rds-endpoint.region.rds.amazonaws.com")
    DB_PORT = int(os.getenv("DB_PORT", 5432))  # 5432 for PostgreSQL, 3306 for MySQL
    DB_NAME = os.getenv("DB_NAME", "news_digest")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
    DB_TYPE = os.getenv("DB_TYPE", "postgresql")  # postgresql or mysql
    
    # Construct DATABASE_URL based on DB_TYPE
    if DB_TYPE == "postgresql":
        DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif DB_TYPE == "mysql":
        DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        SYNC_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Fallback to PostgreSQL
        DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Connection Pool Settings
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 20))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 30))
    DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", 30))
    DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", 3600))
    
    # API Settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # News API Settings
    NEWS_API_BASE_URL = "https://newsapi.org/v2"
    MAX_ARTICLES_PER_REQUEST = 100
    
    # AI Settings
    OPENAI_MODEL = "gpt-4"
    MAX_SUMMARY_LENGTH = 300
    
    # Cache Settings
    CACHE_DURATION_MINUTES = 30
    
    # CORS Settings
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://your-frontend-domain.com"
    ]
    
    # AWS RDS SSL Settings
    DB_SSL_MODE = os.getenv("DB_SSL_MODE", "require")
    DB_SSL_CERT = os.getenv("DB_SSL_CERT", None)  # Path to RDS CA certificate

settings = Settings()
