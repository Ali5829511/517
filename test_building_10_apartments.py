#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for verifying that building 10 has apartments 21 and 22.
Tests for issue #272: Add missing apartment 22 in building 10
"""

import sqlite3
import database_api


def test_building_10_has_22_apartments():
    """Test that building 10 (عمارة 10) has exactly 22 apartments"""
    conn = sqlite3.connect('housing_database.db')
    cursor = conn.cursor()

    # Get count of apartments in building 10
    cursor.execute("""
        SELECT COUNT(*)
        FROM units u
        JOIN buildings b ON u.building_id = b.id
        WHERE b.building_number = 'عمارة 10'
    """)
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 22, f"Building 10 should have 22 apartments, but has {count}"


def test_building_10_has_apartment_21():
    """Test that apartment 21 exists in building 10"""
    conn = sqlite3.connect('housing_database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.unit_number, u.unit_type, u.status
        FROM units u
        JOIN buildings b ON u.building_id = b.id
        WHERE b.building_number = 'عمارة 10' AND u.unit_number = '21'
    """)
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Apartment 21 should exist in building 10"
    assert result[0] == '21', "Unit number should be 21"
    assert result[1] == 'شقة', "Unit type should be شقة (apartment)"


def test_building_10_has_apartment_22():
    """Test that apartment 22 exists in building 10"""
    conn = sqlite3.connect('housing_database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.unit_number, u.unit_type, u.status
        FROM units u
        JOIN buildings b ON u.building_id = b.id
        WHERE b.building_number = 'عمارة 10' AND u.unit_number = '22'
    """)
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Apartment 22 should exist in building 10"
    assert result[0] == '22', "Unit number should be 22"
    assert result[1] == 'شقة', "Unit type should be شقة (apartment)"


def test_total_apartments_is_1022():
    """Test that total apartments count is now 1022"""
    conn = sqlite3.connect('housing_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM units WHERE unit_type = 'شقة'")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1022, f"Total apartments should be 1022, but is {count}"


def test_database_api_returns_building_10_with_22_units():
    """Test that database API correctly returns building 10 with all 22
    apartments"""
    units = database_api.get_all_units()
    building_10_units = [u for u in units if u['buildingNumber'] == 'عمارة 10']

    expected = 22
    actual = len(building_10_units)
    assert actual == expected, \
        f"API should return {expected} units for building 10, but returned {actual}"

    # Check that apartments 21 and 22 are present
    unit_numbers = [u['unitNumber'] for u in building_10_units]
    assert '21' in unit_numbers, "Apartment 21 should be in the API results"
    assert '22' in unit_numbers, "Apartment 22 should be in the API results"


def test_building_10_metadata_updated():
    """Test that building 10 metadata shows 22 total units"""
    conn = sqlite3.connect('housing_database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT total_units
        FROM buildings
        WHERE building_number = 'عمارة 10'
    """)
    total_units = cursor.fetchone()[0]
    conn.close()

    assert total_units == 22, \
        f"Building 10 total_units should be 22, but is {total_units}"
