# دليل إعداد الأمان - Security Setup Guide

هذا الدليل يشرح كيفية تفعيل جميع ميزات الأمان في GitHub لهذا المستودع.

This guide explains how to enable all security features in GitHub for this repository.

---

## ✅ الميزات المكتملة تلقائياً - Automatically Configured Features

تم إعداد هذه الميزات من خلال الملفات في المستودع:

These features are configured through files in the repository:

- ✅ **Security Policy** - ملف `SECURITY.md` في الجذر
- ✅ **CodeQL Analysis** - سير العمل `.github/workflows/codeql.yml`
- ✅ **Dependabot** - ملف التكوين `.github/dependabot.yml`

---

## 🔧 الميزات التي تحتاج إلى تفعيل يدوي - Features Requiring Manual Setup

### 1️⃣ تفعيل Security Advisories (الاستشارات الأمنية)

#### الخطوات بالعربية:
1. انتقل إلى صفحة المستودع على GitHub
2. انقر على تبويب **"Security"** (الأمان)
3. في القسم الجانبي، انقر على **"Advisories"**
4. انقر على **"Enable security advisories"**
5. تأكيد التفعيل

#### Steps in English:
1. Go to the repository page on GitHub
2. Click on the **"Security"** tab
3. In the sidebar, click on **"Advisories"**
4. Click **"Enable security advisories"**
5. Confirm activation

**الفائدة**: يسمح لك بإنشاء واستعراض الاستشارات الأمنية لهذا المستودع.

**Benefit**: Allows you to create and view security advisories for this repository.

---

### 2️⃣ تفعيل Private Vulnerability Reporting (الإبلاغ الخاص عن الثغرات)

#### الخطوات بالعربية:
1. اذهب إلى **Settings** (الإعدادات) في المستودع
2. في القائمة الجانبية، انقر على **"Code security and analysis"**
3. ابحث عن قسم **"Private vulnerability reporting"**
4. انقر على **"Enable"** (تفعيل)

#### Steps in English:
1. Go to **Settings** in the repository
2. In the sidebar, click on **"Code security and analysis"**
3. Find the **"Private vulnerability reporting"** section
4. Click **"Enable"**

**الفائدة**: يسمح للمستخدمين بالإبلاغ بشكل خاص عن الثغرات الأمنية دون نشرها علناً.

**Benefit**: Allows users to privately report security vulnerabilities without public disclosure.

---

### 3️⃣ تفعيل Dependabot Alerts (تنبيهات Dependabot)

#### الخطوات بالعربية:
1. اذهب إلى **Settings** → **"Code security and analysis"**
2. ابحث عن **"Dependabot alerts"**
3. انقر على **"Enable"** (تفعيل)
4. (اختياري) فعّل **"Dependabot security updates"** للتحديثات التلقائية

#### Steps in English:
1. Go to **Settings** → **"Code security and analysis"**
2. Find **"Dependabot alerts"**
3. Click **"Enable"**
4. (Optional) Enable **"Dependabot security updates"** for automatic updates

**الفائدة**: تلقي إشعارات عند اكتشاف ثغرات في المكتبات المستخدمة.

**Benefit**: Receive notifications when vulnerabilities are found in dependencies.

---

### 4️⃣ تفعيل Code Scanning Alerts (تنبيهات فحص الكود)

#### الخطوات بالعربية:
1. اذهب إلى **Settings** → **"Code security and analysis"**
2. ابحث عن **"Code scanning"**
3. انقر على **"Set up"** → **"GitHub Actions"**
4. سيتم اكتشاف ملف `codeql.yml` الموجود تلقائياً
5. انقر على **"Enable CodeQL"**

**ملاحظة**: ملف سير العمل موجود بالفعل (`.github/workflows/codeql.yml`)

#### Steps in English:
1. Go to **Settings** → **"Code security and analysis"**
2. Find **"Code scanning"**
3. Click **"Set up"** → **"GitHub Actions"**
4. The existing `codeql.yml` file will be detected automatically
5. Click **"Enable CodeQL"**

**Note**: The workflow file already exists (`.github/workflows/codeql.yml`)

**الفائدة**: الكشف التلقائي عن الثغرات الأمنية في الكود.

**Benefit**: Automatic detection of security vulnerabilities in code.

---

### 5️⃣ تفعيل Secret Scanning (فحص الأسرار)

#### للمستودعات العامة (Public Repositories):
Secret scanning **مفعّل تلقائياً** في المستودعات العامة!

Secret scanning is **automatically enabled** for public repositories!

#### للمستودعات الخاصة (Private Repositories):

##### الخطوات بالعربية:
1. اذهب إلى **Settings** → **"Code security and analysis"**
2. ابحث عن **"Secret scanning"**
3. انقر على **"Enable"** (تفعيل)
4. (موصى به) فعّل **"Push protection"** لمنع دفع الأسرار

##### Steps in English:
1. Go to **Settings** → **"Code security and analysis"**
2. Find **"Secret scanning"**
3. Click **"Enable"**
4. (Recommended) Enable **"Push protection"** to prevent pushing secrets

