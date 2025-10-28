# دليل سير العمل - Workflow Guide

## نظام إدارة الإسكان الجامعي

هذا الدليل يشرح سير العمل الكامل للتطوير، الاختبار، والنشر.

---

## 📋 نظرة عامة - Overview

```
Developer → Development → Testing → Building → Deployment → Production
   ↓           ↓            ↓          ↓           ↓            ↓
 Clone      Make changes   Test    Build for   Deploy to    Monitor
   &                        &       production   server     & maintain
 Setup                    Verify
```

---

## 🚀 البدء السريع - Quick Start

### للمطورين الجدد:

```bash
# 1. استنساخ المستودع
git clone https://github.com/Ali5829511/517.git
cd 517

# 2. تشغيل إعداد التطوير
./setup_dev.sh

# 3. تفعيل البيئة الافتراضية
source venv/bin/activate

# 4. تشغيل التطبيق
make dev
```

### للمطورين الحاليين:

```bash
# تحديث المستودع
git pull origin main

# تحديث الحزم
make install

# تشغيل التطبيق
make dev
```

---

## 📂 سير العمل الكامل - Complete Workflow

### 1️⃣ الإعداد الأولي - Initial Setup

```bash
# استنساخ المستودع
git clone https://github.com/Ali5829511/517.git
cd 517

# تشغيل إعداد التطوير
./setup_dev.sh

# أو يدوياً:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### 2️⃣ التطوير - Development

#### بدء العمل على ميزة جديدة:

```bash
# إنشاء فرع جديد
git checkout -b feature/feature-name

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تشغيل التطبيق في وضع التطوير
make dev
# أو
FLASK_ENV=development FLASK_DEBUG=1 python app.py
```

#### أثناء التطوير:

```bash
# تشغيل الاختبارات باستمرار
make test-watch

# فحص جودة الكود
make lint

# تنسيق الكود
make format
```

### 3️⃣ الاختبار - Testing

```bash
# تشغيل جميع الاختبارات
make test

# تشغيل الاختبارات مع قياس التغطية
make test-cov

# تشغيل اختبارات محددة
pytest test_app.py::test_app_exists -v

# اختبار يدوي
python app.py
# ثم افتح المتصفح على http://localhost:5000
```

### 4️⃣ المراجعة - Review

```bash
# فحص شامل قبل الحفظ
make check  # يشغل lint + test

# مراجعة التغييرات
git diff

# عرض حالة الملفات
git status

# فحص الأمان
make security
```

### 5️⃣ الحفظ - Commit

```bash
# إضافة الملفات المعدلة
git add .

# أو إضافة ملفات محددة
git add app.py database_api.py

# حفظ التغييرات
git commit -m "وصف واضح للتغييرات"

# أو بالإنجليزية
git commit -m "Add new feature: description"
```

### 6️⃣ الرفع - Push

```bash
# رفع التغييرات
git push origin feature/feature-name

# إنشاء Pull Request على GitHub
# اذهب إلى: https://github.com/Ali5829511/517/pulls
```

### 7️⃣ البناء - Build

```bash
# تنظيف المشروع
make clean

# بناء للإنتاج
make build
# أو
./build.sh

# اختبار الإنتاج محلياً
make run-prod
```

### 8️⃣ النشر - Deployment

راجع `DEPLOYMENT_GUIDE.md` للتفاصيل الكاملة.

```bash
# على Railway.app:
# 1. ادفع إلى GitHub
# 2. اربط Railway بالمستودع
# 3. أضف OPENAI_API_KEY
# 4. سيتم النشر تلقائياً

# على Render.com:
# 1. ادفع إلى GitHub
# 2. أنشئ Web Service
# 3. اختر المستودع
# 4. أضف OPENAI_API_KEY
# 5. سيتم النشر تلقائياً
```

---

## 🔄 سيناريوهات شائعة - Common Scenarios

### إضافة ميزة جديدة:

```bash
git checkout main
git pull origin main
git checkout -b feature/new-feature
# قم بالتعديلات
make test
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
# أنشئ Pull Request
```

### إصلاح خطأ:

```bash
git checkout main
git pull origin main
git checkout -b fix/bug-description
# أصلح الخطأ
make test  # تأكد من نجاح الاختبارات
git add .
git commit -m "Fix: bug description"
git push origin fix/bug-description
# أنشئ Pull Request
```

### تحديث قاعدة البيانات:

```bash
# نسخة احتياطية
make db-backup

# تعديل generate_database.py
nano generate_database.py

# إعادة إنشاء قاعدة البيانات
make db-init

# التحقق
make db-inspect
```

### تحديث الحزم:

```bash
# عرض الحزم القديمة
make deps-update

# تحديث حزمة محددة
pip install --upgrade package-name

# تحديث requirements.txt
pip freeze > requirements.txt

