from flask import Flask, request, jsonify, send_from_directory, session, redirect
import os
import logging
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64
import json
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from database_api import (
    get_all_residents,
    get_all_stickers,
    get_all_parking_spots,
    get_statistics,
    search_by_plate,
    save_processed_image,
    get_processed_images,
    search_processed_images,
    get_processed_images_statistics,
    get_violation_report,
    get_all_buildings,
    get_db_connection,
    get_comprehensive_statistics,
    # وظائف السيارات والمخالفات الجديدة
    get_all_vehicles,
    add_vehicle,
    update_vehicle,
    search_vehicle_by_plate,
    get_all_violations,
    add_violation,
    update_violation_status,
    get_violations_by_plate,
    log_takamul_sync,
    get_takamul_sync_history,
    log_plate_recognizer_analysis,
    get_plate_recognizer_logs,
    get_vehicles_statistics,
    get_violations_statistics,
)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client safely
try:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        OPENAI_AVAILABLE = True
        logger.info("OpenAI client initialized successfully")
    else:
        client = None
        OPENAI_AVAILABLE = False
        logger.warning("OPENAI_API_KEY not found in environment variables")
except ImportError:
    OPENAI_AVAILABLE = False
    client = None
    logger.warning("OpenAI library not installed")
except Exception as e:
    OPENAI_AVAILABLE = False
    client = None
    logger.error(f"Failed to initialize OpenAI client: {e}")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = secrets.token_hex(32)  # مفتاح سري للجلسات

# Secure session cookie configuration
# SESSION_COOKIE_SECURE is only enabled in production to allow HTTP in development
app.config["SESSION_COOKIE_SECURE"] = os.getenv("FLASK_ENV") == "production"
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JavaScript access to session cookie
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # CSRF protection

# تكوين التطبيق

# مجلد لحفظ الصور المعالجة
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# قاعدة بيانات بسيطة في الذاكرة (للتجربة)
database = {"residents": [], "vehicles": [], "processed_images": []}

# قاعدة بيانات المستخدمين (في الإنتاج، استخدم قاعدة بيانات حقيقية)
users_db = {
    "admin": {
        "password": generate_password_hash("Admin@2025"),
        "role": "admin",
        "name": "مدير النظام",
        "email": "aliayashi517@gmail.com",
    }
}

# جدول رموز إعادة تعيين كلمة المرور
reset_tokens = {}


# Decorator للتحقق من تسجيل الدخول
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "يجب تسجيل الدخول أولاً", "redirect": "/login.html"}), 401
            return redirect("/login.html")
        return f(*args, **kwargs)

    return decorated_function


