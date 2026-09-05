from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://vocalis:vocalis_pass@localhost:3306/vocalis_db"
    ZEEBE_GATEWAY: str = "localhost:26500"
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_EXPIRATION_HOURS: int = 24
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]
    
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
