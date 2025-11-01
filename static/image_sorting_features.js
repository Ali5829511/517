// ميزات فرز الصور المتقدمة
// Advanced Image Sorting Features

// إعدادات الفرز / Sorting Settings
let autoSortEnabled = true;
let deleteAfterProcess = false;
const CONFIDENCE_THRESHOLD = 80;
let sortingStats = {
    highConfidence: 0,
    lowConfidence: 0,
    byCategory: {}
};

// ملاحظة: هذا السكريبت يعتمد على المتغيرات العامة التالية من comprehensive_image_processing.html:
// Note: This script depends on the following global variables from comprehensive_image_processing.html:
// - processedResults: Array of processed image results
// - selectedFiles: Array of selected files
// هذه المتغيرات يجب أن تكون متاحة في النطاق العام عند تحميل هذا السكريبت
// These variables must be available in global scope when this script loads

/**
 * إضافة عناصر التحكم في الفرز
 * Add sorting controls to the UI
 */
function addSortingControls() {
    const controlsHTML = `
        <div class="sorting-controls" style="margin: 20px 0; padding: 25px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 20px; color: #5A8CA3; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-cog"></i> إعدادات الفرز والمعالجة
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px;">
                <label style="display: flex; align-items: center; gap: 12px; cursor: pointer; padding: 15px; background: white; border-radius: 10px; transition: all 0.3s;">
                    <input type="checkbox" id="autoSortCheckbox" checked onchange="toggleAutoSort(this)" 
                           style="width: 20px; height: 20px; cursor: pointer;">
                    <span style="flex: 1;">
                        <strong>فرز تلقائي حسب الدقة</strong>
                        <br>
                        <small style="color: #666;">أكثر من 80% تلقائي، أقل من 80% يدوي</small>
                    </span>
                </label>
                
                <label style="display: flex; align-items: center; gap: 12px; cursor: pointer; padding: 15px; background: white; border-radius: 10px; transition: all 0.3s;">
                    <input type="checkbox" id="deleteAfterCheckbox" onchange="toggleDeleteAfter(this)" 
                           style="width: 20px; height: 20px; cursor: pointer;">
                    <span style="flex: 1;">
                        <strong>حذف الصور بعد المعالجة</strong>
                        <br>
                        <small style="color: #666;">تحرير الذاكرة تلقائياً</small>
                    </span>
                </label>
            </div>
            
            <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                <button onclick="sortImagesByCategory()" 
                        style="padding: 12px 25px; background: linear-gradient(135deg, #5A8CA3 0%, #7BA7BC 100%); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; transition: all 0.3s; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-sort"></i> فرز حسب نوع الموقف
                </button>
                
                <button onclick="exportSortingReport()" 
                        style="padding: 12px 25px; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; transition: all 0.3s; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-file-export"></i> تصدير تقرير الفرز
                </button>
                
                <button onclick="showSortingStatistics()" 
                        style="padding: 12px 25px; background: linear-gradient(135deg, #6f42c1 0%, #9c27b0 100%); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; transition: all 0.3s; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-chart-bar"></i> عرض الإحصائيات
                </button>
            </div>
            
            <div id="sortingStatsDisplay" style="margin-top: 20px; display: none;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                    <div class="stat-box" style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px; font-weight: bold; color: #28a745;" id="highConfidenceCount">0</div>
                        <div style="color: #666; font-size: 14px; margin-top: 5px;">دقة عالية (تلقائي)</div>
                    </div>
                    <div class="stat-box" style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px; font-weight: bold; color: #ffc107;" id="lowConfidenceCount">0</div>
                        <div style="color: #666; font-size: 14px; margin-top: 5px;">دقة منخفضة (يدوي)</div>
                    </div>
                    <div class="stat-box" style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px; font-weight: bold; color: #5A8CA3;" id="totalProcessedCount">0</div>
                        <div style="color: #666; font-size: 14px; margin-top: 5px;">إجمالي المعالجة</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // إدراج بعد قسم الرفع
    const uploadSection = document.querySelector('.main-card');
    if (uploadSection) {
        uploadSection.insertAdjacentHTML('afterend', controlsHTML);
    }
}

/**
 * تبديل الفرز التلقائي
 * Toggle automatic sorting
 */
function toggleAutoSort(checkbox) {
    autoSortEnabled = checkbox.checked;
    console.log('✅ الفرز التلقائي:', autoSortEnabled ? 'مفعّل' : 'معطّل');
    
    // إظهار رسالة للمستخدم
    if (autoSortEnabled) {
        showNotification('تم تفعيل الفرز التلقائي', 'success');
    } else {
        showNotification('تم تعطيل الفرز التلقائي', 'info');
    }
}

/**
 * تبديل الحذف بعد المعالجة
 * Toggle delete after processing
 */
function toggleDeleteAfter(checkbox) {
    if (checkbox.checked) {
        if (confirm('⚠️ هل أنت متأكد من حذف الصور بعد المعالجة؟\n\nلا يمكن التراجع عن هذا الإجراء!')) {
            deleteAfterProcess = true;
            showNotification('سيتم حذف الصور بعد المعالجة', 'warning');
        } else {
            checkbox.checked = false;
            deleteAfterProcess = false;
        }
    } else {
        deleteAfterProcess = false;
        showNotification('تم إلغاء الحذف التلقائي', 'info');
    }
}

/**
 * تطبيق الفرز التلقائي
 * Apply automatic sorting
 */
function applyAutoSorting() {
    if (!autoSortEnabled || !processedResults || processedResults.length === 0) {
        return;
    }
    
    const highConfidence = processedResults.filter(r => r.confidence >= CONFIDENCE_THRESHOLD);
    const lowConfidence = processedResults.filter(r => r.confidence < CONFIDENCE_THRESHOLD);
    
    sortingStats.highConfidence = highConfidence.length;
    sortingStats.lowConfidence = lowConfidence.length;
    
    // تحديث العرض
    document.getElementById('highConfidenceCount').textContent = highConfidence.length;
    document.getElementById('lowConfidenceCount').textContent = lowConfidence.length;
    document.getElementById('totalProcessedCount').textContent = processedResults.length;
    document.getElementById('sortingStatsDisplay').style.display = 'block';
    
    console.log(`✅ تم الفرز التلقائي:`, {
        'دقة عالية (≥80%)': highConfidence.length,
        'دقة منخفضة (<80%)': lowConfidence.length,
        'الإجمالي': processedResults.length
    });
    
    showNotification(`تم فرز ${processedResults.length} صورة تلقائياً`, 'success');
}

/**
 * فرز الصور حسب الفئة
 * Sort images by category
 */
function sortImagesByCategory() {
    if (!processedResults || processedResults.length === 0) {
        showNotification('لا توجد صور للفرز', 'warning');
        return;
    }
    
    const categories = {
        'normal': { name: 'مواقف عادية', items: [], icon: 'parking' },
        'disabled': { name: 'مواقف معاقين', items: [], icon: 'wheelchair' },
        'violation': { name: 'مخالفات', items: [], icon: 'exclamation-triangle' },
        'old_buildings': { name: 'المباني القديمة', items: [], icon: 'building' },
        'new_buildings': { name: 'المباني الجديدة', items: [], icon: 'city' },
        'villas': { name: 'منطقة الفلل', items: [], icon: 'home' },
        'impounded': { name: 'السيارات المكبوحة', items: [], icon: 'ban' },
        'tow_truck': { name: 'خروج ودخول سيارات على سطحة', items: [], icon: 'truck' },
        'other': { name: 'أخرى', items: [], icon: 'question-circle' }
    };
    
    // فرز النتائج
    processedResults.forEach(result => {
        const category = result.category || 'other';
        if (categories[category]) {
            categories[category].items.push(result);
        } else {
            categories['other'].items.push(result);
        }
    });
    
    sortingStats.byCategory = categories;
    
    // إنشاء تقرير مفصل
    let reportHTML = `
        <div style="background: white; padding: 30px; border-radius: 15px; max-width: 700px; margin: 20px auto;">
            <h2 style="color: #5A8CA3; margin-bottom: 25px; text-align: center;">
                <i class="fas fa-chart-pie"></i> تقرير الفرز حسب الفئة
            </h2>
            <div style="display: grid; gap: 15px;">
    `;
    
    let totalImages = 0;
    for (const [key, cat] of Object.entries(categories)) {
        if (cat.items.length > 0) {
            totalImages += cat.items.length;
            const percentage = ((cat.items.length / processedResults.length) * 100).toFixed(1);
            reportHTML += `
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 15px; background: #f8f9fa; border-radius: 10px; border-right: 4px solid #5A8CA3;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <i class="fas fa-${cat.icon}" style="font-size: 24px; color: #5A8CA3;"></i>
                        <span style="font-weight: bold;">${cat.name}</span>
                    </div>
                    <div style="text-align: left;">
                        <div style="font-size: 24px; font-weight: bold; color: #5A8CA3;">${cat.items.length}</div>
                        <div style="font-size: 12px; color: #666;">${percentage}%</div>
                    </div>
                </div>
            `;
        }
    }
    
    reportHTML += `
            </div>
            <div style="margin-top: 25px; padding: 20px; background: #e7f3ff; border-radius: 10px; text-align: center;">
                <div style="font-size: 18px; color: #666;">إجمالي الصور</div>
                <div style="font-size: 36px; font-weight: bold; color: #5A8CA3;">${totalImages}</div>
            </div>
            <button onclick="closeModal()" style="width: 100%; margin-top: 20px; padding: 15px; background: #5A8CA3; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold;">
                <i class="fas fa-times"></i> إغلاق
            </button>
        </div>
    `;
    
    showModal(reportHTML);
    console.log('📊 تم الفرز حسب الفئة:', categories);
}

/**
 * تصدير تقرير الفرز
 * Export sorting report
 */
function exportSortingReport() {
    if (!processedResults || processedResults.length === 0) {
        showNotification('لا توجد بيانات للتصدير', 'warning');
        return;
    }
    
    const timestamp = new Date().toLocaleString('ar-SA');
    let report = `تقرير فرز الصور - نظام إدارة الإسكان الجامعي\n`;
    report += `التاريخ والوقت: ${timestamp}\n`;
    report += `${'='.repeat(60)}\n\n`;
    
    report += `إجمالي الصور المعالجة: ${processedResults.length}\n`;
    report += `الصور ذات الدقة العالية (≥80%): ${sortingStats.highConfidence}\n`;
    report += `الصور ذات الدقة المنخفضة (<80%): ${sortingStats.lowConfidence}\n\n`;
    
    report += `الفرز حسب الفئة:\n`;
    report += `${'='.repeat(60)}\n`;
    
    for (const [key, cat] of Object.entries(sortingStats.byCategory || {})) {
        if (cat.items && cat.items.length > 0) {
            const percentage = ((cat.items.length / processedResults.length) * 100).toFixed(1);
            report += `${cat.name}: ${cat.items.length} (${percentage}%)\n`;
        }
    }
    
    report += `\n${'='.repeat(60)}\n`;
    report += `تفاصيل الصور:\n\n`;
    
    processedResults.forEach((result, index) => {
        report += `${index + 1}. ${result.filename}\n`;
        report += `   - رقم اللوحة: ${result.plateNumber || 'غير محدد'}\n`;
        report += `   - نوع السيارة: ${result.carType || 'غير محدد'}\n`;
        report += `   - اللون: ${result.carColor || 'غير محدد'}\n`;
        report += `   - الفئة: ${getCategoryText(result.category)}\n`;
        report += `   - الدقة: ${result.confidence}%\n\n`;
    });
    
    // تنزيل الملف
    const blob = new Blob([report], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `تقرير_فرز_الصور_${Date.now()}.txt`;
    link.click();
    
    showNotification('تم تصدير التقرير بنجاح', 'success');
}

/**
 * عرض إحصائيات الفرز
 * Show sorting statistics
 */
function showSortingStatistics() {
    if (!processedResults || processedResults.length === 0) {
        showNotification('لا توجد إحصائيات لعرضها', 'warning');
        return;
    }
    
    applyAutoSorting();
    document.getElementById('sortingStatsDisplay').style.display = 'block';
    
    // تمرير سلس للإحصائيات
    document.getElementById('sortingStatsDisplay').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

/**
 * حذف الصور المعالجة
 * Delete processed images
 */
function deleteProcessedImages() {
    if (!processedResults || processedResults.length === 0) {
        return;
    }
    
    const count = processedResults.length;
    
    // مسح البيانات
    processedResults = [];
    selectedFiles = [];
    sortingStats = {
        highConfidence: 0,
        lowConfidence: 0,
        byCategory: {}
    };
    
    // مسح العرض
    if (document.getElementById('resultsSection')) {
        document.getElementById('resultsSection').style.display = 'none';
    }
    if (document.getElementById('resultsGrid')) {
        document.getElementById('resultsGrid').innerHTML = '';
    }
    if (document.getElementById('sortingStatsDisplay')) {
        document.getElementById('sortingStatsDisplay').style.display = 'none';
    }
    
    // إعادة تعيين input
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.value = '';
    }
    
    console.log(`🗑️ تم حذف ${count} صورة معالجة`);
    showNotification(`تم حذف ${count} صورة معالجة من الذاكرة`, 'success');
}

/**
 * الحصول على نص الفئة بالعربية
 * Get category text in Arabic
 */
function getCategoryText(category) {
    const texts = {
        'normal': 'موقف عادي',
        'disabled': 'موقف معاقين',
        'violation': 'مخالفة',
        'old_buildings': 'المباني القديمة',
        'new_buildings': 'المباني الجديدة',
        'villas': 'منطقة الفلل',
        'impounded': 'سيارة مكبوحة',
        'tow_truck': 'سطحة',
        'other': 'أخرى'
    };
    return texts[category] || 'غير محدد';
}

/**
 * عرض نافذة منبثقة
 * Show modal dialog
 */
function showModal(content) {
    const modalHTML = `
        <div id="customModal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 10000; display: flex; align-items: center; justify-content: center; padding: 20px;">
            ${content}
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // إغلاق عند النقر خارج المحتوى
    document.getElementById('customModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });
}

/**
 * إغلاق النافذة المنبثقة
 * Close modal dialog
 */
function closeModal() {
    const modal = document.getElementById('customModal');
    if (modal) {
        modal.remove();
    }
}

/**
 * عرض إشعار
 * Show notification
 */
function showNotification(message, type = 'info') {
    const colors = {
        success: '#28a745',
        warning: '#ffc107',
        danger: '#dc3545',
        info: '#17a2b8'
    };
    
    const notificationHTML = `
        <div style="position: fixed; top: 20px; left: 50%; transform: translateX(-50%); background: ${colors[type]}; color: white; padding: 15px 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); z-index: 10001; animation: slideDown 0.3s ease;">
            ${message}
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', notificationHTML);
    
    setTimeout(() => {
        const notification = document.body.lastElementChild;
        notification.style.animation = 'slideUp 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// تهيئة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // إضافة أنماط الرسوم المتحركة
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
        @keyframes slideUp {
            from {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
            to {
                opacity: 0;
                transform: translateX(-50%) translateY(-20px);
            }
        }
    `;
    document.head.appendChild(style);
    
    // إضافة عناصر التحكم
    setTimeout(addSortingControls, 1000);
    
    console.log('✅ تم تحميل ميزات فرز الصور بنجاح');
});

// تصدير الدوال للاستخدام العام
window.applyAutoSorting = applyAutoSorting;
window.sortImagesByCategory = sortImagesByCategory;
window.exportSortingReport = exportSortingReport;
window.showSortingStatistics = showSortingStatistics;
window.deleteProcessedImages = deleteProcessedImages;
window.toggleAutoSort = toggleAutoSort;
window.toggleDeleteAfter = toggleDeleteAfter;
window.closeModal = closeModal;