# Decorator للتحقق من صلاحيات المدير
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "يجب تسجيل الدخول أولاً"}), 401
        if session.get("role") != "admin":
            return jsonify({"error": "غير مصرح لك بالوصول"}), 403
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    return send_from_directory("static", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    # السماح بالوصول لصفحة تسجيل الدخول بدون مصادقة
    if path == "login.html":
        return send_from_directory("static", path)
    # حماية باقي الصفحات
    if "user_id" not in session:
        return redirect("/login.html")
    return send_from_directory("static", path)


@app.route("/api/login", methods=["POST"])
def login():
    """تسجيل الدخول"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        remember = data.get("remember", False)

        if not username or not password:
            return jsonify({"error": "يرجى إدخال اسم المستخدم وكلمة المرور"}), 400

        # التحقق من المستخدم
        user = users_db.get(username)
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "اسم المستخدم أو كلمة المرور غير صحيحة"}), 401

        # إنشاء جلسة
        session["user_id"] = username
        session["role"] = user["role"]
        session["name"] = user["name"]

        if remember:
            session.permanent = True

        return jsonify(
            {
                "success": True,
                "message": "تم تسجيل الدخول بنجاح",
                "user": {"username": username, "name": user["name"], "role": user["role"]},
                "redirect": "/index.html",
            }
        )

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "حدث خطأ أثناء تسجيل الدخول"}), 500


@app.route("/api/logout", methods=["POST"])
def logout():
    """تسجيل الخروج"""
    session.clear()
    return jsonify({"success": True, "message": "تم تسجيل الخروج بنجاح"})


@app.route("/api/current-user", methods=["GET"])
@login_required
def current_user():
    """الحصول على معلومات المستخدم الحالي"""
    return jsonify(
        {
            "username": session.get("user_id"),
            "name": session.get("name"),
            "role": session.get("role"),
        }
    )


@app.route("/api/users", methods=["GET"])
@admin_required
def get_users():
    """الحصول على قائمة المستخدمين (للمدير فقط)"""
    users_list = []
    for username, user in users_db.items():
        users_list.append({"username": username, "name": user["name"], "role": user["role"]})
    return jsonify(users_list)


@app.route("/api/users", methods=["POST"])
@admin_required
def create_user():
    """إنشاء مستخدم جديد (للمدير فقط)"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        role = data.get("role", "user")

        if not username or not password or not name:
            return jsonify({"error": "جميع الحقول مطلوبة"}), 400

        if username in users_db:
            return jsonify({"error": "اسم المستخدم موجود بالفعل"}), 400

        users_db[username] = {
            "password": generate_password_hash(password),
            "name": name,
            "role": role,
        }

        return jsonify(
            {
                "success": True,
                "message": "تم إنشاء المستخدم بنجاح",
                "user": {"username": username, "name": name, "role": role},
            }
        )

    except Exception as e:
        logger.error(f"Create user error: {e}")
        return jsonify({"error": "حدث خطأ أثناء إنشاء المستخدم"}), 500


@app.route("/api/users/<username>", methods=["DELETE"])
@admin_required
def delete_user(username):
    """حذف مستخدم (للمدير فقط)"""
    try:
        if username == "admin":
            return jsonify({"error": "لا يمكن حذف المدير الرئيسي"}), 400

        if username not in users_db:
            return jsonify({"error": "المستخدم غير موجود"}), 404

        del users_db[username]

        return jsonify({"success": True, "message": "تم حذف المستخدم بنجاح"})

    except Exception as e:
        logger.error(f"Delete user error: {e}")
        return jsonify({"error": "حدث خطأ أثناء حذف المستخدم"}), 500


@app.route("/api/extract-plate", methods=["POST"])
def extract_plate():
    """استخراج رقم لوحة السيارة من الصورة"""
    try:
        img_str = None
        saved_filepath = None

        # دعم استقبال الصور بصيغتين: FormData أو base64
        if "image" in request.files:
            # استقبال من FormData
            file = request.files["image"]
            if file.filename == "":
                return jsonify({"error": "لم يتم اختيار ملف"}), 400

            # حفظ الملف بشكل آمن
            filename = secure_filename(file.filename)
            saved_filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(saved_filepath)

            # قراءة الصورة من المسار المحفوظ
            image = Image.open(saved_filepath)

            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

        elif request.is_json:
            # استقبال من JSON (base64)
            data = request.json
            image_data = data.get("image")

            if not image_data:
                return jsonify({"error": "لم يتم إرسال صورة"}), 400

            # إزالة البادئة من base64
            if "," in image_data:
                img_str = image_data.split(",")[1]
            else:
                img_str = image_data

        else:
            return jsonify({"error": "لم يتم إرفاق صورة"}), 400

        if not img_str:
            return jsonify({"error": "فشل في معالجة الصورة"}), 400

        # محاولة استخدام OpenAI أولاً، ثم OCR كبديل
        result = None

        if OPENAI_AVAILABLE and client:
            try:
                # استخدام GPT-4 Vision لاستخراج رقم اللوحة
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        "أنت خبير في قراءة لوحات السيارات السعودية. "
                                        "حلل هذه الصورة بدقة عالية جداً واستخرج:"
                                    )
                                    + """

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

إذا لم تر اللوحة بوضوح، ضع confidence أقل من 50.""",
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{img_str}"},
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )

                # استخراج النتيجة
                result_text = response.choices[0].message.content.strip()

                # إزالة أي نص إضافي قبل أو بعد JSON
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()

                result = json.loads(result_text)

                # البحث في قاعدة البيانات عن اللوحة
                resident_info = None
                if result.get("plate_number") and result.get("confidence", 0) > 50:
                    search_result = search_by_plate(result["plate_number"])
                    if search_result.get("found"):
                        resident_info = search_result

                # إضافة معلومات الساكن إلى النتيجة
                result["resident_info"] = resident_info

                # حفظ في قاعدة البيانات الفعلية
                try:
                    save_processed_image(
                        plate_number=result.get("plate_number", "غير محدد"),
                        vehicle_type=result.get("vehicle_type", "غير محدد"),
                        vehicle_color=result.get("vehicle_color", "غير محدد"),
                        confidence=result.get("confidence", 0),
                        image_path=saved_filepath if saved_filepath else "",
                        notes=(
                            f"استخراج تلقائي - الأحرف: "
                            f"{result.get('english_letters', '')}, "
                            f"الأرقام: {result.get('numbers', '')}"
                        ),
                    )
                except Exception as db_error:
                    logger.warning(f"فشل حفظ الصورة في قاعدة البيانات: {db_error}")

                return jsonify(result)

            except Exception as openai_error:
                logger.error(f"خطأ في OpenAI: {openai_error}")
                result = None

        # إذا فشل OpenAI أو لم يكن متوفراً، استخدم OCR المحلي
        if result is None:
            try:
                # تحويل base64 إلى صورة
                img_data = base64.b64decode(img_str)
                img = Image.open(io.BytesIO(img_data))

                # محاولة استخدام pytesseract
                try:
                    import pytesseract

                    text = pytesseract.image_to_string(img, lang="eng+ara")

                    # استخراج الأرقام والأحرف من النص
                    import re

                    numbers = re.findall(r"\d+", text)
                    letters = re.findall(r"[A-Z]{3}", text)

                    letter_part = letters[0] if letters else ""
                    number_part = numbers[0] if numbers else ""
                    result = {
                        "plate_number": f"{letter_part} {number_part}".strip(),
                        "english_letters": letter_part,
                        "numbers": number_part,
                        "vehicle_type": "غير محدد",
                        "vehicle_color": "غير محدد",
                        "confidence": 30,  # ثقة منخفضة للـ OCR المحلي
                    }
                except ImportError:
                    # إذا لم يكن pytesseract متوفراً
                    result = {
                        "error": "خدمة استخراج اللوحات غير متوفرة حالياً",
                        "plate_number": "غير محدد",
                        "confidence": 0,
                    }
            except Exception as ocr_error:
                logger.error(f"خطأ في OCR المحلي: {ocr_error}")
                result = {
                    "error": "فشل في معالجة الصورة",
                    "plate_number": "غير محدد",
                    "confidence": 0,
                }

        return jsonify(result)

    except Exception as e:
        logger.error(f"خطأ في استخراج اللوحة: {e}")
        return jsonify({"error": "حدث خطأ أثناء معالجة الصورة"}), 500


