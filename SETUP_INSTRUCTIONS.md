# Setup Instructions - تعليمات الإعداد

## Local Development Setup - إعداد البيئة المحلية

### 1. Install Dependencies - تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables - إعداد متغيرات البيئة

Create a `.env` file in the project root by copying the example file:

```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```env
# OpenAI API Key (required for AI features)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-actual-api-key-here

# Other configuration
FLASK_ENV=development
PORT=5000
```

**Note:** If you want to test without OpenAI (mock mode), you can leave `OPENAI_API_KEY` empty or not set it. The application will work in fallback mode using local OCR.

### 3. Run the Application - تشغيل التطبيق

```bash
python app.py
```

Or using Flask directly:

```bash
flask run --host=0.0.0.0 --port=5000
```

The application will be available at: `http://localhost:5000`

### 4. Test the Application - اختبار التطبيق

1. Open your browser and navigate to `http://localhost:5000`
2. Login with default credentials:
   - Username: `admin`
   - Password: `Admin@2025`
3. Test uploading images for license plate extraction
4. Check that files are saved in `uploads/` directory
5. Verify that session cookies are working properly

## Environment Variables - متغيرات البيئة

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | - | No (falls back to local OCR) |
| `FLASK_ENV` | Flask environment (development/production) | development | No |
| `PORT` | Server port | 5000 | No |
| `DATABASE_PATH` | Path to SQLite database | housing_database.db | No |
| `SECRET_KEY` | Flask secret key for sessions | (auto-generated) | No |

## Security Notes - ملاحظات أمنية

- **Development Mode**: HTTP connections are allowed for easier local testing
- **Production Mode**: Set `FLASK_ENV=production` in `.env` to enforce HTTPS-only cookies
- **API Keys**: Never commit `.env` file to version control (it's already in `.gitignore`)
- **File Uploads**: All uploaded files are saved securely using `secure_filename()`
- **Session Cookies**: Configured with `HTTPONLY` and `SAMESITE=Lax` for security

## Troubleshooting - حل المشاكل

### OpenAI Module Not Found
If you see `ModuleNotFoundError: No module named 'openai'`:
```bash
pip install openai>=1.0.0
```

### No API Key Warning
If you see "OPENAI_API_KEY not found in environment variables":
- This is normal if you haven't set the API key
- The app will work in fallback mode using local OCR
- To use AI features, add your API key to `.env`

### Upload Folder Issues
The `uploads/` and `processed_images/` folders are created automatically on startup.
If you encounter permission errors, create them manually:
```bash
mkdir -p uploads processed_images
chmod 755 uploads processed_images
```

## Production Deployment - النشر في الإنتاج

For production deployment:

1. Set environment variables:
   ```
   FLASK_ENV=production
   OPENAI_API_KEY=your-real-api-key
   ```

2. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. Configure HTTPS with nginx or similar reverse proxy

4. Ensure session cookies are secure (HTTPS-only)

## Testing Mock Mode - اختبار الوضع التجريبي

To test the application without OpenAI API:

1. Don't set `OPENAI_API_KEY` in `.env` (or leave it empty)
2. Run the application
3. The app will show warnings but continue to work
4. API endpoints will return 503 for AI features or fall back to local OCR
5. All other features will work normally

This is useful for:
- Development without API costs
- Testing error handling
- CI/CD pipelines
