# سياسة الأمان - Security Policy

## 🔒 نظرة عامة - Overview

نحن نأخذ أمان نظام إدارة الإسكان الجامعي على محمل الجد. يحتوي هذا المستند على معلومات حول كيفية الإبلاغ عن الثغرات الأمنية وما يمكن توقعه من فريق الأمان لدينا.

We take the security of the University Housing Management System seriously. This document contains information about how to report security vulnerabilities and what to expect from our security team.

---

## 📋 الإصدارات المدعومة - Supported Versions

نحن ندعم حالياً الإصدارات التالية بتحديثات الأمان:

We currently support the following versions with security updates:

| الإصدار / Version | مدعوم / Supported |
| ------- | ------------------ |
| الأحدث / Latest (main branch) | ✅ |
| الإصدارات السابقة / Previous versions | ❌ |

---

## 🚨 الإبلاغ عن ثغرة أمنية - Reporting a Vulnerability

### للإبلاغ الخاص - For Private Reporting

إذا اكتشفت ثغرة أمنية، نطلب منك **عدم** فتح مشكلة عامة. بدلاً من ذلك:

If you discover a security vulnerability, we ask that you **do not** open a public issue. Instead:

#### الطريقة 1: GitHub Security Advisory (المفضلة - Preferred)
1. انتقل إلى علامة التبويب **Security** في المستودع
2. انقر على **Report a vulnerability**
3. املأ النموذج بالتفاصيل التالية:
   - وصف الثغرة
   - خطوات إعادة الإنتاج
   - التأثير المحتمل
   - إصدار Python والمكتبات المستخدمة

Steps:
1. Go to the **Security** tab in the repository
2. Click on **Report a vulnerability**
3. Fill in the form with the following details:
   - Vulnerability description
   - Steps to reproduce
   - Potential impact
   - Python version and libraries used

#### الطريقة 2: البريد الإلكتروني المباشر - Direct Email
أرسل تقريرك إلى: **[أضف بريدك الإلكتروني هنا]**

Send your report to: **[Add your email here]**

### ما يجب تضمينه في التقرير - What to Include in Your Report

لمساعدتنا في فهم ومعالجة المشكلة بشكل أفضل، يرجى تضمين:

To help us better understand and address the issue, please include:

- **نوع الثغرة** / Vulnerability type (مثل: SQL Injection, XSS, etc.)
- **الموقع في الكود** / Location in code (اسم الملف ورقم السطر / file name and line number)
- **خطوات إعادة الإنتاج** / Steps to reproduce (تفصيلية / detailed)
- **التأثير المحتمل** / Potential impact (من يمكن أن يتأثر / who can be affected)
- **الأدلة** / Proof of concept (إن أمكن / if possible)
- **البيئة المستخدمة** / Environment (OS, Python version, dependencies)
- **اقتراحات للإصلاح** / Suggested fix (اختياري / optional)

---

## ⏱️ جدول الاستجابة - Response Timeline

نحن ملتزمون بالاستجابة السريعة للثغرات الأمنية:

We are committed to responding quickly to security vulnerabilities:

| الخطوة / Step | الإطار الزمني / Timeframe |
|---------------|---------------------------|
| **الإقرار الأولي** / Initial Acknowledgment | 24-48 ساعة / hours |
| **التقييم الأولي** / Initial Assessment | 3-5 أيام / days |
| **خطة الإصلاح** / Fix Plan | 7 أيام / days |
| **الإصلاح والنشر** / Fix & Release | حسب الخطورة / Based on severity |

### مستويات الخطورة - Severity Levels

#### 🔴 حرجة - Critical
- **الوصف**: ثغرة يمكن استغلالها عن بُعد دون مصادقة
- **مثال**: SQL Injection, Remote Code Execution
- **الإصلاح**: فوري (1-3 أيام)

- **Description**: Remotely exploitable without authentication
- **Example**: SQL Injection, Remote Code Execution
- **Fix**: Immediate (1-3 days)

#### 🟠 عالية - High
- **الوصف**: ثغرة تتطلب مصادقة أو وصول محدود
- **مثال**: XSS, Authentication Bypass
- **الإصلاح**: عاجل (3-7 أيام)

- **Description**: Requires authentication or limited access
- **Example**: XSS, Authentication Bypass
- **Fix**: Urgent (3-7 days)

#### 🟡 متوسطة - Medium
- **الوصف**: ثغرة ذات تأثير محدود أو صعبة الاستغلال
- **مثال**: Information Disclosure, CSRF
- **الإصلاح**: مهم (7-14 يوم)

- **Description**: Limited impact or difficult to exploit
- **Example**: Information Disclosure, CSRF
- **Fix**: Important (7-14 days)

#### 🟢 منخفضة - Low
- **الوصف**: ثغرة بسيطة أو تحسين أمني
- **مثال**: Missing HTTP Headers, Weak Configurations
- **الإصلاح**: روتيني (14-30 يوم)

