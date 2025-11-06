# Makefile for Housing Management System
# نظام إدارة الإسكان الجامعي

.PHONY: help install install-dev dev test test-cov lint format clean build run docs

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## عرض هذه المساعدة / Show this help
	@echo "$(BLUE)نظام إدارة الإسكان الجامعي - Housing Management System$(NC)"
	@echo "$(BLUE)===============================================$(NC)"
	@echo ""
	@echo "$(GREEN)الأوامر المتاحة / Available commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## تثبيت الحزم المطلوبة / Install required packages
	@echo "$(BLUE)Installing required packages...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Installation complete!$(NC)"

install-dev: install ## تثبيت حزم التطوير / Install development packages
	@echo "$(BLUE)Installing development packages...$(NC)"
	pip install pytest pytest-cov black flake8 pylint mypy bandit safety
	@echo "$(GREEN)✓ Development packages installed!$(NC)"

dev: ## تشغيل التطبيق في وضع التطوير / Run app in development mode
	@echo "$(BLUE)Starting development server...$(NC)"
	@echo "$(YELLOW)Access the app at: http://localhost:5000$(NC)"
	FLASK_ENV=development FLASK_DEBUG=1 python app.py

run: ## تشغيل التطبيق / Run the application
	@echo "$(BLUE)Starting application...$(NC)"
	python app.py

run-prod: ## تشغيل التطبيق في وضع الإنتاج / Run in production mode
	@echo "$(BLUE)Starting production server with Gunicorn...$(NC)"
	gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --timeout 120

test: ## تشغيل الاختبارات / Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	python -m pytest test_app.py -v
	@echo "$(GREEN)✓ Tests complete!$(NC)"

test-cov: ## تشغيل الاختبارات مع قياس التغطية / Run tests with coverage
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	python -m pytest --cov=. --cov-report=html --cov-report=term test_app.py -v
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

test-watch: ## تشغيل الاختبارات بشكل مستمر / Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	python -m pytest -f test_app.py

lint: ## فحص جودة الكود / Check code quality
	@echo "$(BLUE)Running code quality checks...$(NC)"
	@echo "$(YELLOW)→ Flake8...$(NC)"
	-flake8 app.py database_api.py generate_database.py generate_reports.py --max-line-length=100 --ignore=E501,W503
	@echo "$(GREEN)✓ Lint complete!$(NC)"

format: ## تنسيق الكود تلقائياً / Format code automatically
	@echo "$(BLUE)Formatting code with Black...$(NC)"
	black app.py database_api.py generate_database.py generate_reports.py test_app.py --line-length=100
	@echo "$(GREEN)✓ Code formatted!$(NC)"

type-check: ## فحص الأنواع / Type checking
	@echo "$(BLUE)Running type checks with mypy...$(NC)"
	-mypy app.py database_api.py --ignore-missing-imports
	@echo "$(GREEN)✓ Type check complete!$(NC)"

security: ## فحص الثغرات الأمنية / Security vulnerability check
	@echo "$(BLUE)Running security checks...$(NC)"
	@echo "$(YELLOW)→ Safety (dependencies)...$(NC)"
	-safety check
	@echo "$(YELLOW)→ Bandit (code)...$(NC)"
	-bandit -r . -ll -x ./venv,./env
	@echo "$(GREEN)✓ Security check complete!$(NC)"

db-init: ## إنشاء قاعدة البيانات / Initialize database
	@echo "$(BLUE)Creating database...$(NC)"
	python generate_database.py
	@echo "$(GREEN)✓ Database created successfully!$(NC)"

db-backup: ## نسخة احتياطية من قاعدة البيانات / Backup database
	@echo "$(BLUE)Creating database backup...$(NC)"
	cp housing_database.db housing_database.backup_$(shell date +%Y%m%d_%H%M%S).db
	@echo "$(GREEN)✓ Backup created!$(NC)"

db-inspect: ## فحص قاعدة البيانات / Inspect database
	@echo "$(BLUE)Database information:$(NC)"
	@sqlite3 housing_database.db "SELECT 'Residents: ' || COUNT(*) FROM residents; SELECT 'Buildings: ' || COUNT(*) FROM buildings; SELECT 'Units: ' || COUNT(*) FROM units; SELECT 'Stickers: ' || COUNT(*) FROM vehicle_stickers; SELECT 'Parking Spots: ' || COUNT(*) FROM parking_spots;"

