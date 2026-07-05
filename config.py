import logging
import sys
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolves the directory where config.py lives, always
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    app_name: str
    groq_api_key: str
    tavily_key:str
    database_url:str
    max_retries: int = 3
    debug_mode: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

settings = Settings()

# Logger
logger = logging.getLogger("Lead_Extraction")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# File Handler
file_handler = logging.FileHandler(BASE_DIR / "data_extraction.log")
file_handler.setFormatter(formatter)

# # Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)