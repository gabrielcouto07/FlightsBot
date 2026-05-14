"""Pydantic Settings configuration for Flight Bot"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "flight-bot"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./flight_bot.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Kiwi.com Tequila API
    kiwi_api_key: str
    kiwi_api_base: str = "https://api.tequila.kiwi.com"
    kiwi_request_timeout: int = 30
    
    # WhatsApp Evolution API
    evolution_api_url: str
    evolution_api_key: str
    evolution_instance_name: str = "flight-bot"
    
    # WhatsApp Groups
    free_group_jid: str
    
    # Scheduler Configuration
    scan_interval_minutes: int = 120
    free_digest_interval_hours: int = 6
    
    # Price Thresholds (in BRL)
    default_deal_threshold_domestic_brl: float = 299.0
    default_deal_threshold_intl_brl: float = 1499.0
    
    # Anti-spam Configuration
    alert_cooldown_hours: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
