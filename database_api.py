#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API للوصول إلى قاعدة بيانات نظام إدارة الإسكان الجامعي
"""

import sqlite3

DATABASE = "housing_database.db"


def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    # تفعيل قيود المفتاح الأجنبي لضمان سلامة العلاقات عند الإدخال/التحديث
    try:
        conn.execute("PRAGMA foreign_keys = ON")
    except Exception:
        pass
    conn.row_factory = sqlite3.Row
    return conn


def get_all_residents():
    """الحصول على جميع السكان"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            r.id,
            r.name,
            r.national_id,
            r.phone,
            r.email,
            r.move_in_date,
            r.status,
            u.unit_number,
            u.unit_type,
            b.building_number
        FROM residents r
        LEFT JOIN units u ON r.unit_id = u.id
        LEFT JOIN buildings b ON u.building_id = b.id
        ORDER BY r.id
    """
    )

    residents = []
    for row in cursor.fetchall():
        residents.append(
            {
                "id": row["id"],
                "name": row["name"],
                "nationalId": row["national_id"],
                "phone": row["phone"],
                "email": row["email"],
                "building": row["building_number"],
                "unit": row["unit_number"],
                "unitType": row["unit_type"],
                "moveInDate": row["move_in_date"],
                "status": row["status"],
            }
        )

    conn.close()
    return residents


def get_all_stickers():
    """الحصول على جميع ملصقات السيارات"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            vs.id,
            vs.sticker_number,
            vs.plate_number,
            vs.vehicle_type,
            vs.vehicle_color,
            vs.issue_date,
            vs.status,
            r.name as owner_name,
            r.national_id,
            u.unit_number,
            b.building_number,
            u.unit_type
        FROM vehicle_stickers vs
        -- دعم حالتين شائعتين: resident_id قد يكون إما id (INTEGER) أو national_id (TEXT)
        LEFT JOIN residents r ON (vs.resident_id = r.id OR vs.resident_id = r.national_id)
        LEFT JOIN units u ON r.unit_id = u.id
        LEFT JOIN buildings b ON u.building_id = b.id
        ORDER BY vs.id
    """
    )

    stickers = []
    for row in cursor.fetchall():
        stickers.append(
            {
                "id": row["id"],
                "stickerNumber": row["sticker_number"],
                "plateNumber": row["plate_number"],
                "vehicleType": row["vehicle_type"],
                "vehicleColor": row["vehicle_color"],
                "ownerName": row["owner_name"],
                "nationalId": row["national_id"],
                "building": row["building_number"],
                "unit": row["unit_number"],
                "unitType": row["unit_type"],
                "issueDate": row["issue_date"],
                "status": row["status"],
            }
        )

    conn.close()
    return stickers


def get_all_parking_spots():
    """الحصول على جميع المواقف"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ps.id,
            ps.spot_number,
            ps.parking_area,
            ps.spot_type,
            ps.status,
            u.unit_number,
            b.building_number,
            r.name as resident_name
        FROM parking_spots ps
        LEFT JOIN units u ON ps.unit_id = u.id
        LEFT JOIN buildings b ON u.building_id = b.id
        LEFT JOIN residents r ON r.unit_id = u.id
        ORDER BY ps.id
    """
    )

    spots = []
    for row in cursor.fetchall():
        spots.append(
            {
                "id": row["id"],
                "spotNumber": row["spot_number"],
                "parkingArea": row["parking_area"],
                "spotType": row["spot_type"],
                "status": row["status"],
                "building": row["building_number"],
                "unit": row["unit_number"],
                "residentName": row["resident_name"],
            }
        )

    conn.close()
    return spots


def get_statistics():
    """الحصول على الإحصائيات العامة"""
    conn = get_db_connection()
    cursor = conn.cursor()

    stats = {}

    # إحصائيات المباني
    cursor.execute("SELECT COUNT(*) as total FROM buildings")
    stats["totalBuildings"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM buildings WHERE building_type = 'عمارة'"
    )
    stats["totalApartmentBuildings"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM buildings WHERE building_type = 'فيلا'"
    )
    stats["totalVillas"] = cursor.fetchone()["total"]

    # إحصائيات الوحدات
    cursor.execute("SELECT COUNT(*) as total FROM units")
    stats["totalUnits"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM units WHERE status = 'مشغول'")
    stats["occupiedUnits"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM units WHERE status = 'شاغر'")
    stats["vacantUnits"] = cursor.fetchone()["total"]

    # إحصائيات السكان
    cursor.execute("SELECT COUNT(*) as total FROM residents")
    stats["totalResidents"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM residents WHERE status = 'نشط'")
    stats["activeResidents"] = cursor.fetchone()["total"]

    # إحصائيات المواقف
    cursor.execute("SELECT COUNT(*) as total FROM parking_spots")
    stats["totalParkingSpots"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM parking_spots WHERE status = 'مشغول'")
    stats["occupiedSpots"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM parking_spots WHERE status = 'متاح'")
    stats["availableSpots"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM parking_spots WHERE spot_type = 'معاقين'"
    )
    stats["disabledSpots"] = cursor.fetchone()["total"]

    # إحصائيات الملصقات
    cursor.execute("SELECT COUNT(*) as total FROM vehicle_stickers")
    stats["totalStickers"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM vehicle_stickers WHERE status = 'فعال'"
    )
    stats["activeStickers"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM vehicle_stickers WHERE status = 'ملغي'"
    )
    stats["cancelledStickers"] = cursor.fetchone()["total"]

    conn.close()
    return stats


def get_stickers_by_resident(resident_id):
    """إرجاع جميع الملصقات المرتبطة بالساكن (يدعم resident_id المخزن كـ id أو national_id)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # بعض السجلات قد تكون مخزنة resident_id كقيمة national_id بدلاً من id.
    # نبحث عن الملصقات حيث vs.resident_id = id أو يطابق national_id للساكن.
    cursor.execute(
        """
        SELECT
            vs.id,
            vs.sticker_number,
            vs.plate_number,
            vs.vehicle_type,
            vs.vehicle_color,
            vs.issue_date,
            vs.status
        FROM vehicle_stickers vs
        WHERE vs.resident_id = ?
           OR vs.resident_id = (SELECT national_id FROM residents WHERE id = ?)
        ORDER BY vs.id
    """,
        (resident_id, resident_id),
    )

    stickers = []
    for row in cursor.fetchall():
        stickers.append(
            {
                "id": row["id"],
                "stickerNumber": row["sticker_number"],
                "plateNumber": row["plate_number"],
                "vehicleType": row["vehicle_type"],
                "vehicleColor": row["vehicle_color"],
                "issueDate": row["issue_date"],
                "status": row["status"],
            }
        )

    conn.close()
    return stickers


