# دليل المساهمة - Contributing Guide

مرحباً بك في نظام إدارة الإسكان الجامعي! 🎉
Welcome to the University Housing Management System! 🎉

نحن نرحب بالمساهمات من الجميع، سواء كنت مطوراً متمرساً أو مبتدئاً.
We welcome contributions from everyone, whether you're an experienced developer or just getting started.

## 📋 جدول المحتويات - Table of Contents

- [كيف يمكنني المساهمة؟](#how-can-i-contribute)
- [الإعداد الأولي](#getting-started)
- [إرشادات الكود](#code-guidelines)
- [عملية المراجعة](#review-process)
- [الحصول على المساعدة](#getting-help)

## 🤝 كيف يمكنني المساهمة؟ - How Can I Contribute?

### الإبلاغ عن الأخطاء - Reporting Bugs

إذا وجدت خطأ، يرجى فتح قضية باستخدام [نموذج تقرير الأخطاء](.github/ISSUE_TEMPLATE/bug_report.yml).
If you find a bug, please open an issue using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml).

### اقتراح ميزات جديدة - Suggesting Features

لديك فكرة لميزة جديدة؟ افتح قضية باستخدام [نموذج طلب الميزة](.github/ISSUE_TEMPLATE/feature_request.yml).
Have an idea for a new feature? Open an issue using the [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml).

### البحث عن قضايا للمبتدئين - Finding Good First Issues

ابحث عن القضايا المصنفة بـ `good first issue` - هذه مناسبة للمساهمين الجدد!
Look for issues labeled `good first issue` - these are great for new contributors!

[رابط القضايا المناسبة للمبتدئين](https://github.com/Ali5829511/517/labels/good%20first%20issue)

## 🚀 الإعداد الأولي - Getting Started

### 1. استنساخ المستودع - Clone the Repository

```bash
git clone https://github.com/Ali5829511/517.git
cd 517
```

### 2. تثبيت المتطلبات - Install Dependencies

```bash
# تثبيت المتطلبات الأساسية
pip install -r requirements.txt

# تثبيت أدوات التطوير
pip install pytest flake8 black
```

أو استخدم Makefile:

```bash
make install
make install-dev
```

### 3. التحقق من الإعداد - Verify Setup

```bash
# تشغيل الاختبارات
make test

# فحص جودة الكود
make lint
```

### 4. إنشاء فرع جديد - Create a New Branch

```bash
git checkout -b feature/your-feature-name
```

## 📝 إرشادات الكود - Code Guidelines

### أسلوب الكود - Code Style

- نتبع معايير **PEP 8** للكود Python
  We follow **PEP 8** standards for Python code
  
- حد الأسطر: **100 حرف**
  Line limit: **100 characters**
  
- استخدم **Black** للتنسيق التلقائي:
  Use **Black** for automatic formatting:
  ```bash
  make format
  ```

### تسمية المتغيرات - Naming Conventions

- الفئات: `CamelCase`
- الوظائف والمتغيرات: `snake_case`
- الثوابت: `UPPER_SNAKE_CASE`
- الوظائف الخاصة: `_leading_underscore`

### التعليقات والتوثيق - Comments and Documentation

- استخدم docstrings لجميع الوظائف والفئات العامة
  Use docstrings for all public functions and classes
  
- قدم وصفاً بالعربية والإنجليزية عند الإمكان
  Provide descriptions in both Arabic and English when possible
  
- مثال - Example:
  ```python
  def get_all_residents():
      """
      الحصول على جميع السكان
      Get all residents from the database
      
      Returns:
          list: قائمة بقواميس تفاصيل السكان
                List of resident dictionaries with details
      """
  ```

### الاختبارات - Testing

- أضف اختبارات للوظائف الجديدة
  Add tests for new functionality
  
- تأكد من نجاح جميع الاختبارات:
  Ensure all tests pass:
  ```bash
  make test
  ```

### الدعم العربي - Arabic Support

- هذا المشروع يدعم اللغة العربية بشكل كامل
  This project has full Arabic language support
  
- قدم ترجمات عربية للنصوص التي تواجه المستخدم
  Provide Arabic translations for user-facing text
  
- استخدم ترميز UTF-8 لجميع الملفات
  Use UTF-8 encoding for all files

## 🔄 عملية طلب السحب - Pull Request Process

### 1. قبل تقديم PR - Before Submitting

```bash
# تشغيل الاختبارات
make test

# فحص الكود
make lint

# تنسيق الكود
make format
```

### 2. تقديم PR - Submitting

1. ادفع التغييرات إلى فرعك
   Push your changes to your branch
   
2. افتح طلب سحب (Pull Request)
   Open a Pull Request
   
3. املأ [نموذج PR](.github/PULL_REQUEST_TEMPLATE.md) بالكامل
   Fill out the [PR template](.github/PULL_REQUEST_TEMPLATE.md) completely
   
4. اربط القضايا ذات الصلة (مثل: `Closes #123`)
   Link related issues (e.g., `Closes #123`)

### 3. قائمة التحقق - Checklist

- [ ] قرأت دليل المساهمة هذا
- [ ] الكود يتبع معايير المشروع
- [ ] أضفت/حدثت الاختبارات
- [ ] جميع الاختبارات تنجح
- [ ] أضفت التعليقات حيث لزم الأمر
- [ ] حدثت التوثيق
- [ ] أضفت ترجمات عربية

## 👀 عملية المراجعة - Review Process

### ماذا تتوقع - What to Expect

1. **المراجعة الأولية** (1-3 أيام)
   Initial Review (1-3 days)
   - سيراجع فريقنا طلب السحب الخاص بك
     Our team will review your pull request

2. **التعليقات والتغييرات**
   Feedback and Changes
   - قد نطلب بعض التغييرات
     We may request some changes
   - الرجاء الرد على التعليقات
     Please respond to comments

3. **الموافقة والدمج**
   Approval and Merge
   - بعد الموافقة، سيتم دمج PR
     After approval, your PR will be merged
   - تهانينا! أنت الآن مساهم رسمي 🎉
     Congratulations! You're now an official contributor 🎉

## 💡 نصائح للمساهمين الجدد - Tips for New Contributors

### ابدأ صغيراً - Start Small

- ابحث عن قضايا `good first issue`
  Look for `good first issue` labeled issues
  
- لا تتردد في طرح الأسئلة
  Don't hesitate to ask questions
  
- اقرأ الكود الموجود لفهم الأنماط
  Read existing code to understand patterns

### التواصل - Communication

- كن محترماً ومهذباً
  Be respectful and polite
  
- اطرح الأسئلة في القضية ذات الصلة
  Ask questions in the relevant issue
  
- أخبرنا إذا كنت بحاجة إلى مساعدة
  Let us know if you need help

### أفضل الممارسات - Best Practices

- اكتب رسائل commit واضحة
  Write clear commit messages
  
- احتفظ بـ PRs صغيرة ومركزة
  Keep PRs small and focused
  
- اختبر التغييرات بدقة
  Test your changes thoroughly

## 📚 الموارد - Resources

### الوثائق - Documentation

- [دليل البدء السريع](../QUICK_START.md)
- [دليل التطوير](../DEVELOPMENT.md)
- [دليل النشر](../DEPLOYMENT_GUIDE.md)

### الأدوات - Tools

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)

### الحصول على المساعدة - Getting Help

- 💬 [المناقشات](https://github.com/Ali5829511/517/discussions)
- 🐛 [الإبلاغ عن مشكلة](https://github.com/Ali5829511/517/issues/new/choose)
- 📧 تواصل مع المشرفين

## 🏆 المساهمون - Contributors

شكراً لجميع المساهمين الذين يساعدون في تحسين هذا المشروع!
Thanks to all contributors who help improve this project!

<a href="https://github.com/Ali5829511/517/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Ali5829511/517" />
</a>

---

## 📜 قواعد السلوك - Code of Conduct

نحن ملتزمون بتوفير بيئة ترحيبية وشاملة للجميع.
We are committed to providing a welcoming and inclusive environment for everyone.

### المتوقع - Expected Behavior

- كن محترماً ومهذباً
- كن متعاوناً وبناءً
- كن منفتحاً على التعليقات
- ركز على ما هو أفضل للمجتمع

### غير المقبول - Unacceptable Behavior

- التحرش بأي شكل من الأشكال
- اللغة أو الصور المسيئة
- الهجمات الشخصية
- نشر معلومات خاصة للآخرين

---

**شكراً لمساهمتك في نظام إدارة الإسكان الجامعي! 🎓**
**Thank you for contributing to the University Housing Management System! 🎓**

Built with ❤️ for Imam Muhammad bin Saud Islamic University
