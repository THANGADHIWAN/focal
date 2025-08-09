from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from enum import Enum
from typing import List, Union
import json


class DBDriverEnum(str, Enum):
    postgresql = "postgresql"
    mysql = "mysql"
    sqlite = "sqlite"


class Settings(BaseSettings):
    # Database
    db_driver: DBDriverEnum = Field(..., env="DB_DRIVER")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")

    @property
    def database_url(self) -> str:
        """
        Constructs the database URL from individual components with proper SQLAlchemy dialect
        """
        driver_mapping = {
            "postgresql": "postgresql+psycopg2",
            "mysql": "mysql+pymysql",
            "sqlite": "sqlite"
        }
        dialect = driver_mapping.get(self.db_driver.value, self.db_driver.value)
        return f"{dialect}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # Application
    app_name: str = Field(..., env="APP_NAME")
    app_version: str = Field(..., env="APP_VERSION")
    debug: bool = Field(..., env="DEBUG")
    host: str = Field(..., env="HOST")
    port: int = Field(..., env="PORT")

    # CORS
    allowed_origins: Union[List[str], str] = Field(default=["*"], env="ALLOWED_ORIGINS")

    @field_validator("allowed_origins", mode="before")
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)  # If passed as JSON string
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]  # Fallback: comma-separated string
        return v

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    api_prefix: str = Field(default="/api", env="API_PREFIX")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance and getter function for dependency injection
settings = Settings()

def get_settings() -> Settings:
    """
    Returns the settings instance for dependency injection.
    """
    return settings
