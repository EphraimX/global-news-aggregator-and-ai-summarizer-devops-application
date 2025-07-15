import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
import random
import uuid

from config import settings
from models import Article, NewsSource, TopicEnum, ArticleFilter
from services.database_service import db_service

class NewsService:
    def __init__(self):
        self.base_url = settings.NEWS_API_BASE_URL
        self.api_key = settings.NEWS_API_KEY
        
        # Source mappings with emojis and colors
        self.source_mappings = {
            "techcrunch": {"favicon": "🚀", "color": "from-blue-500 to-cyan-500"},
            "reuters": {"favicon": "🌍", "color": "from-green-500 to-emerald-500"},
            "bloomberg": {"favicon": "📈", "color": "from-purple-500 to-pink-500"},
            "bbc-news": {"favicon": "📺", "color": "from-red-500 to-orange-500"},
            "cnn": {"favicon": "📰", "color": "from-blue-600 to-indigo-600"},
            "the-verge": {"favicon": "💻", "color": "from-purple-600 to-blue-600"},
            "espn": {"favicon": "⚽", "color": "from-orange-500 to-red-500"},
            "entertainment-weekly": {"favicon": "🎬", "color": "from-pink-500 to-purple-500"},
        }
        
        # Topic to category mapping for NewsAPI
        self.topic_categories = {
            TopicEnum.WORLD: "general",
            TopicEnum.POLITICS: "general",
            TopicEnum.TECHNOLOGY: "technology",
            TopicEnum.BUSINESS: "business",
            TopicEnum.SCIENCE: "science",
            TopicEnum.ENTERTAINMENT: "entertainment",
            TopicEnum.SPORTS: "sports",
        }

    async def fetch_news(self, filters: ArticleFilter) -> List[Article]:
        """Fetch news from NewsAPI and RDS based on filters"""
        try:
            # First, try to get articles from RDS database
            db_articles = await db_service.get_articles_from_db(filters)
            
            # If we have enough articles from DB and they're recent, return them
            if len(db_articles) >= filters.limit:
                recent_threshold = datetime.now() - timedelta(hours=1)
                recent_articles = [a for a in db_articles if a.published_at > recent_threshold]
                if len(recent_articles) >= filters.limit // 2:  # At least half are recent
                    print(f"✅ Returning {len(db_articles)} articles from RDS cache")
                    return db_articles
        
            # Fetch fresh articles from NewsAPI
            async with httpx.AsyncClient() as client:
                # Build query parameters
                params = {
                    "apiKey": self.api_key,
                    "pageSize": min(filters.limit, settings.MAX_ARTICLES_PER_REQUEST),
                    "page": filters.page,
                    "sortBy": "publishedAt",
                    "language": "en"
                }
                
                # Add category filter
                if filters.topic and filters.topic != "All":
                    category = self.topic_categories.get(filters.topic, "general")
                    params["category"] = category
                
                # Add date range
                if filters.date_range:
                    from_date = self._get_date_from_range(filters.date_range)
                    params["from"] = from_date.isoformat()
                
                # Add search query
                if filters.search_query:
                    params["q"] = filters.search_query
                
                # Add region/country filter
                if filters.region and filters.region != "Global":
                    country_code = self._get_country_code(filters.region)
                    params["country"] = country_code
                    endpoint = f"{self.base_url}/top-headlines"
                else:
                    endpoint = f"{self.base_url}/everything"
                
                # Make API request
                response = await client.get(endpoint, params=params)
                response.raise_for_status()
                
                data = response.json()
                articles = []
                
                for article_data in data.get("articles", []):
                    if not article_data.get("title") or article_data["title"] == "[Removed]":
                        continue
                    
                    article = self._convert_to_article(article_data, filters.topic)
                    articles.append(article)
                
                # After getting articles from NewsAPI, save them to RDS
                if articles:
                    await db_service.save_articles(articles)
            
                # Combine with DB articles if needed
                if db_articles:
                    # Remove duplicates and combine
                    existing_urls = {str(a.url) for a in articles}
                    unique_db_articles = [a for a in db_articles if str(a.url) not in existing_urls]
                    articles.extend(unique_db_articles[:filters.limit - len(articles)])
            
                return articles[:filters.limit]
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            # Fallback to database articles or mock data
            db_articles = await db_service.get_articles_from_db(filters)
            if db_articles:
                return db_articles
            return await self._get_mock_articles(filters)

    async def _get_mock_articles(self, filters: ArticleFilter) -> List[Article]:
        """Generate mock articles for development/fallback"""
        mock_articles = [
            {
                "title": "🚀 Revolutionary AI Breakthrough Changes Healthcare Industry Forever",
                "source": "TechCrunch",
                "content": "Scientists at Stanford University have developed a groundbreaking AI system that can diagnose diseases with 99% accuracy, potentially revolutionizing healthcare worldwide and saving millions of lives.",
                "topic": TopicEnum.TECHNOLOGY,
                "url": "https://example.com/article1",
                "image_url": "https://via.placeholder.com/300x200/4F46E5/FFFFFF?text=AI+Healthcare"
            },
            {
                "title": "🌍 Global Climate Summit Reaches Historic Agreement on Carbon Emissions",
                "source": "Reuters",
                "content": "World leaders have signed a groundbreaking agreement to reduce carbon emissions by 50% within the next decade, marking a significant step in fighting climate change.",
                "topic": TopicEnum.WORLD,
                "url": "https://example.com/article2",
                "image_url": "https://via.placeholder.com/300x200/10B981/FFFFFF?text=Climate+Summit"
            },
            {
                "title": "📈 Stock Markets Surge Following Federal Reserve Decision",
                "source": "Bloomberg",
                "content": "Major stock indices reached record highs after the Federal Reserve announced a surprise interest rate cut, boosting investor confidence across all sectors.",
                "topic": TopicEnum.BUSINESS,
                "url": "https://example.com/article3",
                "image_url": "https://via.placeholder.com/300x200/8B5CF6/FFFFFF?text=Stock+Market"
            },
            {
                "title": "🚀 Space Mission Discovers Potentially Habitable Exoplanet",
                "source": "NASA News",
                "content": "The James Webb Space Telescope has identified a new exoplanet in the habitable zone showing signs of water vapor in its atmosphere.",
                "topic": TopicEnum.SCIENCE,
                "url": "https://example.com/article4",
                "image_url": "https://via.placeholder.com/300x200/F59E0B/FFFFFF?text=Space+Discovery"
            },
            {
                "title": "⚽ Championship Final Breaks Viewership Records Worldwide",
                "source": "ESPN",
                "content": "The World Cup final attracted over 2 billion viewers globally, making it the most-watched sporting event in television history.",
                "topic": TopicEnum.SPORTS,
                "url": "https://example.com/article5",
                "image_url": "https://via.placeholder.com/300x200/EF4444/FFFFFF?text=World+Cup"
            },
            {
                "title": "🎬 New Entertainment Streaming Platform Launches with Exclusive Content",
                "source": "Variety",
                "content": "A major tech company has launched its revolutionary streaming service featuring original series and movies from acclaimed directors.",
                "topic": TopicEnum.ENTERTAINMENT,
                "url": "https://example.com/article6",
                "image_url": "https://via.placeholder.com/300x200/EC4899/FFFFFF?text=Streaming"
            }
        ]
        
        articles = []
        for i, mock_data in enumerate(mock_articles):
            if filters.topic and filters.topic != mock_data["topic"]:
                continue
                
            source_info = self.source_mappings.get(
                mock_data["source"].lower().replace(" ", "-"),
                {"favicon": "📰", "color": "from-blue-500 to-purple-500"}
            )
            
            article = Article(
                id=str(uuid.uuid4()),
                title=mock_data["title"],
                source=NewsSource(
                    name=mock_data["source"],
                    favicon=source_info["favicon"],
                    color=source_info["color"]
                ),
                original_excerpt=mock_data["content"],
                published_at=datetime.now() - timedelta(hours=random.randint(1, 48)),
                topic=mock_data["topic"],
                url=mock_data["url"],
                image_url=mock_data.get("image_url"),
                view_count=random.randint(100, 1000),
                like_count=random.randint(10, 100)
            )
            articles.append(article)
        
        return articles[:filters.limit]

    def _convert_to_article(self, article_data: dict, topic_filter: Optional[TopicEnum]) -> Article:
        """Convert NewsAPI article data to our Article model"""
        source_name = article_data.get("source", {}).get("name", "Unknown")
        source_key = source_name.lower().replace(" ", "-")
        source_info = self.source_mappings.get(source_key, {
            "favicon": "📰", 
            "color": "from-blue-500 to-purple-500"
        })
        
        # Determine topic based on source or use filter
        topic = self._determine_topic(source_name, article_data.get("title", ""))
        if topic_filter and topic_filter != "All":
            topic = topic_filter
        
        return Article(
            id=str(uuid.uuid4()),
            title=article_data.get("title", ""),
            source=NewsSource(
                name=source_name,
                favicon=source_info["favicon"],
                color=source_info["color"]
            ),
            original_excerpt=article_data.get("description", ""),
            published_at=datetime.fromisoformat(
                article_data.get("publishedAt", "").replace("Z", "+00:00")
            ),
            topic=topic,
            url=article_data.get("url", ""),
            image_url=article_data.get("urlToImage"),
            view_count=random.randint(50, 500),
            like_count=random.randint(5, 50)
        )

    def _determine_topic(self, source_name: str, title: str) -> TopicEnum:
        """Determine article topic based on source and title"""
        source_lower = source_name.lower()
        title_lower = title.lower()
        
        if "tech" in source_lower or any(word in title_lower for word in ["ai", "tech", "digital", "software"]):
            return TopicEnum.TECHNOLOGY
        elif "sport" in source_lower or "espn" in source_lower:
            return TopicEnum.SPORTS
        elif "entertainment" in source_lower or "variety" in source_lower:
            return TopicEnum.ENTERTAINMENT
        elif "business" in source_lower or "bloomberg" in source_lower:
            return TopicEnum.BUSINESS
        elif any(word in title_lower for word in ["science", "research", "study", "space"]):
            return TopicEnum.SCIENCE
        elif any(word in title_lower for word in ["election", "government", "politics", "policy"]):
            return TopicEnum.POLITICS
        else:
            return TopicEnum.WORLD

    def _get_date_from_range(self, date_range: str) -> datetime:
        """Convert date range to datetime"""
        now = datetime.now()
        if date_range == "Today":
            return now - timedelta(days=1)
        elif date_range == "Last 7 days":
            return now - timedelta(days=7)
        elif date_range == "Last 30 days":
            return now - timedelta(days=30)
        return now - timedelta(days=1)

    def _get_country_code(self, region: str) -> str:
        """Convert region to country code"""
        region_codes = {
            "US": "us",
            "EU": "gb",  # Use UK as EU representative
            "Asia": "jp",  # Use Japan as Asia representative
            "Africa": "za"  # Use South Africa as Africa representative
        }
        return region_codes.get(region, "us")

# Global instance
news_service = NewsService()
