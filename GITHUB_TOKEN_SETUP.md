# GitHub Personal Access Token Setup
# إعداد رمز الوصول الشخصي لـ GitHub

## Overview | نظرة عامة

This document explains how to set up and use a GitHub Personal Access Token (PAT) with the Housing Management System.

هذا المستند يشرح كيفية إعداد واستخدام رمز الوصول الشخصي لـ GitHub (PAT) مع نظام إدارة الإسكان.

## What is a GitHub Personal Access Token? | ما هو رمز الوصول الشخصي؟

A GitHub Personal Access Token is a secure way to authenticate with GitHub's API without using your password. It allows applications to:
- Access repository information
- Create and manage issues
- Perform automated operations
- Integrate with GitHub services

رمز الوصول الشخصي لـ GitHub هو طريقة آمنة للمصادقة مع GitHub API بدون استخدام كلمة المرور. يسمح للتطبيقات بـ:
- الوصول إلى معلومات المستودع
- إنشاء وإدارة المشكلات
- تنفيذ العمليات التلقائية
- التكامل مع خدمات GitHub

## When Do You Need It? | متى تحتاج إليه؟

The GitHub token is **optional** for this application. You only need it if you plan to:
- Integrate GitHub repository features
- Automate GitHub operations
- Access private repository data

الرمز **اختياري** لهذا التطبيق. تحتاجه فقط إذا كنت تخطط لـ:
- دمج ميزات مستودع GitHub
- أتمتة عمليات GitHub
- الوصول إلى بيانات المستودع الخاص

## How to Create a GitHub Token | كيفية إنشاء رمز GitHub

### Step 1: Access Token Settings | الخطوة 1: الوصول إلى إعدادات الرمز

1. Go to GitHub.com and log in | انتقل إلى GitHub.com وسجل الدخول
2. Click your profile photo → **Settings** | انقر على صورة ملفك الشخصي → **الإعدادات**
3. In the left sidebar, click **Developer settings** | في الشريط الجانبي الأيسر، انقر على **إعدادات المطور**
4. Click **Personal access tokens** → **Tokens (classic)** | انقر على **رموز الوصول الشخصية** → **الرموز (الكلاسيكية)**

### Step 2: Generate New Token | الخطوة 2: إنشاء رمز جديد

1. Click **Generate new token** → **Generate new token (classic)** | انقر على **إنشاء رمز جديد** → **إنشاء رمز جديد (كلاسيكي)**
2. Give your token a descriptive name (e.g., "Housing System Integration") | أعط الرمز اسمًا وصفيًا (مثل "تكامل نظام الإسكان")
3. Select the required scopes: | حدد النطاقات المطلوبة:
   - `repo` - Full control of private repositories (if needed) | التحكم الكامل في المستودعات الخاصة (إذا لزم الأمر)
   - `read:user` - Read user profile data (optional) | قراءة بيانات ملف المستخدم (اختياري)
4. Set an expiration date (recommended: 90 days) | حدد تاريخ انتهاء الصلاحية (موصى به: 90 يومًا)
5. Click **Generate token** | انقر على **إنشاء الرمز**

### Step 3: Save Your Token | الخطوة 3: احفظ رمزك

⚠️ **IMPORTANT**: Copy the token immediately! You won't be able to see it again.

⚠️ **مهم**: انسخ الرمز فورًا! لن تتمكن من رؤيته مرة أخرى.

The token will look like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

سيبدو الرمز مثل: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## How to Configure the Token | كيفية تكوين الرمز

### For Development (Local) | للتطوير (محلي)

Create a `.env` file in the project root:

أنشئ ملف `.env` في جذر المشروع:

```bash
# Copy from .env.example
cp .env.example .env

# Edit .env and add your token
GITHUB_TOKEN=ghp_your_actual_token_here
```

### For Production (Railway, Render, etc.) | للإنتاج (Railway، Render، إلخ)

Add the token as an environment variable in your deployment platform:

أضف الرمز كمتغير بيئة في منصة النشر الخاصة بك:

**Railway:**
1. Go to your project settings | انتقل إلى إعدادات مشروعك
2. Click **Variables** | انقر على **المتغيرات**
3. Add: `GITHUB_TOKEN` = `your_token` | أضف: `GITHUB_TOKEN` = `الرمز_الخاص_بك`

**Render:**
1. Go to your service dashboard | انتقل إلى لوحة معلومات الخدمة
2. Click **Environment** | انقر على **البيئة**
3. Add: `GITHUB_TOKEN` = `your_token` | أضف: `GITHUB_TOKEN` = `الرمز_الخاص_بك`

## Security Best Practices | أفضل ممارسات الأمان

### ✅ DO | افعل:

- Store tokens in environment variables only | احفظ الرموز في متغيرات البيئة فقط
- Use `.env` file for local development | استخدم ملف `.env` للتطوير المحلي
- Add `.env` to `.gitignore` (already done) | أضف `.env` إلى `.gitignore` (تم بالفعل)
- Set token expiration dates | حدد تواريخ انتهاء صلاحية الرمز
- Rotate tokens regularly (every 90 days) | قم بتدوير الرموز بانتظام (كل 90 يومًا)
- Use minimum required scopes | استخدم الحد الأدنى من النطاقات المطلوبة

### ❌ DON'T | لا تفعل:

- Never commit tokens to Git | لا تلتزم أبدًا بالرموز في Git
- Never share tokens publicly | لا تشارك الرموز علنًا
- Never use tokens in URLs | لا تستخدم الرموز في عناوين URL
- Never hardcode tokens in source code | لا تقم بترميز الرموز في كود المصدر
- Never use tokens with excessive permissions | لا تستخدم رموزًا بأذونات مفرطة

## Troubleshooting | استكشاف الأخطاء

### Token Not Working | الرمز لا يعمل

1. Verify the token is correctly set in environment variables | تحقق من تعيين الرمز بشكل صحيح في متغيرات البيئة
2. Check token hasn't expired | تحقق من عدم انتهاء صلاحية الرمز
3. Verify required scopes are enabled | تحقق من تمكين النطاقات المطلوبة
4. Check for typos in the token | تحقق من وجود أخطاء في الرمز

### Token Compromised | الرمز مخترق

If you suspect your token has been compromised:

إذا كنت تشك في اختراق الرمز الخاص بك:

1. Go to GitHub Settings → Developer settings → Personal access tokens | انتقل إلى إعدادات GitHub → إعدادات المطور → رموز الوصول الشخصية
2. Find the compromised token | ابحث عن الرمز المخترق
3. Click **Delete** to revoke it immediately | انقر على **حذف** لإلغائه على الفور
4. Generate a new token | أنشئ رمزًا جديدًا
5. Update your environment variables | حدّث متغيرات البيئة الخاصة بك

## Checking Token Status | التحقق من حالة الرمز

You can verify if your token is configured correctly:

يمكنك التحقق من تكوين الرمز بشكل صحيح:

```python
from config import get_config

config = get_config()
print(f"GitHub Token Available: {config.GITHUB_AVAILABLE}")
```

Or check in the application logs:

أو تحقق من سجلات التطبيق:

```bash
# Look for messages about GitHub configuration
python app.py
```

## Additional Resources | موارد إضافية

- [GitHub Tokens Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Best Practices for Token Security](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation)

## Support | الدعم

For questions or issues related to GitHub token setup:

للأسئلة أو المشكلات المتعلقة بإعداد رمز GitHub:

- Check the documentation files in this repository
- Review `.env.example` for configuration examples
- Consult `DEPLOYMENT.md` for deployment-specific guidance

---

**Last Updated**: November 4, 2025
**Version**: 1.0