@app.route("/api/process-images", methods=["POST"])
def process_images():
    """معالجة صور متعددة واستخراج بيانات شاملة"""
    try:
        results = []
        images_data = []

        # دعم استقبال الصور بصيغتين: FormData أو JSON
        if "images" in request.files:
            # استقبال من FormData
            files = request.files.getlist("images")
            for file in files:
                if file.filename == "":
                    continue

                # حفظ الملف بشكل آمن
                filename = secure_filename(file.filename)
                saved_filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(saved_filepath)

                # قراءة الصورة من المسار المحفوظ
                image = Image.open(saved_filepath)
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                images_data.append({"data": img_str, "name": filename, "path": saved_filepath})

        elif request.is_json:
            # استقبال من JSON (base64)
            data = request.json
            images_list = data.get("images", [])
            for idx, image_data in enumerate(images_list):
                if "," in image_data:
                    img_str = image_data.split(",")[1]
                else:
                    img_str = image_data
                images_data.append({"data": img_str, "name": f"image_{idx + 1}.png", "path": ""})

        else:
            return jsonify({"error": "لم يتم إرفاق صور"}), 400

        if not images_data:
            return jsonify({"error": "لم يتم رفع أي صور"}), 400

        # التحقق من توفر OpenAI
        if not OPENAI_AVAILABLE or not client:
            return jsonify({"error": "خدمة معالجة الصور غير متوفرة حالياً"}), 503

        # معالجة كل صورة
        for img_info in images_data:
            img_str = img_info["data"]
            filename = img_info["name"]
            filepath = img_info.get("path", "")

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

إذا لم تتمكن من استخراج معلومة، ضع "غير محدد".""",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{img_str}"},
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )

            # استخراج النتيجة
            result_text = response.choices[0].message.content.strip()

            # إزالة أي نص إضافي
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            result = json.loads(result_text)
            result["filename"] = filename

            # البحث في قاعدة البيانات
            if result.get("plate_number") and result.get("confidence", 0) > 50:
                search_result = search_by_plate(result["plate_number"])
                if search_result.get("found"):
                    result["resident_info"] = search_result

            # حفظ في قاعدة البيانات الفعلية مع مسار الصورة
            try:
                save_processed_image(
                    plate_number=result.get("plate_number", "غير محدد"),
                    vehicle_type=result.get("vehicle_type", "غير محدد"),
                    vehicle_color=result.get("vehicle_color", "غير محدد"),
                    confidence=result.get("confidence", 0),
                    image_path=filepath,
                    notes=f"معالجة تلقائية - التصنيف: {result.get('category', 'غير محدد')}",
                )
            except Exception as db_error:
                logger.warning(f"فشل حفظ الصورة في قاعدة البيانات: {db_error}")

            results.append(result)

        # حفظ في قاعدة البيانات
        database["processed_images"].extend(results)

        return jsonify({"results": results, "total": len(results)})

    except Exception as e:
        logger.error(f"خطأ في معالجة الصور: {e}")
        return jsonify({"error": "حدث خطأ أثناء معالجة الصور"}), 500


@app.route("/api/processed-images-stats", methods=["GET"])
def get_processed_stats():
    """الحصول على إحصائيات الصور المعالجة"""
    total = len(database["processed_images"])
    return jsonify({"success": True, "data": {"total_images": total}})


@app.route("/api/residents", methods=["GET"])
def api_get_residents():
    """الحصول على جميع السكان"""
    try:
        residents = get_all_residents()
        return jsonify({"success": True, "data": residents})
    except Exception as e:
        logger.error(f"Error getting residents: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب بيانات السكان"}), 500


@app.route("/api/stickers", methods=["GET"])
def api_get_stickers():
    """الحصول على جميع ملصقات السيارات"""
    try:
        stickers = get_all_stickers()
        return jsonify({"success": True, "data": stickers})
    except Exception as e:
        logger.error(f"Error getting stickers: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب بيانات الملصقات"}), 500


@app.route("/api/parking", methods=["GET"])
def api_get_parking():
    """الحصول على جميع المواقف"""
    try:
        spots = get_all_parking_spots()
        return jsonify({"success": True, "data": spots})
    except Exception as e:
        logger.error(f"Error getting parking spots: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب بيانات المواقف"}), 500


@app.route("/api/statistics", methods=["GET"])
def api_get_statistics():
    """الحصول على الإحصائيات العامة"""
    try:
        stats = get_statistics()
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب الإحصائيات"}), 500


@app.route("/api/comprehensive-statistics", methods=["GET"])
def api_comprehensive_statistics():
    """الحصول على الإحصائيات الشاملة مع التفاصيل الكاملة"""
    try:
        stats = get_comprehensive_statistics()
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        logger.error(f"Error getting comprehensive statistics: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب الإحصائيات الشاملة"}), 500


@app.route("/api/search-plate", methods=["POST"])
def api_search_plate():
    """البحث عن مركبة برقم اللوحة"""
    try:
        data = request.json
        plate_number = data.get("plateNumber", "")
        result = search_by_plate(plate_number)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Error searching plate: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء البحث عن اللوحة"}), 500


@app.route("/api/save-processed-image", methods=["POST"])
def api_save_processed_image():
    """حفظ صورة معالجة في قاعدة البيانات"""
    try:
        data = request.json
        result = save_processed_image(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error saving processed image: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء حفظ الصورة المعالجة"}), 500


@app.route("/api/get-processed-images", methods=["GET"])
def api_get_processed_images():
    """الحصول على الصور المعالجة"""
    try:
        limit = request.args.get("limit", 100, type=int)
        category = request.args.get("category", "all")
        images = get_processed_images(limit, category)
        return jsonify({"success": True, "data": images})
    except Exception as e:
        logger.error(f"Error getting processed images: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب الصور المعالجة"}), 500


@app.route("/api/search-processed-images", methods=["POST"])
def api_search_processed_images():
    """البحث في الصور المعالجة برقم اللوحة"""
    try:
        data = request.json
        plate_number = data.get("plateNumber", "")
        results = search_processed_images(plate_number)
        return jsonify({"success": True, "data": results, "count": len(results)})
    except Exception as e:
        logger.error(f"Error searching processed images: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء البحث في الصور"}), 500


@app.route("/api/processed-images-statistics", methods=["GET"])
def api_processed_images_statistics():
    """الحصول على إحصائيات الصور المعالجة"""
    try:
        stats = get_processed_images_statistics()
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        logger.error(f"Error getting processed images statistics: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب إحصائيات الصور"}), 500


@app.route("/api/violation-report", methods=["GET"])
def api_violation_report():
    """الحصول على تقرير المخالفات مع عدد التكرار"""
    try:
        report = get_violation_report()
        return jsonify({"success": True, "data": report})
    except Exception as e:
        logger.error(f"Error getting violation report: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب تقرير المخالفات"}), 500


@app.route("/api/buildings", methods=["GET"])
def get_buildings():
    try:
        buildings = get_all_buildings()
        return jsonify({"success": True, "data": buildings})
    except Exception as e:
        logger.error(f"Error getting buildings: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب بيانات المباني"}), 500


@app.route("/api/residents/<int:resident_id>/vehicles", methods=["GET"])
def api_get_resident_vehicles(resident_id):
    """إرجاع جميع الملصقات/المركبات المرتبطة بالساكن المحدد"""
    try:
        # استيراد محلي لتجنب الاعتماد المتداخل أثناء الاستيراد
        from database_api import get_stickers_by_resident

        stickers = get_stickers_by_resident(resident_id)
        return jsonify({"success": True, "data": stickers})
    except Exception as e:
        logger.error(f"Error getting resident vehicles: {e}")
        return jsonify({"success": False, "error": "حدث خطأ أثناء جلب بيانات مركبات الساكن"}), 500


# إضافة headers لمنع الـ cache
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


@app.route("/api/classify_parking", methods=["POST"])
def classify_parking():
    """تصنيف صورة الموقف باستخدام GPT-4 Vision"""
    try:
        if "image" not in request.files:
            return jsonify({"error": "لم يتم إرسال صورة"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "لم يتم اختيار ملف"}), 400

        # حفظ الملف بشكل آمن
        filename = secure_filename(file.filename)
        saved_filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(saved_filepath)

        # قراءة الصورة من المسار المحفوظ
        image = Image.open(saved_filepath)

        # تصغير الصورة إذا كانت كبيرة جداً
        max_size = (1024, 1024)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # تحويل إلى base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # التحقق من توفر OpenAI
        if not OPENAI_AVAILABLE or not client:
            return jsonify({"error": "خدمة تصنيف الصور غير متوفرة حالياً"}), 503

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
}""",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "صنف هذه الصورة"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_str}"},
                        },
                    ],
                },
            ],
            max_tokens=300,
        )

        # استخراج النتيجة
        result_text = response.choices[0].message.content.strip()

        # تنظيف النص وإزالة markdown code blocks
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        result_text = result_text.strip()

        result = json.loads(result_text)

        return jsonify(
            {
                "success": True,
                "category": result.get("category", "other"),
                "confidence": result.get("confidence", 0),
                "reason": result.get("reason", ""),
                "details": result,
            }
        )

    except json.JSONDecodeError as e:
        logger.error(f"خطأ في تحليل JSON: {e}")
        logger.error(f"النص المستلم: {result_text}")
        return jsonify(
            {
                "success": False,
                "category": "other",
                "confidence": 0,
                "error": "خطأ في تحليل النتيجة",
            }
        )
    except Exception as e:
        logger.error(f"خطأ في تصنيف الصورة: {str(e)}")
        return (
            jsonify(
                {
                    "success": False,
                    "category": "other",
                    "confidence": 0,
                    "error": "حدث خطأ أثناء تصنيف الصورة",
                }
            ),
            500,
        )


