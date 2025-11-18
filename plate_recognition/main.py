# main.py - تطبيق FastAPI الرئيسي
# Main FastAPI Application

import os
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, Query, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Event, Vehicle, Violation, Camera
from schemas import EventIn, EventOut, ViolationOut, FilterQuery, ExportRequest
from utils import (
    record_event,
    update_repeat_violations,
    register_unauthorized_entry,
)
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق - Application Lifespan Management"""
    # Startup
    init_db()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="نظام تحليل اللوحات - Plate Analyzer",
    description="نظام متكامل للتعرف على اللوحات وتتبع المخالفات",
    version="1.0.0",
    lifespan=lifespan,
)

# إعداد القوالب
# Setup templates
templates = Jinja2Templates(directory="templates")


def get_db():
    """
    الحصول على جلسة قاعدة البيانات
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    camera_id: Optional[str] = Query(None),
    plate: Optional[str] = Query(None),
    min_confidence: Optional[float] = Query(None),
):
    """
    الصفحة الرئيسية العربية
    Arabic Main Page
    """
    q = (
        db.query(Event, Vehicle, Camera)
        .join(Vehicle, Event.vehicle_id == Vehicle.id)
        .join(Camera, Event.camera_id == Camera.id)
    )
    if start:
        q = q.filter(Event.timestamp >= start)
    if end:
        q = q.filter(Event.timestamp <= end)
    if plate:
        q = q.filter(Vehicle.plate_number == plate)
    if camera_id:
        q = q.filter(Camera.camera_id == camera_id)
    if min_confidence:
        q = q.filter(Event.confidence >= min_confidence)

    rows = []
    for ev, v, c in q.order_by(Event.timestamp.desc()).limit(500).all():
        rows.append(
            {
                "id": ev.id,
                "plate": v.plate_number,
                "timestamp": ev.timestamp,
                "confidence": ev.confidence,
                "type": ev.type or v.type,
                "make": ev.make or v.make,
                "color": ev.color or v.color,
                "camera_id": c.camera_id,
                "image_url": ev.image_url,
            }
        )

    violations = (
        db.query(Violation, Vehicle)
        .join(Vehicle, Violation.vehicle_id == Vehicle.id)
        .order_by(Violation.start_time.desc())
        .limit(100)
        .all()
    )
    viols = [
        {
            "id": vli.id,
            "plate": veh.plate_number,
            "type": vli.violation_type,
            "start_time": vli.start_time,
            "end_time": vli.end_time,
            "count": vli.count,
            "status": vli.status,
            "notes": vli.notes,
        }
        for vli, veh in violations
    ]

    return templates.TemplateResponse(
        request=request, name="index.html", context={"rows": rows, "viols": viols}
    )


@app.post("/api/webhook/plate", response_model=EventOut)
def webhook_plate(payload: EventIn, db: Session = Depends(get_db)):
    """
    استقبال Webhook من نظام التعرف على اللوحات
    Receive Webhook from Plate Recognition System
    """
    veh = payload.vehicle or None
    ev = record_event(
        db=db,
        plate=payload.plate,
        ts=payload.timestamp,
        camera_id=payload.camera_id,
        confidence=payload.confidence,
        image_url=payload.image_url,
        make=veh.make if veh else None,
        color=veh.color if veh else None,
        type_=veh.type if veh else None,
    )
    if ev is None:
        return JSONResponse(
            status_code=202, content={"detail": "تم التجاهل: الثقة أقل من الحد المطلوب"}
        )

    register_unauthorized_entry(db, ev)
    update_repeat_violations(db, ev.vehicle_id, payload.timestamp)
    db.commit()

    return EventOut(
        id=ev.id,
        plate=payload.plate,
        timestamp=payload.timestamp,
        camera_id=payload.camera_id,
        confidence=payload.confidence,
        image_url=payload.image_url,
        make=ev.make,
        color=ev.color,
        type=ev.type,
    )


@app.get("/api/events")
def list_events(
    db: Session = Depends(get_db),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    camera_id: Optional[str] = Query(None),
    plate: Optional[str] = Query(None),
    min_confidence: Optional[float] = Query(None),
):
    """
    استعلام الأحداث مع الفلترة
    Query events with filtering
    """
    q = (
        db.query(Event, Vehicle, Camera)
        .join(Vehicle, Event.vehicle_id == Vehicle.id)
        .join(Camera, Event.camera_id == Camera.id)
    )
    if start:
        q = q.filter(Event.timestamp >= start)
    if end:
        q = q.filter(Event.timestamp <= end)
    if plate:
        q = q.filter(Vehicle.plate_number == plate)
    if camera_id:
        q = q.filter(Camera.camera_id == camera_id)
    if min_confidence:
        q = q.filter(Event.confidence >= min_confidence)
    data = []
    for ev, v, c in q.order_by(Event.timestamp.desc()).limit(1000).all():
        data.append(
            {
                "id": ev.id,
                "plate": v.plate_number,
                "timestamp": ev.timestamp.isoformat(),
                "camera_id": c.camera_id,
                "confidence": ev.confidence,
                "image_url": ev.image_url,
                "type": ev.type or v.type,
                "make": ev.make or v.make,
                "color": ev.color or v.color,
            }
        )
    return data


