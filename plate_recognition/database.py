# database.py - تهيئة الاتصال بقاعدة البيانات
# Database Connection Initialization

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# قراءة رابط قاعدة البيانات من المتغيرات البيئية
# Read database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./plates.db")

# إنشاء محرك قاعدة البيانات
# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# إنشاء مصنع الجلسات
# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    تهيئة قاعدة البيانات - إنشاء كافة الجداول
    Initialize database - Create all tables
    """
    Base.metadata.create_all(bind=engine)