# دالة إرسال البريد الإلكتروني
def send_reset_email(email, token, username):
    """إرسال بريد إلكتروني لإعادة تعيين كلمة المرور"""
    try:
        # إعدادات Gmail
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "aliayashi517@gmail.com"
        sender_password = os.environ.get("EMAIL_PASSWORD", "")  # يجب تعيينها في متغيرات البيئة

        # رابط إعادة التعيين
        reset_link = f"https://five17.onrender.com/reset-password.html?token={token}"

        # إنشاء الرسالة
        message = MIMEMultipart("alternative")
        message["Subject"] = "إعادة تعيين كلمة المرور - نظام إدارة الإسكان"
        message["From"] = sender_email
        message["To"] = email

        # محتوى الرسالة
        html_content = f"""
        <html dir="rtl">
        <body style="font-family: Arial, sans-serif; direction: rtl;
              text-align: right;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;
                 background: #f5f5f5;">
                <div style="background: white; padding: 30px; border-radius: 10px;
                     box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #667eea; margin-bottom: 20px;">
                        إعادة تعيين كلمة المرور
                    </h2>
                    <p style="font-size: 16px; line-height: 1.6; color: #333;">
                        مرحباً <strong>{username}</strong>،
                    </p>
                    <p style="font-size: 16px; line-height: 1.6; color: #333;">
                        تلقينا طلباً لإعادة تعيين كلمة المرور لحسابك في نظام إدارة
                        الإسكان.
                    </p>
                    <p style="font-size: 16px; line-height: 1.6; color: #333;">
                        لإعادة تعيين كلمة المرور، يرجى الضغط على الرابط أدناه:
                    </p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}"
                           style="display: inline-block; padding: 15px 40px;
                                  background: linear-gradient(135deg,
                                  #667eea 0%, #764ba2 100%); color: white;
                                  text-decoration: none; border-radius: 5px;
                                  font-size: 16px; font-weight: bold;">
                            إعادة تعيين كلمة المرور
                        </a>
                    </div>
                    <p style="font-size: 14px; color: #666;">
                        إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذه الرسالة.
                    </p>
                    <p style="font-size: 14px; color: #666;">
                        هذا الرابط صالح لمدة <strong>30 دقيقة</strong> فقط.
                    </p>
                    <hr style="margin: 30px 0; border: none;
                              border-top: 1px solid #ddd;">
                    <p style="font-size: 12px; color: #999; text-align: center;">
                        &copy; 2025 جامعة الإمام محمد بن سعود الإسلامية
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        message.attach(MIMEText(html_content, "html"))

        # إرسال البريد
        if sender_password:  # فقط إذا كانت كلمة المرور متوفرة
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            return True
        else:
            logger.warning(" EMAIL_PASSWORD غير معرفة في متغيرات البيئة")
            return False
    except Exception as e:
        logger.error(f"خطأ في إرسال البريد: {str(e)}")
        return False


# API endpoint لطلب إعادة تعيين كلمة المرور
@app.route("/api/forgot-password", methods=["POST"])
def forgot_password():
    """طلب إعادة تعيين كلمة المرور"""
    try:
        data = request.get_json()
        username = data.get("username")

        if not username:
            return jsonify({"error": "يرجى إدخال اسم المستخدم"}), 400

        # التحقق من وجود المستخدم
        user = users_db.get(username)
        if not user or "email" not in user:
            # لا نكشف عن وجود المستخدم أو عدمه لأسباب أمنية
            return jsonify(
                {
                    "success": True,
                    "message": (
                        "إذا كان اسم المستخدم صحيحاً، ستصلك رسالة بريد "
                        "إلكتروني لإعادة تعيين كلمة المرور."
                    ),
                }
            )

        # إنشاء رمز إعادة تعيين
        token = secrets.token_urlsafe(32)
        reset_tokens[token] = {
            "username": username,
            "expires": datetime.now() + timedelta(minutes=30),
        }

        # إرسال البريد الإلكتروني
        email_sent = send_reset_email(user["email"], token, user["name"])

        return jsonify(
            {
                "success": True,
                "message": (
                    "إذا كان اسم المستخدم صحيحاً، ستصلك رسالة بريد "
                    "إلكتروني لإعادة تعيين كلمة المرور."
                ),
                "email_sent": email_sent,
            }
        )
    except Exception as e:
        logger.error(f"خطأ في forgot_password: {str(e)}")
        return jsonify({"error": "حدث خطأ. يرجى المحاولة لاحقاً."}), 500


# API endpoint لإعادة تعيين كلمة المرور
@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    """إعادة تعيين كلمة المرور"""
    try:
        data = request.get_json()
        token = data.get("token")
        new_password = data.get("password")

        if not token or not new_password:
            return jsonify({"error": "يرجى إدخال جميع البيانات"}), 400

        # التحقق من الرمز
        token_data = reset_tokens.get(token)
        if not token_data:
            return jsonify({"error": "رمز غير صحيح أو منتهي الصلاحية"}), 400

        # التحقق من صلاحية الرمز
        if datetime.now() > token_data["expires"]:
            del reset_tokens[token]
            return jsonify({"error": "انتهت صلاحية الرمز. يرجى طلب رمز جديد."}), 400

        # تحديث كلمة المرور
        username = token_data["username"]
        users_db[username]["password"] = generate_password_hash(new_password)

        # حذف الرمز بعد الاستخدام
        del reset_tokens[token]

        return jsonify({"success": True, "message": "تم تغيير كلمة المرور بنجاح"})
    except Exception as e:
        logger.error(f"خطأ في reset_password: {str(e)}")
        return jsonify({"error": "حدث خطأ. يرجى المحاولة لاحقاً."}), 500


# ==================== API التقارير ====================


@app.route("/api/reports/<report_type>")
def get_report(report_type):
    """API للحصول على بيانات التقارير"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        report_data = {"stats": {}, "records": []}

        if report_type == "residents":
            # تقرير السكان الشامل
            cursor.execute("SELECT COUNT(*) as total FROM residents")
            total = cursor.fetchone()["total"]

            cursor.execute('SELECT COUNT(*) as occupied FROM units WHERE status="occupied"')
            occupied = cursor.fetchone()["occupied"]

            cursor.execute('SELECT COUNT(*) as vacant FROM units WHERE status="vacant"')
            vacant = cursor.fetchone()["vacant"]

            report_data["stats"] = {
                "إجمالي السكان": total,
                "الوحدات المشغولة": occupied,
                "الوحدات الشاغرة": vacant,
                "معدل الإشغال": (
                    f"{(occupied / (occupied + vacant) * 100):.1f}%"
                    if (occupied + vacant) > 0
                    else "0%"
                ),
            }

            cursor.execute(
                """
                SELECT r.name as "الاسم", r.national_id as "رقم الهوية",
                       b.name as "المبنى", u.unit_number as "رقم الوحدة",
                       r.phone as "الهاتف", r.email as "البريد الإلكتروني"
                FROM residents r
                LEFT JOIN units u ON r.unit_id = u.id
                LEFT JOIN buildings b ON u.building_id = b.id
            """
            )

        elif report_type == "buildings":
            # تقرير حالة المباني
            cursor.execute("SELECT COUNT(*) as total FROM buildings")
            total = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) as total_units FROM units")
            total_units = cursor.fetchone()["total_units"]

            cursor.execute('SELECT COUNT(*) as occupied FROM units WHERE status="occupied"')
            occupied = cursor.fetchone()["occupied"]

            report_data["stats"] = {
                "إجمالي المباني": total,
                "إجمالي الوحدات": total_units,
                "الوحدات المشغولة": occupied,
                "الوحدات الشاغرة": total_units - occupied,
            }

            cursor.execute(
                """
                SELECT b.name as "اسم المبنى", b.location as "الموقع",
                       COUNT(u.id) as "عدد الوحدات",
                       SUM(CASE WHEN u.status="occupied" THEN 1 ELSE 0 END) as "المشغولة",
                       SUM(CASE WHEN u.status="vacant" THEN 1 ELSE 0 END) as "الشاغرة"
                FROM buildings b
                LEFT JOIN units u ON b.id = u.building_id
                GROUP BY b.id
            """
            )

        elif report_type == "vehicles":
            # تقرير السيارات الشامل
            cursor.execute("SELECT COUNT(*) as total FROM vehicles")
            total = cursor.fetchone()["total"]

            cursor.execute('SELECT COUNT(*) as active FROM stickers WHERE status="active"')
            active_stickers = cursor.fetchone()["active"]

            cursor.execute('SELECT COUNT(*) as expired FROM stickers WHERE status="expired"')
            expired_stickers = cursor.fetchone()["expired"]

            cursor.execute(
                'SELECT COUNT(*) as available FROM parking_spots WHERE status="available"'
            )
            available_parking = cursor.fetchone()["available"]

            report_data["stats"] = {
                "إجمالي السيارات": total,
                "الملصقات الفعالة": active_stickers,
                "الملصقات المنتهية": expired_stickers,
                "المواقف المتاحة": available_parking,
            }

            cursor.execute(
                """
                SELECT v.plate_number as "رقم اللوحة", v.make as "النوع",
                       v.model as "الموديل", v.color as "اللون",
                       r.name as "المالك", s.sticker_number as "رقم الملصق",
                       s.status as "حالة الملصق"
                FROM vehicles v
                LEFT JOIN residents r ON v.resident_id = r.id
                LEFT JOIN stickers s ON v.id = s.vehicle_id
            """
            )

        elif report_type == "security":
            # تقرير الأمن والحوادث
            cursor.execute("SELECT COUNT(*) as total FROM violations")
            total = cursor.fetchone()["total"]

            cursor.execute('SELECT COUNT(*) as pending FROM violations WHERE status="pending"')
            pending = cursor.fetchone()["pending"]

            cursor.execute('SELECT COUNT(*) as resolved FROM violations WHERE status="resolved"')
            resolved = cursor.fetchone()["resolved"]

            report_data["stats"] = {
                "إجمالي المخالفات": total,
                "المخالفات المعلقة": pending,
                "المخالفات المحلولة": resolved,
            }

            cursor.execute(
                """
                SELECT v.violation_type as "نوع المخالفة", v.description as "الوصف",
                       v.date as "التاريخ", v.status as "الحالة",
                       ve.plate_number as "رقم اللوحة"
                FROM violations v
                LEFT JOIN vehicles ve ON v.vehicle_id = ve.id
                ORDER BY v.date DESC
            """
            )

        elif report_type == "parking_status":
            # تقرير حالة المواقف
            cursor.execute("SELECT COUNT(*) as total FROM parking_spots")
            total = cursor.fetchone()["total"]

            cursor.execute('SELECT COUNT(*) as occupied FROM parking_spots WHERE status="occupied"')
            occupied = cursor.fetchone()["occupied"]

            cursor.execute(
                'SELECT COUNT(*) as available FROM parking_spots WHERE status="available"'
            )
            available = cursor.fetchone()["available"]

            report_data["stats"] = {
                "إجمالي المواقف": total,
                "المواقف المشغولة": occupied,
                "المواقف المتاحة": available,
                "نسبة الإشغال": f"{(occupied / total * 100):.1f}%" if total > 0 else "0%",
            }

            cursor.execute(
                """
                SELECT spot_number as "رقم الموقف", location as "الموقع",
                       type as "النوع", status as "الحالة"
                FROM parking_spots
                ORDER BY spot_number
            """
            )

        elif report_type == "stickers_per_resident":
            # تقرير الملصقات لكل ساكن
            cursor.execute(
                """
                SELECT r.name as "الاسم",
                       COUNT(v.id) as "عدد السيارات",
                       COUNT(s.id) as "عدد الملصقات",
                       SUM(CASE WHEN s.status="active" THEN 1 ELSE 0 END) as "الملصقات الفعالة"
                FROM residents r
                LEFT JOIN vehicles v ON r.id = v.resident_id
                LEFT JOIN stickers s ON v.id = s.vehicle_id
                GROUP BY r.id
            """
            )

        elif report_type == "occupancy":
            # تقرير إشغال المباني
            cursor.execute(
                """
                SELECT b.name as "المبنى",
                       COUNT(u.id) as "إجمالي الوحدات",
                       SUM(CASE WHEN u.status="occupied" THEN 1 ELSE 0 END)
                           as "المشغولة",
                       SUM(CASE WHEN u.status="vacant" THEN 1 ELSE 0 END)
                           as "الشاغرة",
                       ROUND(SUM(CASE WHEN u.status="occupied" THEN 1 ELSE 0 END)
                             * 100.0 / COUNT(u.id), 1) || '%' as "نسبة الإشغال"
                FROM buildings b
                LEFT JOIN units u ON b.id = u.building_id
                GROUP BY b.id
            """
            )

        else:
            return jsonify({"error": "نوع التقرير غير معروف"}), 404

        # تحويل النتائج إلى قائمة من القواميس
        rows = cursor.fetchall()
        report_data["records"] = [dict(row) for row in rows]

        conn.close()
        return jsonify(report_data)

    except Exception as e:
        logger.error(f"خطأ في get_report: {str(e)}")
        return jsonify({"error": "حدث خطأ أثناء إنشاء التقرير"}), 500


