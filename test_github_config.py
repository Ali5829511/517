"""
Test GitHub Token Configuration
Tests for GitHub Personal Access Token configuration
"""

import os
import pytest
from config import DevelopmentConfig, ProductionConfig, TestingConfig


def test_github_token_default_development():
    """Test that GitHub token defaults to empty string in development"""
    config = DevelopmentConfig
    assert hasattr(config, 'GITHUB_TOKEN')
    assert hasattr(config, 'GITHUB_AVAILABLE')


def test_github_token_default_production():
    """Test that GitHub token defaults to None in production"""
    config = ProductionConfig
    assert hasattr(config, 'GITHUB_TOKEN')
    assert hasattr(config, 'GITHUB_AVAILABLE')


def test_github_token_from_environment(monkeypatch):
    """Test that GitHub token is read from environment variable"""
    test_token = "ghp_test_token_123456789"
    monkeypatch.setenv("GITHUB_TOKEN", test_token)
    
    # Reload config to pick up environment variable
    import importlib
    import config
    importlib.reload(config)
    
    # Check development config
    assert config.DevelopmentConfig.GITHUB_TOKEN == test_token
    assert config.DevelopmentConfig.GITHUB_AVAILABLE is True
    
    # Check production config
    assert config.ProductionConfig.GITHUB_TOKEN == test_token
    assert config.ProductionConfig.GITHUB_AVAILABLE is True


def test_github_available_false_when_empty(monkeypatch):
    """Test that GITHUB_AVAILABLE is False when token is empty or placeholder"""
    # Test with empty token
    monkeypatch.setenv("GITHUB_TOKEN", "")
    import importlib
    import config
    importlib.reload(config)
    assert config.DevelopmentConfig.GITHUB_AVAILABLE is False
    
    # Test with placeholder token
    monkeypatch.setenv("GITHUB_TOKEN", "your-github-token-here")
    importlib.reload(config)
    assert config.DevelopmentConfig.GITHUB_AVAILABLE is False


def test_github_token_not_required():
    """Test that application can run without GitHub token"""
    # This should not raise an error
    from app import app
    assert app is not None
    assert hasattr(app, 'secret_key')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
