/**
 * تنسيق أرقام اللوحات السعودية
 * يحول رقم اللوحة من نص عادي إلى عرض احترافي
 */

function formatSaudiPlate(plateNumber) {
    if (!plateNumber || plateNumber === '-' || plateNumber === 'غير محدد') {
        return '<span style="color: #9ca3af;">غير محدد</span>';
    }

    // تقسيم رقم اللوحة إلى أحرف وأرقام
    // التنسيق المتوقع: "ج ب ي 6953" أو "أ ب ج 1234"
    const parts = plateNumber.trim().split(' ');
    
    let letters = [];
    let numbers = '';
    
    // فصل الأحرف عن الأرقام
    for (let part of parts) {
        if (/^\d+$/.test(part)) {
            // إذا كان رقم
            numbers = part;
        } else if (/[\u0600-\u06FF]/.test(part)) {
            // إذا كان حرف عربي
            letters.push(part);
        }
    }
    
    // إنشاء HTML للوحة
    const lettersHTML = letters.map(letter => `<span>${letter}</span>`).join('');
    
    return `
        <div class="saudi-plate">
            <div class="plate-numbers">${numbers}</div>
            <div class="plate-separator"></div>
            <div class="plate-letters">${lettersHTML}</div>
        </div>
        <div class="saudi-plate-print">
            <div class="plate-numbers-print">${numbers}</div>
            <div class="plate-separator-print"></div>
            <div class="plate-letters-print">${lettersHTML}</div>
        </div>
    `;
}

/**
 * تطبيق التنسيق على جميع أرقام اللوحات في الصفحة
 */
function formatAllPlates() {
    // البحث عن جميع عناصر أرقام اللوحات
    const plateElements = document.querySelectorAll('[data-plate]');
    
    plateElements.forEach(element => {
        const plateNumber = element.getAttribute('data-plate');
        element.innerHTML = formatSaudiPlate(plateNumber);
    });
}

/**
 * تنسيق رقم اللوحة للطباعة فقط (نص بسيط)
 */
function formatPlateForPrint(plateNumber) {
    if (!plateNumber || plateNumber === '-' || plateNumber === 'غير محدد') {
        return 'غير محدد';
    }
    return plateNumber;
}

/**
 * تنسيق رقم اللوحة بشكل مضغوط (للجداول)
 */
function formatPlateCompact(plateNumber) {
    if (!plateNumber || plateNumber === '-' || plateNumber === 'غير محدد') {
        return '<span style="color: #9ca3af;">غير محدد</span>';
    }

    const parts = plateNumber.trim().split(' ');
    let letters = [];
    let numbers = '';
    
    for (let part of parts) {
        if (/^\d+$/.test(part)) {
            numbers = part;
        } else if (/[\u0600-\u06FF]/.test(part)) {
            letters.push(part);
        }
    }
    
    const lettersHTML = letters.join(' ');
    
    return `
        <span style="font-family: 'Courier New', monospace; font-weight: bold; direction: rtl; white-space: nowrap;">
            <span style="color: #1e40af;">${lettersHTML}</span>
            <span style="margin: 0 4px;">-</span>
            <span style="color: #000;">${numbers}</span>
        </span>
    `;
}

// تطبيق التنسيق تلقائياً عند تحميل الصفحة
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', formatAllPlates);
} else {
    formatAllPlates();
}