**الفائدة**: الكشف التلقائي عن المفاتيح السرية وكلمات المرور المدفوعة إلى المستودع.

**Benefit**: Automatic detection of secret keys and passwords pushed to the repository.

---

## 📋 قائمة التحقق النهائية - Final Checklist

استخدم هذه القائمة للتأكد من تفعيل جميع الميزات:

Use this checklist to ensure all features are enabled:

### ملفات التكوين - Configuration Files
- [x] ✅ `SECURITY.md` - سياسة الأمان
- [x] ✅ `.github/workflows/codeql.yml` - CodeQL workflow
- [x] ✅ `.github/dependabot.yml` - Dependabot config

### إعدادات GitHub - GitHub Settings
- [ ] ⚙️ Security Advisories - تفعيل الاستشارات الأمنية
- [ ] ⚙️ Private Vulnerability Reporting - الإبلاغ الخاص
- [ ] ⚙️ Dependabot Alerts - تنبيهات Dependabot
- [ ] ⚙️ Dependabot Security Updates - التحديثات التلقائية
- [ ] ⚙️ Code Scanning - فحص الكود (CodeQL)
- [ ] ⚙️ Secret Scanning - فحص الأسرار
- [ ] ⚙️ Push Protection - حماية الدفع (للأسرار)

---

## 🔍 التحقق من الإعدادات - Verify Settings

### 1. صفحة الأمان - Security Tab
بعد التفعيل، يجب أن ترى:
- **Security advisories** - قسم للاستشارات
- **Dependabot alerts** - التنبيهات
- **Code scanning** - نتائج الفحص
- **Secret scanning** - تنبيهات الأسرار

After enabling, you should see:
- **Security advisories** - Advisory section
- **Dependabot alerts** - Alerts
- **Code scanning** - Scan results
- **Secret scanning** - Secret alerts

### 2. Actions Tab
تحقق من تشغيل سير العمل:
- ✅ **CodeQL Analysis** - يعمل تلقائياً
- ✅ **Python Package** - الاختبارات

Verify workflows are running:
- ✅ **CodeQL Analysis** - Runs automatically
- ✅ **Python Package** - Tests

### 3. Insights → Dependency Graph
يجب أن ترى:
- قائمة بجميع المكتبات
- تنبيهات الأمان (إن وجدت)
- طلبات Dependabot

You should see:
- List of all dependencies
- Security alerts (if any)
- Dependabot pull requests

---

## 📊 مراقبة الأمان - Security Monitoring

### الإشعارات - Notifications
ستتلقى إشعارات عن:
- ثغرات جديدة في المكتبات
- تنبيهات CodeQL
- أسرار مكتشفة
- تحديثات Dependabot

You will receive notifications about:
- New vulnerabilities in dependencies
- CodeQL alerts
- Detected secrets
- Dependabot updates

### التقارير الدورية - Regular Reports
- **أسبوعي**: Dependabot checks
- **يومي**: فحص التحديثات الأمنية
- **تلقائي**: مع كل push

- **Weekly**: Dependabot checks
- **Daily**: Security update scanning
- **Automatic**: With every push

---

## 🆘 الدعم والمساعدة - Support & Help

### مشاكل شائعة - Common Issues

#### ❓ CodeQL لا يعمل
**الحل**: تأكد من وجود ملف `.github/workflows/codeql.yml` وأن GitHub Actions مفعّل.

**Solution**: Ensure `.github/workflows/codeql.yml` exists and GitHub Actions is enabled.

#### ❓ Dependabot لا يُنشئ طلبات سحب
**الحل**: تحقق من إعدادات الأذونات في Settings → Actions → General

**Solution**: Check permissions in Settings → Actions → General

#### ❓ Secret Scanning لا يظهر
**الحل**: 
- للمستودعات العامة: تلقائي
- للمستودعات الخاصة: يتطلب GitHub Advanced Security

**Solution**:
- For public repos: Automatic
- For private repos: Requires GitHub Advanced Security

---

## 📚 موارد إضافية - Additional Resources

### التوثيق الرسمي - Official Documentation
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

### أدلة داخلية - Internal Guides
- `SECURITY.md` - سياسة الأمان الكاملة
- `SECURITY_SUMMARY.md` - ملخص الأمان
- `.github/workflows/codeql.yml` - تكوين CodeQL

---

## ✅ الخلاصة - Summary

بعد إكمال جميع الخطوات، سيكون المستودع:

After completing all steps, the repository will have:

- 🔒 **سياسة أمان واضحة** - Clear security policy
- 🔍 **فحص تلقائي للكود** - Automatic code scanning
- 📦 **مراقبة التبعيات** - Dependency monitoring
- 🔐 **كشف الأسرار** - Secret detection
- 📢 **آلية إبلاغ آمنة** - Safe reporting mechanism
- 🚀 **تحديثات تلقائية** - Automatic updates

**الوقت المقدر للإعداد الكامل**: 10-15 دقيقة

**Estimated time for complete setup**: 10-15 minutes

---

**آخر تحديث**: 6 نوفمبر 2025  
**Last updated**: November 6, 2025

**نظام إدارة الإسكان الجامعي**  
**University Housing Management System**
