from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, timedelta
from typing import List, Optional
import logging

from database import ArticleDB, UserInteractionDB, TrendingTopicDB, get_async_db
from models import Article, NewsSource, TopicEnum, ArticleFilter

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.db = None
    
    async def init_db(self):
        """Initialize async database connection"""
        self.db = await get_async_db()
    
    async def save_articles(self, articles: List[Article]) -> bool:
        """Save articles to RDS database"""
        try:
            if not self.db:
                await self.init_db()
            
            for article in articles:
                # Check if article already exists
                existing_query = """
                SELECT id FROM articles WHERE url = :url
                """
                existing = await self.db.fetch_one(existing_query, {"url": str(article.url)})
                
                if not existing:
                    # Insert new article
                    insert_query = """
                    INSERT INTO articles (
                        id, title, source_name, source_favicon, source_color,
                        original_excerpt, published_at, topic, url, image_url,
                        view_count, like_count, region
                    ) VALUES (
                        :id, :title, :source_name, :source_favicon, :source_color,
                        :original_excerpt, :published_at, :topic, :url, :image_url,
                        :view_count, :like_count, :region
                    )
                    """
                    
                    values = {
                        "id": article.id,
                        "title": article.title,
                        "source_name": article.source.name,
                        "source_favicon": article.source.favicon,
                        "source_color": article.source.color,
                        "original_excerpt": article.original_excerpt,
                        "published_at": article.published_at,
                        "topic": article.topic.value,
                        "url": str(article.url),
                        "image_url": str(article.image_url) if article.image_url else None,
                        "view_count": article.view_count,
                        "like_count": article.like_count,
                        "region": "Global"
                    }
                    
                    await self.db.execute(insert_query, values)
            
            logger.info(f"✅ Saved {len(articles)} articles to RDS")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving articles to RDS: {e}")
            return False
    
    async def get_articles_from_db(self, filters: ArticleFilter) -> List[Article]:
        """Get articles from RDS database with filters"""
        try:
            if not self.db:
                await self.init_db()
            
            # Build query with filters
            where_conditions = []
            query_params = {}
            
            # Topic filter
            if filters.topic and filters.topic != "All":
                where_conditions.append("topic = :topic")
                query_params["topic"] = filters.topic
            
            # Search query filter
            if filters.search_query:
                where_conditions.append("(title ILIKE :search OR original_excerpt ILIKE :search)")
                query_params["search"] = f"%{filters.search_query}%"
            
            # Date range filter
            if filters.date_range:
                date_from = self._get_date_from_range(filters.date_range)
                where_conditions.append("published_at >= :date_from")
                query_params["date_from"] = date_from
            
            # Source filter
            if filters.source and filters.source != "All":
                where_conditions.append("source_name = :source")
                query_params["source"] = filters.source
            
            # Build final query
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            query = f"""
            SELECT * FROM articles 
            WHERE {where_clause}
            ORDER BY published_at DESC
            LIMIT :limit OFFSET :offset
            """
            
            query_params["limit"] = filters.limit
            query_params["offset"] = (filters.page - 1) * filters.limit
            
            rows = await self.db.fetch_all(query, query_params)
            
            # Convert to Article objects
            articles = []
            for row in rows:
                article = Article(
                    id=row["id"],
                    title=row["title"],
                    source=NewsSource(
                        name=row["source_name"],
                        favicon=row["source_favicon"],
                        color=row["source_color"]
                    ),
                    original_excerpt=row["original_excerpt"],
                    summary=row["summary"],
                    published_at=row["published_at"],
                    topic=TopicEnum(row["topic"]),
                    url=row["url"],
                    image_url=row["image_url"],
                    view_count=row["view_count"],
                    like_count=row["like_count"]
                )
                articles.append(article)
            
            logger.info(f"✅ Retrieved {len(articles)} articles from RDS")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Error getting articles from RDS: {e}")
            return []
    
    async def update_article_summary(self, article_id: str, summary: str) -> bool:
        """Update article summary in RDS"""
        try:
            if not self.db:
                await self.init_db()
            
            query = """
            UPDATE articles 
            SET summary = :summary, updated_at = :updated_at
            WHERE id = :article_id
            """
            
            values = {
                "summary": summary,
                "updated_at": datetime.utcnow(),
                "article_id": article_id
            }
            
            await self.db.execute(query, values)
            logger.info(f"✅ Updated summary for article {article_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating article summary: {e}")
            return False
    
    async def track_interaction(self, article_id: str, interaction_type: str, user_ip: str = None) -> bool:
        """Track user interactions in RDS"""
        try:
            if not self.db:
                await self.init_db()
            
            # Insert interaction record
            insert_query = """
            INSERT INTO user_interactions (article_id, interaction_type, user_ip)
            VALUES (:article_id, :interaction_type, :user_ip)
            """
            
            await self.db.execute(insert_query, {
                "article_id": article_id,
                "interaction_type": interaction_type,
                "user_ip": user_ip
            })
            
            # Update article counters
            if interaction_type == "view":
                update_query = "UPDATE articles SET view_count = view_count + 1 WHERE id = :article_id"
            elif interaction_type == "like":
                update_query = "UPDATE articles SET like_count = like_count + 1 WHERE id = :article_id"
            else:
                return True
            
            await self.db.execute(update_query, {"article_id": article_id})
            logger.info(f"✅ Tracked {interaction_type} for article {article_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error tracking interaction: {e}")
            return False
    
    async def get_trending_topics(self) -> List[dict]:
        """Get trending topics from RDS"""
        try:
            if not self.db:
                await self.init_db()
            
            # Get topic counts from recent articles
            query = """
            SELECT 
                topic,
                COUNT(*) as count,
                SUM(view_count) as total_views,
                SUM(like_count) as total_likes
            FROM articles 
            WHERE published_at >= :date_from
            GROUP BY topic
            ORDER BY (COUNT(*) + SUM(view_count) * 0.1 + SUM(like_count) * 0.5) DESC
            LIMIT 10
            """
            
            date_from = datetime.utcnow() - timedelta(days=7)
            rows = await self.db.fetch_all(query, {"date_from": date_from})
            
            trending_topics = []
            emoji_map = {
                "Technology": "💻",
                "World": "🌍",
                "Business": "💼",
                "Science": "🔬",
                "Sports": "⚽",
                "Entertainment": "🎬",
                "Politics": "🏛️"
            }
            
            for i, row in enumerate(rows):
                trend_type = "hot" if i == 0 else "trending" if i < 3 else "rising"
                trending_topics.append({
                    "name": row["topic"],
                    "count": row["count"],
                    "trend_type": trend_type,
                    "emoji": emoji_map.get(row["topic"], "📰"),
                    "total_views": row["total_views"],
                    "total_likes": row["total_likes"]
                })
            
            logger.info(f"✅ Retrieved {len(trending_topics)} trending topics from RDS")
            return trending_topics
            
        except Exception as e:
            logger.error(f"❌ Error getting trending topics: {e}")
            return []
    
    async def get_statistics(self) -> dict:
        """Get comprehensive statistics from RDS"""
        try:
            if not self.db:
                await self.init_db()
            
            # Total articles
            total_query = "SELECT COUNT(*) as total FROM articles"
            total_result = await self.db.fetch_one(total_query)
            total_articles = total_result["total"] if total_result else 0
            
            # Articles by topic
            topic_query = """
            SELECT topic, COUNT(*) as count 
            FROM articles 
            GROUP BY topic 
            ORDER BY count DESC
            """
            topic_results = await self.db.fetch_all(topic_query)
            articles_by_topic = {row["topic"]: row["count"] for row in topic_results}
            
            # Articles by source
            source_query = """
            SELECT source_name, COUNT(*) as count 
            FROM articles 
            GROUP BY source_name 
            ORDER BY count DESC
            LIMIT 10
            """
            source_results = await self.db.fetch_all(source_query)
            articles_by_source = {row["source_name"]: row["count"] for row in source_results}
            
            return {
                "total_articles": total_articles,
                "articles_by_topic": articles_by_topic,
                "articles_by_source": articles_by_source
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting statistics: {e}")
            return {"total_articles": 0, "articles_by_topic": {}, "articles_by_source": {}}
    
    def _get_date_from_range(self, date_range: str) -> datetime:
        """Convert date range to datetime"""
        now = datetime.utcnow()
        if date_range == "Today":
            return now - timedelta(days=1)
        elif date_range == "Last 7 days":
            return now - timedelta(days=7)
        elif date_range == "Last 30 days":
            return now - timedelta(days=30)
        return now - timedelta(days=1)

# Global instance
db_service = DatabaseService()
