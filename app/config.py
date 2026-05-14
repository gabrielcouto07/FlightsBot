"""Pydantic Settings configuration for Flight Bot."""

from functools import lru_cache
from typing import Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
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
    kiwi_api_key: Optional[str] = None
    kiwi_api_base: str = "https://api.tequila.kiwi.com"
    kiwi_request_timeout: int = 30
    
    # WhatsApp Evolution API
    evolution_api_url: Optional[str] = None
    evolution_api_key: Optional[str] = None
    evolution_instance_name: str = "flight-bot"
    
    # WhatsApp Groups
    free_group_jid: Optional[str] = None
    
    # Scheduler Configuration
    scan_interval_minutes: int = 120
    free_digest_interval_hours: int = 6
    
    # Price Thresholds (in BRL)
    default_deal_threshold_domestic_brl: float = 299.0
    default_deal_threshold_intl_brl: float = 1499.0
    
    # Anti-spam Configuration
    alert_cooldown_hours: int = 24
    
    # Demo Mode Configuration
    demo_mode: bool = True
    whatsapp_enabled: bool = False
    frontend_url: str = "http://localhost:3000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def default_threshold_domestic(self) -> float:
        """Backward-compatible domestic threshold alias."""
        return self.default_deal_threshold_domestic_brl

    @computed_field  # type: ignore[prop-decorator]
    @property
    def default_threshold_intl(self) -> float:
        """Backward-compatible international threshold alias."""
        return self.default_deal_threshold_intl_brl

    @property
    def kiwi_enabled(self) -> bool:
        """Whether Kiwi API credentials are configured."""
        return bool(self.kiwi_api_key)

    @property
    def whatsapp_ready(self) -> bool:
        """Whether WhatsApp delivery is both enabled and configured."""
        return bool(
            self.whatsapp_enabled
            and self.evolution_api_url
            and self.evolution_api_key
        )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