@app.route("/api/resident-card")
def get_resident_card():
    """البطاقة الشاملة للساكن - بناءً على رقم المبنى ورقم الوحدة"""
    try:
        building_number = request.args.get("building")
        unit_number = request.args.get("unit")

        if not building_number or not unit_number:
            return jsonify({"found": False, "error": "يجب إدخال رقم المبنى ورقم الوحدة"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # البحث عن الوحدة والساكن
        cursor.execute(
            """
            SELECT
                r.id as resident_id,
                r.name as resident_name,
                r.national_id,
                r.phone,
                r.email,
                u.id as unit_id,
                u.unit_number,
                u.status as unit_status,
                b.id as building_id,
                b.name as building_name,
                b.location as building_location
            FROM residents r
            JOIN units u ON r.unit_id = u.id
            JOIN buildings b ON u.building_id = b.id
            WHERE b.name = ? AND u.unit_number = ?
        """,
            (building_number, unit_number),
        )

        resident_row = cursor.fetchone()

        if not resident_row:
            conn.close()
            return jsonify({"found": False, "error": "لم يتم العثور على ساكن في هذه الوحدة"})

        resident_data = dict(resident_row)

        # السيارات والملصقات
        cursor.execute(
            """
            SELECT
                v.id,
                v.plate_number,
                v.make,
                v.model,
                v.color,
                s.sticker_number,
                s.status as sticker_status,
                s.issue_date,
                s.expiry_date
            FROM vehicles v
            LEFT JOIN stickers s ON v.id = s.vehicle_id
            WHERE v.resident_id = ?
        """,
            (resident_data["resident_id"],),
        )

        vehicles = [dict(row) for row in cursor.fetchall()]

        # المواقف المخصصة
        cursor.execute(
            """
            SELECT
                ps.spot_number,
                ps.location,
                ps.type,
                ps.status
            FROM parking_spots ps
            WHERE ps.unit_id = ?
        """,
            (resident_data["unit_id"],),
        )

        parking = [dict(row) for row in cursor.fetchall()]

        # المخالفات
        vehicle_ids = [v["id"] for v in vehicles]
        violations = []

        if vehicle_ids:
            placeholders = ",".join("?" * len(vehicle_ids))
            cursor.execute(
                f"""
                SELECT
                    vio.date,
                    vio.violation_type,
                    vio.description,
                    vio.status,
                    v.plate_number
                FROM violations vio
                JOIN vehicles v ON vio.vehicle_id = v.id
                WHERE vio.vehicle_id IN ({placeholders})
                ORDER BY vio.date DESC
            """,
                vehicle_ids,
            )

            violations = [dict(row) for row in cursor.fetchall()]

        conn.close()

        # إرجاع البيانات الشاملة
        return jsonify(
            {
                "found": True,
                "resident": {
                    "name": resident_data["resident_name"],
                    "national_id": resident_data["national_id"],
                    "phone": resident_data["phone"],
                    "email": resident_data["email"],
                },
                "unit": {
                    "building_name": resident_data["building_name"],
                    "unit_number": resident_data["unit_number"],
                    "location": resident_data["building_location"],
                    "status": resident_data["unit_status"],
                },
                "vehicles": vehicles,
                "parking": parking,
                "violations": violations,
            }
        )

    except Exception as e:
        logger.error(f"خطأ في get_resident_card: {str(e)}")
        return jsonify({"found": False, "error": "حدث خطأ أثناء جلب بيانات الساكن"}), 500


# ============================================
# API endpoints للسيارات والمخالفات
# Vehicles and Violations API endpoints
# ============================================

@app.route("/api/vehicles", methods=["GET"])
@login_required
def api_get_vehicles():
    """الحصول على جميع السيارات"""
    try:
        vehicles = get_all_vehicles()
        return jsonify({"success": True, "vehicles": vehicles, "count": len(vehicles)})
    except Exception as e:
        logger.error(f"خطأ في api_get_vehicles: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/vehicles", methods=["POST"])
@login_required
def api_add_vehicle():
    """إضافة سيارة جديدة"""
    try:
        data = request.json
        result = add_vehicle(
            resident_id=data.get("resident_id"),
            plate_number=data.get("plate_number"),
            vehicle_make=data.get("vehicle_make"),
            vehicle_model=data.get("vehicle_model"),
            vehicle_year=data.get("vehicle_year"),
            vehicle_type=data.get("vehicle_type"),
            vehicle_color=data.get("vehicle_color"),
            plate_arabic=data.get("plate_arabic"),
            plate_english=data.get("plate_english"),
            notes=data.get("notes")
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"خطأ في api_add_vehicle: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/vehicles/<int:vehicle_id>", methods=["PUT"])
@login_required
def api_update_vehicle(vehicle_id):
    """تحديث معلومات سيارة"""
    try:
        data = request.json
        result = update_vehicle(vehicle_id, **data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"خطأ في api_update_vehicle: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/vehicles/search", methods=["POST"])
@login_required
def api_search_vehicle():
    """البحث عن سيارة برقم اللوحة"""
    try:
        data = request.json
        plate_number = data.get("plate_number", "")
        result = search_vehicle_by_plate(plate_number)
        return jsonify(result)
    except Exception as e:
        logger.error(f"خطأ في api_search_vehicle: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/vehicles/statistics", methods=["GET"])
@login_required
def api_vehicles_statistics():
    """الحصول على إحصائيات السيارات"""
    try:
        stats = get_vehicles_statistics()
        return jsonify({"success": True, "statistics": stats})
    except Exception as e:
        logger.error(f"خطأ في api_vehicles_statistics: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/violations", methods=["GET"])
@login_required
def api_get_violations():
    """الحصول على جميع المخالفات"""
    try:
        violations = get_all_violations()
        return jsonify({"success": True, "violations": violations, "count": len(violations)})
    except Exception as e:
        logger.error(f"خطأ في api_get_violations: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/violations", methods=["POST"])
@login_required
def api_add_violation():
    """إضافة مخالفة جديدة"""
    try:
        data = request.json
        result = add_violation(
            vehicle_id=data.get("vehicle_id"),
            plate_number=data.get("plate_number"),
            violation_type=data.get("violation_type"),
            violation_description=data.get("violation_description"),
            violation_location=data.get("violation_location"),
            fine_amount=data.get("fine_amount", 0),
            image_path=data.get("image_path"),
            confidence_score=data.get("confidence_score"),
            notes=data.get("notes")
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"خطأ في api_add_violation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/violations/<int:violation_id>", methods=["PUT"])
@login_required
def api_update_violation(violation_id):
    """تحديث حالة مخالفة"""
    try:
        data = request.json
        result = update_violation_status(
            violation_id=violation_id,
            status=data.get("status"),
            payment_date=data.get("payment_date")
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"خطأ في api_update_violation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/violations/by-plate", methods=["POST"])
@login_required
def api_violations_by_plate():
    """الحصول على مخالفات سيارة معينة"""
    try:
        data = request.json
        plate_number = data.get("plate_number", "")
        violations = get_violations_by_plate(plate_number)
        return jsonify({"success": True, "violations": violations, "count": len(violations)})
    except Exception as e:
        logger.error(f"خطأ في api_violations_by_plate: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/violations/statistics", methods=["GET"])
@login_required
def api_violations_statistics():
    """الحصول على إحصائيات المخالفات"""
    try:
        stats = get_violations_statistics()
        return jsonify({"success": True, "statistics": stats})
    except Exception as e:
        logger.error(f"خطأ في api_violations_statistics: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# Plate Recognizer Integration
# ============================================

@app.route("/api/plate-recognizer/analyze", methods=["POST"])
@login_required
def api_plate_recognizer_analyze():
    """تحليل صورة باستخدام Plate Recognizer API"""
    try:
        from plate_recognizer_client import PlateRecognizerClient
        
        # التحقق من وجود صورة
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "لم يتم إرفاق صورة"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"success": False, "error": "لم يتم تحديد ملف"}), 400
        
        # حفظ الصورة مؤقتاً
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # تحليل الصورة
        client = PlateRecognizerClient()
        result = client.recognize_plate(
            image_path=filepath,
            regions=['sa']  # السعودية
        )
        
        # تسجيل النتيجة في قاعدة البيانات
        if result.get("success"):
            log_plate_recognizer_analysis(
                image_path=filepath,
                plate_number=result.get("plate_number"),
                vehicle_type=result.get("vehicle", {}).get("type"),
                vehicle_color=result.get("vehicle", {}).get("color"),
                confidence=result.get("confidence"),
                api_response=json.dumps(result.get("raw_response", {})),
                status="نجح"
            )
        else:
            log_plate_recognizer_analysis(
                image_path=filepath,
                status="فشل",
                notes=result.get("error")
            )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"خطأ في api_plate_recognizer_analyze: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/webhooks/plate-recognizer", methods=["POST"])
