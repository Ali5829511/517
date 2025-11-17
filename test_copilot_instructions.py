"""
Test GitHub Copilot Instructions Configuration
Tests to verify copilot-instructions.md is properly configured
"""

import os
import re


def test_copilot_instructions_file_exists():
    """Test that copilot-instructions.md exists in .github directory"""
    instructions_path = '.github/copilot-instructions.md'
    assert os.path.exists(instructions_path), \
        "copilot-instructions.md should exist in .github directory"


def test_copilot_instructions_readable():
    """Test that the file is readable and contains content"""
    instructions_path = '.github/copilot-instructions.md'
    with open(instructions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert len(content) > 1000, \
        "Instructions should be comprehensive (> 1000 chars)"
    assert content.strip(), "Instructions file should not be empty"


def test_copilot_instructions_has_required_sections():
    """Test that all required sections are present"""
    instructions_path = '.github/copilot-instructions.md'
    with open(instructions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_sections = [
        "Project Overview",
        "Technology Stack",
        "Coding Standards",
        "Development Workflow",
        "Testing",
        "Security",
        "Quick Reference"
    ]
    
    for section in required_sections:
        assert section in content, \
            f"Instructions should include '{section}' section"


def test_copilot_instructions_has_commands():
    """Test that essential commands are documented"""
    instructions_path = '.github/copilot-instructions.md'
    with open(instructions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    essential_commands = [
        "make test",
        "make lint",
        "make install",
        "make dev"
    ]
    
    for command in essential_commands:
        assert command in content, \
            f"Instructions should document '{command}' command"


def test_copilot_instructions_mentions_bilingual():
    """Test that bilingual nature is documented"""
    instructions_path = '.github/copilot-instructions.md'
    with open(instructions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "Arabic" in content or "العربية" in content or "نظام" in content, \
        "Instructions should mention Arabic language support"


def test_copilot_instructions_has_security_guidance():
    """Test that security considerations are documented"""
    instructions_path = '.github/copilot-instructions.md'
    with open(instructions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    security_topics = ["security", "API key", "secret", "password", "credential"]
    found = any(topic.lower() in content.lower() for topic in security_topics)
    
    assert found, \
        "Instructions should include security guidance"


def test_copilot_instructions_proper_markdown():
    """Test that the file uses proper markdown formatting"""
    instructions_path = '.github/copilot-instructions.md'
    with open(instructions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for markdown headers
    assert re.search(r'^#+ ', content, re.MULTILINE), \
        "Instructions should use markdown headers"
    
    # Check for code blocks
    assert '```' in content, \
        "Instructions should include code examples in code blocks"


def test_copilot_instructions_has_agent_guidelines():
    """Test that Copilot Agent Guidelines section exists"""
    instructions_path = '.github/copilot-instructions.md'
    with open(instructions_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "Copilot Agent Guidelines" in content or "Agent Guidelines" in content, \
        "Instructions should include Copilot Agent Guidelines section"


if __name__ == "__main__":
    # Run tests manually
    import sys
    
    tests = [
        test_copilot_instructions_file_exists,
        test_copilot_instructions_readable,
        test_copilot_instructions_has_required_sections,
        test_copilot_instructions_has_commands,
        test_copilot_instructions_mentions_bilingual,
        test_copilot_instructions_has_security_guidance,
        test_copilot_instructions_proper_markdown,
        test_copilot_instructions_has_agent_guidelines,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
    
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(0 if failed == 0 else 1)
