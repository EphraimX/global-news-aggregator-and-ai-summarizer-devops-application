from fastapi import APIRouter, HTTPException
from models import SummaryRequest, SummaryResponse
from services.ai_service import ai_service

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_article(request: SummaryRequest):
    """Generate AI summary for an article"""
    try:
        if not request.title or not request.content:
            raise HTTPException(status_code=400, detail="Title and content are required")
        
        summary = await ai_service.generate_summary(request.title, request.content)
        
        return SummaryResponse(summary=summary)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@router.post("/analyze-sentiment")
async def analyze_sentiment(text: str):
    """Analyze sentiment of text (placeholder for future feature)"""
    # This could be implemented with additional AI models
    return {
        "sentiment": "positive",
        "confidence": 0.85,
        "message": "Sentiment analysis feature coming soon!"
    }

@router.post("/generate-tags")
async def generate_tags(title: str, content: str):
    """Generate relevant tags for an article (placeholder for future feature)"""
    # This could be implemented with additional AI models
    sample_tags = ["breaking news", "technology", "innovation", "global impact"]
    return {
        "tags": sample_tags,
        "message": "Tag generation feature coming soon!"
    }
