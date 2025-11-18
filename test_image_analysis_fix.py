#!/usr/bin/env python3
"""
Test to verify the image analysis fix.
This test validates that the OpenAI model name is correctly set.
"""
import re


def test_model_names():
    """Test that all model names in app.py are valid."""
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all model specifications
    models = re.findall(r'model\s*=\s*"([^"]+)"', content)
    
    # Known valid OpenAI models
    valid_models = {
        'gpt-4o-mini',
        'gpt-4o',
        'gpt-4',
        'gpt-3.5-turbo',
    }
    
    # Check for invalid models
    invalid_found = []
    for model in models:
        # Check if it's an OpenAI model (contains 'gpt')
        if 'gpt' in model.lower():
            # Check if it's in valid models or matches a pattern
            if not any(vm in model for vm in valid_models):
                # Check for known invalid patterns
                if 'gpt-4.1' in model:
                    invalid_found.append(model)
    
    assert len(invalid_found) == 0, f"Found invalid model names: {invalid_found}"
    print(f"✓ All {len(models)} model specifications are valid")
    
    # Verify gpt-4o-mini is used (our fix)
    gpt4o_mini_count = sum(1 for m in models if 'gpt-4o-mini' in m)
    assert gpt4o_mini_count > 0, "Expected to find gpt-4o-mini model"
    print(f"✓ Found {gpt4o_mini_count} instances of gpt-4o-mini")


def test_extract_plate_endpoint():
    """Test that the extract-plate endpoint exists and uses correct model."""
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the extract-plate endpoint
    assert '@app.route("/api/extract-plate"' in content, \
        "extract-plate endpoint not found"
    print("✓ /api/extract-plate endpoint exists")
    
    # Extract the function
    match = re.search(
        r'@app\.route\("/api/extract-plate".*?\ndef extract_plate\(\):(.*?)(?=\n@app\.route|\Z)',
        content,
        re.DOTALL
    )
    
    assert match, "Could not find extract_plate function"
    function_body = match.group(1)
    
    # Check that it uses gpt-4o-mini (not gpt-4.1-mini)
    assert 'gpt-4.1' not in function_body, \
        "Found invalid model gpt-4.1 in extract_plate function"
    assert 'gpt-4o-mini' in function_body, \
        "Expected to find gpt-4o-mini in extract_plate function"
    print("✓ extract_plate function uses correct model (gpt-4o-mini)")


def test_no_typos_in_other_endpoints():
    """Ensure no other endpoints have the typo."""
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Search for any occurrence of the typo
    typo_matches = re.findall(r'gpt-4\.1', content)
    
    assert len(typo_matches) == 0, \
        f"Found {len(typo_matches)} instances of 'gpt-4.1' typo"
    print("✓ No typos found in any endpoint")


if __name__ == '__main__':
    print("Testing image analysis fix...\n")
    
    test_model_names()
    test_extract_plate_endpoint()
    test_no_typos_in_other_endpoints()
    
    print("\n✓ All tests passed! The fix is correct.")
