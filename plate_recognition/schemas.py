# schemas.py - مخططات Pydantic للتحقق من البيانات
# Pydantic Schemas for Data Validation

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VehicleIn(BaseModel):
    """مخطط إدخال بيانات المركبة - Vehicle Input Schema"""

    plate_number: Optional[str] = None
    make: Optional[str] = None
    color: Optional[str] = None
    type: Optional[str] = None


class EventIn(BaseModel):
    """مخطط إدخال حدث التعرف - Event Input Schema"""

    plate: str
    timestamp: datetime
    camera_id: str
    confidence: float
    image_url: Optional[str] = None
    vehicle: Optional[VehicleIn] = None


class EventOut(BaseModel):
    """مخطط إخراج حدث التعرف - Event Output Schema"""

    id: int
    plate: str
    timestamp: datetime
    camera_id: str
    confidence: float
    image_url: Optional[str] = None
    make: Optional[str] = None
    color: Optional[str] = None
    type: Optional[str] = None

    model_config = {"from_attributes": True}


class ViolationOut(BaseModel):
    """مخطط إخراج المخالفة - Violation Output Schema"""

    id: int
    plate: str
    violation_type: str
    start_time: datetime
    end_time: Optional[datetime]
    count: int
    status: str
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class FilterQuery(BaseModel):
    """مخطط استعلام الفلترة - Filter Query Schema"""

    start: Optional[datetime] = None
    end: Optional[datetime] = None
    camera_id: Optional[str] = None
    plate: Optional[str] = None
    min_confidence: Optional[float] = None


class ExportRequest(BaseModel):
    """مخطط طلب التصدير - Export Request Schema"""

    format: str = Field(pattern="^(excel|pdf|html)$")
    filter: Optional[FilterQuery] = None
