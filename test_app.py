"""Basic tests for the housing system application."""
import pytest


def test_imports():
    """Test that main modules can be imported."""
    import app
    import database_api
    
    assert app is not None
    assert database_api is not None


def test_app_creation():
    """Test that the Flask app is created successfully."""
    from app import app
    
    assert app is not None
    assert app.secret_key is not None


def test_gpt_model_names():
    """Test that GPT model names are correct (no typos)."""
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that the correct model name is used
    assert 'gpt-4o-mini' in content
    
    # Check that the typo is not present
    assert 'gpt-4.1-mini' not in content, "Found typo 'gpt-4.1-mini' instead of 'gpt-4o-mini'"


def test_app_routes():
    """Test that essential routes are defined."""
    from app import app
    
    # Get all registered routes
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    
    # Check for essential routes
    assert '/' in routes
    assert '/api/login' in routes
    assert '/api/extract-plate' in routes


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
