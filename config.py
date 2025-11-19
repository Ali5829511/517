"""
Development Configuration
إعدادات التطوير
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Flask Configuration


class DevelopmentConfig:
    """Development configuration"""

    # Flask
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # Server
    HOST = "0.0.0.0"
    PORT = 5000

    # Database
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "housing_database.db")
    DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

    # Upload folders
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    PROCESSED_FOLDER = os.environ.get("PROCESSED_FOLDER", "processed_images")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # Session
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # OpenAI
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_AVAILABLE = bool(OPENAI_API_KEY and OPENAI_API_KEY != "your-api-key-here")

    # GitHub
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
    GITHUB_AVAILABLE = bool(GITHUB_TOKEN and GITHUB_TOKEN != "your-github-token-here")

    # ParkPow API
    PARKPOW_API_TOKEN = os.environ.get("PARKPOW_API_TOKEN", "")
    PARKPOW_AVAILABLE = bool(PARKPOW_API_TOKEN and PARKPOW_API_TOKEN != "your-parkpow-token-here")

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("LOG_FILE", "logs/app.log")

    # Development-specific
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable caching


class TestingConfig(DevelopmentConfig):
    """Testing configuration"""

    TESTING = True
    DEBUG = True
    DATABASE_PATH = ":memory:"  # Use in-memory database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    SESSION_COOKIE_SECURE = True  # Always require secure cookies in tests


class ProductionConfig:
    """Production configuration"""

    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Server
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 8000))

    # Database
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "housing_database.db")
    DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

    # Upload folders
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    PROCESSED_FOLDER = os.environ.get("PROCESSED_FOLDER", "processed_images")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # Session
    SESSION_COOKIE_SECURE = True  # Require HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"
    PERMANENT_SESSION_LIFETIME = 3600

    # OpenAI
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_AVAILABLE = bool(OPENAI_API_KEY)

    # GitHub
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    GITHUB_AVAILABLE = bool(GITHUB_TOKEN)

    # ParkPow API
    PARKPOW_API_TOKEN = os.environ.get("PARKPOW_API_TOKEN")
    PARKPOW_AVAILABLE = bool(PARKPOW_API_TOKEN)

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")
    LOG_FILE = os.environ.get("LOG_FILE", "logs/app.log")

    # Production-specific
    TEMPLATES_AUTO_RELOAD = False
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year caching


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")
    return config.get(env, config["default"])
