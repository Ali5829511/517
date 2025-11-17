# GitHub Copilot Instructions for University Housing Management System
# نظام إدارة الإسكان الجامعي

## Quick Reference

**Essential Commands:**
- `make install` - Install dependencies
- `make test` - Run tests
- `make lint` - Check code quality
- `make dev` - Run development server
- `make format` - Auto-format code with Black

**Project Root:** `/home/runner/work/517/517` or current working directory  
**Main Files:** `app.py`, `database_api.py`, `config.py`  
**Database:** `housing_database.db` (SQLite3)  
**Language:** Bilingual (Arabic/English) - maintain both in user-facing content

---

## Project Overview

This is a comprehensive Faculty Housing Management System (نظام إدارة الإسكان الجامعي) for Imam Muhammad bin Saud Islamic University. It's a Flask-based web application with AI-powered features for managing residential units, residents, vehicle stickers, and parking spots.

### Key Features
- Resident management with 1,057 residents tracked
- Building management with 165 buildings
- 1,134 residential units
- 2,381 vehicle stickers
- AI-powered license plate recognition using OpenAI Vision API
- Arabic language support throughout the interface
- Administrative dashboard with comprehensive reporting

## Technology Stack

- **Backend:** Flask 3.0.0, Python 3.11+
- **Database:** SQLite3 with `housing_database.db`
- **AI/ML:** OpenAI API (GPT-4 Vision), EasyOCR, Tesseract, OpenCV
- **Frontend:** HTML/CSS/JavaScript (static files in `/static/`)
- **Authentication:** Flask-Login with bcrypt
- **Deployment:** Gunicorn, Railway/Render compatible

## Architecture & File Structure

### Core Application Files
- `app.py` - Main Flask application with routes and AI integration
- `database_api.py` - Database access layer with SQLite operations
- `config.py` - Configuration management (Development, Testing, Production)
- `generate_database.py` - Database initialization and seeding
- `generate_reports.py` - Report generation utilities

### Static Assets
- `/static/` - HTML pages, CSS, images (30+ HTML files)
- `/uploads/` - User-uploaded images
- `/processed_images/` - AI-processed vehicle plate images

### Testing & Development
- `test_app.py` - Basic Flask application tests
- `test_development_setup.py` - Development environment validation tests
- `Makefile` - Development commands (install, test, lint, build, etc.)
- `.env.example` - Environment variable template

## Coding Standards & Best Practices

### Python Style
- **Follow PEP 8** with 100 character line limit
- Use **Black** for automatic formatting: `make format`
- Use **Flake8** for linting: `make lint`
- Type hints are encouraged but not strictly enforced

### Naming Conventions
- Classes: `CamelCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Arabic Language Support
- This application has **extensive Arabic language support**
- Use UTF-8 encoding for all files with Arabic text
- Database tables include Arabic field names and values
- HTML files contain Arabic RTL (right-to-left) content
- Comments may be in Arabic or English - maintain consistency within files
- When adding new features, provide Arabic translations for user-facing text

### Documentation
- Use docstrings for all public functions and classes
- Include both Arabic and English descriptions when relevant
- Comment complex logic, but prefer self-documenting code
- Example:
```python
def get_all_residents():
    """
    الحصول على جميع السكان
    Get all residents from the database
    
    Returns:
        list: List of resident dictionaries with details
    """
```

## Development Workflow

### Setup Commands
```bash
make install          # Install dependencies
make install-dev      # Install dev dependencies (pytest, black, flake8)
make dev             # Run development server
make test            # Run tests
make lint            # Check code quality
make build           # Build for production
```

### Before Committing
1. Run `make test` to ensure tests pass
2. Run `make lint` to check code quality
3. Format code with `make format` if needed
4. Ensure no sensitive data (API keys) in commits

### Testing
- Write tests for new functionality in `test_app.py` or new `test_*.py` files
- Use pytest fixtures for shared setup
- Aim for meaningful test coverage, focus on critical paths
- Run `make test-cov` to check coverage

## Database Schema

### Key Tables
- `residents` - Faculty member information
- `buildings` - Building details
- `units` - Residential units (linked to buildings)
- `vehicle_stickers` - Vehicle registration and plates
- `parking_spots` - Parking space management
- `processed_images` - AI-processed vehicle images with metadata

### Database Operations
- Use `database_api.py` functions for all database access
- Foreign key constraints are enabled: `PRAGMA foreign_keys = ON`
- All functions return dictionaries or lists of dictionaries
- Connection handling is managed in `get_db_connection()`

## OpenAI Integration

### Configuration
- API key stored in environment variable `OPENAI_API_KEY`
- Client initialization with fallback handling in `app.py`
- `OPENAI_AVAILABLE` flag indicates API availability

### Usage Patterns
```python
if OPENAI_AVAILABLE and client:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[...]
    )