clean: ## تنظيف الملفات المؤقتة / Clean temporary files
	@echo "$(BLUE)Cleaning temporary files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-all: clean ## تنظيف شامل (مع البيئة الافتراضية) / Deep clean (including venv)
	@echo "$(BLUE)Deep cleaning...$(NC)"
	rm -rf venv/ env/ .venv/ 2>/dev/null || true
	rm -rf uploads/*.jpg uploads/*.jpeg uploads/*.png 2>/dev/null || true
	rm -rf processed_images/*.jpg processed_images/*.jpeg processed_images/*.png 2>/dev/null || true
	@echo "$(GREEN)✓ Deep cleanup complete!$(NC)"

build: clean ## بناء التطبيق للإنتاج / Build for production
	@echo "$(BLUE)Building application for production...$(NC)"
	@echo "$(YELLOW)→ Running tests...$(NC)"
	make test
	@echo "$(YELLOW)→ Checking code quality...$(NC)"
	make lint
	@echo "$(GREEN)✓ Build successful! Ready for deployment.$(NC)"

deps-update: ## تحديث الحزم / Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	pip list --outdated
	@echo "$(YELLOW)Run 'pip install --upgrade <package>' to update specific packages$(NC)"

deps-check: ## فحص الحزم الزائدة / Check for unused dependencies
	@echo "$(BLUE)Checking for unused dependencies...$(NC)"
	pip install pip-autoremove
	pip-autoremove -l

venv: ## إنشاء بيئة افتراضية / Create virtual environment
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	python3 -m venv venv
	@echo "$(GREEN)✓ Virtual environment created!$(NC)"
	@echo "$(YELLOW)Activate it with: source venv/bin/activate$(NC)"

setup: venv install-dev ## إعداد كامل للتطوير / Complete development setup
	@echo "$(BLUE)Setting up development environment...$(NC)"
	@echo "$(GREEN)✓ Development environment ready!$(NC)"
	@echo "$(YELLOW)Activate venv with: source venv/bin/activate$(NC)"
	@echo "$(YELLOW)Then run: make dev$(NC)"

docs: ## إنشاء التوثيق / Generate documentation
	@echo "$(BLUE)Documentation files:$(NC)"
	@echo "  $(YELLOW)README.md$(NC) - Overview"
	@echo "  $(YELLOW)DEVELOPMENT.md$(NC) - Development guide"
	@echo "  $(YELLOW)DEPLOYMENT_GUIDE.md$(NC) - Deployment instructions"
	@echo "  $(YELLOW)QUICK_START.md$(NC) - Quick start guide"
	@echo "  $(YELLOW)PROJECT_STATUS.md$(NC) - Project status"

status: ## عرض حالة المشروع / Show project status
	@echo "$(BLUE)Project Status$(NC)"
	@echo "$(BLUE)==============$(NC)"
	@echo ""
	@echo "$(YELLOW)Files:$(NC)"
	@find . -type f -name "*.py" | wc -l | xargs echo "  Python files:"
	@find . -type f -name "*.html" | wc -l | xargs echo "  HTML files:"
	@find . -type f -name "*.md" | wc -l | xargs echo "  Documentation files:"
	@echo ""
	@echo "$(YELLOW)Lines of Code:$(NC)"
	@find . -type f -name "*.py" -exec wc -l {} + | tail -1 | awk '{print "  Python: " $$1}'
	@echo ""
	@if [ -f "housing_database.db" ]; then \
		echo "$(YELLOW)Database:$(NC)"; \
		ls -lh housing_database.db | awk '{print "  Size: " $$5}'; \
	fi

check: lint test ## فحص شامل (lint + test) / Full check (lint + test)
	@echo "$(GREEN)✓ All checks passed!$(NC)"

serve: dev ## اختصار لـ dev / Alias for dev

watch: test-watch ## اختصار لـ test-watch / Alias for test-watch

info: ## معلومات عن البيئة / Environment information
	@echo "$(BLUE)Environment Information$(NC)"
	@echo "$(BLUE)======================$(NC)"
	@echo "$(YELLOW)Python:$(NC)"
	@python --version
	@echo "$(YELLOW)Pip:$(NC)"
	@pip --version
	@echo "$(YELLOW)Virtual Environment:$(NC)"
	@if [ -n "$$VIRTUAL_ENV" ]; then echo "  Active: $$VIRTUAL_ENV"; else echo "  Not active"; fi
	@echo "$(YELLOW)Working Directory:$(NC)"
	@pwd
