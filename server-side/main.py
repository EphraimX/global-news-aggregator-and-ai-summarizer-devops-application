from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from routers.ai import router as ai_router
from routers.news import router as news_router

app = FastAPI(
    title="📰 Global News Digest AI",
    description="A modern news API powered by AI for summarization and analytics.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",  # or the port your frontend uses
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust based on your deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_router)
app.include_router(news_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Global News Digest AI API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
