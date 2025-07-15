from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from database import get_db
from models import Article, ArticleFilter, NewsStats, TrendingTopic
from services.news_service import news_service
from services.ai_service import ai_service

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/articles", response_model=List[Article])
async def get_articles(
    region: Optional[str] = Query("Global", description="Region filter"),
    topic: Optional[str] = Query(None, description="Topic filter"),
    source: Optional[str] = Query(None, description="Source filter"),
    date_range: Optional[str] = Query("Today", description="Date range filter"),
    search_query: Optional[str] = Query(None, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Articles per page"),
    db: Session = Depends(get_db)
):
    """Get filtered news articles"""
    try:
        filters = ArticleFilter(
            region=region,
            topic=topic,
            source=source,
            date_range=date_range,
            search_query=search_query,
            page=page,
            limit=limit
        )
        
        articles = await news_service.fetch_news(filters)
        return articles
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")

@router.get("/trending", response_model=List[TrendingTopic])
async def get_trending_topics():
    """Get trending topics"""
    try:
        # Fetch recent articles to analyze trends
        filters = ArticleFilter(limit=100)
        articles = await news_service.fetch_news(filters)
        
        # Convert to dict format for AI service
        articles_dict = [
            {
                "topic": article.topic.value,
                "title": article.title,
                "like_count": article.like_count,
                "view_count": article.view_count
            }
            for article in articles
        ]
        
        insights = await ai_service.generate_trending_insights(articles_dict)
        trending_topics = insights.get("trending_topics", [])
        
        return [
            TrendingTopic(
                name=topic["name"],
                count=topic["count"],
                trend_type=topic["trend_type"],
                emoji=topic["emoji"]
            )
            for topic in trending_topics
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending topics: {str(e)}")

@router.get("/stats", response_model=NewsStats)
async def get_news_stats():
    """Get news statistics"""
    try:
        # Fetch articles for stats
        filters = ArticleFilter(limit=100)
        articles = await news_service.fetch_news(filters)
        
        # Calculate statistics
        total_articles = len(articles)
        articles_by_topic = {}
        articles_by_source = {}
        
        for article in articles:
            topic = article.topic.value
            source = article.source.name
            
            articles_by_topic[topic] = articles_by_topic.get(topic, 0) + 1
            articles_by_source[source] = articles_by_source.get(source, 0) + 1
        
        # Get trending topics
        trending_response = await get_trending_topics()
        
        return NewsStats(
            total_articles=total_articles,
            articles_by_topic=articles_by_topic,
            articles_by_source=articles_by_source,
            trending_topics=trending_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.get("/sources")
async def get_news_sources():
    """Get available news sources"""
    sources = [
        {"name": "TechCrunch", "favicon": "🚀", "color": "from-blue-500 to-cyan-500"},
        {"name": "Reuters", "favicon": "🌍", "color": "from-green-500 to-emerald-500"},
        {"name": "Bloomberg", "favicon": "📈", "color": "from-purple-500 to-pink-500"},
        {"name": "BBC News", "favicon": "📺", "color": "from-red-500 to-orange-500"},
        {"name": "CNN", "favicon": "📰", "color": "from-blue-600 to-indigo-600"},
        {"name": "The Verge", "favicon": "💻", "color": "from-purple-600 to-blue-600"},
        {"name": "ESPN", "favicon": "⚽", "color": "from-orange-500 to-red-500"},
        {"name": "Variety", "favicon": "🎬", "color": "from-pink-500 to-purple-500"},
    ]
    return sources

@router.post("/articles/{article_id}/view")
async def increment_view_count(article_id: str):
    """Increment view count for an article"""
    # In a real implementation, you'd update the database
    return {"message": "View count incremented", "article_id": article_id}

@router.post("/articles/{article_id}/like")
async def toggle_like(article_id: str):
    """Toggle like status for an article"""
    # In a real implementation, you'd update the database
    return {"message": "Like toggled", "article_id": article_id}
