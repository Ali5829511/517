# إعدادات GitHub للمستودع - Repository GitHub Configuration

هذا المجلد يحتوي على جميع إعدادات وسير العمل الخاصة بـ GitHub.

This directory contains all GitHub-specific configurations and workflows.

---

## 📁 محتويات المجلد - Directory Contents

### 🔒 الأمان - Security

#### `SECURITY_SETUP_GUIDE.md`
**دليل شامل لإعداد ميزات الأمان في GitHub**

دليل خطوة بخطوة لتفعيل:
- Security Advisories (الاستشارات الأمنية)
- Private Vulnerability Reporting (الإبلاغ الخاص)
- Dependabot Alerts (تنبيهات التبعيات)
- Code Scanning (فحص الكود)
- Secret Scanning (فحص الأسرار)

**Comprehensive guide for setting up GitHub security features**

Step-by-step guide to enable:
- Security Advisories
- Private Vulnerability Reporting
- Dependabot Alerts
- Code Scanning
- Secret Scanning

📖 **اقرأ الدليل**: [SECURITY_SETUP_GUIDE.md](./SECURITY_SETUP_GUIDE.md)

---

#### `dependabot.yml`
**تكوين Dependabot للتحديثات التلقائية**

يتحكم في:
- فحص التبعيات يومياً
- إنشاء طلبات سحب للتحديثات
- تجميع التحديثات حسب النوع
- تنبيهات الأمان الفورية

**Dependabot configuration for automatic updates**

Controls:
- Daily dependency scanning
- Automatic pull request creation
- Grouped updates by type
- Immediate security alerts

📄 **الملف**: [dependabot.yml](./dependabot.yml)

---

### ⚙️ سير العمل - Workflows

#### `workflows/codeql.yml`
**فحص أمني شامل باستخدام CodeQL**

ميزات:
- ✅ فحص تلقائي مع كل push
- ✅ فحص أسبوعي مجدول
- ✅ فحص ثغرات Python
- ✅ رفع النتائج إلى GitHub Security
- ✅ فحص التبعيات بواسطة Safety

**Comprehensive security scanning with CodeQL**

Features:
- ✅ Automatic scan on every push
- ✅ Weekly scheduled scan
- ✅ Python vulnerability detection
- ✅ Results uploaded to GitHub Security
- ✅ Dependency check with Safety

📄 **الملف**: [workflows/codeql.yml](./workflows/codeql.yml)

---

#### `workflows/python-package-conda.yml`
**بناء واختبار الحزمة Python**

يتم تشغيله عند:
- كل push للمستودع
- طلبات السحب

الخطوات:
1. إعداد Python 3.10
2. تثبيت التبعيات
3. Flake8 linting
4. تشغيل الاختبارات بواسطة pytest

**Build and test Python package**

Runs on:
- Every push to repository
- Pull requests

Steps:
1. Set up Python 3.10
2. Install dependencies
3. Flake8 linting
4. Run tests with pytest

📄 **الملف**: [workflows/python-package-conda.yml](./workflows/python-package-conda.yml)

---

### 📝 التوثيق - Documentation

#### `copilot-instructions.md`
تعليمات مخصصة لـ GitHub Copilot حول المشروع

Custom instructions for GitHub Copilot about the project

---

## 🚀 البدء السريع - Quick Start

### 1️⃣ تفعيل جميع ميزات الأمان
```bash
# اقرأ دليل الإعداد / Read setup guide
cat .github/SECURITY_SETUP_GUIDE.md
```

### 2️⃣ مراجعة سير العمل
```bash
# عرض سير العمل / View workflows
ls -la .github/workflows/
```

### 3️⃣ فحص تكوين Dependabot
```bash
# عرض تكوين Dependabot / View Dependabot config
cat .github/dependabot.yml
```

---

## 📊 حالة الأمان - Security Status

### ✅ المميزات المفعّلة - Enabled Features

| الميزة / Feature | الحالة / Status | الملف / File |
|-----------------|----------------|--------------|
| Security Policy | ✅ Active | `/SECURITY.md` |
| CodeQL Scanning | ✅ Active | `workflows/codeql.yml` |
| Dependabot | ✅ Configured | `dependabot.yml` |
| CI/CD Tests | ✅ Active | `workflows/python-package-conda.yml` |

### ⚙️ يتطلب تفعيل يدوي - Requires Manual Setup

هذه الميزات تحتاج تفعيل من إعدادات GitHub:

These features need activation from GitHub settings:

- [ ] Security Advisories
- [ ] Private Vulnerability Reporting
- [ ] Dependabot Alerts
- [ ] Code Scanning Alerts
- [ ] Secret Scanning
- [ ] Push Protection

📖 **راجع دليل الإعداد الكامل**: [SECURITY_SETUP_GUIDE.md](./SECURITY_SETUP_GUIDE.md)

---

## 🔄 سير العمل التلقائي - Automated Workflows

### عند كل Push
1. **Python Package Test** - اختبار الحزمة
   - Flake8 linting
   - pytest tests
   
2. **CodeQL Analysis** - فحص الأمان
   - Python vulnerability scan
   - Dependency check

### أسبوعياً (Mondays 6 AM)
- **CodeQL Scheduled Scan** - فحص مجدول
- **Dependabot Check** - فحص التبعيات

### يومياً
- **Dependabot Security Check** - فحص الثغرات

---

## 🛠️ الصيانة - Maintenance

### تحديث سير العمل - Update Workflows
```bash
# تحرير سير عمل CodeQL / Edit CodeQL workflow
vim .github/workflows/codeql.yml

# تحرير تكوين Dependabot / Edit Dependabot config
vim .github/dependabot.yml
```

### مراجعة السجلات - Review Logs
1. اذهب إلى **Actions** tab في GitHub
2. اختر سير العمل
3. راجع نتائج التشغيل

Go to:
1. **Actions** tab on GitHub
2. Select workflow
3. Review run results

---

## 📚 الموارد - Resources

### داخلية - Internal
- [SECURITY.md](../SECURITY.md) - سياسة الأمان الكاملة
- [SECURITY_SUMMARY.md](../SECURITY_SUMMARY.md) - ملخص الأمان
- [SECURITY_SETUP_GUIDE.md](./SECURITY_SETUP_GUIDE.md) - دليل الإعداد

### خارجية - External
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)

---

## 🤝 المساهمة - Contributing

عند إضافة سير عمل جديد:
1. أضفه في `workflows/`
2. أضف وثائق هنا
3. اختبره محلياً إن أمكن
4. راجع السجلات بعد التشغيل

When adding new workflows:
1. Add to `workflows/`
2. Document here
3. Test locally if possible
4. Review logs after running

---

## 📞 الدعم - Support

للأسئلة حول الإعدادات:
- افتح Issue مع علامة `question`
- راجع [SECURITY_SETUP_GUIDE.md](./SECURITY_SETUP_GUIDE.md)

For questions about configurations:
- Open Issue with `question` label
- Review [SECURITY_SETUP_GUIDE.md](./SECURITY_SETUP_GUIDE.md)

---

**آخر تحديث**: 6 نوفمبر 2025  
**Last updated**: November 6, 2025

**نظام إدارة الإسكان الجامعي**  
**University Housing Management System**
