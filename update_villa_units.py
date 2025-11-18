#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتحديث أسماء الوحدات السكنية للفلل
Script to update villa unit names from "1" to "فلة1", "فلة2", etc.
"""

import sqlite3

DATABASE = "housing_database.db"


def update_villa_unit_names():
    """
    تحديث أسماء وحدات الفلل من "1" إلى "فلة1", "فلة2", إلخ
    Update villa unit names from "1" to "فلة1", "فلة2", etc.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")

        # Get all villa buildings with their units
        cursor.execute(
            """
            SELECT b.id as building_id, b.building_number, u.id as unit_id, u.unit_number
            FROM buildings b
            JOIN units u ON b.id = u.building_id
            WHERE b.building_type = 'فيلا'
            ORDER BY b.id
        """
        )

        villas = cursor.fetchall()
        print(f"Found {len(villas)} villa units to update")

        # Update each villa unit
        updated_count = 0
        for i, villa in enumerate(villas, start=1):
            unit_id = villa["unit_id"]
            new_unit_number = f"فلة{i}"

            # Update the unit_number
            cursor.execute(
                """
                UPDATE units
                SET unit_number = ?
                WHERE id = ?
            """,
                (new_unit_number, unit_id),
            )

            updated_count += 1

            if i % 10 == 0:
                print(f"Updated {i} units...")

        # Commit the changes
        conn.commit()
        print(f"\n✓ Successfully updated {updated_count} villa units")

        # Verify the updates
        cursor.execute(
            """
            SELECT b.building_number, u.unit_number, u.unit_type
            FROM buildings b
            JOIN units u ON b.id = u.building_id
            WHERE b.building_type = 'فيلا'
            ORDER BY b.id
            LIMIT 10
        """
        )

        print("\nSample of updated units:")
        print("-" * 60)
        for row in cursor.fetchall():
            building = row["building_number"]
            unit = row["unit_number"]
            unit_type = row["unit_type"]
            print(f"Building: {building}, Unit: {unit}, Type: {unit_type}")

    except Exception as e:
        conn.rollback()
        print(f"Error updating villa units: {e}")
        raise
    finally:
        conn.close()


def verify_update():
    """
    التحقق من تحديث أسماء وحدات الفلل
    Verify villa unit name updates
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Count villa units
        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM units u
            JOIN buildings b ON u.building_id = b.id
            WHERE b.building_type = 'فيلا'
        """
        )
        total = cursor.fetchone()["count"]

        # Count units with new naming convention
        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM units u
            JOIN buildings b ON u.building_id = b.id
            WHERE b.building_type = 'فيلا' AND u.unit_number LIKE 'فلة%'
        """
        )
        updated = cursor.fetchone()["count"]

        print("\nVerification Results:")
        print(f"  Total villa units: {total}")
        print(f"  Updated to 'فلة' format: {updated}")
        print(f"  Success rate: {(updated/total*100):.1f}%")

        return updated == total

    finally:
        conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("تحديث أسماء وحدات الفلل")
    print("Updating Villa Unit Names")
    print("=" * 60)
    print()

    update_villa_unit_names()

    print()
    if verify_update():
        print("✓ All villa units updated successfully!")
    else:
        print("⚠ Warning: Not all villa units were updated")
