import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'recoverai-secure-dev-secret-key-32bytes-long-min')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///recoverai.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'recoverai-jwt-super-secret-key-at-least-32-chars-long')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600'))
    )
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

    # AI
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'mock')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')

    # Recovery Settings
    HIGH_VALUE_THRESHOLD = float(os.getenv('HIGH_VALUE_THRESHOLD', '10000'))
    REMINDER_COOLDOWN_HOURS = int(os.getenv('REMINDER_COOLDOWN_HOURS', '48'))
    MAX_AUTO_REMINDER_AMOUNT = float(os.getenv('MAX_AUTO_REMINDER_AMOUNT', '5000'))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=300)


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
