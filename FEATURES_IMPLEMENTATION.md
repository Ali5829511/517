# دليل إضافة الميزات الجديدة والأمان

## 📋 الميزات المطلوبة

### 1. نظام تسجيل دخول آمن
### 2. فرز تلقائي للصور حسب الدقة
### 3. خيار حذف الصور بعد المعالجة
### 4. فرز الصور حسب نوع الموقف

---

## 🔐 الجزء الأول: نظام تسجيل الدخول الآمن

### الخطوة 1: تحديث requirements.txt

أضف المكتبات التالية:

```txt
Flask-Login==0.6.3
Flask-WTF==1.2.1
bcrypt==4.1.2
python-dotenv==1.0.1
```

### الخطوة 2: إنشاء جدول المستخدمين في قاعدة البيانات

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    ip_address TEXT,
    success BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### الخطوة 3: إنشاء ملف auth.py

```python
# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('housing_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Check login attempts
def check_login_attempts(username, ip_address):
    conn = get_db_connection()
    # Check last 5 attempts in last 15 minutes
    fifteen_min_ago = datetime.now() - timedelta(minutes=15)
    attempts = conn.execute('''
        SELECT COUNT(*) as count FROM login_attempts 
        WHERE username = ? AND ip_address = ? 
        AND timestamp > ? AND success = 0
    ''', (username, ip_address, fifteen_min_ago)).fetchone()
    conn.close()
    return attempts['count'] < 5

# Log login attempt
def log_login_attempt(username, ip_address, success):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO login_attempts (username, ip_address, success)
        VALUES (?, ?, ?)
    ''', (username, ip_address, success))
    conn.commit()
    conn.close()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip_address = request.remote_addr
        
        # Check login attempts
        if not check_login_attempts(username, ip_address):
            flash('تم تجاوز عدد محاولات تسجيل الدخول. يرجى المحاولة بعد 15 دقيقة', 'danger')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', 
                           (username,)).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            # Successful login
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session.permanent = True
            
            # Update last login
            conn.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                        (datetime.now(), user['id']))
            conn.commit()
            
            log_login_attempt(username, ip_address, True)
            flash('تم تسجيل الدخول بنجاح', 'success')
            conn.close()
            return redirect(url_for('index'))
        else:
            # Failed login
            log_login_attempt(username, ip_address, False)
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            conn.close()
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('كلمات المرور غير متطابقة', 'danger')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('يجب أن تكون كلمة المرور 8 أحرف على الأقل', 'danger')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, 'user'))
            conn.commit()
            flash('تم إنشاء الحساب بنجاح. يمكنك تسجيل الدخول الآن', 'success')
            conn.close()
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل', 'danger')
            conn.close()
    
    return render_template('register.html')
```

### الخطوة 4: تحديث app.py

أضف في بداية الملف:

```python
from auth import auth_bp, login_required
from datetime import timedelta

# إعدادات الأمان
app.secret_key = 'your-very-secret-key-change-this-in-production'  # غيّر هذا في الإنتاج
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# تسجيل Blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
```

ثم أضف `@login_required` فوق كل route تريد حمايته:

```python
@app.route('/')
@login_required
def index():
    return render_template('index.html')
```

