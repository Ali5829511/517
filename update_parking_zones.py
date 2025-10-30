#!/usr/bin/env python3
"""
تحديث مناطق الوقوف للمباني القديمة
Update parking zones for old buildings based on G.L.P zones
"""

import sqlite3

# Database connection
conn = sqlite3.connect('housing_database.db')
cursor = conn.cursor()

# توزيع المباني القديمة على مناطق الوقوف
# Distribution of old buildings to parking zones
# Based on the data provided and the mapping table
parking_zone_mapping = {
    # G.L.P-7: Buildings 1, 2, 3
    'G.L.P-7': [1, 2, 3],
    # G.L.P-6: Buildings 4, 5, 6
    'G.L.P-6': [4, 5, 6],
    # G.L.P-4: Buildings 8, 9 (also includes 4, 5, 6 per table)
    'G.L.P-4': [8, 9],
    # G.L.P-3: Buildings 12-17
    'G.L.P-3': [12, 13, 14, 15, 16, 17],
    # G.L.P-2: Buildings 18, 19, 20
    'G.L.P-2': [18, 19, 20],
    # G.L.P-1: Buildings 22-26
    'G.L.P-1': [22, 23, 24, 25, 26],
    # G.L.P-8: Buildings 28, 29, 30
    'G.L.P-8': [28, 29, 30],
}

# Buildings not assigned: 7, 10, 11, 21, 27
# Let's assign them based on proximity
parking_zone_mapping['G.L.P-6'].append(7)  # Near 6
parking_zone_mapping['G.L.P-4'].extend([10, 11])  # Between zones
parking_zone_mapping['G.L.P-1'].append(21)  # Near 22
parking_zone_mapping['G.L.P-1'].append(27)  # Near 26

print("🔄 بدء تحديث مناطق الوقوف...")
print("=" * 60)

# Update parking spots for old buildings
for zone, buildings in parking_zone_mapping.items():
    for building_num in buildings:
        # Get building ID
        cursor.execute("""
            SELECT id FROM buildings 
            WHERE name = ? AND type = 'مبنى قديم'
        """, (f'مبنى قديم {building_num}',))
        
        building = cursor.fetchone()
        if not building:
            print(f"⚠️  المبنى {building_num} غير موجود")
            continue
            
        building_id = building[0]
        
        # Get all units in this building
        cursor.execute("""
            SELECT id, unit_number FROM units 
            WHERE building_id = ?
        """, (building_id,))
        
        units = cursor.fetchall()
        
        # Update parking spots for each unit
        for unit_id, unit_number in units:
            cursor.execute("""
                UPDATE parking_spots 
                SET parking_area = ?
                WHERE unit_id = ?
            """, (zone, unit_id))
        
        print(f"✅ تحديث المبنى {building_num}: {len(units)} شقة → {zone}")

conn.commit()

# Print summary
print("\n" + "=" * 60)
print("📊 ملخص التحديث:")
print("=" * 60)

for zone in sorted(parking_zone_mapping.keys()):
    cursor.execute("""
        SELECT COUNT(*) FROM parking_spots 
        WHERE parking_area = ?
    """, (zone,))
    count = cursor.fetchone()[0]
    buildings = ', '.join(map(str, sorted(parking_zone_mapping[zone])))
    print(f"{zone}: {count} موقف (مباني: {buildings})")

# Total old buildings parkings
cursor.execute("""
    SELECT COUNT(*) FROM parking_spots ps
    JOIN units u ON ps.unit_id = u.id
    JOIN buildings b ON u.building_id = b.id
    WHERE b.type = 'مبنى قديم'
""")
total_old = cursor.fetchone()[0]

print(f"\n📍 إجمالي مواقف المباني القديمة: {total_old}")

conn.close()
print("\n✅ تم التحديث بنجاح!")
