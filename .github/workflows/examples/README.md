# CI/CD Examples for Cloud Deployment
# أمثلة CI/CD للنشر السحابي

This directory contains example CI/CD workflow files for automated deployment to various cloud platforms.

هذا المجلد يحتوي على ملفات أمثلة لسير عمل CI/CD للنشر التلقائي إلى منصات سحابية مختلفة.

## 📄 الملفات | Files

### cloud-deploy-example.yml
مثال شامل لنشر تلقائي على 6 منصات:
- Railway.app
- Render.com
- Heroku
- Google Cloud Run
- Azure App Service
- AWS Elastic Beanstalk

Comprehensive example for automated deployment to 6 platforms.

## 🚀 كيفية الاستخدام | How to Use

### 1. اختيار المنصة | Choose Platform

اختر المنصة التي تريد استخدامها من الملف المثال واحذف الباقي.

Choose the platform you want to use from the example file and remove the rest.

### 2. نسخ الملف | Copy File

```bash
# انسخ الملف إلى مجلد workflows
# Copy file to workflows directory
cp .github/workflows/examples/cloud-deploy-example.yml .github/workflows/deploy.yml
```

### 3. إضافة الأسرار | Add Secrets

أضف الأسرار المطلوبة في GitHub Settings → Secrets and variables → Actions:

Add required secrets in GitHub Settings → Secrets and variables → Actions:

#### Railway
- `RAILWAY_TOKEN` - من Railway dashboard

#### Render
- `RENDER_SERVICE_ID` - معرف الخدمة
- `RENDER_API_KEY` - مفتاح API

#### Heroku
- `HEROKU_API_KEY` - مفتاح API
- `HEROKU_APP_NAME` - اسم التطبيق
- `HEROKU_EMAIL` - البريد الإلكتروني

#### Google Cloud
- `GCP_SA_KEY` - مفتاح حساب الخدمة (JSON)
- `GCP_PROJECT_ID` - معرف المشروع

#### Azure
- `AZURE_CREDENTIALS` - بيانات اعتماد Azure (JSON)

#### AWS
- `AWS_ACCESS_KEY_ID` - مفتاح الوصول
- `AWS_SECRET_ACCESS_KEY` - المفتاح السري

### 4. تفعيل Workflow

```bash
# عدّل الملف حسب احتياجاتك
# Edit the file according to your needs
nano .github/workflows/deploy.yml

# ادفع التغييرات
# Push changes
git add .github/workflows/deploy.yml
git commit -m "Add deployment workflow"
git push
```

## ⚙️ تخصيص Workflow | Customize Workflow

### تغيير الفرع | Change Branch

```yaml
on:
  push:
    branches:
      - main  # غيّر إلى الفرع المطلوب
```

### إضافة متغيرات بيئة | Add Environment Variables

```yaml
env:
  FLASK_ENV: production
  DATABASE_PATH: housing_database.db
```

### تخصيص خطوات الاختبار | Customize Test Steps

```yaml
- name: Run tests
  run: |
    pytest test_app.py -v --cov
    flake8 . --count --statistics
```

## 📚 موارد إضافية | Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [CLOUD_DEPLOYMENT_GUIDE.md](../../CLOUD_DEPLOYMENT_GUIDE.md) - دليل النشر الشامل
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Heroku Docs](https://devcenter.heroku.com/)

## 💡 نصائح | Tips

1. ✅ اختبر الـ workflow محلياً أولاً باستخدام [act](https://github.com/nektos/act)
2. ✅ استخدم environments للحماية الإضافية
3. ✅ فعّل فقط المنصة التي تستخدمها لتوفير الوقت
4. ✅ راقب استخدام دقائق GitHub Actions

## 🆘 الدعم | Support

للمساعدة:
- 📧 housing@imamu.edu.sa
- 🌐 [GitHub Issues](https://github.com/Ali5829511/517/issues)

---

© 2025 جامعة الإمام محمد بن سعود الإسلامية  
© 2025 Imam Muhammad bin Saud Islamic University