### الخطوة 5: إنشاء صفحة تسجيل الدخول (login.html)

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول - نظام إدارة الإسكان</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            direction: rtl;
        }
        
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header i {
            font-size: 60px;
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .login-header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .login-header p {
            color: #666;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn-login {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .btn-login:hover {
            transform: translateY(-2px);
        }
        
        .alert {
            padding: 12px 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .alert-danger {
            background: #fee;
            color: #c33;
            border: 1px solid #fcc;
        }
        
        .alert-success {
            background: #efe;
            color: #3c3;
            border: 1px solid #cfc;
        }
        
        .register-link {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
        
        .register-link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <i class="fas fa-user-shield"></i>
            <h1>تسجيل الدخول</h1>
            <p>نظام إدارة الإسكان الجامعي</p>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST" action="{{ url_for('auth.login') }}">
            <div class="form-group">
                <label for="username">اسم المستخدم</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">كلمة المرور</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="btn-login">
                <i class="fas fa-sign-in-alt"></i> تسجيل الدخول
            </button>
        </form>
        
        <div class="register-link">
            ليس لديك حساب؟ <a href="{{ url_for('auth.register') }}">إنشاء حساب جديد</a>
        </div>
    </div>
</body>
</html>
```

### الخطوة 6: إنشاء مستخدم افتراضي

```python
# create_admin.py
import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('housing_database.db')

# Create tables
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    ip_address TEXT,
    success BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create admin user
admin_password = generate_password_hash('Admin@2025')
conn.execute('''
    INSERT OR IGNORE INTO users (username, email, password_hash, role)
    VALUES (?, ?, ?, ?)
''', ('admin', 'admin@imamu.edu.sa', admin_password, 'admin'))

conn.commit()
conn.close()

print("✅ تم إنشاء المستخدم الافتراضي:")
print("اسم المستخدم: admin")
print("كلمة المرور: Admin@2025")
print("⚠️ يرجى تغيير كلمة المرور بعد أول تسجيل دخول!")
```

---

## 📸 الجزء الثاني: ميزات فرز الصور

### تحديث comprehensive_image_processing.html

أضف في قسم JavaScript:

```javascript
// إعدادات الفرز
let autoSortEnabled = true;
let deleteAfterProcess = false;
const CONFIDENCE_THRESHOLD = 80;

// إضافة عناصر التحكم في الواجهة
function addSortingControls() {
    const controlsHTML = `
        <div class="sorting-controls" style="margin: 20px 0; padding: 20px; background: #f5f5f5; border-radius: 10px;">
            <h3 style="margin-bottom: 15px;">
                <i class="fas fa-cog"></i> إعدادات الفرز والمعالجة
            </h3>
            
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input type="checkbox" id="autoSortCheckbox" checked onchange="toggleAutoSort(this)">
                    <span>فرز تلقائي حسب الدقة (>80% تلقائي، <80% يدوي)</span>
                </label>
                
                <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                    <input type="checkbox" id="deleteAfterCheckbox" onchange="toggleDeleteAfter(this)">
                    <span>حذف الصور بعد المعالجة</span>
                </label>
                
                <button onclick="sortImagesByCategory()" style="padding: 10px 20px; background: #5A8CA3; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    <i class="fas fa-sort"></i> فرز حسب نوع الموقف
                </button>
            </div>
            
            <div id="sortingStats" style="margin-top: 15px; display: none;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
                    <div class="stat-box">
                        <div class="stat-number" id="highConfidenceCount">0</div>
                        <div class="stat-label">دقة عالية (تلقائي)</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number" id="lowConfidenceCount">0</div>
                        <div class="stat-label">دقة منخفضة (يدوي)</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Insert after upload section
    const uploadSection = document.querySelector('.upload-section');
    uploadSection.insertAdjacentHTML('afterend', controlsHTML);
}

function toggleAutoSort(checkbox) {
    autoSortEnabled = checkbox.checked;
    console.log('Auto sort:', autoSortEnabled);
}

function toggleDeleteAfter(checkbox) {
    deleteAfterProcess = checkbox.checked;
    if (deleteAfterProcess) {
        if (!confirm('هل أنت متأكد من حذف الصور بعد المعالجة؟ لا يمكن التراجع عن هذا الإجراء.')) {
            checkbox.checked = false;
            deleteAfterProcess = false;
        }
    }
}

// تحديث دالة processImages لتطبيق الفرز التلقائي
async function processImages() {
    // ... الكود الموجود ...
    
    // بعد معالجة جميع الصور
    if (autoSortEnabled) {
        applySorting();
    }
    
    if (deleteAfterProcess) {
        deleteProcessedImages();
    }
}

function applySorting() {
    const highConfidence = processedResults.filter(r => r.confidence >= CONFIDENCE_THRESHOLD);
    const lowConfidence = processedResults.filter(r => r.confidence < CONFIDENCE_THRESHOLD);
    
    document.getElementById('highConfidenceCount').textContent = highConfidence.length;
    document.getElementById('lowConfidenceCount').textContent = lowConfidence.length;
    document.getElementById('sortingStats').style.display = 'block';
    
    console.log(`✅ تم الفرز: ${highConfidence.length} دقة عالية، ${lowConfidence.length} يدوي`);
}

function sortImagesByCategory() {
    const categories = {
        'normal': [],
        'disabled': [],
        'violation': [],
        'old_buildings': [],
        'new_buildings': [],
        'villas': [],
        'impounded': [],
        'tow_truck': [],
        'other': []
    };
    
    processedResults.forEach(result => {
        const category = result.category || 'other';
        if (categories[category]) {
            categories[category].push(result);
        }
    });
    
    console.log('📊 تم الفرز حسب الفئة:', categories);
    
    // عرض النتائج
    let message = 'نتائج الفرز:\n\n';
    for (const [category, items] of Object.entries(categories)) {
        if (items.length > 0) {
            message += `${getCategoryText(category)}: ${items.length}\n`;
        }
    }
    
    alert(message);
}

function deleteProcessedImages() {
    // حذف الصور من الذاكرة
    selectedFiles = [];
    processedResults = [];
    
    // مسح العرض
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('resultsGrid').innerHTML = '';
    
    // إعادة تعيين input
    document.getElementById('imageInput').value = '';
    
    console.log('🗑️ تم حذف جميع الصور المعالجة');
    alert('تم حذف جميع الصور المعالجة');
}

// استدعاء عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    addSortingControls();
});
```

---

## 🚀 الجزء الثالث: النشر على Render.com

### الخطوات:

1. **رفع الكود إلى GitHub**
```bash
git add .
git commit -m "Add authentication and image sorting features"
git push origin main
```

2. **إنشاء Web Service على Render.com**
- Name: `housing-management-system`
- Language: **Python 3**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Instance Type: **Starter** ($7/month) للأمان والأداء

3. **إضافة Environment Variables**
```
SECRET_KEY=your-very-secret-random-key-here
FLASK_ENV=production
```

4. **Deploy**

---

## ✅ قائمة التحقق النهائية

- [ ] تم إضافة نظام تسجيل الدخول
- [ ] تم اختبار تسجيل الدخول محلياً
- [ ] تم إضافة ميزات فرز الصور
- [ ] تم اختبار فرز الصور محلياً
- [ ] تم رفع الكود إلى GitHub
- [ ] تم النشر على Render.com
- [ ] تم اختبار النظام المنشور
- [ ] تم تغيير كلمة المرور الافتراضية

---

**تم إعداد هذا الدليل بواسطة Manus AI**

