# دليل الهوية البصرية الموحدة
# Visual Identity Guide - Unified Theme

## نظرة عامة | Overview

تم توحيد الهوية البصرية لنظام إدارة الإسكان الجامعي لجامعة الإمام محمد بن سعود الإسلامية لضمان تجربة مستخدم متسقة واحترافية عبر جميع صفحات النظام.

The visual identity of the Faculty Housing Management System for Imam Muhammad bin Saud Islamic University has been unified to ensure a consistent and professional user experience across all system pages.

---

## الألوان الرسمية | Official Colors

### الألوان الأساسية | Primary Colors

```css
--imam-dark-green: #1a472a;   /* الأخضر الداكن */
--imam-green: #2d6a3e;         /* الأخضر المتوسط */
--imam-gold: #C9A961;          /* الذهبي */
```

### الألوان الثانوية | Secondary Colors

```css
--background-light: #f5f7fa;   /* خلفية فاتحة */
--background-white: #ffffff;   /* أبيض */
--text-dark: #333333;          /* نص داكن */
--text-medium: #666666;        /* نص متوسط */
--text-light: #999999;         /* نص فاتح */
```

### ألوان الحالة | Status Colors

```css
--success-green: #28a745;      /* نجاح */
--warning-orange: #ff9800;     /* تحذير */
--error-red: #dc3545;          /* خطأ */
--info-blue: #17a2b8;          /* معلومات */
```

---

## الخطوط | Typography

### الخط الأساسي | Primary Font

```css
font-family: 'Tajawal', Arial, sans-serif;
```

**Tajawal** - خط عربي حديث ومقروء، مُحسَّن للنصوص العربية
- خط عربي احترافي من Google Fonts
- يدعم الأوزان: 400 (عادي)، 500 (متوسط)، 700 (عريض)
- مُحسَّن للقراءة على الشاشات

---

## التدرجات اللونية | Gradients

### التدرج الأساسي | Primary Gradient

```css
background: linear-gradient(135deg, #1a472a 0%, #2d6a3e 100%);
```

يُستخدم في:
- الرؤوس والعناوين
- أزرار الإجراءات الأساسية
- الأشرطة العلوية

### تدرج الذهبي | Gold Gradient

```css
background: linear-gradient(135deg, #C9A961 0%, #d4b56e 100%);
```

يُستخدم في:
- العناصر المميزة
- الأزرار الثانوية
- الأيقونات الخاصة

---

## المكونات | Components

### الأزرار | Buttons

#### الزر الأساسي | Primary Button
```css
.btn-primary {
    background: linear-gradient(135deg, #2d6a3e 0%, #1a472a 100%);
    color: white;
    padding: 12px 25px;
    border-radius: 12px;
}
```

#### الزر الثانوي | Secondary Button
```css
.btn-secondary {
    background: #C9A961;
    color: #1a472a;
    padding: 12px 25px;
    border-radius: 12px;
}
```

### البطاقات | Cards

```css
.card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(26, 71, 42, 0.15);
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #2d6a3e 0%, #1a472a 100%);
}
```

### الرؤوس | Headers

```css
.header {
    background: linear-gradient(135deg, #1a472a 0%, #2d6a3e 100%);
    color: white;
    padding: 30px;
    border-radius: 20px;
}
```

---

## الصفحات المحدثة | Updated Pages

### ✅ الصفحات الرئيسية | Main Pages
- `main_portal.html` - البوابة الرئيسية
- `login.html` - تسجيل الدخول
- `index.html` - النظام الرئيسي
- `interactive_dashboard.html` - لوحة المعلومات التفاعلية

### ✅ صفحات الإدارة | Management Pages
- `residents_management_updated.html` - إدارة السكان
- `residential_units_management.html` - إدارة الوحدات السكنية
- `buildings_management_updated.html` - إدارة المباني
- `admin_users.html` - إدارة المستخدمين
- `enhanced_stickers_management.html` - إدارة الملصقات
- `enhanced_parking_management.html` - إدارة المواقف
- `enhanced_traffic_violations_updated.html` - إدارة المخالفات
- `complaints_management.html` - إدارة الشكاوى
- `security_incidents.html` - الحوادث الأمنية

### ✅ صفحات الذكاء الاصطناعي | AI Pages
- `comprehensive_image_processing.html` - معالجة الصور
- `visual_parking_classifier.html` - فرز الصور
- `advanced_plate_recognition.html` - التعرف على اللوحات

