#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبارات ميزات فرز الصور
Image sorting features tests
"""

import pytest
import os


def test_image_sorting_js_exists():
    """Test that image sorting JavaScript file exists"""
    js_file = "static/image_sorting_features.js"
    assert os.path.exists(js_file), "Image sorting JS file should exist"
    
    # Check file size (should be substantial)
    file_size = os.path.getsize(js_file)
    assert file_size > 5000, "Image sorting JS file should contain substantial code"


def test_comprehensive_image_processing_updated():
    """Test that comprehensive image processing page includes sorting features"""
    html_file = "static/comprehensive_image_processing.html"
    assert os.path.exists(html_file), "Comprehensive image processing HTML should exist"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that sorting script is included
    assert "image_sorting_features.js" in content, \
        "Sorting features script should be included"
    
    # Check for sorting integration
    assert "applyAutoSorting" in content or "autoSortEnabled" in content, \
        "Sorting integration code should be present"


def test_sorting_features_functions():
    """Test that sorting features JavaScript contains required functions"""
    js_file = "static/image_sorting_features.js"
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required functions
    required_functions = [
        'addSortingControls',
        'toggleAutoSort',
        'toggleDeleteAfter',
        'applyAutoSorting',
        'sortImagesByCategory',
        'exportSortingReport',
        'showSortingStatistics',
        'deleteProcessedImages'
    ]
    
    for func in required_functions:
        assert f"function {func}" in content, \
            f"Function {func} should be defined in sorting features"


def test_sorting_constants_defined():
    """Test that sorting constants are properly defined"""
    js_file = "static/image_sorting_features.js"
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for constants
    assert "CONFIDENCE_THRESHOLD" in content, "Confidence threshold should be defined"
    assert "autoSortEnabled" in content, "Auto sort flag should be defined"
    assert "deleteAfterProcess" in content, "Delete after process flag should be defined"


def test_arabic_support_in_sorting():
    """Test that sorting features have Arabic language support"""
    js_file = "static/image_sorting_features.js"
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for Arabic text
    arabic_terms = ['فرز', 'حذف', 'معالجة', 'تلقائي']
    for term in arabic_terms:
        assert term in content, f"Arabic term '{term}' should be present"


def test_category_types_defined():
    """Test that all category types are defined"""
    js_file = "static/image_sorting_features.js"
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for all category types
    categories = [
        'normal',
        'disabled',
        'violation',
        'old_buildings',
        'new_buildings',
        'villas',
        'impounded',
        'tow_truck',
        'other'
    ]
    
    for category in categories:
        assert f"'{category}'" in content or f'"{category}"' in content, \
            f"Category '{category}' should be defined"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
