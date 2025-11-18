# تحديث بيانات الفلل والوحدات السكنية من Excel
# Update Villas and Residential Units from Excel

## نظرة عامة / Overview

تم إنشاء هذا السكريبت لتحديث بيانات الفلل والوحدات السكنية في قاعدة البيانات من ملف Excel `الوحدات السكنية.xlsx`.

This script was created to update villas and residential units data in the database from the Excel file `الوحدات السكنية.xlsx`.

## الملفات / Files

- **`update_units_from_excel.py`**: السكريبت الرئيسي للتحديث / Main update script
- **`الوحدات السكنية.xlsx`**: ملف Excel المصدر الذي يحتوي على البيانات / Source Excel file containing the data
- **`housing_database.db`**: قاعدة البيانات / Database file
- **`housing_database.db.backup_*`**: نسخة احتياطية تلقائية / Automatic backup

## الاستخدام / Usage

### الوضع الاختباري (Dry Run)

لاختبار التحديث بدون حفظ التغييرات:

```bash
python3 update_units_from_excel.py --dry-run
```

أو:

```bash
python3 update_units_from_excel.py -n
```

### التحديث الفعلي

لتنفيذ التحديث وحفظ التغييرات:

```bash
python3 update_units_from_excel.py
```

## ما يفعله السكريبت / What the Script Does

### الخطوة 1: إنشاء نسخة احتياطية / Step 1: Create Backup

- يتم إنشاء نسخة احتياطية تلقائية من قاعدة البيانات قبل أي تعديل
- اسم الملف: `housing_database.db.backup_YYYYMMDD_HHMMSS`

An automatic backup of the database is created before any modifications.

### الخطوة 2: حذف البيانات القديمة / Step 2: Clear Old Data

- يتم حفظ ارتباطات السكان بالوحدات مؤقتاً
- يتم حذف جداول `units` و `buildings` القديمة

Resident associations are temporarily saved, then old `units` and `buildings` tables are cleared.

### الخطوة 3: إضافة الفلل / Step 3: Add Villas

- يتم إضافة 114 فيلا من ملف Excel
- كل فيلا تحتوي على وحدة واحدة

114 villas are added from the Excel file, each containing one unit.

### الخطوة 4: إضافة العمارات والشقق / Step 4: Add Apartment Buildings

- يتم إضافة 51 عمارة
- يتم إضافة الشقق في كل عمارة حسب البيانات في Excel
- أرقام الشقق تُستخدم كما هي في Excel (مثال: 1، 2، 3، 4، 11، 12، ...)

51 apartment buildings are added with their units using the exact apartment numbers from Excel.

### الخطوة 5: استعادة ارتباطات السكان / Step 5: Restore Resident Associations

- يتم محاولة ربط السكان بوحداتهم السابقة
- السكان الذين لم يتم العثور على وحداتهم يتم تعيينهم كـ "غير نشط"

Residents are re-associated with their units. Those whose units no longer exist are marked as inactive.

### الخطوة 6: تحديث الإحصائيات / Step 6: Update Statistics

- يتم تحديث عدد الوحدات المشغولة في كل مبنى

Occupied unit counts are updated for each building.

## البيانات / Data

### من ملف Excel / From Excel File

- **114 فيلا** (فلة 1 - 114)
- **51 عمارة** (العمارات القديمة: 1-30، الجديدة: 53-79)
- **1,019 شقة** موزعة على العمارات
- **إجمالي: 1,133 وحدة سكنية**

### في قاعدة البيانات بعد التحديث / In Database After Update

- إجمالي المباني: 165 (114 فيلا + 51 عمارة)
- إجمالي الوحدات: 1,133 (114 فيلا + 1,019 شقة)
- الوحدات المشغولة: تم الحفاظ عليها حيثما أمكن
- الوحدات الشاغرة: الباقي

## ملاحظات مهمة / Important Notes

### التغييرات في أرقام العمارات

**المباني التي تمت إزالتها:**
- عمارة 51، 52، 57، 58، 59، 60، 69، 70

**المباني المضافة:**
- عمارة 72، 73، 74، 75، 76، 77، 78، 79

### التغييرات في أرقام الشقق

أرقام الشقق الآن تتبع نظام الترقيم الموجود في Excel:
- الدور الأرضي: 1، 2، 3، 4
- الدور الأول: 11، 12، 13، 14
- الدور الثاني: 21، 22، 23، 24
- إلخ...

Apartment numbers now follow the Excel numbering system (floor-based).

### السكان المتأثرون

السكان الذين كانوا في الوحدات/المباني التي لم تعد موجودة:
- تم تعيينهم كـ "غير نشط"
- `unit_id` تم تعيينه إلى `NULL`
- يمكن إعادة تعيينهم يدوياً إلى وحدات جديدة

Residents from removed units/buildings are marked as inactive and can be manually reassigned.

## الاستعادة من النسخة الاحتياطية / Restore from Backup

في حالة الحاجة للعودة إلى النسخة القديمة:

```bash
# إيقاف التطبيق أولاً
# Stop the application first

# استعادة من النسخة الاحتياطية
# Restore from backup
cp housing_database.db.backup_YYYYMMDD_HHMMSS housing_database.db

# إعادة تشغيل التطبيق
# Restart the application
```

## الإحصائيات النهائية / Final Statistics

بعد التحديث:
- ✅ إجمالي الفلل: 114
- ✅ إجمالي العمارات: 51
- ✅ إجمالي وحدات الفلل: 114
- ✅ إجمالي الشقق: 1,019
- ✅ إجمالي الوحدات: 1,133
- ℹ️ الوحدات المشغولة: يعتمد على نجاح إعادة الربط
- ℹ️ الوحدات الشاغرة: الباقي

## المتطلبات / Requirements

```bash
pip install pandas openpyxl
```

## الأمان / Safety

- ✅ نسخة احتياطية تلقائية قبل التحديث
- ✅ وضع اختباري (dry run) متاح
- ✅ تعطيل مؤقت لقيود المفاتيح الأجنبية أثناء التحديث
- ✅ إعادة تفعيل قيود المفاتيح الأجنبية بعد التحديث
- ✅ معالجة الأخطاء والتراجع (rollback) في حالة الفشل

## الدعم / Support

للمزيد من المعلومات أو المساعدة، يرجى الرجوع إلى:
- مستودع المشروع على GitHub
- وثائق النظام

---

**تم التحديث:** 2025-11-18  
**الحالة:** ✅ جاهز للاستخدام
