from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
import os
from openai import OpenAI
from PIL import Image
import io
import base64
import json
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from database_api import get_all_residents, get_all_stickers, get_all_parking_spots, get_statistics, search_by_plate, save_processed_image, get_processed_images, search_processed_images, get_processed_images_statistics, get_violation_report, get_all_buildings

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = secrets.token_hex(32)  # مفتاح سري للجلسات

# تكوين OpenAI
client = OpenAI()

# مجلد لحفظ الصور المعالجة
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# قاعدة بيانات بسيطة في الذاكرة (للتجربة)
database = {
    'residents': [],
    'vehicles': [],
    'processed_images': []
}

# قاعدة بيانات المستخدمين (في الإنتاج، استخدم قاعدة بيانات حقيقية)
users_db = {
    'admin': {
        'password': generate_password_hash('Admin@2025'),
        'role': 'admin',
        'name': 'مدير النظام'
    }
}

# Decorator للتحقق من تسجيل الدخول
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'يجب تسجيل الدخول أولاً', 'redirect': '/login.html'}), 401
            return redirect('/login.html')
        return f(*args, **kwargs)
    return decorated_function

# Decorator للتحقق من صلاحيات المدير
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
        if session.get('role') != 'admin':
            return jsonify({'error': 'غير مصرح لك بالوصول'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # السماح بالوصول لصفحة تسجيل الدخول بدون مصادقة
    if path == 'login.html':
        return send_from_directory('static', path)
    # حماية باقي الصفحات
    if 'user_id' not in session:
        return redirect('/login.html')
    return send_from_directory('static', path)

@app.route('/api/login', methods=['POST'])
def login():
    """تسجيل الدخول"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)
        
        if not username or not password:
            return jsonify({'error': 'يرجى إدخال اسم المستخدم وكلمة المرور'}), 400
        
        # التحقق من المستخدم
        user = users_db.get(username)
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
        
        # إنشاء جلسة
        session['user_id'] = username
        session['role'] = user['role']
        session['name'] = user['name']
        
        if remember:
            session.permanent = True
        
        return jsonify({
            'success': True,
            'message': 'تم تسجيل الدخول بنجاح',
            'user': {
                'username': username,
                'name': user['name'],
                'role': user['role']
            },
            'redirect': '/index.html'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """تسجيل الخروج"""
    session.clear()
    return jsonify({'success': True, 'message': 'تم تسجيل الخروج بنجاح'})

@app.route('/api/current-user', methods=['GET'])
@login_required
def current_user():
    """الحصول على معلومات المستخدم الحالي"""
    return jsonify({
        'username': session.get('user_id'),
        'name': session.get('name'),
        'role': session.get('role')
    })

@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """الحصول على قائمة المستخدمين (للمدير فقط)"""
    users_list = []
    for username, user in users_db.items():
        users_list.append({
            'username': username,
            'name': user['name'],
            'role': user['role']
        })
    return jsonify(users_list)

@app.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    """إنشاء مستخدم جديد (للمدير فقط)"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        role = data.get('role', 'user')
        
        if not username or not password or not name:
            return jsonify({'error': 'جميع الحقول مطلوبة'}), 400
        
        if username in users_db:
            return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400
        
        users_db[username] = {
            'password': generate_password_hash(password),
            'name': name,
            'role': role
        }
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء المستخدم بنجاح',
            'user': {
                'username': username,
                'name': name,
                'role': role
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<username>', methods=['DELETE'])
@admin_required
def delete_user(username):
    """حذف مستخدم (للمدير فقط)"""
    try:
        if username == 'admin':
            return jsonify({'error': 'لا يمكن حذف المدير الرئيسي'}), 400
        
        if username not in users_db:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        del users_db[username]
        
        return jsonify({
            'success': True,
            'message': 'تم حذف المستخدم بنجاح'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract-plate', methods=['POST'])
def extract_plate():
    """استخراج رقم لوحة السيارة من الصورة"""
    try:
        img_str = None
        
        # دعم استقبال الصور بصيغتين: FormData أو base64
        if 'image' in request.files:
            # استقبال من FormData
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'لم يتم اختيار ملف'}), 400
            
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
        
        elif request.is_json:
            # استقبال من JSON (base64)
            data = request.json
            image_data = data.get('image')
            
            if not image_data:
                return jsonify({'error': 'لم يتم إرسال صورة'}), 400
            
            # إزالة البادئة من base64
            if ',' in image_data:
                img_str = image_data.split(',')[1]
            else:
                img_str = image_data
        
        else:
            return jsonify({'error': 'لم يتم إرفاق صورة'}), 400
        
        if not img_str:
            return jsonify({'error': 'فشل في معالجة الصورة'}), 400
        
        # استخدام GPT-4 Vision لاستخراج رقم اللوحة
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """أنت خبير في قراءة لوحات السيارات السعودية. حلل هذه الصورة بدقة عالية جداً واستخرج:

**مهم جداً:**
- اللوحات السعودية تحتوي على 3 أحرف إنجليزية + 4 أرقام
- الأحرف الإنجليزية تكون على اليمين والأرقام على اليسار
- اقرأ اللوحة بدقة تامة من الصورة الفعلية
- استخرج الأحرف بالإنجليزية مباشرة (مثل: ABC, XYZ)
- لا تخترع أرقام أو أحرف، اقرأ ما هو موجود فقط

استخرج:
1. الأحرف الإنجليزية الثلاثة (مثل: ABC, XYZ)
2. الأرقام الأربعة (مثل: 5687)
3. نوع السيارة (الماركة مثل: Toyota, Ford, Honda)
4. لون السيارة

أرجع JSON فقط:
{
    "plate_number": "ABC 5687" (الأحرف بالإنجليزية + الأرقام),
    "english_letters": "ABC" (الأحرف الإنجليزية فقط),
    "numbers": "5687" (الأرقام فقط),
    "vehicle_type": "نوع السيارة",
    "vehicle_color": "اللون",
    "confidence": رقم من 0-100
}

إذا لم تر اللوحة بوضوح، ضع confidence أقل من 50."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        # استخراج النتيجة
        result_text = response.choices[0].message.content.strip()
        
        # إزالة أي نص إضافي قبل أو بعد JSON
        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(result_text)
        
        # البحث في قاعدة البيانات عن اللوحة
        resident_info = None
        if result.get('plate_number') and result.get('confidence', 0) > 50:
            search_result = search_by_plate(result['plate_number'])
            if search_result.get('found'):
                resident_info = search_result
        
        # إضافة معلومات الساكن إلى النتيجة
        result['resident_info'] = resident_info
        
        # حفظ في قاعدة البيانات الفعلية
        try:
            save_processed_image(
                plate_number=result.get('plate_number', 'غير محدد'),
                vehicle_type=result.get('vehicle_type', 'غير محدد'),
                vehicle_color=result.get('vehicle_color', 'غير محدد'),
                confidence=result.get('confidence', 0),
                image_path='',  # يمكن إضافة حفظ الصورة لاحقاً
                notes=f"استخراج تلقائي - الأحرف: {result.get('english_letters', '')}, الأرقام: {result.get('numbers', '')}"
            )
        except Exception as db_error:
            print(f"تحذير: فشل حفظ الصورة في قاعدة البيانات: {db_error}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"خطأ في استخراج اللوحة: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-images', methods=['POST'])
def process_images():
    """معالجة صور متعددة واستخراج بيانات شاملة"""
    try:
        results = []
        images_data = []
        
        # دعم استقبال الصور بصيغتين: FormData أو JSON
        if 'images' in request.files:
            # استقبال من FormData
            files = request.files.getlist('images')
            for file in files:
                if file.filename == '':
                    continue
                image_bytes = file.read()
                image = Image.open(io.BytesIO(image_bytes))
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                images_data.append({'data': img_str, 'name': file.filename})
        
        elif request.is_json:
            # استقبال من JSON (base64)
            data = request.json
            images_list = data.get('images', [])
            for idx, image_data in enumerate(images_list):
                if ',' in image_data:
                    img_str = image_data.split(',')[1]
                else:
                    img_str = image_data
                images_data.append({'data': img_str, 'name': f'image_{idx+1}.png'})
        
        else:
            return jsonify({'error': 'لم يتم إرفاق صور'}), 400
        
        if not images_data:
            return jsonify({'error': 'لم يتم رفع أي صور'}), 400
        
        # معالجة كل صورة
        for img_info in images_data:
            img_str = img_info['data']
            filename = img_info['name']
            
            # استخدام GPT-4 Vision لتحليل الصورة
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """حلل هذه الصورة بدقة واستخرج جميع البيانات.

أرجع النتيجة بصيغة JSON فقط بدون أي نص إضافي:
{
    "category": "نوع الصورة: موقف عادي / موقف معاقين / مخالفة / أخرى",
    "plate_number": "رقم اللوحة إن وجد",
    "vehicle_color": "لون السيارة",
    "vehicle_type": "نوع السيارة",
    "confidence": رقم من 0 إلى 100
}

إذا لم تتمكن من استخراج معلومة، ضع "غير محدد"."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_str}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            # استخراج النتيجة
            result_text = response.choices[0].message.content.strip()
            
            # إزالة أي نص إضافي
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(result_text)
            result['filename'] = filename
            
            # البحث في قاعدة البيانات
            if result.get('plate_number') and result.get('confidence', 0) > 50:
                search_result = search_by_plate(result['plate_number'])
                if search_result.get('found'):
                    result['resident_info'] = search_result
            
            results.append(result)
        
        # حفظ في قاعدة البيانات
        database['processed_images'].extend(results)
        
        return jsonify({'results': results, 'total': len(results)})
        
    except Exception as e:
        print(f"خطأ في معالجة الصور: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/processed-images-stats', methods=['GET'])
def get_processed_stats():
    """الحصول على إحصائيات الصور المعالجة"""
    total = len(database['processed_images'])
    return jsonify({
        'success': True,
        'data': {
            'total_images': total
        }
    })

@app.route('/api/residents', methods=['GET'])
def api_get_residents():
    """الحصول على جميع السكان"""
    try:
        residents = get_all_residents()
        return jsonify({'success': True, 'data': residents})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stickers', methods=['GET'])
def api_get_stickers():
    """الحصول على جميع ملصقات السيارات"""
    try:
        stickers = get_all_stickers()
        return jsonify({'success': True, 'data': stickers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/parking', methods=['GET'])
def api_get_parking():
    """الحصول على جميع المواقف"""
    try:
        spots = get_all_parking_spots()
        return jsonify({'success': True, 'data': spots})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def api_get_statistics():
    """الحصول على الإحصائيات العامة"""
    try:
        stats = get_statistics()
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search-plate', methods=['POST'])
def api_search_plate():
    """البحث عن مركبة برقم اللوحة"""
    try:
        data = request.json
        plate_number = data.get('plateNumber', '')
        result = search_by_plate(plate_number)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save-processed-image', methods=['POST'])
def api_save_processed_image():
    """حفظ صورة معالجة في قاعدة البيانات"""
    try:
        data = request.json
        result = save_processed_image(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-processed-images', methods=['GET'])
def api_get_processed_images():
    """الحصول على الصور المعالجة"""
    try:
        limit = request.args.get('limit', 100, type=int)
        category = request.args.get('category', 'all')
        images = get_processed_images(limit, category)
        return jsonify({'success': True, 'data': images})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search-processed-images', methods=['POST'])
def api_search_processed_images():
    """البحث في الصور المعالجة برقم اللوحة"""
    try:
        data = request.json
        plate_number = data.get('plateNumber', '')
        results = search_processed_images(plate_number)
        return jsonify({'success': True, 'data': results, 'count': len(results)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/processed-images-statistics', methods=['GET'])
def api_processed_images_statistics():
    """الحصول على إحصائيات الصور المعالجة"""
    try:
        stats = get_processed_images_statistics()
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/violation-report', methods=['GET'])
def api_violation_report():
    """الحصول على تقرير المخالفات مع عدد التكرار"""
    try:
        report = get_violation_report()
        return jsonify({'success': True, 'data': report})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buildings', methods=['GET'])
def get_buildings():
    try:
        buildings = get_all_buildings()
        return jsonify({'success': True, 'data': buildings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# إضافة headers لمنع الـ cache
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/api/classify_parking', methods=['POST'])
def classify_parking():
    """تصنيف صورة الموقف باستخدام GPT-4 Vision"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'لم يتم إرسال صورة'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'لم يتم اختيار ملف'}), 400
        
        # قراءة الصورة وتحويلها إلى base64
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # تصغير الصورة إذا كانت كبيرة جداً
        max_size = (1024, 1024)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # تحويل إلى base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # استخدام GPT-4 Vision لتصنيف الصورة
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """أنت نظام ذكاء اصطناعي متخصص في تصنيف صور مواقف السيارات.
                    
قم بتحليل الصورة وتصنيفها إلى أحد الأنواع التالية:
- normal: موقف سيارات عادي
- disabled: موقف معاقين/احتياجات خاصة (يحتوي على رمز الكرسي المتحرك أو علامة معاقين)
- private: موقف خاص (يحتوي على لافتة "خاص" أو "Private" أو اسم شخص/شركة)
- basement: موقف قبو/تحت الأرض (يظهر أنه في قبو أو موقف سفلي)
- license: صورة ترخيص أو تصريح (ورقة رسمية)
- qr: صورة تحتوي على QR Code
- violation: صورة مخالفة (سيارة متوقفة بشكل خاطئ أو في مكان ممنوع)
- other: أي شيء آخر

أرجع النتيجة بصيغة JSON فقط بدون أي نص إضافي:
{
    "category": "نوع التصنيف",
    "confidence": رقم من 0 إلى 100,
    "reason": "سبب التصنيف بالعربية"
}"""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "صنف هذه الصورة"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        # استخراج النتيجة
        result_text = response.choices[0].message.content.strip()
        
        # تنظيف النص وإزالة markdown code blocks
        if result_text.startswith('```'):
            result_text = result_text.split('```')[1]
            if result_text.startswith('json'):
                result_text = result_text[4:]
        result_text = result_text.strip()
        
        result = json.loads(result_text)
        
        return jsonify({
            'success': True,
            'category': result.get('category', 'other'),
            'confidence': result.get('confidence', 0),
            'reason': result.get('reason', ''),
            'details': result
        })
        
    except json.JSONDecodeError as e:
        print(f"خطأ في تحليل JSON: {e}")
        print(f"النص المستلم: {result_text}")
        return jsonify({
            'success': False,
            'category': 'other',
            'confidence': 0,
            'error': 'خطأ في تحليل النتيجة'
        })
    except Exception as e:
        print(f"خطأ في تصنيف الصورة: {str(e)}")
        return jsonify({
            'success': False,
            'category': 'other',
            'confidence': 0,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