def search_by_plate(plate_number):
    """البحث عن مركبة برقم اللوحة"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            vs.sticker_number,
            vs.plate_number,
            vs.vehicle_type,
            vs.vehicle_color,
            vs.status,
            r.name as owner_name,
            r.phone,
            r.national_id,
            u.unit_number,
            b.building_number,
            u.unit_type
        FROM vehicle_stickers vs
        LEFT JOIN residents r ON vs.resident_id = r.id
        LEFT JOIN units u ON r.unit_id = u.id
        LEFT JOIN buildings b ON u.building_id = b.id
        WHERE vs.plate_number LIKE ?
        LIMIT 1
    """,
        (f"%{plate_number}%",),
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "found": True,
            "stickerNumber": row["sticker_number"],
            "plateNumber": row["plate_number"],
            "vehicleType": row["vehicle_type"],
            "vehicleColor": row["vehicle_color"],
            "status": row["status"],
            "resident": {
                "name": row["owner_name"],
                "phone": row["phone"],
                "nationalId": row["national_id"],
                "building": row["building_number"],
                "unit": row["unit_number"],
                "unitType": row["unit_type"],
            },
        }
    else:
        return {"found": False}


def save_processed_image(image_data):
    """حفظ صورة معالجة في قاعدة البيانات"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # البحث عن الساكن والملصق
        resident_id = None
        sticker_id = None

        if image_data.get("plateNumber"):
            cursor.execute(
                """
                SELECT vs.id as sticker_id, r.id as resident_id
                FROM vehicle_stickers vs
                LEFT JOIN residents r ON vs.resident_id = r.id
                WHERE vs.plate_number LIKE ?
                LIMIT 1
            """,
                (f'%{image_data["plateNumber"]}%',),
            )

            result = cursor.fetchone()
            if result:
                sticker_id = result["sticker_id"]
                resident_id = result["resident_id"]

        # إدخال البيانات
        cursor.execute(
            """
            INSERT INTO processed_images (
                image_filename,
                plate_number,
                arabic_letters,
                numbers,
                vehicle_type,
                vehicle_color,
                confidence,
                category,
                resident_id,
                sticker_id,
                notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                image_data.get("filename", ""),
                image_data.get("plateNumber", ""),
                image_data.get("arabicLetters", ""),
                image_data.get("numbers", ""),
                image_data.get("carType", ""),
                image_data.get("carColor", ""),
                image_data.get("confidence", 0),
                image_data.get("category", "normal"),
                resident_id,
                sticker_id,
                image_data.get("notes", ""),
            ),
        )

        conn.commit()
        image_id = cursor.lastrowid
        conn.close()

        return {"success": True, "id": image_id, "message": "تم حفظ الصورة بنجاح"}

    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e), "message": "فشل في حفظ الصورة"}


