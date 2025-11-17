#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة التكامل مع Plate Recognizer API
Plate Recognizer API Integration Module
"""

import requests
import os
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PlateRecognizerClient:
    """
    عميل للتكامل مع Plate Recognizer API
    Client for Plate Recognizer API integration
    """
    
    def __init__(self, api_token=None):
        """
        تهيئة العميل
        
        Args:
            api_token: رمز API من Plate Recognizer
        """
        self.api_token = api_token or os.getenv("PLATE_RECOGNIZER_TOKEN")
        self.base_url = "https://api.platerecognizer.com/v1"
        self.snapshot_url = f"{self.base_url}/plate-reader/"
        
        if not self.api_token:
            logger.warning("PLATE_RECOGNIZER_TOKEN not found in environment variables")
    
    def recognize_plate(self, image_path=None, image_data=None, regions=None):
        """
        تحليل صورة واستخراج رقم اللوحة
        Analyze image and extract plate number
        
        Args:
            image_path: مسار الصورة على القرص
            image_data: بيانات الصورة (bytes)
            regions: قائمة المناطق للتحليل (مثل: ['sa'] للسعودية)
        
        Returns:
            dict: نتيجة التحليل
        """
        if not self.api_token:
            return {
                "success": False,
                "error": "API token not configured"
            }
        
        headers = {
            "Authorization": f"Token {self.api_token}"
        }
        
        # إعداد البيانات
        data = {}
        if regions:
            data['regions'] = regions
        
        files = {}
        if image_path and os.path.exists(image_path):
            files['upload'] = open(image_path, 'rb')
        elif image_data:
            files['upload'] = image_data
        else:
            return {
                "success": False,
                "error": "No image provided"
            }
        
        try:
            response = requests.post(
                self.snapshot_url,
                headers=headers,
                data=data,
                files=files
            )
            
            if response.status_code == 201:
                result = response.json()
                return self._parse_response(result)
            else:
                logger.error(f"Plate Recognizer API error: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "message": response.text
                }
        
        except Exception as e:
            logger.error(f"Error calling Plate Recognizer API: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        
        finally:
            # إغلاق الملف إذا تم فتحه
            if 'upload' in files and hasattr(files['upload'], 'close'):
                files['upload'].close()
    
    def _parse_response(self, response):
        """
        تحليل الاستجابة من API
        Parse API response
        
        Args:
            response: الاستجابة من API
        
        Returns:
            dict: البيانات المنسقة
        """
        results = response.get('results', [])
        
        if not results:
            return {
                "success": False,
                "error": "No plates detected",
                "raw_response": response
            }
        
        # أخذ أول نتيجة (الأعلى ثقة)
        plate_data = results[0]
        
        return {
            "success": True,
            "plate_number": plate_data.get('plate', ''),
            "confidence": plate_data.get('score', 0) * 100,  # تحويل إلى نسبة مئوية
            "region": plate_data.get('region', {}).get('code', ''),
            "vehicle": {
                "type": plate_data.get('vehicle', {}).get('type', ''),
                "color": plate_data.get('vehicle', {}).get('color', [{}])[0].get('color', '') if plate_data.get('vehicle', {}).get('color') else '',
                "make": plate_data.get('vehicle', {}).get('make', [{}])[0].get('make', '') if plate_data.get('vehicle', {}).get('make') else '',
                "model": plate_data.get('vehicle', {}).get('make_model', [{}])[0].get('model', '') if plate_data.get('vehicle', {}).get('make_model') else '',
            },
            "box": plate_data.get('box', {}),
            "processing_time": response.get('processing_time', 0),
            "raw_response": response
        }
    
    def get_statistics(self):
        """
        الحصول على إحصائيات الاستخدام
        Get usage statistics
        """
        if not self.api_token:
            return {
                "success": False,
                "error": "API token not configured"
            }
        
        headers = {
            "Authorization": f"Token {self.api_token}"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/statistics/",
                headers=headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}"
                }
        
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# مثال على الاستخدام
if __name__ == "__main__":
    # تهيئة العميل
    client = PlateRecognizerClient()
    
    # مثال: تحليل صورة
    # result = client.recognize_plate(
    #     image_path="path/to/image.jpg",
    #     regions=['sa']  # السعودية
    # )
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("Plate Recognizer Client initialized successfully")