def webhook_plate_recognizer():
    """
    Webhook لاستقبال البيانات من Plate Recognizer
    Webhook endpoint for Plate Recognizer
    """
    try:
        data = request.json
        logger.info(f"Received Plate Recognizer webhook: {data}")
        
        # استخراج البيانات
        results = data.get('results', [])
        
        if not results:
            return jsonify({"success": False, "error": "No results in webhook data"}), 400
        
        # معالجة كل نتيجة
        for result in results:
            plate_number = result.get('plate', '')
            confidence = result.get('score', 0) * 100
            
            # تسجيل في قاعدة البيانات
            log_plate_recognizer_analysis(
                image_path=data.get('image_url', ''),
                plate_number=plate_number,
                vehicle_type=result.get('vehicle', {}).get('type'),
                vehicle_color=result.get('vehicle', {}).get('color', [{}])[0].get('color', ''),
                confidence=confidence,
                webhook_data=json.dumps(data),
                status="معالج من webhook"
            )
            
            # البحث عن السيارة في النظام
            vehicle_result = search_vehicle_by_plate(plate_number)
            
            # إذا لم توجد السيارة، يمكن إنشاء تنبيه أو مخالفة
            if not vehicle_result.get("found"):
                logger.warning(f"Unknown vehicle detected: {plate_number}")
                # يمكن إضافة منطق لإنشاء مخالفة تلقائياً
        
        return jsonify({"success": True, "processed": len(results)})
    
    except Exception as e:
        logger.error(f"خطأ في webhook_plate_recognizer: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/plate-recognizer/logs", methods=["GET"])
