"""
Basic tests for the Flask application
"""
import pytest
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


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_static_folder_exists(client):
    """Test that static folder is configured"""
    assert app.static_folder is not None
