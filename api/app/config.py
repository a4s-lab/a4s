from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    cors_origins: list[str] = Field(default_factory=list)


config = Config()