def get_processed_images(limit=100, category=None):
    """الحصول على الصور المعالجة"""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            pi.id,
            pi.image_filename,
            pi.plate_number,
            pi.arabic_letters,
            pi.numbers,
            pi.vehicle_type,
            pi.vehicle_color,
            pi.confidence,
            pi.category,
            pi.processing_date,
            pi.notes,
            r.name as resident_name,
            u.unit_number,
            b.building_number
        FROM processed_images pi
        LEFT JOIN residents r ON pi.resident_id = r.id
        LEFT JOIN units u ON r.unit_id = u.id
        LEFT JOIN buildings b ON u.building_id = b.id
    """

    if category and category != "all":
        query += " WHERE pi.category = ?"
        cursor.execute(
            query + " ORDER BY pi.processing_date DESC LIMIT ?", (category, limit)
        )
    else:
        cursor.execute(query + " ORDER BY pi.processing_date DESC LIMIT ?", (limit,))

    images = []
    for row in cursor.fetchall():
        images.append(
            {
                "id": row["id"],
                "filename": row["image_filename"],
                "plateNumber": row["plate_number"],
                "arabicLetters": row["arabic_letters"],
                "numbers": row["numbers"],
                "vehicleType": row["vehicle_type"],
                "vehicleColor": row["vehicle_color"],
                "confidence": row["confidence"],
                "category": row["category"],
                "processingDate": row["processing_date"],
                "notes": row["notes"],
                "residentName": row["resident_name"],
                "unitNumber": row["unit_number"],
                "buildingNumber": row["building_number"],
            }
        )

    conn.close()
    return images


def search_processed_images(plate_number):
    """البحث في الصور المعالجة برقم اللوحة"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            pi.id,
            pi.image_filename,
            pi.plate_number,
            pi.arabic_letters,
            pi.numbers,
            pi.vehicle_type,
            pi.vehicle_color,
            pi.confidence,
            pi.category,
            pi.processing_date,
            pi.notes,
            r.name as resident_name,
            r.phone as resident_phone,
            r.national_id,
            u.unit_number,
            b.building_number,
            vs.sticker_number
        FROM processed_images pi
        LEFT JOIN residents r ON pi.resident_id = r.id
        LEFT JOIN units u ON r.unit_id = u.id
        LEFT JOIN buildings b ON u.building_id = b.id
        LEFT JOIN vehicle_stickers vs ON pi.sticker_id = vs.id
        WHERE pi.plate_number LIKE ?
        ORDER BY pi.processing_date DESC
    """,
        (f"%{plate_number}%",),
    )

    results = []
    for row in cursor.fetchall():
        results.append(
            {
                "id": row["id"],
                "filename": row["image_filename"],
                "plateNumber": row["plate_number"],
                "arabicLetters": row["arabic_letters"],
                "numbers": row["numbers"],
                "vehicleType": row["vehicle_type"],
                "vehicleColor": row["vehicle_color"],
                "confidence": row["confidence"],
                "category": row["category"],
                "processingDate": row["processing_date"],
                "notes": row["notes"],
                "resident": {
                    "name": row["resident_name"],
                    "phone": row["resident_phone"],
                    "nationalId": row["national_id"],
                    "building": row["building_number"],
                    "unit": row["unit_number"],
                },
                "stickerNumber": row["sticker_number"],
            }
        )

    conn.close()
    return results


def get_violation_report():
    """الحصول على تقرير المخالفات مع عدد التكرار"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. الحصول على جميع المخالفات
    # 2. حساب عدد التكرار لكل لوحة
    query = """
        SELECT
            pi.id,
            pi.image_filename,
            pi.plate_number,
            pi.arabic_letters,
            pi.numbers,
            pi.vehicle_type,
            pi.vehicle_color,
            pi.confidence,
            pi.category,
            pi.processing_date,
            pi.notes,
            r.name as resident_name,
            u.unit_number,
            b.building_number,
            (
                SELECT COUNT(*)
                FROM processed_images p2
                WHERE p2.plate_number = pi.plate_number AND p2.category = 'violation'
            ) as violation_count
        FROM processed_images pi
        LEFT JOIN residents r ON pi.resident_id = r.id
        LEFT JOIN units u ON r.unit_id = u.id
        LEFT JOIN buildings b ON u.building_id = b.id
        WHERE pi.category = 'violation'
        ORDER BY pi.processing_date DESC
    """

    cursor.execute(query)

    report_data = []
    for row in cursor.fetchall():
        report_data.append(
            {
                "id": row["id"],
                "imageFilename": row["image_filename"],
                "plateNumber": row["plate_number"],
                "arabicLetters": row["arabic_letters"],
                "numbers": row["numbers"],
                "vehicleType": row["vehicle_type"],
                "vehicleColor": row["vehicle_color"],
                "confidence": row["confidence"],
                "category": row["category"],
                "processingDate": row["processing_date"],
                "notes": row["notes"],
                "residentName": row["resident_name"],
                "unitNumber": row["unit_number"],
                "buildingNumber": row["building_number"],
                "violationCount": row["violation_count"],  # حقل عدد التكرار الجديد
            }
        )

    conn.close()
    return report_data


