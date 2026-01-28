from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """MCP server configuration."""

    api_base_url: str = "http://localhost:8000"


config = Config()
