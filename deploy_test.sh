#!/bin/bash
# Deployment Test Script
# نظام إدارة الإسكان الجامعي
# This script tests the deployment configuration locally

set -e  # Exit on error

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Testing Deployment Configuration${NC}"
echo -e "${BLUE}اختبار إعدادات النشر${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}✗ app.py not found! Are you in the project directory?${NC}"
    exit 1
fi

# Check Python version
echo -e "${YELLOW}→ Checking Python version...${NC}"
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"
echo ""

# Check required files
echo -e "${YELLOW}→ Checking deployment files...${NC}"
REQUIRED_FILES=("Procfile" "requirements.txt" "runtime.txt" "render.yaml" "railway.json" "app.py" "housing_database.db")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓ $file${NC}"
    else
        echo -e "  ${RED}✗ $file (missing)${NC}"
    fi
done
echo ""

# Validate Procfile
echo -e "${YELLOW}→ Validating Procfile...${NC}"
if grep -q "web: gunicorn app:app" Procfile; then
    echo -e "${GREEN}✓ Procfile is valid${NC}"
else
    echo -e "${RED}✗ Procfile has issues${NC}"
fi
echo ""

# Check for extra blank lines in Procfile
echo -e "${YELLOW}→ Checking Procfile format...${NC}"
PROCFILE_LINES=$(wc -l < Procfile)
if [ "$PROCFILE_LINES" -eq 1 ]; then
    echo -e "${GREEN}✓ Procfile format is correct (1 line)${NC}"
else
    echo -e "${YELLOW}⚠ Procfile has $PROCFILE_LINES lines (should be 1)${NC}"
fi
echo ""

# Check render.yaml
echo -e "${YELLOW}→ Validating render.yaml...${NC}"
if grep -q "gunicorn app:app --bind 0.0.0.0:\$PORT" render.yaml; then
    echo -e "${GREEN}✓ render.yaml has correct start command${NC}"
else
    echo -e "${RED}✗ render.yaml needs update${NC}"
fi
echo ""

# Check railway.json
echo -e "${YELLOW}→ Validating railway.json...${NC}"
if [ -f "railway.json" ]; then
    if python -m json.tool railway.json > /dev/null 2>&1; then
        echo -e "${GREEN}✓ railway.json is valid JSON${NC}"
    else
        echo -e "${RED}✗ railway.json has invalid JSON${NC}"
    fi
else
    echo -e "${YELLOW}⚠ railway.json not found${NC}"
fi
echo ""

# Check .env.example
echo -e "${YELLOW}→ Checking .env.example...${NC}"
if [ -f ".env.example" ]; then
    echo -e "${GREEN}✓ .env.example exists${NC}"
    if grep -q "OPENAI_API_KEY" .env.example; then
        echo -e "${GREEN}✓ Contains OPENAI_API_KEY${NC}"
    fi
else
    echo -e "${RED}✗ .env.example not found${NC}"
fi
echo ""

# Check database
echo -e "${YELLOW}→ Checking database...${NC}"
if [ -f "housing_database.db" ]; then
    DB_SIZE=$(du -h housing_database.db | awk '{print $1}')
    echo -e "${GREEN}✓ Database exists (size: $DB_SIZE)${NC}"
else
    echo -e "${RED}✗ Database not found${NC}"
fi
echo ""

# Check required directories
echo -e "${YELLOW}→ Checking required directories...${NC}"
REQUIRED_DIRS=("static" "uploads" "processed_images" "logs")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓ $dir/${NC}"
    else
        echo -e "  ${YELLOW}⚠ $dir/ (will be created)${NC}"
        mkdir -p "$dir"
    fi
done
echo ""

# Test gunicorn
echo -e "${YELLOW}→ Testing gunicorn...${NC}"
if command -v gunicorn &> /dev/null; then
    echo -e "${GREEN}✓ Gunicorn is installed${NC}"
    
    # Test if app can be imported
    if python -c "from app import app" 2>/dev/null; then
        echo -e "${GREEN}✓ App can be imported${NC}"
    else
        echo -e "${RED}✗ App import failed (check dependencies)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Gunicorn not installed (required for production)${NC}"
    echo -e "${YELLOW}  Install with: pip install gunicorn${NC}"
fi
echo ""

# Final summary
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✓ Deployment configuration check complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${BLUE}Next steps for deployment:${NC}"
echo -e "  1. Commit and push changes to GitHub"
echo -e "  2. Deploy on your chosen platform:"
echo -e "     - Railway.app (recommended)"
echo -e "     - Render.com"
echo -e "     - Vercel"
echo -e "     - Heroku"
echo -e "  3. Set environment variables:"
echo -e "     - FLASK_ENV=production"
echo -e "     - OPENAI_API_KEY=your-key (optional)"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo -e "  ${YELLOW}DEPLOYMENT.md${NC} - Comprehensive deployment guide"
echo -e "  ${YELLOW}README.md${NC}     - Project overview"
echo ""