```

### Vision API for Plate Recognition
- Used for license plate detection and OCR
- Base64 image encoding for API submission
- Fallback to EasyOCR/Tesseract if OpenAI unavailable
- Results stored in `processed_images` table

## Security Considerations

### Authentication
- Flask-Login for session management
- Bcrypt for password hashing
- Session cookies: HttpOnly, SameSite protection
- CSRF protection via Flask-WTF

### API Keys & Secrets
- **NEVER commit API keys or secrets**
- Use `.env` file for local development (in `.gitignore`)
- Use environment variables in production
- Check `.env.example` for required variables

### Input Validation
- Validate and sanitize all user inputs
- Use `secure_filename()` for file uploads
- Parameterized SQL queries (avoid SQL injection)
- File type validation for uploads (images only)

## Common Tasks & Patterns

### Adding a New Route
```python
@app.route('/api/new_endpoint')
def new_endpoint():
    """Brief description of endpoint"""
    try:
        # Implementation
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"Error in new_endpoint: {e}")
        return jsonify({'error': str(e)}), 500
```

### Database Query Pattern
```python
def get_something():
    """Get something from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM table WHERE condition = ?', (value,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
```

### Error Handling
- Use try-except blocks for external operations (DB, API, file I/O)
- Log errors with `logger.error()` for debugging
- Return user-friendly error messages
- Include Arabic error messages for user-facing errors

## Environment Configuration

### Development
- `FLASK_ENV=development`
- `FLASK_DEBUG=1`
- Auto-reload enabled
- Detailed error pages

### Production
- `FLASK_ENV=production`
- `DEBUG=False`
- Use Gunicorn: `gunicorn app:app --bind 0.0.0.0:8000 --workers 4`
- HTTPS required (SESSION_COOKIE_SECURE=True)

### Required Environment Variables
```
OPENAI_API_KEY=sk-...           # OpenAI API key
SECRET_KEY=...                   # Flask secret key
DATABASE_PATH=housing_database.db
FLASK_ENV=development|production
```

## Deployment

### Supported Platforms
- **Railway** (primary): Auto-deploys from GitHub
- **Render**: Configured via `render.yaml`
- **Vercel**: Serverless configuration available

### Build Process
1. Install dependencies: `pip install -r requirements.txt`
2. Database is included in repo (housing_database.db)
3. Set environment variables on platform
4. Run with Gunicorn in production

## UI/UX Guidelines

### HTML Structure
- Static HTML files in `/static/` directory
- RTL (right-to-left) layout for Arabic content
- Responsive design with mobile optimization
- Imam University branding and logo

### Styling
- Consistent Arabic typography
- Blue and green color scheme (university colors)
- Print-friendly styles in `print_styles.css`
- Mobile-optimized CSS in `mobile_optimized.css`

## Performance Considerations

- SQLite database suitable for current scale (1000+ residents)
- Consider connection pooling for high traffic
- Image upload size limit: 16 MB
- AI processing is async-friendly but currently synchronous
- Static file caching disabled in development, enabled in production

## Maintenance & Operations

### Database Backup
```bash
make db-backup  # Creates timestamped backup
```

### Logs
- Configured in `config.py` (LOG_LEVEL, LOG_FILE)
- Production logs to `logs/app.log`
- Use `logger.info()`, `logger.warning()`, `logger.error()`

### Monitoring
- Check `/api/statistics` for system health
- Database record counts
- OpenAI API availability status

## Additional Notes

- **Language Context**: This is a bilingual project (Arabic/English)
- **University Context**: Imam Muhammad bin Saud Islamic University
- **Data Sensitivity**: Contains faculty personal information - handle with care
- **AI Features**: Optional but enhance user experience
- **Browser Support**: Modern browsers, IE not supported

## Getting Help

- Check `DEVELOPMENT.md` for detailed development guide
- See `QUICK_START.md` for quick setup instructions
- Review `DEPLOYMENT_GUIDE.md` for deployment details
- Makefile has `make help` command for available operations

## CI/CD Pipeline

### GitHub Actions Workflow
- **Workflow File**: `.github/workflows/python-package-conda.yml`
- **Trigger**: Runs on every push to any branch
- **Python Version**: 3.10 (via Conda)
- **Steps**:
  1. Checkout code
  2. Set up Python environment with Conda
  3. Install dependencies from `environment.yml`
  4. Run Flake8 linting (syntax errors cause failure)
  5. Run pytest tests

### CI Expectations
- All tests must pass before merging
- Linting must pass (E9, F63, F7, F82 errors will fail the build)
- Code complexity should be reasonable (max-complexity=10)
- Line length warnings at 127 characters

## Git Workflow

### Branching Strategy
- **main/master**: Production-ready code
- **feature/\***: New features (e.g., `feature/add-parking-reports`)
- **fix/\***: Bug fixes (e.g., `fix/vehicle-sticker-validation`)
- **copilot/\***: Automated branches created by Copilot agents

### Commit Messages
- Use clear, descriptive commit messages in English or Arabic
- Format: `<type>: <description>`
- Examples:
  - `feat: Add parking spot analytics dashboard`
  - `fix: Correct vehicle sticker validation logic`
  - `docs: Update deployment instructions`
  - `refactor: Improve database query performance`

### Before Pushing
1. Run `make test` - Ensure all tests pass
2. Run `make lint` - Check code quality
3. Run `make format` - Format code with Black
4. Review changes with `git diff`
5. Ensure no sensitive data (API keys, passwords) in commits

## Pull Request Guidelines

### Creating a PR
1. **Title**: Clear and descriptive (e.g., "Add vehicle sticker analytics feature")
2. **Description**: Include:
   - What changes were made
   - Why the changes were needed
   - How to test the changes
   - Any breaking changes or migration steps
   - Screenshots for UI changes
3. **Link Issues**: Reference related issues (e.g., "Fixes #123")
4. **Labels**: Add appropriate labels (bug, enhancement, documentation, etc.)

### PR Checklist
- [ ] Tests added/updated and passing
- [ ] Code follows project style guidelines
- [ ] Documentation updated (if needed)
- [ ] No console.log or debug code left in
- [ ] Arabic translations provided for user-facing text
- [ ] Security considerations reviewed
- [ ] Database migrations included (if schema changed)

### Code Review Process
- PRs require review before merging
- Address all review comments
- Keep PRs focused and reasonably sized
- Respond to feedback promptly

## Issue Reporting

### Bug Reports
When reporting bugs, include:
- **Description**: What went wrong?
- **Steps to Reproduce**: How can we reproduce the issue?
- **Expected Behavior**: What should happen?
- **Actual Behavior**: What actually happens?
- **Environment**: OS, Python version, browser (if applicable)
- **Screenshots**: If UI-related
- **Error Messages**: Full error text and stack traces

### Feature Requests
When requesting features, include:
- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives Considered**: Other approaches you've thought about
- **Impact**: Who will benefit from this feature?

## Common Pitfalls & Troubleshooting

### Database Issues
- **Problem**: Database locked errors
  - **Solution**: Ensure only one process accesses the database at a time
  - Close connections properly with `conn.close()`

- **Problem**: Foreign key constraint failures
  - **Solution**: Ensure `PRAGMA foreign_keys = ON` is set
  - Verify referenced records exist before insertion

### OpenAI API Issues
- **Problem**: API key not working
  - **Solution**: Check `.env` file or environment variables
  - Verify `OPENAI_AVAILABLE` flag in `app.py`

- **Problem**: Rate limiting
  - **Solution**: Implement exponential backoff
  - Use fallback OCR methods (EasyOCR, Tesseract)

### Arabic Text Issues
- **Problem**: Garbled Arabic text in database
  - **Solution**: Ensure UTF-8 encoding everywhere
  - Check database connection uses UTF-8

- **Problem**: Arabic not displaying correctly in browser
  - **Solution**: Verify HTML has `<meta charset="UTF-8">`
  - Check CSS includes RTL directives where needed

### Deployment Issues
- **Problem**: App crashes on Railway/Render
  - **Solution**: Check environment variables are set
  - Review logs for specific errors
  - Ensure Gunicorn configuration is correct

- **Problem**: Database not found in production
  - **Solution**: Verify `DATABASE_PATH` environment variable
  - Ensure database file is included in deployment

## When Making Changes

1. **Understand the context**: This is a production system for university housing
2. **Test thoroughly**: Run `make test` and `make lint` before committing
3. **Respect bilingual nature**: Maintain Arabic translations
4. **Security first**: Never expose sensitive data or credentials
5. **Document changes**: Update relevant documentation files
6. **Follow patterns**: Use existing code patterns for consistency
7. **Consider scale**: System manages 1000+ residents, 165 buildings
8. **Review CI/CD**: Ensure changes don't break the build pipeline
9. **Update tests**: Add tests for new functionality
10. **Check dependencies**: Run security checks before adding new packages

## Copilot Agent Guidelines

### When Assisting with Code
- **Always test changes**: Run `make test` and `make lint` after modifications
- **Preserve Arabic content**: Never remove or corrupt Arabic text - use UTF-8 encoding
- **Follow existing patterns**: Match the coding style and structure of existing files
- **Think security-first**: Validate inputs, use parameterized queries, never expose secrets
- **Document as you go**: Add docstrings for new functions with both Arabic and English

### When Suggesting Solutions
- **Provide runnable examples**: Include complete code snippets that can be tested
- **Reference existing code**: Point to similar implementations in the codebase
- **Consider the full stack**: Think about database, backend, frontend, and deployment impacts
- **Suggest testing approaches**: Recommend how to test the proposed changes

### When Creating New Features
- **Start with database**: Consider if schema changes are needed (check `database_api.py`)
- **Add API endpoints**: Follow the pattern in `app.py` with proper error handling
- **Update frontend**: Add corresponding HTML/CSS/JS in `/static/` directory
- **Provide translations**: Include both Arabic and English text for user-facing features
- **Write tests**: Add test cases in `test_app.py` or new test files

### Do Not
- Remove or modify existing tests unless fixing a bug
- Change core database schema without careful consideration
- Disable security features or validation
- Remove Arabic language support
- Commit API keys or sensitive data
- Break backward compatibility without discussion

---

**Built with assistance from Manus AI for Imam Muhammad bin Saud Islamic University**
