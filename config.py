from dotenv import load_dotenv
import os
from dataclasses import dataclass
from typing import Literal

@dataclass
class Config:
    """Application configuration from environment variables"""
    
    version: str
    app_title: str
    phase: Literal['DEV', 'PROD', 'TEST']
    theme: Literal['dark', 'light']
    database: str
    debug: bool
    port: int
    
    @classmethod
    def load_config(cls) -> 'Config':
        """Load configuration from .env file"""
        load_dotenv()
        
        return cls(
            version=os.getenv('VERSION', '0.1.0'),
            app_title=os.getenv('APP_TITLE', 'TwirTee'),
            phase=os.getenv('PHASE', 'DEV'),
            theme=os.getenv('THEME', 'dark'),
            database=os.getenv('DATABASE', 'sqlite:///data.db'),
            debug=os.getenv('DEBUG', 'False').lower() == 'true',
            port=int(os.getenv('PORT', '5000'))
        )
