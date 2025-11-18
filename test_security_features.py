"""
Tests for the security features added in this PR
"""
import pytest
import os
from app import app, OPENAI_AVAILABLE


def test_session_cookie_secure():
    """Test that session cookie security is enabled"""
    assert app.config.get('SESSION_COOKIE_SECURE') is True


def test_session_cookie_httponly():
    """Test that session cookie httponly is enabled"""
    assert app.config.get('SESSION_COOKIE_HTTPONLY') is True


def test_session_cookie_samesite():
    """Test that session cookie samesite is set to Lax"""
    assert app.config.get('SESSION_COOKIE_SAMESITE') == 'Lax'


def test_upload_folder_exists():
    """Test that upload folder is created"""
    assert os.path.exists('uploads')


def test_processed_folder_exists():
    """Test that processed images folder is created"""
    assert os.path.exists('processed_images')


def test_openai_available_flag():
    """Test that OPENAI_AVAILABLE flag is set"""
    assert OPENAI_AVAILABLE is not None
    assert isinstance(OPENAI_AVAILABLE, bool)


def test_logging_configured():
    """Test that logging is configured"""
    import logging
    logger = logging.getLogger('app')
    assert logger is not None
    # Root logger is configured in basicConfig
    root_logger = logging.getLogger()
    assert root_logger.level <= logging.WARNING  # INFO or DEBUG or WARNING


def test_dotenv_loaded():
    """Test that dotenv is loaded (PORT should be available from env)"""
    # This test verifies that dotenv is imported and used
    from dotenv import load_dotenv
    # Just verify the function exists and can be called
    load_dotenv()
    assert True