- **Description**: Minor vulnerability or security improvement
- **Example**: Missing HTTP Headers, Weak Configurations
- **Fix**: Routine (14-30 days)

---

## 🛡️ ميزات الأمان المطبقة - Security Features Implemented

### حماية البيانات - Data Protection
- ✅ **تشفير كلمات المرور** / Password hashing with **bcrypt**
- ✅ **استعلامات SQL آمنة** / Parameterized SQL queries (SQL Injection prevention)
- ✅ **التحقق من أنواع الملفات** / File type validation for uploads
- ✅ **حد أقصى لحجم الملفات** / File size limits (16 MB)

### أمان الجلسات - Session Security
- ✅ **HttpOnly Cookies** - منع XSS من الوصول للكوكيز
- ✅ **SameSite Cookies** - حماية CSRF
- ✅ **Secure Cookies** - في الإنتاج (HTTPS only)
- ✅ **مفاتيح سرية قوية** / Strong secret keys with `secrets.token_hex()`

### أمان API
- ✅ **حماية مفاتيح API** / API key protection (environment variables)
- ✅ **معالجة آمنة للأخطاء** / Safe error handling (no sensitive data in errors)
- ✅ **حد زمني للاستعلامات** / Query timeouts
- ✅ **التحقق من المدخلات** / Input validation

### فحوصات الأمان الآلية - Automated Security Checks
- ✅ **CodeQL Scanning** - فحص الثغرات في الكود
- ✅ **Dependabot** - تنبيهات الثغرات في المكتبات
- ✅ **Secret Scanning** - كشف الأسرار المسربة
- ✅ **Flake8 Linting** - جودة الكود وأفضل الممارسات

---

## 🔍 الفحوصات الأمنية المنتظمة - Regular Security Audits

نحن نقوم بفحوصات أمنية منتظمة:

We conduct regular security audits:

- **CodeQL**: يتم تشغيله تلقائياً مع كل دفعة / Runs automatically with every push
- **Dependabot**: فحص أسبوعي للمكتبات / Weekly dependency scan
- **Code Review**: مراجعة يدوية لجميع التغييرات الهامة / Manual review of all significant changes
- **Penetration Testing**: حسب الحاجة / As needed

---

## 📚 الموارد الأمنية - Security Resources

### التوثيق - Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/stable/security/)
- [Python Security Guidelines](https://python.readthedocs.io/en/stable/library/security_warnings.html)

### الأدوات - Tools
- **CodeQL**: لفحص الثغرات الأمنية / For vulnerability scanning
- **Bandit**: لفحص الكود Python / For Python code analysis
- **Safety**: لفحص المكتبات / For dependency checking
- **Flake8**: لجودة الكود / For code quality

---

## ⚖️ سياسة الإفصاح - Disclosure Policy

نتبع سياسة **الإفصاح المسؤول**:

We follow a **Responsible Disclosure** policy:

1. **الخصوصية أولاً**: لا نفصح علناً حتى يتم الإصلاح
2. **الشفافية**: نقوم بإبلاغ المستخدمين عند الإصلاح
3. **التقدير**: نذكر الباحثين الأمنيين (إذا رغبوا)
4. **النشر**: ننشر استشارات أمنية بعد الإصلاح

1. **Privacy First**: We do not disclose publicly until fixed
2. **Transparency**: We inform users when fixed
3. **Recognition**: We credit security researchers (if desired)
4. **Publication**: We publish security advisories after fixing

---

## 📞 الاتصال - Contact

للأسئلة الأمنية العامة (غير الحساسة):
- **افتح مشكلة** / Open an issue مع علامة `security`
- **المناقشات** / Discussions في GitHub

For general security questions (non-sensitive):
- **Open an issue** with the `security` label
- **Discussions** on GitHub

للإبلاغ عن ثغرات حساسة:
- **GitHub Security Advisory** (المفضل)
- **البريد الإلكتروني المباشر** (انظر أعلاه)

For reporting sensitive vulnerabilities:
- **GitHub Security Advisory** (Preferred)
- **Direct Email** (See above)

---

## 🙏 شكر خاص - Special Thanks

نشكر جميع الباحثين الأمنيين والمساهمين الذين يساعدون في جعل هذا النظام أكثر أماناً.

We thank all security researchers and contributors who help make this system more secure.

---

## 📝 التحديثات - Updates

آخر تحديث لهذه السياسة: **6 نوفمبر 2025**
Last updated: **November 6, 2025**

نحن نراجع ونحدث هذه السياسة بانتظام للتأكد من أنها تعكس أفضل الممارسات الحالية.

We regularly review and update this policy to ensure it reflects current best practices.

---

**نظام إدارة الإسكان الجامعي**  
**University Housing Management System**  
**جامعة الإمام محمد بن سعود الإسلامية**  
**Imam Muhammad bin Saud Islamic University**
