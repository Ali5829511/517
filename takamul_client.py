#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة التكامل مع نظام تكامل
Takamul System Integration Module
"""

import requests
import os
import json
from datetime import datetime
import logging
from database_api import log_takamul_sync, add_vehicle, get_all_vehicles

logger = logging.getLogger(__name__)


class TakamulClient:
    """
    عميل للتكامل مع نظام تكامل
    Client for Takamul system integration
    """
    
    def __init__(self, api_url=None, api_key=None):
        """
        تهيئة العميل
        
        Args:
            api_url: رابط API نظام تكامل
            api_key: مفتاح API
        """
        self.api_url = api_url or os.getenv("TAKAMUL_API_URL")
        self.api_key = api_key or os.getenv("TAKAMUL_API_KEY")
        
        if not self.api_url:
            logger.warning("TAKAMUL_API_URL not found in environment variables")
        if not self.api_key:
            logger.warning("TAKAMUL_API_KEY not found in environment variables")
    
    def fetch_vehicles_data(self):
        """
        جلب بيانات السيارات من نظام تكامل
        Fetch vehicles data from Takamul system
        
        Returns:
            dict: نتيجة العملية
        """
        if not self.api_url or not self.api_key:
            return {
                "success": False,
                "error": "API configuration not found"
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # افتراض endpoint للسيارات
            endpoint = f"{self.api_url}/api/vehicles"
            
            response = requests.get(
                endpoint,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "data": data,
                    "count": len(data) if isinstance(data, list) else 0
                }
            else:
                logger.error(f"Takamul API error: {response.status_code}")
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "message": response.text
                }
        
        except requests.exceptions.Timeout:
            logger.error("Takamul API timeout")
            return {
                "success": False,
                "error": "API timeout"
            }
        except Exception as e:
            logger.error(f"Error calling Takamul API: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def fetch_residents_data(self):
        """
        جلب بيانات السكان من نظام تكامل
        Fetch residents data from Takamul system
        
        Returns:
            dict: نتيجة العملية
        """
        if not self.api_url or not self.api_key:
            return {
                "success": False,
                "error": "API configuration not found"
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            endpoint = f"{self.api_url}/api/residents"
            
            response = requests.get(
                endpoint,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "data": data,
                    "count": len(data) if isinstance(data, list) else 0
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}"
                }
        
        except Exception as e:
            logger.error(f"Error fetching residents: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def sync_vehicles(self):
        """
        مزامنة بيانات السيارات
        Synchronize vehicles data
        
        Returns:
            dict: نتيجة المزامنة
        """
        # جلب البيانات من تكامل
        result = self.fetch_vehicles_data()
        
        if not result.get("success"):
            # تسجيل الفشل
            log_takamul_sync(
                sync_type="vehicles",
                records_synced=0,
                status="فشل",
                error_message=result.get("error", "Unknown error")
            )
            return result
        
        vehicles_data = result.get("data", [])
        synced_count = 0
        errors = []
        
        # معالجة كل سيارة
        for vehicle in vehicles_data:
            try:
                # محاولة إضافة السيارة
                add_result = add_vehicle(
                    resident_id=vehicle.get("resident_id"),
                    plate_number=vehicle.get("plate_number"),
                    vehicle_make=vehicle.get("make"),
                    vehicle_model=vehicle.get("model"),
                    vehicle_year=vehicle.get("year"),
                    vehicle_type=vehicle.get("type"),
                    vehicle_color=vehicle.get("color"),
                    notes="مزامنة من تكامل"
                )
                
                if add_result.get("success"):
                    synced_count += 1
                else:
                    errors.append({
                        "plate": vehicle.get("plate_number"),
                        "error": add_result.get("error")
                    })
            
            except Exception as e:
                errors.append({
                    "plate": vehicle.get("plate_number"),
                    "error": str(e)
                })
        
        # تسجيل النتيجة
        log_takamul_sync(
            sync_type="vehicles",
            records_synced=synced_count,
            status="نجح" if synced_count > 0 else "فشل",
            error_message=json.dumps(errors, ensure_ascii=False) if errors else None,
            data_snapshot=json.dumps({
                "total": len(vehicles_data),
                "synced": synced_count,
                "errors": len(errors)
            }, ensure_ascii=False)
        )
        
        return {
            "success": True,
            "synced": synced_count,
            "total": len(vehicles_data),
            "errors": errors
        }
    
    def send_violation_report(self, violation_data):
        """
        إرسال تقرير مخالفة إلى نظام تكامل
        Send violation report to Takamul system
        
        Args:
            violation_data: بيانات المخالفة
        
        Returns:
            dict: نتيجة العملية
        """
        if not self.api_url or not self.api_key:
            return {
                "success": False,
                "error": "API configuration not found"
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            endpoint = f"{self.api_url}/api/violations"
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=violation_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
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
            logger.error(f"Error sending violation: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# دالة مساعدة للمزامنة الدورية
def auto_sync_with_takamul():
    """
    مزامنة تلقائية مع نظام تكامل
    Automatic synchronization with Takamul
    
    يمكن استدعاء هذه الدالة من cron job أو scheduler
    """
    client = TakamulClient()
    
    # مزامنة السيارات
    vehicles_result = client.sync_vehicles()
    logger.info(f"Vehicles sync result: {vehicles_result}")
    
    return vehicles_result


# مثال على الاستخدام
if __name__ == "__main__":
    # تهيئة العميل
    client = TakamulClient()
    
    # مثال: جلب بيانات السيارات
    # result = client.fetch_vehicles_data()
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("Takamul Client initialized successfully")
