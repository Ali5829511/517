# بطاقة المرجع السريع للنشر | Quick Deployment Reference Card

## 🚀 نشر سريع في 3 دقائق | Quick Deploy in 3 Minutes

### 🏆 Railway.app (الموصى به / Recommended)
```bash
# 1. اذهب إلى / Go to
https://railway.app

# 2. Login with GitHub

# 3. Deploy from GitHub repo
Ali5829511/517

# 4. Done! ✅
# الوقت: 2-3 دقائق / Time: 2-3 minutes
```

### ⚡ Render.com (للإنتاج / Production)
```bash
# 1. اذهب إلى / Go to
https://render.com

# 2. New + → Web Service

# 3. Connect GitHub: Ali5829511/517

# 4. Settings:
Build: pip install -r requirements.txt
Start: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120

# 5. Done! ✅
# الوقت: 5-10 دقائق / Time: 5-10 minutes
```

### 💻 Heroku (CLI)
```bash
# التثبيت / Install
brew install heroku/brew/heroku  # macOS
# or download from heroku.com

# النشر / Deploy
heroku login
heroku create housing-system
git push heroku main
heroku open

# الوقت: 5-7 دقائق / Time: 5-7 minutes
```

### ⚡ Vercel (CLI)
```bash
# التثبيت / Install
npm install -g vercel

# النشر / Deploy
vercel login
vercel --prod

# الوقت: 2-3 دقائق / Time: 2-3 minutes
# ⚠️ محدود لتطبيقات Flask / Limited for Flask apps
```

---

## 🐳 Docker

```bash
# بناء / Build
docker build -t housing-system .

# تشغيل / Run
docker run -p 8080:8080 -e OPENAI_API_KEY=sk-xxx housing-system

# Docker Compose (أنشئ docker-compose.yml)
docker-compose up
```

---

## 🔧 متغيرات البيئة | Environment Variables

### إلزامية / Required
```bash
SECRET_KEY=auto-generated
```

### اختيارية / Optional
```bash
OPENAI_API_KEY=sk-your-key-here  # للذكاء الاصطناعي / for AI
FLASK_ENV=production              # بيئة الإنتاج / production env
DATABASE_PATH=housing_database.db # مسار قاعدة البيانات / DB path
```

---

## 📊 جدول المقارنة السريع | Quick Comparison

| المنصة | مجاني | الوقت | السهولة | التقييم |
|--------|-------|-------|---------|---------|
| **Railway** | ✅ 500h | 2-3m | ⭐⭐⭐⭐⭐ | **5/5** 🏆 |
| **Render** | ✅ 750h | 5-10m | ⭐⭐⭐⭐ | **4.5/5** |
| **Heroku** | ❌ $5+ | 5-7m | ⭐⭐⭐⭐ | **4/5** |
| **Vercel** | ✅ محدود | 2-3m | ⭐⭐⭐ | **3.5/5** |

---

## 🔥 استكشاف أخطاء سريع | Quick Troubleshooting

### التطبيق لا يبدأ | App Won't Start
```bash
# تحقق من السجلات / Check logs
railway logs --tail  # Railway
heroku logs --tail   # Heroku

# تحقق من Procfile
cat Procfile
# يجب أن يكون: web: gunicorn app:app
```

### خطأ قاعدة البيانات | Database Error
```bash
# تحقق من وجودها / Check existence
ls -lh housing_database.db

# أنشئها / Create it
python generate_database.py
```

### خطأ OpenAI API
```bash
# تحقق من المفتاح / Check key
echo $OPENAI_API_KEY

# ملاحظة: النظام يعمل بدون OpenAI
# Note: System works without OpenAI
```

### الملفات الثابتة لا تعمل | Static Files Don't Work
```bash
# أنشئ المجلدات / Create directories
mkdir -p static uploads processed_images logs

# ارفعها في Git / Upload to Git
git add static/
git push
```

---

## 📚 الأدلة الكاملة | Full Guides

### الدليل الشامل | Comprehensive Guide
📖 **[CLOUD_DEPLOYMENT_GUIDE.md](CLOUD_DEPLOYMENT_GUIDE.md)**
- 8 منصات سحابية
- خطوات مفصلة
- استكشاف أخطاء شامل
- إرشادات أمان
- تحسينات أداء

### أدلة أخرى | Other Guides
- [DEPLOYMENT.md](DEPLOYMENT.md) - دليل النشر العام
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - نشر في 3 دقائق
- [QUICK_START.md](QUICK_START.md) - البدء السريع
- [README.md](README.md) - نظرة عامة

### سكريبتات | Scripts
```bash
# سكريبت تفاعلي / Interactive script
./quick_cloud_deploy.sh

# أمثلة CI/CD
.github/workflows/examples/
```

---

## 🆘 الدعم | Support

### للمساعدة | For Help
- 📧 housing@imamu.edu.sa
- 🌐 https://github.com/Ali5829511/517/issues

### الوثائق الرسمية | Official Docs
- [Railway](https://docs.railway.app/)
- [Render](https://render.com/docs)
- [Heroku](https://devcenter.heroku.com/)
- [Vercel](https://vercel.com/docs)

---

## ✅ قائمة التحقق | Checklist

قبل النشر / Before Deployment:
- [ ] جميع الملفات في Git
- [ ] requirements.txt محدث
- [ ] Procfile صحيح
- [ ] متغيرات البيئة مضبوطة
- [ ] اختبار محلي ناجح
- [ ] المفاتيح السرية آمنة

---

**نصيحة:** ابدأ بـ Railway.app للنشر السريع!  
**Tip:** Start with Railway.app for quick deployment!

---

© 2025 جامعة الإمام محمد بن سعود الإسلامية  
© 2025 Imam Muhammad bin Saud Islamic University
