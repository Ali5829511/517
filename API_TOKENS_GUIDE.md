# دليل التوكنات وAPI - API Tokens Guide

## 📋 نظرة عامة / Overview

هذا الدليل يشرح كيفية إدارة التوكنات والمفاتيح الأمنية بشكل آمن في نظام إدارة الإسكان الجامعي.

This guide explains how to securely manage tokens and API keys in the University Housing Management System.

---

## 🔐 التوكنات المدعومة / Supported Tokens

### 1. OpenAI API Key
**الغرض / Purpose:** تحليل صور السيارات واستخراج أرقام اللوحات  
**Purpose:** Vehicle image analysis and license plate extraction

**الحصول على المفتاح / Get Your Key:**
- زيارة: https://platform.openai.com/api-keys
- Visit: https://platform.openai.com/api-keys

**التنسيق / Format:** `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**الميزات المفعلة / Enabled Features:**
- ✅ تحليل صور السيارات / Vehicle image analysis
- ✅ استخراج أرقام اللوحات / License plate extraction
- ✅ التعرف على الأحرف العربية والإنجليزية / Arabic/English character recognition
- ✅ اكتشاف نوع ولون السيارة / Vehicle type and color detection

**الاستخدام / Usage:**
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

---

### 2. GitHub Personal Access Token
**الغرض / Purpose:** التكامل مع GitHub API (اختياري)  
**Purpose:** GitHub API integration (optional)

**الحصول على المفتاح / Get Your Token:**
- زيارة: https://github.com/settings/tokens
- Visit: https://github.com/settings/tokens
- الصلاحيات المطلوبة / Required scopes: `repo`

**التنسيق / Format:** `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**الاستخدام / Usage:**
```bash
GITHUB_TOKEN=ghp_your-actual-token-here
```

---

### 3. ParkPow API Token ⭐ NEW
**الغرض / Purpose:** إدارة المخالفات والمواقف  
**Purpose:** Parking violation and enforcement management

**الحصول على المفتاح / Get Your Token:**
- زيارة: https://app.parkpow.com/accounts/token/
- Visit: https://app.parkpow.com/accounts/token/

**التنسيق / Format:** 40 character hexadecimal string

**الميزات المفعلة / Enabled Features:**
- 🚗 إدارة مخالفات المواقف / Parking violation management
- 📊 تقارير المواقف المشغولة / Occupied spots reporting
- 🚫 تتبع السيارات المخالفة / Violation tracking
- 📸 ربط الصور بالمخالفات / Link images to violations

**الاستخدام / Usage:**
```bash
PARKPOW_API_TOKEN=your-parkpow-token-here
```

**وظائف ParkPow المتاحة / Available ParkPow Functions:**
1. تسجيل المخالفات تلقائياً / Auto-report violations
2. تتبع حالة المواقف / Track parking spot status
3. إرسال إشعارات المخالفات / Send violation notifications
4. تكامل مع نظام الملصقات / Integration with sticker system

---

## ⚙️ التكوين / Configuration

### في التطوير / Development Setup

1. **إنشاء ملف البيئة / Create environment file:**
```bash
cp .env.example .env
```

2. **تحرير الملف / Edit the file:**
```bash
nano .env
# أو / or
code .env
```

3. **إضافة التوكنات / Add your tokens:**
```env
# Required for image analysis
OPENAI_API_KEY=sk-your-actual-openai-key

# Optional: For GitHub integration
GITHUB_TOKEN=ghp_your-github-token

# Optional: For ParkPow parking management
PARKPOW_API_TOKEN=your-parkpow-token
```

4. **التحقق / Verify:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OpenAI:', bool(os.getenv('OPENAI_API_KEY'))); print('ParkPow:', bool(os.getenv('PARKPOW_API_TOKEN')))"
```

---

### في الإنتاج / Production Setup

#### Railway / Render:
1. افتح لوحة التحكم / Open dashboard
2. اذهب إلى Environment Variables / Go to Environment Variables
3. أضف التوكنات / Add tokens:
```
OPENAI_API_KEY=sk-...
PARKPOW_API_TOKEN=...
```

#### Heroku:
```bash
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set PARKPOW_API_TOKEN=...
```

#### Docker:
```bash
docker run -e OPENAI_API_KEY=sk-... -e PARKPOW_API_TOKEN=... your-app
```

---

## 🔒 أفضل الممارسات الأمنية / Security Best Practices

### ✅ يجب فعله / DO:
1. ✅ **استخدم متغيرات البيئة** / Use environment variables
2. ✅ **دور التوكنات بانتظام** / Rotate tokens regularly (every 90 days)
3. ✅ **استخدم توكنات مختلفة** / Use different tokens for:
   - التطوير / Development
   - المرحلة التجريبية / Staging
   - الإنتاج / Production
4. ✅ **راقب الاستخدام** / Monitor API usage
5. ✅ **فعّل التحقق بخطوتين** / Enable 2FA on API accounts
6. ✅ **احتفظ بنسخة احتياطية آمنة** / Keep secure backup of tokens

### ❌ لا تفعل / DON'T:
1. ❌ **لا تضف .env إلى Git** / Never commit .env to Git
2. ❌ **لا تشارك التوكنات علناً** / Never share tokens publicly
3. ❌ **لا تضع التوكنات في الكود** / Never hardcode tokens
4. ❌ **لا تستخدم نفس التوكن في بيئات مختلفة** / Don't use same token across environments
5. ❌ **لا تخزن التوكنات في قاعدة البيانات** / Don't store tokens in database

---

## 🧪 الاختبار / Testing

### اختبار OpenAI:
```bash
python -c "
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    client = OpenAI(api_key=api_key)
    print('✅ OpenAI API متصل / Connected')