@login_required
def api_plate_recognizer_logs():
    """الحصول على سجل تحليلات Plate Recognizer"""
    try:
        limit = request.args.get('limit', 100, type=int)
        logs = get_plate_recognizer_logs(limit=limit)
        return jsonify({"success": True, "logs": logs, "count": len(logs)})
    except Exception as e:
        logger.error(f"خطأ في api_plate_recognizer_logs: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# Takamul Integration
# ============================================

@app.route("/api/takamul/sync", methods=["POST"])
@login_required
def api_takamul_sync():
    """مزامنة البيانات مع نظام تكامل"""
    try:
        from takamul_client import TakamulClient
        
        data = request.json
        sync_type = data.get("sync_type", "vehicles")
        
        client = TakamulClient()
        
        if sync_type == "vehicles":
            result = client.sync_vehicles()
        elif sync_type == "residents":
            result = client.fetch_residents_data()
        else:
            return jsonify({"success": False, "error": "نوع مزامنة غير صحيح"}), 400
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"خطأ في api_takamul_sync: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/takamul/sync-history", methods=["GET"])
@login_required
def api_takamul_sync_history():
    """الحصول على سجل المزامنة مع تكامل"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = get_takamul_sync_history(limit=limit)
        return jsonify({"success": True, "history": history, "count": len(history)})
    except Exception as e:
        logger.error(f"خطأ في api_takamul_sync_history: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/takamul/send-violation", methods=["POST"])
@login_required
def api_takamul_send_violation():
    """إرسال مخالفة إلى نظام تكامل"""
    try:
        from takamul_client import TakamulClient
        
        data = request.json
        client = TakamulClient()
        result = client.send_violation_report(data)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"خطأ في api_takamul_send_violation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
