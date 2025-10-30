#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تصنيف الصور الذكي بالذكاء الاصطناعي
AI-Powered Image Classification System
"""

import os
import base64
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# فئات التصنيف المتاحة
IMAGE_CATEGORIES = {
    'disabled_parking': {
        'name_ar': 'موقف معاقين',
        'name_en': 'Disabled Parking',
        'keywords': ['wheelchair', 'disabled', 'handicap', 'accessibility', 'معاقين', 'ذوي الاحتياجات'],
        'description': 'صور مواقف السيارات المخصصة لذوي الاحتياجات الخاصة'
    },
    'vip_parking': {
        'name_ar': 'موقف خاص / VIP',
        'name_en': 'VIP Parking',
        'keywords': ['vip', 'reserved', 'special', 'خاص', 'مخصص'],
        'description': 'صور المواقف المخصصة للشخصيات المهمة'
    },
    'violation': {
        'name_ar': 'مخالفة مرورية',
        'name_en': 'Traffic Violation',
        'keywords': ['violation', 'illegal parking', 'wrong parking', 'مخالفة', 'خطأ', 'ممنوع'],
        'description': 'صور المخالفات المرورية والمواقف الخاطئة'
    },
    'qr_code': {
        'name_ar': 'رمز QR',
        'name_en': 'QR Code',
        'keywords': ['qr code', 'qr', 'barcode', 'رمز', 'باركود'],
        'description': 'صور تحتوي على رموز QR أو باركود'
    },
    'documents': {
        'name_ar': 'مستندات',
        'name_en': 'Documents',
        'keywords': ['document', 'paper', 'form', 'letter', 'مستند', 'ورقة', 'نموذج'],
        'description': 'صور المستندات والأوراق الرسمية'
    },
    'complaints': {
        'name_ar': 'شكاوى',
        'name_en': 'Complaints',
        'keywords': ['complaint', 'issue', 'problem', 'شكوى', 'مشكلة', 'بلاغ'],
        'description': 'صور الشكاوى والبلاغات'
    },
    'pledges': {
        'name_ar': 'تعهدات',
        'name_en': 'Pledges',
        'keywords': ['pledge', 'commitment', 'promise', 'تعهد', 'التزام', 'وعد'],
        'description': 'صور التعهدات والالتزامات'
    },
    'normal_parking': {
        'name_ar': 'موقف عادي',
        'name_en': 'Normal Parking',
        'keywords': ['parking', 'car', 'vehicle', 'موقف', 'سيارة', 'مركبة'],
        'description': 'صور المواقف العادية'
    },
    'other': {
        'name_ar': 'أخرى',
        'name_en': 'Other',
        'keywords': ['other', 'misc', 'unknown', 'أخرى', 'متنوع'],
        'description': 'صور غير مصنفة'
    }
}

def classify_image_with_ai(image_base64: str, openai_client=None) -> Dict:
    """
    تصنيف الصورة باستخدام الذكاء الاصطناعي
    Classify image using AI vision
    """
    try:
        if not openai_client:
            logger.warning("OpenAI client not available, using fallback classification")
            return fallback_classification()
        
        # إنشاء prompt للتصنيف
        prompt = f"""
        قم بتحليل هذه الصورة وتصنيفها إلى إحدى الفئات التالية:
        
        1. موقف معاقين (Disabled Parking) - إذا كانت تحتوي على علامات أو رموز المعاقين
        2. موقف خاص/VIP (VIP Parking) - إذا كانت موقف مخصص أو محجوز
        3. مخالفة مرورية (Violation) - إذا كانت توثق مخالفة أو موقف خاطئ
        4. رمز QR (QR Code) - إذا كانت تحتوي على رمز QR أو باركود
        5. مستندات (Documents) - إذا كانت صورة لمستند أو ورقة رسمية
        6. شكاوى (Complaints) - إذا كانت توثق شكوى أو مشكلة
        7. تعهدات (Pledges) - إذا كانت صورة لتعهد أو التزام
        8. موقف عادي (Normal Parking) - صورة موقف سيارات عادي
        9. أخرى (Other) - إذا لم تتطابق مع أي فئة
        
        أجب بصيغة JSON فقط:
        {{
            "category": "اسم_الفئة_بالإنجليزية",
            "confidence": نسبة_الثقة_من_0_إلى_100,
            "description": "وصف_قصير_بالعربية",
            "visual_features": ["ميزة1", "ميزة2", "ميزة3"]
        }}
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_base64 if image_base64.startswith('data:') else f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # استخراج JSON من الرد
        import json
        import re
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            
            # تحويل اسم الفئة إلى المفتاح المناسب
            category_map = {
                'disabled_parking': 'disabled_parking',
                'vip_parking': 'vip_parking',
                'violation': 'violation',
                'qr_code': 'qr_code',
                'documents': 'documents',
                'complaints': 'complaints',
                'pledges': 'pledges',
                'normal_parking': 'normal_parking',
                'other': 'other'
            }
            
            category = result.get('category', 'other').lower().replace(' ', '_')
            category = category_map.get(category, 'other')
            
            return {
                'category': category,
                'category_name_ar': IMAGE_CATEGORIES[category]['name_ar'],
                'category_name_en': IMAGE_CATEGORIES[category]['name_en'],
                'confidence': result.get('confidence', 50),
                'description': result.get('description', ''),
                'visual_features': result.get('visual_features', []),
                'method': 'ai'
            }
        else:
            return fallback_classification()
            
    except Exception as e:
        logger.error(f"Error in AI classification: {e}")
        return fallback_classification()

def fallback_classification() -> Dict:
    """تصنيف احتياطي عند عدم توفر AI"""
    return {
        'category': 'normal_parking',
        'category_name_ar': 'موقف عادي',
        'category_name_en': 'Normal Parking',
        'confidence': 30,
        'description': 'تصنيف تلقائي (AI غير متاح)',
        'visual_features': [],
        'method': 'fallback'
    }

def classify_images_batch(images: List[str], openai_client=None) -> List[Dict]:
    """
    تصنيف مجموعة من الصور
    Classify multiple images
    """
    results = []
    for img_base64 in images:
        result = classify_image_with_ai(img_base64, openai_client)
        results.append(result)
    return results

def group_similar_images(classifications: List[Dict]) -> Dict[str, List[int]]:
    """
    تجميع الصور المتشابهة حسب الفئة
    Group similar images by category
    """
    groups = {}
    for idx, classification in enumerate(classifications):
        category = classification['category']
        if category not in groups:
            groups[category] = []
        groups[category].append(idx)
    
    return groups

def get_category_statistics(classifications: List[Dict]) -> Dict:
    """
    إحصائيات التصنيفات
    Get classification statistics
    """
    stats = {}
    total = len(classifications)
    
    for category_key, category_info in IMAGE_CATEGORIES.items():
        count = sum(1 for c in classifications if c['category'] == category_key)
        if count > 0:
            stats[category_key] = {
                'name_ar': category_info['name_ar'],
                'name_en': category_info['name_en'],
                'count': count,
                'percentage': round((count / total) * 100, 2) if total > 0 else 0
            }
    
    return stats

if __name__ == '__main__':
    print("✅ نظام تصنيف الصور الذكي جاهز")
    print(f"📊 الفئات المتاحة: {len(IMAGE_CATEGORIES)}")
    for key, info in IMAGE_CATEGORIES.items():
        print(f"   - {info['name_ar']} ({info['name_en']})")