# اختبار التغييرات
make test
```

---

## 🎯 أفضل الممارسات - Best Practices

### الكود:

1. **اتبع PEP 8**: استخدم `make format` و `make lint`
2. **اكتب اختبارات**: كل ميزة جديدة يجب أن يكون لها اختبار
3. **علّق الكود المعقد**: ولكن لا تبالغ في التعليقات
4. **استخدم أسماء واضحة**: للمتغيرات والدوال

### Git:

1. **Commits صغيرة**: كل commit يجب أن يكون تغييراً واحداً منطقياً
2. **رسائل واضحة**: اشرح ماذا ولماذا
3. **فروع منفصلة**: لكل ميزة أو إصلاح
4. **اسحب بانتظام**: `git pull` قبل البدء بالعمل

### الاختبار:

1. **اختبر قبل الحفظ**: `make test` قبل كل commit
2. **اختبر يدوياً**: لا تعتمد فقط على الاختبارات الآلية
3. **اختبر على أكثر من متصفح**: Chrome, Firefox, Safari
4. **اختبر على الجوال**: استخدم responsive mode

### الأمان:

1. **لا تحفظ مفاتيح API**: استخدم .env
2. **لا تعطل CSRF**: إلا للضرورة القصوى
3. **نظّف المدخلات**: validate و sanitize
4. **استخدم HTTPS**: في الإنتاج

---

## 🛠️ أدوات مفيدة - Useful Tools

### محررات الكود:
- **VS Code**: محرر قوي مع extensions
- **PyCharm**: IDE كامل لـ Python
- **Sublime Text**: سريع وخفيف

### الاختبار:
- **Postman**: لاختبار APIs
- **curl**: لاختبار سريع من الطرفية
- **httpie**: curl ولكن أسهل

### قاعدة البيانات:
- **DB Browser for SQLite**: GUI لفحص قاعدة البيانات
- **sqlite3**: أداة الطرفية

### Git:
- **GitHub Desktop**: GUI لـ Git
- **GitKraken**: أداة مرئية قوية
- **tig**: terminal interface لـ Git

---

## 🐛 حل المشاكل - Troubleshooting

### التطبيق لا يعمل:

```bash
# تحقق من Python
python3 --version  # يجب أن يكون 3.11+

# تحقق من الحزم
pip list

# أعد تثبيت الحزم
pip install -r requirements.txt --force-reinstall

# تحقق من قاعدة البيانات
make db-inspect
```

### الاختبارات تفشل:

```bash
# شغّل اختبار واحد للتفصيل
pytest test_app.py::test_name -v -s

# تحقق من logs
cat logs/app.log

# أعد إنشاء البيئة
deactivate
rm -rf venv
./setup_dev.sh
```

### مشاكل Git:

```bash
# إلغاء التغييرات المحلية
git checkout -- filename.py

# إلغاء آخر commit
git reset --soft HEAD~1

# تحديث من main
git fetch origin
git merge origin/main

# حل تعارضات
git mergetool
```

### مشاكل الأداء:

```bash
# تفعيل profiling
python -m cProfile app.py

# فحص الذاكرة
pip install memory_profiler
python -m memory_profiler app.py
```

---

## 📊 مؤشرات الجودة - Quality Metrics

### قبل كل Pull Request:

- ✅ جميع الاختبارات تنجح (`make test`)
- ✅ الكود يتبع معايير PEP 8 (`make lint`)
- ✅ التغطية > 80% (`make test-cov`)
- ✅ لا توجد ثغرات أمنية (`make security`)
- ✅ التطبيق يعمل محلياً (`make dev`)
- ✅ البناء ينجح (`make build`)

### مراجعة دورية:

- 📅 **أسبوعياً**: تحديث الحزم (`make deps-update`)
- 📅 **شهرياً**: نسخة احتياطية من قاعدة البيانات (`make db-backup`)
- 📅 **ربع سنوي**: مراجعة الأمان (`make security`)

---

## 📚 موارد إضافية - Additional Resources

### التوثيق:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python PEP 8](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)

### الدروس:
- [Real Python](https://realpython.com/)
- [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Git Branching](https://learngitbranching.js.org/)

### المجتمع:
- [Stack Overflow](https://stackoverflow.com/)
- [GitHub Discussions](https://github.com/Ali5829511/517/discussions)
- [Reddit r/flask](https://www.reddit.com/r/flask/)

---

## 📞 الدعم - Support

### للمساعدة:

1. **راجع التوثيق**: ابدأ بـ `DEVELOPMENT.md` و `README.md`
2. **ابحث في Issues**: قد تكون المشكلة محلولة
3. **افتح Issue جديد**: على GitHub
4. **اتصل بالفريق**: housing@imamu.edu.sa

### عند فتح Issue:

- وصف واضح للمشكلة
- خطوات إعادة إنتاج المشكلة
- لقطات شاشة إن أمكن
- نسخة Python والحزم المستخدمة
- رسائل الخطأ كاملة

---

**جامعة الإمام محمد بن سعود الإسلامية**  
**نظام إدارة الإسكان الجامعي**  
**Workflow Guide v1.0**
