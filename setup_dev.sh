#!/bin/bash
# إعداد بيئة التطوير - Development Environment Setup
# نظام إدارة الإسكان الجامعي

set -e  # Exit on error

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}إعداد بيئة التطوير - Development Environment Setup${NC}"
echo -e "${BLUE}نظام إدارة الإسكان الجامعي${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}→ Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found! Please install Python 3.11 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}→ Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}→ Removing old virtual environment...${NC}"
        rm -rf venv
    else
        echo -e "${GREEN}✓ Using existing virtual environment${NC}"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}→ Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}→ Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${YELLOW}→ Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install production dependencies
echo -e "${YELLOW}→ Installing production dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Production dependencies installed${NC}"
echo ""

# Install development dependencies
echo -e "${YELLOW}→ Installing development dependencies...${NC}"
pip install pytest pytest-cov black flake8 pylint mypy bandit safety > /dev/null 2>&1
echo -e "${GREEN}✓ Development dependencies installed${NC}"
echo ""

# Create necessary directories
echo -e "${YELLOW}→ Creating necessary directories...${NC}"
mkdir -p uploads
mkdir -p processed_images
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}→ Creating .env file...${NC}"
    cat > .env << EOF
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1

# OpenAI API Key (required for AI features)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-api-key-here

# Database
DATABASE_PATH=housing_database.db

# Upload folders
UPLOAD_FOLDER=uploads
PROCESSED_FOLDER=processed_images
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}  ⚠ Remember to add your OpenAI API key to .env${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo ""

# Check if database exists
if [ ! -f "housing_database.db" ]; then
    echo -e "${YELLOW}→ Database not found. Creating database...${NC}"
    python generate_database.py
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${GREEN}✓ Database already exists${NC}"
fi
echo ""

# Run tests
echo -e "${YELLOW}→ Running tests to verify setup...${NC}"
python -m pytest test_app.py -v
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${RED}✗ Some tests failed${NC}"
fi
echo ""

# Success message
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✓ Development environment setup complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Activate the virtual environment:"
echo -e "     ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo -e "  2. Start the development server:"
echo -e "     ${YELLOW}make dev${NC}"
echo -e "     or"
echo -e "     ${YELLOW}python app.py${NC}"
echo ""
echo -e "  3. Access the application at:"
echo -e "     ${YELLOW}http://localhost:5000${NC}"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo -e "  ${YELLOW}make help${NC}         - Show all available commands"
echo -e "  ${YELLOW}make test${NC}         - Run tests"
echo -e "  ${YELLOW}make lint${NC}         - Check code quality"
echo -e "  ${YELLOW}make format${NC}       - Format code"
echo -e "  ${YELLOW}make clean${NC}        - Clean temporary files"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo -e "  ${YELLOW}DEVELOPMENT.md${NC}    - Development guide"
echo -e "  ${YELLOW}QUICK_START.md${NC}    - Quick start guide"
echo -e "  ${YELLOW}README.md${NC}         - Project overview"
echo ""
