"""
Environment variables & settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    PROJECT_NAME: str = "Pulse"
    API_PREFIX: str = "/api"
    PULSE_ENV: str = "local"
    PULSE_API_PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    # Read database URL from environment
    PULSE_DATABASE_URL: str
    
    # Monitoring Settings
    DEFAULT_CHECK_INTERVAL_MINUTES: int = 5
    MIN_CHECK_INTERVAL_MINUTES: int = 1
    
    # Safety Guardrails (per customer/connection)
    MAX_QUERIES_PER_MINUTE: int = 60
    MAX_CONCURRENT_QUERIES: int = 5
    QUERY_TIMEOUT_SECONDS: int = 2
    
    # Replica Safety
    REPLICA_LAG_THRESHOLD_SECONDS: int = 30
    BACKPRESSURE_ENABLED: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

