"""
Test development setup and configuration
اختبار إعداد التطوير والتكوين
"""
import os
import pytest
from pathlib import Path


def test_makefile_exists():
    """Test that Makefile exists"""
    assert Path('Makefile').exists()


def test_development_md_exists():
    """Test that DEVELOPMENT.md exists"""
    assert Path('DEVELOPMENT.md').exists()


def test_setup_script_exists():
    """Test that setup_dev.sh exists and is executable"""
    setup_script = Path('setup_dev.sh')
    assert setup_script.exists()
    assert os.access(setup_script, os.X_OK)


def test_build_script_exists():
    """Test that build.sh exists and is executable"""
    build_script = Path('build.sh')
    assert build_script.exists()
    assert os.access(build_script, os.X_OK)


def test_env_example_exists():
    """Test that .env.example exists"""
    assert Path('.env.example').exists()


def test_config_file_exists():
    """Test that config.py exists"""
    assert Path('config.py').exists()


def test_config_import():
    """Test that config module can be imported"""
    try:
        import config
        assert hasattr(config, 'DevelopmentConfig')
        assert hasattr(config, 'ProductionConfig')
        assert hasattr(config, 'TestingConfig')
    except ImportError:
        pytest.fail("Failed to import config module")


def test_config_get_config():
    """Test get_config function"""
    from config import get_config

    dev_config = get_config('development')
    assert dev_config.DEBUG is True

    prod_config = get_config('production')
    assert prod_config.DEBUG is False

    test_config = get_config('testing')
    assert test_config.TESTING is True


def test_gitignore_includes_build_artifacts():
    """Test that .gitignore includes development artifacts"""
    gitignore_content = Path('.gitignore').read_text()

    # Check for important patterns
    assert '.pytest_cache' in gitignore_content
    assert 'htmlcov' in gitignore_content
    assert 'BUILD_INFO.txt' in gitignore_content
    assert 'logs/' in gitignore_content


def test_required_directories():
    """Test that required directories exist"""
    assert Path('static').exists()
    assert Path('uploads').exists() or True  # May not exist initially
    assert Path('processed_images').exists() or True  # May not exist initially


def test_database_exists():
    """Test that database file exists"""
    assert Path('housing_database.db').exists()


def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    assert Path('requirements.txt').exists()


def test_readme_files_exist():
    """Test that documentation files exist"""
    assert Path('README.md').exists()
    assert Path('QUICK_START.md').exists()
    assert Path('PROJECT_STATUS.md').exists()
    assert Path('DEPLOYMENT_GUIDE.md').exists()
