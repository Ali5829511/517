#!/bin/bash
# Quick Deploy Script for Cloud Platforms
# سكريبت النشر السريع للمنصات السحابية

set -e

echo "🚀 دليل النشر السريع | Quick Deploy Guide"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Display menu
echo "اختر منصة النشر / Choose deployment platform:"
echo ""
echo "  1️⃣  Railway.app (الموصى به - Recommended)"
echo "  2️⃣  Render.com (للإنتاج - Production)"
echo "  3️⃣  Heroku (الكلاسيكي - Classic)"
echo "  4️⃣  Vercel (Serverless)"
echo "  5️⃣  Google Cloud Run (Containers)"
echo "  6️⃣  AWS Elastic Beanstalk"
echo "  7️⃣  Azure App Service"
echo "  8️⃣  DigitalOcean App Platform"
echo "  9️⃣  عرض الدليل الشامل / Show Full Guide"
echo "  0️⃣  إلغاء / Cancel"
echo ""
read -p "اختيارك / Your choice (0-9): " choice

case $choice in
    1)
        print_info "Railway.app - الأسرع والأسهل!"
        echo ""
        echo "الخطوات / Steps:"
        echo "1. اذهب إلى: https://railway.app"
        echo "2. سجل دخول بـ GitHub / Login with GitHub"
        echo "3. انقر 'Deploy from GitHub repo'"
        echo "4. اختر: Ali5829511/517"
        echo "5. انتظر النشر التلقائي / Wait for auto-deploy"
        echo ""
        print_success "الوقت المتوقع: 2-3 دقائق / Expected time: 2-3 minutes"
        echo ""
        print_info "📖 للمزيد من التفاصيل، راجع: CLOUD_DEPLOYMENT_GUIDE.md"
        ;;
    
    2)
        print_info "Render.com - موثوقية عالية!"
        echo ""
        echo "الخطوات / Steps:"
        echo "1. اذهب إلى: https://render.com"
        echo "2. سجل دخول بـ GitHub / Login with GitHub"
        echo "3. New + → Web Service"
        echo "4. اختر: Ali5829511/517"
        echo "5. Build Command: pip install -r requirements.txt"
        echo "6. Start Command: gunicorn app:app --bind 0.0.0.0:\$PORT --workers 4 --timeout 120"
        echo ""
        print_success "الوقت المتوقع: 5-10 دقائق / Expected time: 5-10 minutes"
        echo ""
        print_info "📖 للمزيد من التفاصيل، راجع: CLOUD_DEPLOYMENT_GUIDE.md"
        ;;
    
    3)
        print_info "Heroku - المنصة الكلاسيكية"
        echo ""
        if ! command -v heroku &> /dev/null; then
            print_warning "Heroku CLI غير مثبت / not installed"
            echo "تثبيت / Install: https://devcenter.heroku.com/articles/heroku-cli"
        else
            print_success "Heroku CLI مثبت / installed"
            echo ""
            echo "تشغيل الأوامر / Running commands:"
            echo ""
            
            read -p "اسم التطبيق / App name: " app_name
            
            if [ -z "$app_name" ]; then
                print_error "اسم التطبيق مطلوب / App name required"
                exit 1
            fi
            
            print_info "تسجيل الدخول / Logging in..."
            heroku login
            
            print_info "إنشاء التطبيق / Creating app..."
            heroku create "$app_name"
            
            print_info "النشر / Deploying..."
            git push heroku main
            
            print_success "تم النشر! / Deployed!"
            heroku open
        fi
        ;;
    
    4)
        print_info "Vercel - Serverless"
        echo ""
        if ! command -v vercel &> /dev/null; then
            print_warning "Vercel CLI غير مثبت / not installed"
            echo "تثبيت / Install: npm install -g vercel"
        else
            print_success "Vercel CLI مثبت / installed"
            echo ""
            print_info "تسجيل الدخول / Logging in..."
            vercel login
            
            print_info "النشر / Deploying..."
            vercel --prod
            
            print_success "تم النشر! / Deployed!"
        fi
        echo ""
        print_warning "ملاحظة: Vercel محدود لتطبيقات Flask"
        print_warning "Note: Vercel has limitations for Flask apps"
        print_info "يُفضل استخدام Railway أو Render / Prefer Railway or Render"
        ;;
    
    5)
        print_info "Google Cloud Run - حاويات Docker"
        echo ""
        if ! command -v gcloud &> /dev/null; then
            print_warning "Google Cloud SDK غير مثبت / not installed"
            echo "تثبيت / Install: https://cloud.google.com/sdk/docs/install"
        else
            print_success "Google Cloud SDK مثبت / installed"
            echo ""
            print_info "📖 راجع الدليل الشامل للخطوات التفصيلية"
            print_info "📖 See comprehensive guide for detailed steps"
        fi
        ;;
    
    6)
        print_info "AWS Elastic Beanstalk"
        echo ""
        if ! command -v eb &> /dev/null; then
            print_warning "EB CLI غير مثبت / not installed"
            echo "تثبيت / Install: pip install awsebcli"
        else
            print_success "EB CLI مثبت / installed"
            echo ""
            print_info "📖 راجع الدليل الشامل للخطوات التفصيلية"
            print_info "📖 See comprehensive guide for detailed steps"
        fi
        ;;
    
    7)
        print_info "Azure App Service"
        echo ""
        if ! command -v az &> /dev/null; then
            print_warning "Azure CLI غير مثبت / not installed"
            echo "تثبيت / Install: https://docs.microsoft.com/cli/azure/install-azure-cli"
        else
            print_success "Azure CLI مثبت / installed"
            echo ""
            print_info "📖 راجع الدليل الشامل للخطوات التفصيلية"
            print_info "📖 See comprehensive guide for detailed steps"
        fi
        ;;
    
    8)
        print_info "DigitalOcean App Platform"
        echo ""
        echo "الخطوات / Steps:"
        echo "1. اذهب إلى: https://cloud.digitalocean.com"
        echo "2. Apps → Create App"
        echo "3. اختر GitHub → Ali5829511/517"
        echo "4. اتبع المعالج / Follow wizard"
        echo ""
        print_success "الوقت المتوقع: 8-10 دقائق / Expected time: 8-10 minutes"
        ;;
    
    9)
        print_info "فتح الدليل الشامل / Opening comprehensive guide..."
        echo ""
        if command -v xdg-open &> /dev/null; then
            xdg-open CLOUD_DEPLOYMENT_GUIDE.md
        elif command -v open &> /dev/null; then
            open CLOUD_DEPLOYMENT_GUIDE.md
        else
            print_info "يرجى فتح: CLOUD_DEPLOYMENT_GUIDE.md"
            print_info "Please open: CLOUD_DEPLOYMENT_GUIDE.md"
        fi
        ;;
    
    0)
        print_info "إلغاء / Cancelled"
        exit 0
        ;;
    
    *)
        print_error "خيار غير صحيح / Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
print_info "💡 نصيحة: للحصول على دليل شامل مفصل، راجع:"
print_info "💡 Tip: For comprehensive detailed guide, see:"
echo "   📖 CLOUD_DEPLOYMENT_GUIDE.md"
echo ""
print_info "🆘 للدعم / For support:"
echo "   📧 housing@imamu.edu.sa"
echo "   🌐 https://github.com/Ali5829511/517/issues"
echo ""
print_success "شكراً لاستخدام نظام إدارة الإسكان الجامعي!"
print_success "Thank you for using the University Housing Management System!"
