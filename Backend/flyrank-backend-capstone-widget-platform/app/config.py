from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./widget_platform.db"
    app_env: str = "development"

    rate_limit_per_minute: int = 10

    geo_provider_a_down: bool = False
    geo_provider_b_down: bool = False

    email_should_fail: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
