-- Migration: Add vehicles and traffic violations tables
-- تاريخ: 2025-11-17
-- الهدف: إضافة قاعدة بيانات السيارات والمخالفات المرورية

-- جدول السيارات المسجلة
-- Vehicles table for comprehensive vehicle management
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resident_id INTEGER,
    plate_number TEXT UNIQUE NOT NULL,
    plate_arabic TEXT,
    plate_english TEXT,
    vehicle_make TEXT,
    vehicle_model TEXT,
    vehicle_year INTEGER,
    vehicle_type TEXT,
    vehicle_color TEXT,
    registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
    last_seen TEXT,
    status TEXT DEFAULT 'نشط',
    notes TEXT,
    FOREIGN KEY (resident_id) REFERENCES residents(id)
);

CREATE INDEX IF NOT EXISTS idx_vehicles_plate_number ON vehicles(plate_number);
CREATE INDEX IF NOT EXISTS idx_vehicles_resident_id ON vehicles(resident_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_status ON vehicles(status);

-- جدول المخالفات المرورية
-- Traffic violations table
CREATE TABLE IF NOT EXISTS traffic_violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    plate_number TEXT,
    violation_type TEXT NOT NULL,
    violation_date TEXT DEFAULT CURRENT_TIMESTAMP,
    violation_location TEXT,
    violation_description TEXT,
    fine_amount REAL DEFAULT 0,
    status TEXT DEFAULT 'مفتوح',
    payment_date TEXT,
    image_path TEXT,
    confidence_score INTEGER,
    notes TEXT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

CREATE INDEX IF NOT EXISTS idx_violations_vehicle_id ON traffic_violations(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_violations_plate_number ON traffic_violations(plate_number);
CREATE INDEX IF NOT EXISTS idx_violations_status ON traffic_violations(status);
CREATE INDEX IF NOT EXISTS idx_violations_date ON traffic_violations(violation_date);

-- جدول التكامل مع نظام تكامل
-- Takamul integration table for data synchronization
CREATE TABLE IF NOT EXISTS takamul_integration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_type TEXT NOT NULL,
    sync_date TEXT DEFAULT CURRENT_TIMESTAMP,
    records_synced INTEGER DEFAULT 0,
    status TEXT DEFAULT 'نجح',
    error_message TEXT,
    data_snapshot TEXT
);

CREATE INDEX IF NOT EXISTS idx_takamul_sync_date ON takamul_integration(sync_date);
CREATE INDEX IF NOT EXISTS idx_takamul_status ON takamul_integration(status);

-- جدول سجل تحليل الصور من Plate Recognizer
-- Plate Recognizer analysis log
CREATE TABLE IF NOT EXISTS plate_recognizer_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    plate_number TEXT,
    vehicle_type TEXT,
    vehicle_color TEXT,
    confidence REAL,
    processing_date TEXT DEFAULT CURRENT_TIMESTAMP,
    api_response TEXT,
    webhook_data TEXT,
    status TEXT DEFAULT 'معالج',
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_plate_recognizer_date ON plate_recognizer_log(processing_date);
CREATE INDEX IF NOT EXISTS idx_plate_recognizer_plate ON plate_recognizer_log(plate_number);