@app.get("/api/violations", response_model=list[ViolationOut])
def list_violations(db: Session = Depends(get_db)):
    """
    استعلام المخالفات
    Query violations
    """
    viols = (
        db.query(Violation, Vehicle)
        .join(Vehicle, Violation.vehicle_id == Vehicle.id)
        .order_by(Violation.start_time.desc())
        .all()
    )
    return [
        ViolationOut(
            id=v.id,
            plate=veh.plate_number,
            violation_type=v.violation_type,
            start_time=v.start_time,
            end_time=v.end_time,
            count=v.count,
            status=v.status,
            notes=v.notes,
        )
        for v, veh in viols
    ]


@app.post("/api/export")
def export_data(req: ExportRequest, db: Session = Depends(get_db)):
    """
    تصدير البيانات إلى Excel/HTML/PDF
    Export data to Excel/HTML/PDF
    """
    # بناء استعلام البيانات
    # Build data query
    q = (
        db.query(Event, Vehicle, Camera)
        .join(Vehicle, Event.vehicle_id == Vehicle.id)
        .join(Camera, Event.camera_id == Camera.id)
    )
    f = req.filter
    if f:
        if f.start:
            q = q.filter(Event.timestamp >= f.start)
        if f.end:
            q = q.filter(Event.timestamp <= f.end)
        if f.plate:
            q = q.filter(Vehicle.plate_number == f.plate)
        if f.camera_id:
            q = q.filter(Camera.camera_id == f.camera_id)
        if f.min_confidence:
            q = q.filter(Event.confidence >= f.min_confidence)
    records = []
    for ev, v, c in q.order_by(Event.timestamp.desc()).all():
        records.append(
            {
                "اللوحة": v.plate_number,
                "التاريخ": ev.timestamp,
                "الكاميرا": c.camera_id,
                "الثقة": ev.confidence,
                "النوع": ev.type or v.type,
                "الشركة": ev.make or v.make,
                "اللون": ev.color or v.color,
                "رابط_الصورة": ev.image_url,
            }
        )
    df = pd.DataFrame(records)

    if req.format == "html":
        html = df.to_html(index=False)
        return HTMLResponse(content=html)

    if req.format == "excel":
        bio = BytesIO()
        with pd.ExcelWriter(bio, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="الأحداث", index=False)
        bio.seek(0)
        return StreamingResponse(
            bio,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=events.xlsx"},
        )

    if req.format == "pdf":
        bio = BytesIO()
        c = canvas.Canvas(bio, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2 * cm, height - 2 * cm, "تقرير أحداث التعرف على اللوحات")
        c.setFont("Helvetica", 9)
        y = height - 3 * cm
        for idx, row in enumerate(records[:500]):  # حد الأحداث لكل PDF
            text = f"{row['التاريخ']} | {row['اللوحة']} | {row['الكاميرا']} | ثقة={row['الثقة']} | {row['الشركة']} {row['اللون']} ({row['النوع']})"
            c.drawString(2 * cm, y, text)
            y -= 0.6 * cm
            if y < 2 * cm:
                c.showPage()
                y = height - 3 * cm
        c.save()
        bio.seek(0)
        return StreamingResponse(
            bio,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=events.pdf"},
        )


@app.post("/api/import/excel")
async def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    استيراد البيانات من Excel
    Import data from Excel
    """
    content = await file.read()
    bio = BytesIO(content)
    df = pd.read_excel(bio)
    # الأعمدة المتوقعة: اللوحة، التاريخ، الكاميرا، الثقة، النوع، الشركة، اللون، رابط_الصورة
    # Expected columns: Plate, Timestamp, Camera, Confidence, Type, Make, Color, ImageURL
    imported = 0
    for _, r in df.iterrows():
        try:
            ev = record_event(
                db=db,
                plate=str(r.get("اللوحة", r.get("Plate", ""))),
                ts=pd.to_datetime(r.get("التاريخ", r.get("Timestamp"))).to_pydatetime(),
                camera_id=str(r.get("الكاميرا", r.get("Camera", ""))),
                confidence=float(r.get("الثقة", r.get("Confidence", 0))),
                image_url=r.get("رابط_الصورة", r.get("ImageURL")),
                make=r.get("الشركة", r.get("Make")),
                color=r.get("اللون", r.get("Color")),
                type_=r.get("النوع", r.get("Type")),
            )
            if ev:
                register_unauthorized_entry(db, ev)
                update_repeat_violations(db, ev.vehicle_id, ev.timestamp)
                imported += 1
        except Exception:
            continue
    db.commit()
    return {"imported": imported, "message": f"تم استيراد {imported} حدث بنجاح"}


@app.get("/health")
def health_check():
    """فحص صحة التطبيق - Health Check"""
    return {"status": "ok", "service": "نظام تحليل اللوحات"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
