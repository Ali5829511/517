# models.py - نماذج SQLAlchemy لنظام التعرف على اللوحات
# SQLAlchemy Models for Plate Recognition System

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    Index,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Vehicle(Base):
    """نموذج المركبة - Vehicle Model"""

    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    plate_number = Column(String(32), unique=True, index=True, nullable=False)
    make = Column(String(64))  # الشركة المصنعة
    color = Column(String(64))  # اللون
    type = Column(String(64))  # النوع
    events = relationship("Event", back_populates="vehicle", cascade="all, delete-orphan")
    violations = relationship(
        "Violation", back_populates="vehicle", cascade="all, delete-orphan"
    )


class Camera(Base):
    """نموذج الكاميرا - Camera Model"""

    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True)
    camera_id = Column(String(64), unique=True, index=True, nullable=False)
    location = Column(String(128))  # الموقع


class Event(Base):
    """نموذج حدث التعرف - Recognition Event Model"""

    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    confidence = Column(Float, nullable=False)  # نسبة الثقة
    image_url = Column(Text)  # رابط الصورة
    # Snapshot metadata - البيانات الوصفية
    make = Column(String(64))
    color = Column(String(64))
    type = Column(String(64))

    vehicle = relationship("Vehicle", back_populates="events")
    camera = relationship("Camera")


# Create composite index for efficient querying
Index("ix_event_vehicle_time", Event.vehicle_id, Event.timestamp)


class Violation(Base):
    """نموذج المخالفة - Violation Model"""

    __tablename__ = "violations"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True)
    violation_type = Column(
        String(64), index=True
    )  # نوع المخالفة: repeat, unauthorized_entry, etc.
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime)
    count = Column(Integer, default=0)  # عدد التكرار في الفترة
    status = Column(String(32), default="open")  # الحالة: open, reviewing, closed
    notes = Column(Text)  # ملاحظات

    vehicle = relationship("Vehicle", back_populates="violations")
