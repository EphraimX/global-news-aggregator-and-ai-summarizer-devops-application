import openai
from typing import Optional
import asyncio

from config import settings

class AIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.max_length = settings.MAX_SUMMARY_LENGTH

    async def generate_summary(self, title: str, content: str) -> str:
        """Generate AI summary for an article"""
        try:
            # Create a more engaging prompt
            prompt = f"""
            You are a professional news summarizer with a vibrant personality. 
            Create a concise, informative summary that captures the key points of this news article in 1-3 sentences. 
            Focus on the most important facts and implications while maintaining an engaging tone.

            Title: {title}
            Content: {content}

            Provide a clear, concise summary that captures the essential information and significance of this news story. 
            Make it engaging and informative!
            """

            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional news summarizer. Create engaging, concise summaries."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )

            summary = response.choices[0].message.content.strip()
            
            # Ensure summary isn't too long
            if len(summary) > self.max_length:
                summary = summary[:self.max_length] + "..."
            
            return summary

        except Exception as e:
            print(f"Error generating summary: {e}")
            # Return a fallback summary
            return self._generate_fallback_summary(title, content)

    def _generate_fallback_summary(self, title: str, content: str) -> str:
        """Generate a simple fallback summary when AI fails"""
        # Simple extractive summary - take first sentence or two
        sentences = content.split('. ')
        if len(sentences) >= 2:
            return f"{sentences[0]}. {sentences[1]}."
        elif len(sentences) == 1:
            return sentences[0]
        else:
            return "This article discusses important developments in the news."

    async def generate_trending_insights(self, articles: list) -> dict:
        """Generate insights about trending topics"""
        try:
            topics = {}
            for article in articles:
                topic = article.get('topic', 'General')
                topics[topic] = topics.get(topic, 0) + 1
            
            # Sort by frequency
            sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
            
            trending_topics = []
            for i, (topic, count) in enumerate(sorted_topics[:5]):
                trend_type = "hot" if i == 0 else "trending" if i < 3 else "rising"
                emoji_map = {
                    "Technology": "💻",
                    "World": "🌍", 
                    "Business": "💼",
                    "Science": "🔬",
                    "Sports": "⚽",
                    "Entertainment": "🎬",
                    "Politics": "🏛️"
                }
                
                trending_topics.append({
                    "name": topic,
                    "count": count,
                    "trend_type": trend_type,
                    "emoji": emoji_map.get(topic, "📰")
                })
            
            return {"trending_topics": trending_topics}
            
        except Exception as e:
            print(f"Error generating trending insights: {e}")
            return {"trending_topics": []}

# Global instance
ai_service = AIService()