def get_processed_images_statistics():
    """الحصول على إحصائيات الصور المعالجة"""
    conn = get_db_connection()
    cursor = conn.cursor()

    stats = {}

    cursor.execute("SELECT COUNT(*) as total FROM processed_images")
    stats["total"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM processed_images WHERE category = 'normal'"
    )
    stats["normal"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM processed_images WHERE category = 'disabled'"
    )
    stats["disabled"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM processed_images WHERE category = 'violation'"
    )
    stats["violation"] = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM processed_images WHERE resident_id IS NOT NULL"
    )
    stats["withResident"] = cursor.fetchone()["total"]

    cursor.execute("SELECT AVG(confidence) as avg FROM processed_images")
    stats["avgConfidence"] = cursor.fetchone()["avg"] or 0

    conn.close()
    return stats


def get_all_buildings():
    """الحصول على جميع المباني"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            building_number as buildingNumber,
            building_type as buildingType,
            total_units as totalUnits,
            occupied_units as occupiedUnits,
            status
        FROM buildings
        ORDER BY building_number
    """
    )
    buildings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return buildings


def get_all_units():
    """
    الحصول على جميع الوحدات السكنية مع معلومات المباني
    Get all residential units with building information
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            u.id,
            u.unit_number as unitNumber,
            u.unit_type as unitType,
            u.status,
            b.building_number as buildingNumber,
            b.building_type as buildingType
        FROM units u
        LEFT JOIN buildings b ON u.building_id = b.id
        ORDER BY b.building_number, u.id
    """
    )
    units = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return units


