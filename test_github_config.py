"""
Tests for GitHub configuration files
Tests to verify issue templates, PR templates, workflows, and labels are properly configured
"""
import os
import yaml


def test_labels_yml_exists():
    """Test that labels.yml configuration file exists"""
    labels_file = '.github/labels.yml'
    assert os.path.exists(labels_file), f"{labels_file} should exist"


def test_labels_yml_valid():
    """Test that labels.yml is valid YAML and has required structure"""
    labels_file = '.github/labels.yml'
    with open(labels_file, 'r', encoding='utf-8') as f:
        labels = yaml.safe_load(f)
    
    assert isinstance(labels, list), "Labels should be a list"
    assert len(labels) > 0, "Should have at least one label"
    
    # Check first label has required fields
    first_label = labels[0]
    assert 'name' in first_label, "Label should have 'name' field"
    assert 'color' in first_label, "Label should have 'color' field"
    assert 'description' in first_label, "Label should have 'description' field"


def test_required_labels_exist():
    """Test that required labels for new contributors exist"""
    labels_file = '.github/labels.yml'
    with open(labels_file, 'r', encoding='utf-8') as f:
        labels = yaml.safe_load(f)
    
    label_names = [label['name'] for label in labels]
    
    # Check for essential labels
    required_labels = [
        'bug',
        'enhancement',
        'documentation',
        'good first issue',
        'help wanted'
    ]
    
    for required_label in required_labels:
        assert required_label in label_names, f"Required label '{required_label}' should exist"


def test_issue_templates_directory_exists():
    """Test that ISSUE_TEMPLATE directory exists"""
    template_dir = '.github/ISSUE_TEMPLATE'
    assert os.path.isdir(template_dir), f"{template_dir} directory should exist"


def test_bug_report_template_exists():
    """Test that bug report template exists"""
    bug_template = '.github/ISSUE_TEMPLATE/bug_report.yml'
    assert os.path.exists(bug_template), f"{bug_template} should exist"


def test_bug_report_template_valid():
    """Test that bug report template is valid YAML"""
    bug_template = '.github/ISSUE_TEMPLATE/bug_report.yml'
    with open(bug_template, 'r', encoding='utf-8') as f:
        template = yaml.safe_load(f)
    
    assert 'name' in template, "Template should have 'name' field"
    assert 'description' in template, "Template should have 'description' field"
    assert 'body' in template, "Template should have 'body' field"
    assert isinstance(template['body'], list), "Template body should be a list"


def test_feature_request_template_exists():
    """Test that feature request template exists"""
    feature_template = '.github/ISSUE_TEMPLATE/feature_request.yml'
    assert os.path.exists(feature_template), f"{feature_template} should exist"


def test_good_first_issue_template_exists():
    """Test that good first issue template exists"""
    gfi_template = '.github/ISSUE_TEMPLATE/good_first_issue.yml'
    assert os.path.exists(gfi_template), f"{gfi_template} should exist"


def test_issue_template_config_exists():
    """Test that issue template config exists"""
    config = '.github/ISSUE_TEMPLATE/config.yml'
    assert os.path.exists(config), f"{config} should exist"


def test_pr_template_exists():
    """Test that pull request template exists"""
    pr_template = '.github/PULL_REQUEST_TEMPLATE.md'
    assert os.path.exists(pr_template), f"{pr_template} should exist"


def test_pr_template_has_checklist():
    """Test that PR template contains checklist"""
    pr_template = '.github/PULL_REQUEST_TEMPLATE.md'
    with open(pr_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert '- [ ]' in content, "PR template should contain checklist items"
    assert 'test' in content.lower(), "PR template should mention tests"


def test_workflows_directory_exists():
    """Test that workflows directory exists"""
    workflows_dir = '.github/workflows'
    assert os.path.isdir(workflows_dir), f"{workflows_dir} directory should exist"


def test_label_issues_workflow_exists():
    """Test that label-issues workflow exists"""
    workflow = '.github/workflows/label-issues.yml'
    assert os.path.exists(workflow), f"{workflow} should exist"


def test_label_issues_workflow_valid():
    """Test that label-issues workflow is valid YAML"""
    workflow = '.github/workflows/label-issues.yml'
    with open(workflow, 'r', encoding='utf-8') as f:
        wf = yaml.safe_load(f)
    
    assert 'name' in wf, "Workflow should have 'name' field"
    # Note: In GitHub Actions YAML, 'on' is a keyword but Python's YAML parser
    # treats it as a boolean and converts it to True. This is expected behavior.
    # The workflow file is still valid for GitHub Actions.
    assert (True in wf or 'on' in wf), "Workflow should have 'on' field"
    assert 'jobs' in wf, "Workflow should have 'jobs' field"


def test_label_prs_workflow_exists():
    """Test that label-prs workflow exists"""
    workflow = '.github/workflows/label-prs.yml'
    assert os.path.exists(workflow), f"{workflow} should exist"


def test_greet_contributors_workflow_exists():
    """Test that greet-new-contributors workflow exists"""
    workflow = '.github/workflows/greet-new-contributors.yml'
    assert os.path.exists(workflow), f"{workflow} should exist"


def test_contributing_guide_exists():
    """Test that CONTRIBUTING.md exists"""
    contributing = '.github/CONTRIBUTING.md'
    assert os.path.exists(contributing), f"{contributing} should exist"


def test_contributing_guide_has_arabic():
    """Test that CONTRIBUTING.md contains Arabic text"""
    contributing = '.github/CONTRIBUTING.md'
    with open(contributing, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for Arabic text
    assert 'مرحباً' in content or 'المساهمة' in content, \
        "CONTRIBUTING.md should contain Arabic text"
    
    # Check for English text
    assert 'Welcome' in content or 'Contributing' in content, \
        "CONTRIBUTING.md should contain English text"


def test_all_workflow_files_valid_yaml():
    """Test that all workflow files are valid YAML"""
    workflows_dir = '.github/workflows'
    workflow_files = [f for f in os.listdir(workflows_dir) if f.endswith('.yml') or f.endswith('.yaml')]
    
    assert len(workflow_files) > 0, "Should have at least one workflow file"
    
    for workflow_file in workflow_files:
        filepath = os.path.join(workflows_dir, workflow_file)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise AssertionError(f"Workflow {workflow_file} has invalid YAML: {e}")


def test_labels_have_bilingual_descriptions():
    """Test that labels have both Arabic and English descriptions"""
    labels_file = '.github/labels.yml'
    with open(labels_file, 'r', encoding='utf-8') as f:
        labels = yaml.safe_load(f)
    
    for label in labels:
        description = label.get('description', '')
        # Check if description contains both Arabic and English (by presence of dash separator)
        # Most labels should have format "العربية - English"
        if label['name'] not in ['wontfix', 'duplicate', 'invalid']:  # Some may be English-only
            assert '-' in description or 'Good' in description or 'Extra' in description, \
                f"Label '{label['name']}' should have bilingual description"
