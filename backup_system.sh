#!/bin/bash
# نسخ احتياطي شامل لنظام إدارة الإسكان
# Comprehensive Backup Script for Housing Management System

echo "=========================================="
echo "نسخ احتياطي للنظام - System Backup"
echo "=========================================="
echo ""

# تحديد اسم النسخة الاحتياطية مع التاريخ والوقت
BACKUP_NAME="housing_system_backup_$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$HOME/$BACKUP_NAME"

echo "📦 إنشاء مجلد النسخ الاحتياطي..."
echo "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# نسخ الملفات الأساسية
echo ""
echo "📄 نسخ الملفات الأساسية..."
echo "Copying core files..."

# نسخ ملفات Python
cp *.py "$BACKUP_DIR/" 2>/dev/null
echo "  ✓ Python files copied"

# نسخ قاعدة البيانات
cp *.db "$BACKUP_DIR/" 2>/dev/null
echo "  ✓ Database files copied"

# نسخ ملفات التكوين
cp requirements.txt "$BACKUP_DIR/" 2>/dev/null
cp Procfile "$BACKUP_DIR/" 2>/dev/null
cp runtime.txt "$BACKUP_DIR/" 2>/dev/null
cp render.yaml "$BACKUP_DIR/" 2>/dev/null
cp railway.json "$BACKUP_DIR/" 2>/dev/null
cp vercel.json "$BACKUP_DIR/" 2>/dev/null
cp config.py "$BACKUP_DIR/" 2>/dev/null
cp .env.example "$BACKUP_DIR/" 2>/dev/null
cp environment.yml "$BACKUP_DIR/" 2>/dev/null
echo "  ✓ Configuration files copied"

# نسخ ملفات Excel والبيانات
cp *.xlsx "$BACKUP_DIR/" 2>/dev/null
cp *.csv "$BACKUP_DIR/" 2>/dev/null
echo "  ✓ Data files (Excel, CSV) copied"

# نسخ سكريبتات التشغيل
cp *.sh "$BACKUP_DIR/" 2>/dev/null
cp *.bat "$BACKUP_DIR/" 2>/dev/null
echo "  ✓ Startup scripts copied"

# نسخ مجلد static
if [ -d "static" ]; then
    cp -r static "$BACKUP_DIR/"
    echo "  ✓ Static files copied"
fi

# نسخ مجلدات البيانات (إذا كانت موجودة وتحتوي على ملفات)
if [ -d "uploads" ] && [ "$(ls -A uploads 2>/dev/null)" ]; then
    cp -r uploads "$BACKUP_DIR/"
    echo "  ✓ Uploads folder copied"
fi

if [ -d "processed_images" ] && [ "$(ls -A processed_images 2>/dev/null)" ]; then
    cp -r processed_images "$BACKUP_DIR/"
    echo "  ✓ Processed images copied"
fi

# نسخ الوثائق المهمة
echo ""
echo "📚 نسخ الوثائق..."
echo "Copying documentation..."
cp README*.md "$BACKUP_DIR/" 2>/dev/null
cp QUICK_START.md "$BACKUP_DIR/" 2>/dev/null
cp DEPLOYMENT*.md "$BACKUP_DIR/" 2>/dev/null
cp SYSTEM_REVIEW_REPORT.md "$BACKUP_DIR/" 2>/dev/null
cp TASK_COMPLETION_SUMMARY_AR.md "$BACKUP_DIR/" 2>/dev/null
echo "  ✓ Documentation copied"

# إنشاء ملف معلومات النسخة الاحتياطية
echo ""
echo "📝 إنشاء ملف معلومات النسخة..."
echo "Creating backup info file..."

cat > "$BACKUP_DIR/BACKUP_INFO.txt" << EOF
نسخة احتياطية لنظام إدارة الإسكان الجامعي
Housing Management System Backup

التاريخ / Date: $(date)
الاسم / Name: $BACKUP_NAME
المسار / Path: $BACKUP_DIR

محتويات النسخة / Backup Contents:
- Python source files (*.py)
- Database files (*.db)
- Configuration files
- Data files (Excel, CSV)
- Static files (HTML, CSS, JS)
- Uploads and processed images
- Documentation files

لاستعادة النظام / To restore:
1. انسخ جميع الملفات إلى مجلد جديد
   Copy all files to a new directory
   
2. ثبت المتطلبات:
   Install requirements:
   pip install -r requirements.txt
   
3. شغل التطبيق:
   Run the application:
   python app.py
   
للمزيد من المعلومات، راجع:
For more information, see:
- README.md
- QUICK_START.md
- DEPLOYMENT.md
EOF

echo "  ✓ Backup info created"

# حساب حجم النسخة الاحتياطية
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

# إنشاء أرشيف مضغوط (اختياري)
echo ""
read -p "هل تريد ضغط النسخة الاحتياطية؟ (y/n) / Compress backup? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗜️  جاري الضغط..."
    echo "Compressing..."
    cd "$HOME"
    tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"
    ARCHIVE_SIZE=$(du -sh "${BACKUP_NAME}.tar.gz" | cut -f1)
    echo "  ✓ Archive created: ${BACKUP_NAME}.tar.gz ($ARCHIVE_SIZE)"
    
    read -p "حذف المجلد غير المضغوط؟ (y/n) / Delete uncompressed folder? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$BACKUP_DIR"
        echo "  ✓ Uncompressed folder deleted"
    fi
fi

echo ""
echo "=========================================="
echo "✅ اكتملت النسخة الاحتياطية بنجاح!"
echo "✅ Backup completed successfully!"
echo "=========================================="
echo ""
echo "📍 الموقع / Location: $BACKUP_DIR"
echo "📊 الحجم / Size: $BACKUP_SIZE"
echo ""
echo "استخدم هذا الأمر للاستعادة:"
echo "Use this command to restore:"
echo "  cp -r $BACKUP_DIR/* /path/to/restore/"
echo ""
