#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتوليد قاعدة بيانات نظام إدارة الإسكان الجامعي
بناءً على التقرير النهائي الشامل
"""

import sqlite3
import random
from datetime import datetime, timedelta

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('housing_database.db')
cursor = conn.cursor()

# إنشاء الجداول
print("إنشاء الجداول...")

# جدول المباني
cursor.execute('''
CREATE TABLE IF NOT EXISTS buildings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_number TEXT UNIQUE NOT NULL,
    building_type TEXT NOT NULL,
    total_units INTEGER,
    occupied_units INTEGER,
    status TEXT DEFAULT 'نشط'
)
''')

# جدول الوحدات السكنية
cursor.execute('''
CREATE TABLE IF NOT EXISTS units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_id INTEGER,
    unit_number TEXT NOT NULL,
    unit_type TEXT NOT NULL,
    status TEXT DEFAULT 'شاغر',
    FOREIGN KEY (building_id) REFERENCES buildings(id)
)
''')

# جدول السكان
cursor.execute('''
CREATE TABLE IF NOT EXISTS residents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    national_id TEXT UNIQUE NOT NULL,
    phone TEXT,
    email TEXT,
    unit_id INTEGER,
    move_in_date TEXT,
    status TEXT DEFAULT 'نشط',
    FOREIGN KEY (unit_id) REFERENCES units(id)
)
''')

# جدول المواقف
cursor.execute('''
CREATE TABLE IF NOT EXISTS parking_spots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spot_number TEXT UNIQUE NOT NULL,
    parking_area TEXT NOT NULL,
    spot_type TEXT NOT NULL,
    status TEXT DEFAULT 'متاح',
    unit_id INTEGER,
    FOREIGN KEY (unit_id) REFERENCES units(id)
)
''')

# جدول ملصقات السيارات
cursor.execute('''
CREATE TABLE IF NOT EXISTS vehicle_stickers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sticker_number TEXT UNIQUE NOT NULL,
    plate_number TEXT NOT NULL,
    resident_id INTEGER,
    vehicle_type TEXT,
    vehicle_color TEXT,
    issue_date TEXT,
    status TEXT DEFAULT 'فعال',
    FOREIGN KEY (resident_id) REFERENCES residents(id)
)
''')

conn.commit()

print("✅ تم إنشاء الجداول بنجاح")

# توليد البيانات
print("\nبدء توليد البيانات...")

# 1. إنشاء المباني (165 مبنى)
print("1. إنشاء المباني...")

# العمارات القديمة (30 عمارة)
for i in range(1, 31):
    cursor.execute('''
        INSERT INTO buildings (building_number, building_type, total_units, occupied_units)
        VALUES (?, ?, ?, ?)
    ''', (f'عمارة {i}', 'عمارة', 20, random.randint(18, 20)))

# العمارات الجديدة (21 عمارة)
for i in range(51, 72):
    cursor.execute('''
        INSERT INTO buildings (building_number, building_type, total_units, occupied_units)
        VALUES (?, ?, ?, ?)
    ''', (f'عمارة {i}', 'عمارة', 20, random.randint(18, 20)))

# الفلل (114 فيلا)
for i in range(1, 115):
    cursor.execute('''
        INSERT INTO buildings (building_number, building_type, total_units, occupied_units)
        VALUES (?, ?, ?, ?)
    ''', (f'فيلا {i}', 'فيلا', 1, 1))

conn.commit()
print(f"✅ تم إنشاء 165 مبنى")

# 2. إنشاء الوحدات السكنية (1,134 وحدة)
print("2. إنشاء الوحدات السكنية...")

unit_count = 0

# الشقق في العمارات (1,020 شقة)
cursor.execute("SELECT id, building_number FROM buildings WHERE building_type = 'عمارة'")
apartments = cursor.fetchall()

for building_id, building_name in apartments:
    for unit_num in range(1, 21):  # 20 شقة لكل عمارة
        status = 'مشغول' if random.random() > 0.07 else 'شاغر'
        cursor.execute('''
            INSERT INTO units (building_id, unit_number, unit_type, status)
            VALUES (?, ?, ?, ?)
        ''', (building_id, str(unit_num), 'شقة', status))
        unit_count += 1

# الفلل (114 فيلا)
cursor.execute("SELECT id FROM buildings WHERE building_type = 'فيلا'")
villas = cursor.fetchall()

for (building_id,) in villas:
    cursor.execute('''
        INSERT INTO units (building_id, unit_number, unit_type, status)
        VALUES (?, ?, ?, ?)
    ''', (building_id, '1', 'فيلا', 'مشغول'))
    unit_count += 1

conn.commit()
print(f"✅ تم إنشاء {unit_count} وحدة سكنية")

# 3. إنشاء السكان (1,057 ساكن)
print("3. إنشاء السكان...")

# أسماء عربية للتوليد
first_names = ['أحمد', 'محمد', 'عبدالله', 'خالد', 'سعد', 'فهد', 'عبدالعزيز', 'سلطان', 'فيصل', 'عمر',
               'فاطمة', 'نورة', 'سارة', 'منى', 'هند', 'ريم', 'لطيفة', 'وفاء', 'نوال', 'أمل']
middle_names = ['عبدالله', 'محمد', 'علي', 'أحمد', 'سعد', 'عبدالعزيز', 'إبراهيم', 'سليمان', 'عبدالرحمن', 'حمد']
last_names = ['العتيبي', 'الدوسري', 'القحطاني', 'الغامدي', 'الشمري', 'المطيري', 'العنزي', 'الحربي', 'الزهراني', 'السهلي',
              'الشهري', 'العمري', 'الجهني', 'البقمي', 'السبيعي', 'المالكي', 'الأحمدي', 'الثبيتي', 'الرشيدي', 'اليامي']

cursor.execute("SELECT id FROM units WHERE status = 'مشغول'")
occupied_units = cursor.fetchall()

resident_count = 0
for (unit_id,) in occupied_units[:1057]:  # 1,057 ساكن
    name = f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"
    national_id = f"1{''.join([str(random.randint(0, 9)) for _ in range(9)])}"
    phone = f"05{random.randint(0, 9)}{random.randint(1000000, 9999999)}"
    email = f"resident{resident_count+1}@imamu.edu.sa"
    move_in_date = (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime('%Y-%m-%d')
    
    cursor.execute('''
        INSERT INTO residents (name, national_id, phone, email, unit_id, move_in_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, national_id, phone, email, unit_id, move_in_date))
    resident_count += 1

conn.commit()
print(f"✅ تم إنشاء {resident_count} ساكن")

# 4. إنشاء المواقف (1,308 موقف)
print("4. إنشاء المواقف...")

parking_areas = [
    ('G.L.P-1', 126, 'خاص'),
    ('G.L.P-2', 100, 'خاص'),
    ('G.L.P-3', 71, 'خاص'),
    ('G.L.P-5', 80, 'خاص'),
    ('G.L.P-6', 100, 'خاص'),
    ('G.L.P-7', 69, 'خاص'),
    ('G.L.P-8', 54, 'خاص'),
    ('G.L.P-(53-54-55-56)', 80, 'خاص'),
    ('G.L.P-(61-62-63-64)', 80, 'خاص'),
    ('G.L.P-(65-66-67-68)', 80, 'خاص'),
    ('G.L.P-(71-72)', 40, 'خاص'),
    ('G.L.P-(73-74-75)', 60, 'خاص'),
    ('G.L.P-(76-77-78-79)', 80, 'خاص'),
]

# مواقف المعاقين (39 موقف)
for i in range(1, 14):
    for j in range(1, 4):
        cursor.execute('''
            INSERT INTO parking_spots (spot_number, parking_area, spot_type, status)
            VALUES (?, ?, ?, ?)
        ''', (f'D-{i}-{j}', f'G.L.P-{i}', 'معاقين', 'متاح'))

# المواقف الخاصة (1,028 موقف)
cursor.execute("SELECT id FROM units WHERE unit_type = 'شقة' AND status = 'مشغول'")
occupied_apartments = cursor.fetchall()

spot_count = 39  # بدءاً من بعد مواقف المعاقين
for area_name, total_spots, spot_type in parking_areas:
    for i in range(1, total_spots + 1):
        unit_id = occupied_apartments[spot_count % len(occupied_apartments)][0] if spot_count < len(occupied_apartments) else None
        status = 'مشغول' if unit_id and random.random() > 0.3 else 'متاح'
        
        cursor.execute('''
            INSERT INTO parking_spots (spot_number, parking_area, spot_type, status, unit_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (f'{area_name}-{i}', area_name, spot_type, status, unit_id))
        spot_count += 1

# المواقف العامة (241 موقف)
for i in range(1, 14):
    for j in range(1, 19):
        cursor.execute('''
            INSERT INTO parking_spots (spot_number, parking_area, spot_type, status)
            VALUES (?, ?, ?, ?)
        ''', (f'P-{i}-{j}', f'G.L.P-{i}', 'عام', 'متاح'))

conn.commit()
print(f"✅ تم إنشاء 1,308 موقف")

# 5. إنشاء ملصقات السيارات (2,381 ملصق)
print("5. إنشاء ملصقات السيارات...")

vehicle_types = ['تويوتا كامري', 'هونداي سوناتا', 'نيسان التيما', 'شيفروليه كابرس', 'فورد فيوجن',
                 'مازدا 6', 'كيا أوبتيما', 'تويوتا كورولا', 'هونداي إلنترا', 'نيسان سنترا']
vehicle_colors = ['أبيض', 'أسود', 'فضي', 'رمادي', 'أزرق', 'أحمر', 'بني', 'ذهبي']

cursor.execute("SELECT id FROM residents")
all_residents = cursor.fetchall()

sticker_count = 0
for (resident_id,) in all_residents:
    # عدد السيارات لكل ساكن (معظمهم 2-3 سيارات)
    num_vehicles = random.choices([1, 2, 3, 4, 5], weights=[20, 40, 25, 10, 5])[0]
    
    for v in range(num_vehicles):
        if sticker_count >= 2381:
            break
            
        sticker_number = f"S{str(sticker_count + 1).zfill(6)}"
        
        # توليد رقم لوحة سعودي
        arabic_letters = ['أ', 'ب', 'ج', 'د', 'ر', 'س', 'ص', 'ط', 'ع', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي']
        plate_number = f"{random.choice(arabic_letters)} {random.choice(arabic_letters)} {random.choice(arabic_letters)} {random.randint(1000, 9999)}"
        
        vehicle_type = random.choice(vehicle_types)
        vehicle_color = random.choice(vehicle_colors)
        issue_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        status = 'فعال' if random.random() > 0.07 else 'ملغي'
        
        cursor.execute('''
            INSERT INTO vehicle_stickers (sticker_number, plate_number, resident_id, vehicle_type, vehicle_color, issue_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sticker_number, plate_number, resident_id, vehicle_type, vehicle_color, issue_date, status))
        sticker_count += 1
    
    if sticker_count >= 2381:
        break

conn.commit()
print(f"✅ تم إنشاء {sticker_count} ملصق سيارة")

# طباعة الإحصائيات النهائية
print("\n" + "="*60)
print("📊 الإحصائيات النهائية")
print("="*60)

cursor.execute("SELECT COUNT(*) FROM buildings")
print(f"إجمالي المباني: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM units")
print(f"إجمالي الوحدات السكنية: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM residents")
print(f"إجمالي السكان: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM parking_spots")
print(f"إجمالي المواقف: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM vehicle_stickers")
print(f"إجمالي ملصقات السيارات: {cursor.fetchone()[0]}")

print("="*60)
print("✅ تم إنشاء قاعدة البيانات بنجاح!")

conn.close()

