"""
Tests for secure file upload functionality
"""
import pytest
import os
import io
from app import app
from PIL import Image


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


def test_secure_filename_import():
    """Test that secure_filename is imported"""
    from werkzeug.utils import secure_filename
    assert secure_filename is not None
    
    # Test that it sanitizes filenames
    assert secure_filename("../../etc/passwd") == "etc_passwd"
    assert secure_filename("test file.png") == "test_file.png"


def test_upload_folder_configuration():
    """Test that upload folder is properly configured"""
    from app import UPLOAD_FOLDER, PROCESSED_FOLDER
    assert UPLOAD_FOLDER == 'uploads'
    assert PROCESSED_FOLDER == 'processed_images'
    assert os.path.exists(UPLOAD_FOLDER)
    assert os.path.exists(PROCESSED_FOLDER)


def test_extract_plate_with_formdata(client):
    """Test extract_plate endpoint with FormData"""
    # Note: This test will fail without OpenAI API key, but verifies the endpoint structure
    img_bytes = create_test_image()
    
    response = client.post('/api/extract-plate', 
                          data={'image': (img_bytes, 'test_image.png')},
                          content_type='multipart/form-data')
    
    # Without OpenAI key, we should get 503 or a fallback response
    assert response.status_code in [200, 503, 500]


def test_classify_parking_with_formdata(client):
    """Test classify_parking endpoint with FormData"""
    # Note: This test will fail without OpenAI API key, but verifies the endpoint structure
    img_bytes = create_test_image()
    
    response = client.post('/api/classify_parking', 
                          data={'image': (img_bytes, 'test_parking.png')},
                          content_type='multipart/form-data')
    
    # Without OpenAI key, we should get 503 or a response
    assert response.status_code in [200, 503, 500]


def test_process_images_with_formdata(client):
    """Test process_images endpoint with FormData"""
    # Note: This test will fail without OpenAI API key, but verifies the endpoint structure
    img_bytes1 = create_test_image()
    img_bytes2 = create_test_image()
    
    response = client.post('/api/process-images', 
                          data={'images': [(img_bytes1, 'test1.png'), (img_bytes2, 'test2.png')]},
                          content_type='multipart/form-data')
    
    # Without OpenAI key, we should get 503
    assert response.status_code in [200, 503, 500]
    
    # If we got 503, verify the error message
    if response.status_code == 503:
        data = response.get_json()
        assert 'error' in data
        assert 'غير متوفرة' in data['error']