### ✅ صفحات التقارير | Report Pages
- `comprehensive_reports.html` - التقارير الشاملة
- `comprehensive_system_report.html` - التقرير الشامل للنظام
- `advanced_reports.html` - التقارير المتقدمة
- `detailed_reports.html` - التقارير التفصيلية
- `professional_report.html` - التقارير الاحترافية
- `violations_report.html` - تقرير المخالفات

### ✅ صفحات أخرى | Other Pages
- `forgot-password.html` - نسيت كلمة المرور
- `reset-password.html` - إعادة تعيين كلمة المرور
- `resident_card.html` - بطاقة الساكن

---

## ملف CSS الموحد | Unified CSS File

تم إنشاء ملف `unified_theme.css` يحتوي على جميع أنماط الهوية البصرية الموحدة:

```
/static/unified_theme.css
```

يمكن استخدامه في صفحات جديدة بإضافة:

```html
<link rel="stylesheet" href="unified_theme.css">
```

---

## الظلال | Shadows

```css
--shadow-sm: 0 2px 4px rgba(26, 71, 42, 0.1);
--shadow-md: 0 4px 12px rgba(26, 71, 42, 0.15);
--shadow-lg: 0 10px 40px rgba(26, 71, 42, 0.2);
```

---

## نصف القطر | Border Radius

```css
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 20px;
--radius-full: 50%;
```

---

## الانتقالات | Transitions

```css
--transition-fast: 0.2s ease;
--transition-normal: 0.3s ease;
--transition-slow: 0.5s ease;
```

---

## إرشادات الاستخدام | Usage Guidelines

### 1. الألوان | Colors
- استخدم الأخضر الداكن (#1a472a) والأخضر المتوسط (#2d6a3e) للعناصر الرئيسية
- استخدم الذهبي (#C9A961) للعناصر المميزة والتأكيدات
- حافظ على التباين الجيد بين النص والخلفية

### 2. الخطوط | Fonts
- استخدم خط Tajawal لجميع النصوص العربية
- الأوزان: 400 للنص العادي، 500 للعناوين الفرعية، 700 للعناوين الرئيسية

### 3. المسافات | Spacing
- استخدم padding متسق: 15px، 20px، 25px، 30px
- استخدم gap متسق: 15px، 20px، 30px للشبكات

### 4. الرسوم المتحركة | Animations
- استخدم transition-normal (0.3s) للتفاعلات العادية
- استخدم transition-fast (0.2s) للتفاعلات السريعة
- استخدم transition-slow (0.5s) للرسوم المتحركة البطيئة

---

## التوافق | Compatibility

### المتصفحات المدعومة | Supported Browsers
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### الأجهزة | Devices
- ✅ أجهزة سطح المكتب (Desktop)
- ✅ الأجهزة اللوحية (Tablets)
- ✅ الهواتف المحمولة (Mobile)

---

## الصور والأمثلة | Screenshots & Examples

### 1. البوابة الرئيسية | Main Portal
![Main Portal](https://github.com/user-attachments/assets/11cb4042-cb78-41f6-aee4-c4ff75e67768)

### 2. تسجيل الدخول | Login Page
![Login Page](https://github.com/user-attachments/assets/8e928661-d2bf-40cd-8b8a-7adfa1f95225)

### 3. لوحة التحكم الرئيسية | Main Dashboard
![Main Dashboard](https://github.com/user-attachments/assets/4edf592c-9b38-496c-af86-1e6c88e0d811)

### 4. لوحة المعلومات التفاعلية | Interactive Dashboard
![Interactive Dashboard](https://github.com/user-attachments/assets/631a782c-98bb-4d41-b0a6-b0b187470c28)

---

## ملاحظات التطوير | Development Notes

### التغييرات الرئيسية | Major Changes
1. استبدال جميع الألوان البنفسجية (#667eea, #764ba2) بالألوان الخضراء للجامعة
2. استبدال جميع الألوان الزرقاء (#0f3d68, #2e8bc0) بالألوان الخضراء للجامعة
3. توحيد الخط إلى Tajawal عبر جميع الصفحات
4. إنشاء ملف CSS موحد للاستخدام المستقبلي

### أدوات التحديث | Update Tools
- تم استخدام sed لتحديث الألوان بشكل جماعي
- تم التحقق يدوياً من جميع الصفحات المحدثة

---

## الدعم والصيانة | Support & Maintenance

للحصول على دعم أو للإبلاغ عن مشاكل في الهوية البصرية:
- افتح issue في مستودع GitHub
- تواصل مع فريق التطوير

---

**تاريخ آخر تحديث:** 2025-11-07  
**الإصدار:** 2.0  
**المطور:** نظام إدارة الإسكان الجامعي - جامعة الإمام محمد بن سعود الإسلامية
