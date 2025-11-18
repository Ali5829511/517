#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبارات لأسماء وحدات الفلل
Tests for villa unit names
"""

import sqlite3
import pytest


DATABASE = "housing_database.db"


def test_villa_units_exist():
    """Test that villa units exist in the database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) as count
        FROM units u
        JOIN buildings b ON u.building_id = b.id
        WHERE b.building_type = 'فيلا'
    """
    )

    count = cursor.fetchone()[0]
    conn.close()

    assert count == 114, f"Expected 114 villa units, found {count}"


def test_villa_units_naming_convention():
    """Test that all villa units use the 'فلة' naming convention"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Count units with new naming convention
    cursor.execute(
        """
        SELECT COUNT(*) as count
        FROM units u
        JOIN buildings b ON u.building_id = b.id
        WHERE b.building_type = 'فيلا' AND u.unit_number LIKE 'فلة%'
    """
    )

    count = cursor.fetchone()[0]
    conn.close()

    assert count == 114, f"Expected 114 units with 'فلة' naming, found {count}"


def test_villa_units_sequential():
    """Test that villa units are numbered sequentially from 1 to 114"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT u.unit_number
        FROM units u
        JOIN buildings b ON u.building_id = b.id
        WHERE b.building_type = 'فيلا'
        ORDER BY b.id
    """
    )

    units = [row["unit_number"] for row in cursor.fetchall()]
    conn.close()

    # Check that we have exactly 114 units
    assert len(units) == 114

    # Check that all units follow the expected pattern
    expected = [f"فلة{i}" for i in range(1, 115)]
    assert units == expected, "Villa units are not numbered sequentially"


def test_villa_units_unique():
    """Test that all villa unit names are unique"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT u.unit_number, COUNT(*) as count
        FROM units u
        JOIN buildings b ON u.building_id = b.id
        WHERE b.building_type = 'فيلا'
        GROUP BY u.unit_number
        HAVING count > 1
    """
    )

    duplicates = cursor.fetchall()
    conn.close()

    assert len(duplicates) == 0, f"Found duplicate unit names: {duplicates}"


def test_villa_buildings_match_units():
    """Test that each villa building has exactly one unit"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT b.building_number, COUNT(u.id) as unit_count
        FROM buildings b
        LEFT JOIN units u ON b.id = u.building_id
        WHERE b.building_type = 'فيلا'
        GROUP BY b.id
    """
    )

    results = cursor.fetchall()
    conn.close()

    for building_number, unit_count in results:
        assert (
            unit_count == 1
        ), f"Building {building_number} has {unit_count} units, expected 1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
