# 🚀 دليل البدء السريع - النسخ الاحتياطي والتشغيل المحلي
# Quick Start Guide - Backup and Local Run

**⏱️ الوقت: 5 دقائق / Time: 5 minutes**

---

## 📦 النسخ الاحتياطي - Backup (دقيقة واحدة)

### على Linux/Mac:
```bash
chmod +x backup_system.sh
./backup_system.sh
```

### على Windows:
```batch
backup_system.bat
```

**✅ النتيجة:**
- نسخة كاملة من النظام في: `~/housing_system_backup_YYYYMMDD_HHMMSS/`
- يمكنك ضغطها إلى ملف `.tar.gz` أو `.zip`

---

## 🚀 التشغيل المحلي - Local Run (3 دقائق)

### على Linux/Mac:
```bash
chmod +x run_local.sh
./run_local.sh
```

### على Windows:
```batch
run_local.bat
```

**✅ النتيجة:**
- التطبيق يعمل على: http://localhost:5000
- جاهز للاستخدام فوراً!

---

## 📋 المتطلبات - Requirements

### قبل البدء:
1. ✅ Python 3.11+ مثبت
2. ✅ pip مثبت
3. ✅ 10 MB مساحة فارغة

### تثبيت Python (إذا لم يكن مثبتاً):
- **Windows/Mac:** https://www.python.org/downloads/
- **Ubuntu/Debian:** `sudo apt install python3 python3-pip`
- **CentOS/RHEL:** `sudo yum install python3 python3-pip`

---

## 🎯 أوامر سريعة - Quick Commands

### نسخ احتياطي سريع:
```bash
# Linux/Mac
./backup_system.sh

# Windows
backup_system.bat
```

### تشغيل فوري:
```bash
# Linux/Mac
./run_local.sh

# Windows
run_local.bat
```

### تشغيل يدوي (إذا فشلت السكريبتات):
```bash
pip install -r requirements.txt
python app.py
```

---

## ❓ استكشاف الأخطاء السريع - Quick Troubleshooting

### المشكلة: Python غير موجود
**الحل:** ثبت Python من https://www.python.org/downloads/

### المشكلة: Permission denied على Linux/Mac
**الحل:** `chmod +x backup_system.sh run_local.sh`

### المشكلة: المنفذ 5000 مستخدم
**الحل:** غير المنفذ عند التشغيل أو أوقف العملية المستخدمة له

### المشكلة: قاعدة البيانات مفقودة
**الحل:** السكريبت سيسأل عن إنشاء قاعدة بيانات جديدة تلقائياً

---

## 📖 للمزيد من المعلومات - For More Information

- 📄 **LOCAL_SETUP_GUIDE.md** - دليل شامل
- 📄 **README.md** - نظرة عامة على المشروع
- 📄 **QUICK_START.md** - دليل البدء

---

## ✅ تم! - Done!

بعد تشغيل السكريبتات:
1. ✅ النظام يعمل على: http://localhost:5000
2. ✅ النسخة الاحتياطية موجودة في: `~/{backup_folder}`
3. ✅ جاهز للاستخدام!

**استمتع! - Enjoy!** 🎉
