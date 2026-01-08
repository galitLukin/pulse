"""
FastAPI app entrypoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import health, tables, connections, alerts
from app.startup import on_startup, on_shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Real-time data health monitoring via read replicas",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health.router, prefix=settings.API_PREFIX, tags=["health"])
app.include_router(tables.router, prefix=f"{settings.API_PREFIX}/tables", tags=["tables"])
app.include_router(connections.router, prefix=f"{settings.API_PREFIX}/connections", tags=["connections"])
app.include_router(alerts.router, prefix=f"{settings.API_PREFIX}/alerts", tags=["alerts"])


@app.on_event("startup")
async def startup_event():
    """Startup hooks"""
    await on_startup()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown hooks"""
    await on_shutdown()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "healthy"
    }

