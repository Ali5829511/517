# utils.py - منطق التكرار والمخالفات والإعدادات
# Utilities for Violations Detection and Configuration

import os
from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from models import Vehicle, Camera, Event, Violation

# قراءة الإعدادات من المتغيرات البيئية
# Read configuration from environment variables
CONFIDENCE_MIN = float(os.getenv("CONFIDENCE_MIN", "80"))
REPEAT_THRESHOLD_COUNT = int(os.getenv("REPEAT_THRESHOLD_COUNT", "3"))
REPEAT_WINDOW_HOURS = int(os.getenv("REPEAT_WINDOW_HOURS", "24"))
ALLOWED_START = os.getenv("ALLOWED_START", "06:00")
ALLOWED_END = os.getenv("ALLOWED_END", "22:00")
PERMIT_REQUIRED = os.getenv("PERMIT_REQUIRED", "false").lower() == "true"


def parse_time(t: str) -> time:
    """
    تحويل النص إلى كائن وقت
    Convert string to time object
    """
    h, m = map(int, t.split(":"))
    return time(hour=h, minute=m)


def ensure_vehicle(
    db: Session, plate: str, make=None, color=None, type_=None
) -> Vehicle:
    """
    التأكد من وجود المركبة أو إنشائها
    Ensure vehicle exists or create it
    """
    v = db.query(Vehicle).filter_by(plate_number=plate).first()
    if not v:
        v = Vehicle(plate_number=plate, make=make, color=color, type=type_)
        db.add(v)
        db.flush()
    else:
        # تحديث البيانات الوصفية إذا كانت موجودة
        # Update metadata if present
        if make:
            v.make = make
        if color:
            v.color = color
        if type_:
            v.type = type_
    return v


def ensure_camera(db: Session, camera_id: str) -> Camera:
    """
    التأكد من وجود الكاميرا أو إنشائها
    Ensure camera exists or create it
    """
    c = db.query(Camera).filter_by(camera_id=camera_id).first()
    if not c:
        c = Camera(camera_id=camera_id)
        db.add(c)
        db.flush()
    return c


def record_event(
    db: Session,
    plate: str,
    ts: datetime,
    camera_id: str,
    confidence: float,
    image_url=None,
    make=None,
    color=None,
    type_=None,
) -> Event:
    """
    تسجيل حدث تعرف جديد
    Record a new recognition event
    """
    if confidence < CONFIDENCE_MIN:
        return None  # تجاهل الأحداث ذات الثقة المنخفضة
    v = ensure_vehicle(db, plate, make, color, type_)
    c = ensure_camera(db, camera_id)
    ev = Event(
        vehicle_id=v.id,
        camera_id=c.id,
        timestamp=ts,
        confidence=confidence,
        image_url=image_url,
        make=make,
        color=color,
        type=type_,
    )
    db.add(ev)
    db.flush()
    return ev


def within_allowed_hours(ts: datetime) -> bool:
    """
    التحقق من أن الوقت ضمن الساعات المسموحة
    Check if time is within allowed hours
    """
    start = parse_time(ALLOWED_START)
    end = parse_time(ALLOWED_END)
    tt = ts.time()
    return start <= tt <= end


def update_repeat_violations(db: Session, vehicle_id: int, now: datetime):
    """
    تحديث مخالفات التكرار للمركبة
    Update repeat violations for vehicle
    """
    window_start = now - timedelta(hours=REPEAT_WINDOW_HOURS)
    count = (
        db.query(Event)
        .filter(
            Event.vehicle_id == vehicle_id,
            Event.timestamp >= window_start,
            Event.timestamp <= now,
        )
        .count()
    )
    # الحصول على مخالفة التكرار المفتوحة
    # Get open repeat violation
    viol = (
        db.query(Violation)
        .filter(
            Violation.vehicle_id == vehicle_id,
            Violation.violation_type == "repeat",
            Violation.status == "open",
        )
        .first()
    )
    if count >= REPEAT_THRESHOLD_COUNT:
        if not viol:
            viol = Violation(
                vehicle_id=vehicle_id,
                violation_type="repeat",
                start_time=window_start,
                end_time=None,
                count=count,
                status="open",
                notes=f"ظهور >= {REPEAT_THRESHOLD_COUNT} مرات في {REPEAT_WINDOW_HOURS} ساعة",
            )
            db.add(viol)
        else:
            viol.count = count
            viol.end_time = now
    else:
        # إغلاق المخالفة إذا كان العدد أقل من العتبة
        # Close violation if below threshold
        if viol:
            viol.status = "closed"
            viol.end_time = now


def register_unauthorized_entry(db: Session, ev: Event):
    """
    تسجيل مخالفة دخول غير مصرح به
    Register unauthorized entry violation
    """
    # مثال: إذا كان خارج الساعات المسموحة -> غير مصرح إلا إذا كان معفى
    # Example: if outside allowed hours -> unauthorized unless exempt
    if not within_allowed_hours(ev.timestamp):
        viol = Violation(
            vehicle_id=ev.vehicle_id,
            violation_type="unauthorized_entry",
            start_time=ev.timestamp,
            end_time=ev.timestamp,
            count=1,
            status="open",
            notes="دخول خارج الساعات المسموحة",
        )
        db.add(viol)
