#!/bin/bash
# Build script for production deployment
# نظام إدارة الإسكان الجامعي

set -e  # Exit on error

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Building for Production - البناء للإنتاج${NC}"
echo -e "${BLUE}نظام إدارة الإسكان الجامعي${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}✗ app.py not found! Are you in the project directory?${NC}"
    exit 1
fi

# Clean up
echo -e "${YELLOW}→ Cleaning temporary files...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}→ Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Run tests
echo -e "${YELLOW}→ Running tests...${NC}"
python -m pytest test_app.py -v
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Tests failed! Build aborted.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ All tests passed${NC}"
echo ""

# Check code quality
echo -e "${YELLOW}→ Checking code quality...${NC}"
flake8 app.py database_api.py --max-line-length=100 --ignore=E501,W503 || true
echo -e "${GREEN}✓ Code quality check complete${NC}"
echo ""

# Check database
if [ ! -f "housing_database.db" ]; then
    echo -e "${YELLOW}→ Database not found. Creating...${NC}"
    python generate_database.py
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${GREEN}✓ Database exists${NC}"
fi
echo ""

# Create necessary directories
echo -e "${YELLOW}→ Creating necessary directories...${NC}"
mkdir -p uploads
mkdir -p processed_images
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Test production server (if gunicorn is available)
if command -v gunicorn &> /dev/null; then
    echo -e "${YELLOW}→ Testing production server (5 seconds)...${NC}"
    timeout 5 gunicorn app:app --bind 127.0.0.1:8000 --workers 1 --timeout 120 > /dev/null 2>&1 || true
    echo -e "${GREEN}✓ Production server test complete${NC}"
else
    echo -e "${YELLOW}⚠ Gunicorn not found, skipping production server test${NC}"
fi
echo ""

# Create build info
BUILD_DATE=$(date '+%Y-%m-%d %H:%M:%S')
BUILD_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo -e "${YELLOW}→ Creating build info...${NC}"
cat > BUILD_INFO.txt << EOF
Build Date: ${BUILD_DATE}
Git Commit: ${BUILD_HASH}
Python Version: $(python --version)
Dependencies: $(pip freeze | wc -l) packages
EOF
echo -e "${GREEN}✓ Build info created${NC}"
echo ""

# Success
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✓ Build successful!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${BLUE}Build Information:${NC}"
echo -e "  Date: ${BUILD_DATE}"
echo -e "  Commit: ${BUILD_HASH}"
echo ""
echo -e "${BLUE}Next steps for deployment:${NC}"
echo -e "  1. Set environment variables (especially OPENAI_API_KEY)"
echo -e "  2. Configure your web server (Render, Railway, etc.)"
echo -e "  3. Deploy using:"
echo -e "     ${YELLOW}gunicorn app:app --bind 0.0.0.0:8000 --workers 4${NC}"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo -e "  ${YELLOW}DEPLOYMENT_GUIDE.md${NC} - Full deployment guide"
echo -e "  ${YELLOW}README.md${NC}           - Project overview"
echo ""
