# Use the following environment variables, map them into a Python object for easy use and reference in code.

# Allow advanced python type handling (map data to python objs)
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

# Inherit BaseSettings from pydantic_settings
class Settings(BaseSettings):
    # Define your environment variables here (automatically load and be used)
    DATABASE_URL: str
    API_PREFIX: str = "/api" # Default API prefix
    DEBUG: bool = False

    ALLOW_ORIGINS: str = ""
    OPEN_AI_API_KEY: str


    @field_validator('ALLOW_ORIGINS')   # tell pydantic to use this function to process ALLOW_ORIGINS field
    def parse_allowed_origins(cls, value: str) -> List[str]:    # str to list (since env dont allow lists) 
        return value.split(",") if value else []
        # replace what we have in ALLOW_ORIGINS

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# When create this class, auto load environment variables
settings = Settings()