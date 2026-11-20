from pydantic_settings import BaseSettings, SettingsConfigDict
 
 
class ServiceSettings(BaseSettings):
    """Settings every service shares. Read from environment variables or a .env file.
 
    A service can extend it:  class Settings(ServiceSettings): database_url: str
    """
 
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "familymeet-service"
    environment: str = "dev"
    log_level: str = "INFO"
    request_timeout_seconds: float = 3.0
    retry_attempts: int = 3
    jwt_secret: str = "change-me-for-local-development-only"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
