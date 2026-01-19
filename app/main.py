"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine, init_db

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="OldGoods Marketplace API - Marketplace for students and residents",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    # init_db()  # Uncomment để auto-create tables (không khuyến khích trong production)
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    pass


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to OldGoods Marketplace API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Import routers (sẽ được tạo sau)
# from app.api.v1 import auth, listings, chat, deals, moderation
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(listings.router, prefix="/api/v1/listings", tags=["listings"])
# app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
# app.include_router(deals.router, prefix="/api/v1/deals", tags=["deals"])
# app.include_router(moderation.router, prefix="/api/v1/moderation", tags=["moderation"])
