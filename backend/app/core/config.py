from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "PUBG AI Analyzer"
    ENV: str = "development"
    API_BASE_URL: str = "http://api:8000"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    TELEGRAM_BOT_TOKEN: str = ""
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    RATE_LIMIT_PER_MINUTE: int = 30
    FREE_DAILY_LIMIT: int = 5
    PRO_DAILY_LIMIT: int = 100
    PREMIUM_DAILY_LIMIT: int = 1000

    class Config:
        env_file = ".env"

settings = Settings()