def get_units_statistics():
    """
    الحصول على إحصائيات الوحدات السكنية
    Get residential units statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # إحصائيات عامة
    cursor.execute(
        """
        SELECT
            COUNT(*) as total_units,
            SUM(CASE WHEN status = 'مشغول' THEN 1 ELSE 0 END) as occupied_units,
            SUM(CASE WHEN status = 'شاغر' THEN 1 ELSE 0 END) as vacant_units,
            SUM(CASE WHEN unit_type = 'شقة' THEN 1 ELSE 0 END) as apartments_count,
            SUM(CASE WHEN unit_type = 'فيلا' THEN 1 ELSE 0 END) as villas_count
        FROM units
    """
    )
    stats = dict(cursor.fetchone())
    conn.close()
    return stats


def get_comprehensive_statistics():
    """
    الحصول على إحصائيات شاملة للنظام
    Get comprehensive system statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # إحصائيات المباني
    cursor.execute(
        """
        SELECT
            COUNT(*) as total_buildings,
            SUM(CASE WHEN building_type = 'عمارة' THEN 1 ELSE 0 END) as apartments_count,
            SUM(CASE WHEN building_type = 'فيلا' THEN 1 ELSE 0 END) as villas_count
        FROM buildings
    """
    )
    buildings_stats = dict(cursor.fetchone())

    # إحصائيات الوحدات
    cursor.execute(
        """
        SELECT
            COUNT(*) as total_units,
            SUM(CASE WHEN status = 'مشغول' THEN 1 ELSE 0 END) as occupied_units,
            SUM(CASE WHEN status = 'شاغر' THEN 1 ELSE 0 END) as vacant_units
        FROM units
    """
    )
    units_stats = dict(cursor.fetchone())

    # إحصائيات السكان
    cursor.execute(
        """
        SELECT
            COUNT(*) as total_residents,
            SUM(CASE WHEN status = 'نشط' THEN 1 ELSE 0 END) as active_residents
        FROM residents
    """
    )
    residents_stats = dict(cursor.fetchone())

    # إحصائيات المواقف
    cursor.execute(
        """
        SELECT
            COUNT(*) as total_parking,
            SUM(CASE WHEN spot_type = 'خاص' THEN 1 ELSE 0 END) as private_parking,
            SUM(CASE WHEN spot_type = 'عام' THEN 1 ELSE 0 END) as public_parking,
            SUM(CASE WHEN spot_type = 'معاق' THEN 1 ELSE 0 END) as disabled_parking,
            SUM(CASE WHEN status = 'مشغول' THEN 1 ELSE 0 END) as occupied_parking,
            SUM(CASE WHEN status = 'متاح' THEN 1 ELSE 0 END) as available_parking
        FROM parking_spots
    """
    )
    parking_stats = dict(cursor.fetchone())

    # إحصائيات الملصقات
    cursor.execute(
        """
        SELECT
            COUNT(*) as total_stickers,
            SUM(CASE WHEN status = 'فعال' THEN 1 ELSE 0 END) as active_stickers,
            SUM(CASE WHEN status = 'ملغي' THEN 1 ELSE 0 END) as cancelled_stickers
        FROM vehicle_stickers
    """
    )
    stickers_stats = dict(cursor.fetchone())

    # السكان الأكثر ملصقات
    cursor.execute(
        """
        SELECT
            r.name,
            COUNT(vs.id) as vehicle_count
        FROM residents r
        LEFT JOIN vehicle_stickers vs ON r.id = vs.resident_id
        GROUP BY r.id, r.name
        ORDER BY vehicle_count DESC
        LIMIT 10
    """
    )
    top_residents = [dict(row) for row in cursor.fetchall()]

    # المباني الأكثر ملصقات
    cursor.execute(
        """
        SELECT
            b.building_number,
            b.building_type,
            COUNT(vs.id) as sticker_count
        FROM buildings b
        LEFT JOIN units u ON b.id = u.building_id
        LEFT JOIN residents r ON u.id = r.unit_id
        LEFT JOIN vehicle_stickers vs ON r.id = vs.resident_id
        GROUP BY b.id, b.building_number, b.building_type
        ORDER BY sticker_count DESC
        LIMIT 10
    """
    )
    top_buildings = [dict(row) for row in cursor.fetchall()]

    conn.close()

    # حساب النسب
    occupancy_rate = (
        (units_stats["occupied_units"] / units_stats["total_units"] * 100)
        if units_stats["total_units"] > 0
        else 0
    )
    parking_utilization = (
        (parking_stats["occupied_parking"] / parking_stats["total_parking"] * 100)
        if parking_stats["total_parking"] > 0
        else 0
    )
    stickers_per_resident = (
        (stickers_stats["total_stickers"] / residents_stats["total_residents"])
        if residents_stats["total_residents"] > 0
        else 0
    )

    return {
        "buildings": buildings_stats,
        "units": units_stats,
        "residents": residents_stats,
        "parking": parking_stats,
        "stickers": stickers_stats,
        "kpis": {
            "occupancy_rate": round(occupancy_rate, 1),
            "parking_utilization": round(parking_utilization, 1),
            "stickers_per_resident": round(stickers_per_resident, 2),
            "active_sticker_rate": round(
                (
                    (
                        stickers_stats["active_stickers"]
                        / stickers_stats["total_stickers"]
                        * 100
                    )
                    if stickers_stats["total_stickers"] > 0
                    else 0
                ),
                1,
            ),
        },
        "top_residents": top_residents,
        "top_buildings": top_buildings,
    }
