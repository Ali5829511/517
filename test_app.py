"""
Basic tests for the Flask application
"""

from app import app


def test_app_exists():
    """Test that the Flask app is created"""
    assert app is not None


def test_app_is_flask_instance():
    """Test that app is a Flask instance"""
    from flask import Flask

    assert isinstance(app, Flask)


def test_app_has_secret_key():
    """Test that the app has a secret key configured"""
    assert app.secret_key is not None
    assert len(app.secret_key) > 0


def test_static_folder_exists():
    """Test that static folder is configured"""
    assert app.static_folder is not None


def test_version_endpoint():
    """Test that the version endpoint works"""
    with app.test_client() as client:
        response = client.get('/api/version')
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data
        assert 'version' in data['data']
        assert 'app_name' in data['data']


def test_statistics_endpoint():
    """Test that the statistics endpoint works"""
    with app.test_client() as client:
        response = client.get('/api/statistics')
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