else:
    print('❌ OPENAI_API_KEY غير موجود / Not found')
"
```

### اختبار ParkPow:
```bash
python -c "
import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('PARKPOW_API_TOKEN')

if token:
    headers = {'Authorization': f'Token {token}'}
    response = requests.get('https://api.parkpow.com/v1/verify', headers=headers)
    if response.status_code == 200:
        print('✅ ParkPow API متصل / Connected')
    else:
        print('⚠️  ParkPow API: خطأ في التوكن / Token error')
else:
    print('❌ PARKPOW_API_TOKEN غير موجود / Not found')
"
```

---

## 🔄 تدوير التوكنات / Token Rotation

### متى تدور التوكن / When to Rotate:
- ⏰ كل 90 يوم بشكل منتظم / Every 90 days routinely
- 🚨 فوراً إذا تم الكشف عنه / Immediately if exposed
- 🔄 عند تغيير الموظفين / When staff changes
- 🔧 بعد مشكلة أمنية / After security incident

### كيفية التدوير / How to Rotate:

#### 1. إنشاء توكن جديد / Generate New Token:
- OpenAI: https://platform.openai.com/api-keys
- ParkPow: https://app.parkpow.com/accounts/token/

#### 2. تحديث متغيرات البيئة / Update Environment:
```bash
# Development
nano .env
# Update the token

# Production (Railway/Render)
# Update in dashboard

# Production (Heroku)
heroku config:set PARKPOW_API_TOKEN=new-token
```

#### 3. إعادة التشغيل / Restart Application:
```bash
# Local
python app.py

# Production
# Auto-restarts on Railway/Render
# Heroku: heroku restart
```

#### 4. إلغاء التوكن القديم / Revoke Old Token:
- احذف التوكن القديم من المنصة / Delete old token from platform
- تحقق من عدم استخدامه / Verify it's not in use

---

## 📊 مراقبة الاستخدام / Usage Monitoring

### OpenAI:
- لوحة التحكم / Dashboard: https://platform.openai.com/usage
- راقب الطلبات والتكلفة / Monitor requests and costs

### ParkPow:
- لوحة التحكم / Dashboard: https://app.parkpow.com/dashboard
- راقب المخالفات والنشاط / Monitor violations and activity

---

## 🆘 استكشاف الأخطاء / Troubleshooting

### خطأ: "OPENAI_API_KEY not found"
```bash
# تحقق من وجود الملف / Check file exists
ls -la .env

# تحقق من المحتوى / Check content
cat .env | grep OPENAI_API_KEY

# تحقق من التحميل / Verify loading
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY'))"
```

### خطأ: "Invalid API Key"
1. ✅ تحقق من صحة التوكن / Verify token is correct
2. ✅ تحقق من عدم وجود مسافات / Check for spaces
3. ✅ تحقق من تاريخ الانتهاء / Check expiration
4. ✅ أنشئ توكن جديد / Generate new token

### خطأ: "Rate limit exceeded"
1. ⏳ انتظر قليلاً / Wait a moment
2. 📊 راقب الاستخدام / Monitor usage
3. 💳 ارفع الحد / Upgrade plan if needed

---

## 📝 التحديث الأخير / Last Updated
- **التاريخ / Date:** 2025-11-18
- **الإصدار / Version:** 2.0
- **التغييرات / Changes:** أضيف دعم ParkPow Token / Added ParkPow Token support

---

## 📞 الدعم / Support

للمساعدة في التوكنات والأمان:
For help with tokens and security:

- 📧 Email: aliayashi517@gmail.com
- 🐛 Issues: https://github.com/Ali5829511/517/issues
- 📚 Docs: راجع هذا الدليل / Refer to this guide

---

**تذكر / Remember:** 🔐 الأمان أولاً! لا تشارك التوكنات أبداً / Security first! Never share tokens!
