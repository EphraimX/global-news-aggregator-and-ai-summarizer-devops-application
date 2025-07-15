from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TopicEnum(str, Enum):
    WORLD = "World"
    POLITICS = "Politics"
    TECHNOLOGY = "Technology"
    BUSINESS = "Business"
    SCIENCE = "Science"
    ENTERTAINMENT = "Entertainment"
    SPORTS = "Sports"

class RegionEnum(str, Enum):
    GLOBAL = "Global"
    US = "US"
    EU = "EU"
    ASIA = "Asia"
    AFRICA = "Africa"

class DateRangeEnum(str, Enum):
    TODAY = "Today"
    LAST_7_DAYS = "Last 7 days"
    LAST_30_DAYS = "Last 30 days"

class NewsSource(BaseModel):
    name: str
    favicon: str
    color: str

class Article(BaseModel):
    id: str
    title: str
    source: NewsSource
    original_excerpt: str
    summary: Optional[str] = None
    published_at: datetime
    topic: TopicEnum
    url: HttpUrl
    image_url: Optional[HttpUrl] = None
    is_loading_summary: bool = False
    view_count: int = 0
    like_count: int = 0

class ArticleCreate(BaseModel):
    title: str
    source_name: str
    original_excerpt: str
    published_at: datetime
    topic: TopicEnum
    url: HttpUrl
    image_url: Optional[HttpUrl] = None

class ArticleFilter(BaseModel):
    region: Optional[RegionEnum] = RegionEnum.GLOBAL
    topic: Optional[TopicEnum] = None
    source: Optional[str] = None
    date_range: Optional[DateRangeEnum] = DateRangeEnum.TODAY
    search_query: Optional[str] = None
    page: int = 1
    limit: int = 20

class SummaryRequest(BaseModel):
    title: str
    content: str

class SummaryResponse(BaseModel):
    summary: str

class TrendingTopic(BaseModel):
    name: str
    count: int
    trend_type: str  # "hot", "trending", "rising"
    emoji: str

class NewsStats(BaseModel):
    total_articles: int
    articles_by_topic: dict
    articles_by_source: dict
    trending_topics: List[TrendingTopic]

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
