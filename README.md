# نظام إدارة الإسكان الجامعي

![Build Status](https://github.com/Ali5829511/517/workflows/Python%20Package%20using%20Conda/badge.svg)
![Deployment](https://github.com/Ali5829511/517/workflows/Deployment%20Automation/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

نظام متكامل لإدارة إسكان أعضاء هيئة التدريس مع ميزات الذكاء الاصطناعي

## 🚀 التشغيل السريع

### المتطلبات
- Python 3.11+
- مفتاح OpenAI API

### التثبيت
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-your-key-here"
python app.py
```

## 📊 قاعدة البيانات
- 165 مبنى
- 1,134 وحدة سكنية
- 1,057 ساكن
- 2,381 ملصق سيارة
- 1,308 موقف

## 🆕 آخر التحديثات (1 نوفمبر 2025)
- ✅ إصلاح مشكلة عدم انعكاس التحديثات على الاستضافة
- ✅ إضافة GitHub Actions للنشر التلقائي
- ✅ إضافة نقطة نهاية `/api/version` للتحقق من الإصدار
- ✅ تحسين عملية النشر مع Railway/Render/Vercel
- ✅ إضافة سكريبت التحقق من النشر
- راجع `DEPLOYMENT_WORKFLOW.md` للتفاصيل الكاملة

## 🌐 النشر
النظام جاهز للنشر على منصات متعددة:

### المنصات الموصى بها:
- **Railway.app** (موصى به) - نشر تلقائي ⚡
- **Render.com** - خطة مجانية 🆓
- **Fly.io** - أداء عالي 🚀
- **Deta Space** - مجاني 100% للتعليم 🎓

### المنصات الإضافية:
- **Vercel** - نشر سريع
- **Heroku** - الأكثر شهرة
- **Azure App Service** - للمشاريع الحكومية
- **Google Cloud Run** - للمشاريع الكبيرة
- و**10+ منصات أخرى**

📖 **أدلة النشر:**
- [DEPLOYMENT.md](DEPLOYMENT.md) - دليل شامل للمنصات الرئيسية (10 منصات)
- [ALTERNATIVE_HOSTING_PLATFORMS.md](ALTERNATIVE_HOSTING_PLATFORMS.md) - **جديد!** 10 منصات إضافية
- [HOSTING_COMPARISON.md](HOSTING_COMPARISON.md) - مقارنة تفصيلية لجميع المنصات

### خطوات سريعة للنشر على Railway:
1. سجل على https://railway.app
2. اربط GitHub repo
3. أضف OPENAI_API_KEY (اختياري)
4. سيتم النشر تلقائياً ✅

تم التطوير بواسطة Manus AI
