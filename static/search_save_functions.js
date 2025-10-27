// حفظ النتائج في قاعدة البيانات
async function saveToDatabase() {
    if (processedResults.length === 0) {
        alert('لا توجد نتائج لحفظها');
        return;
    }

    const confirmed = confirm(`هل تريد حفظ ${processedResults.length} صورة في قاعدة البيانات؟`);
    if (!confirmed) return;

    let savedCount = 0;
    let failedCount = 0;

    for (const result of processedResults) {
        try {
            const response = await fetch('/api/save-processed-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: result.filename || 'unknown.jpg',
                    plateNumber: result.plateNumber,
                    arabicLetters: result.arabicLetters,
                    numbers: result.numbers,
                    carType: result.carType,
                    carColor: result.carColor,
                    confidence: result.confidence,
                    category: result.category || 'normal',
                    notes: result.notes || ''
                })
            });

            const data = await response.json();
            if (data.success) {
                savedCount++;
            } else {
                failedCount++;
                console.error('فشل حفظ الصورة:', data.error);
            }
        } catch (error) {
            failedCount++;
            console.error('خطأ في حفظ الصورة:', error);
        }
    }

    if (savedCount > 0) {
        alert(`✅ تم حفظ ${savedCount} صورة بنجاح!${failedCount > 0 ? `\n⚠️ فشل حفظ ${failedCount} صورة` : ''}`);
    } else {
        alert('❌ فشل حفظ جميع الصور');
    }
}

// إظهار نافذة البحث
function showSearchDialog() {
    const plateNumber = prompt('أدخل رقم اللوحة للبحث:\n(مثال: ن ن ب 5687)');
    
    if (plateNumber && plateNumber.trim() !== '') {
        searchByPlateNumber(plateNumber.trim());
    }
}

// البحث برقم اللوحة
async function searchByPlateNumber(plateNumber) {
    try {
        // إظهار مؤشر التحميل
        const loadingMsg = document.createElement('div');
        loadingMsg.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); z-index: 10000; text-align: center;';
        loadingMsg.innerHTML = '<div class="loading-spinner" style="margin: 0 auto 15px;"></div><p style="color: #2D5F3F; font-weight: bold;">جاري البحث...</p>';
        document.body.appendChild(loadingMsg);

        const response = await fetch('/api/search-processed-images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ plateNumber })
        });

        const result = await response.json();
        document.body.removeChild(loadingMsg);

        if (result.success && result.data && result.data.length > 0) {
            displaySearchResults(result.data, plateNumber);
        } else {
            alert(`❌ لم يتم العثور على نتائج للوحة: ${plateNumber}`);
        }
    } catch (error) {
        console.error('خطأ في البحث:', error);
        alert('حدث خطأ أثناء البحث');
    }
}

// عرض نتائج البحث
function displaySearchResults(results, searchTerm) {
    // إنشاء نافذة منبثقة
    const modal = document.createElement('div');
    modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 9999; display: flex; align-items: center; justify-content: center; padding: 20px;';
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = 'background: white; border-radius: 20px; padding: 30px; max-width: 900px; max-height: 80vh; overflow-y: auto; width: 100%;';
    
    let html = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h2 style="color: #2D5F3F; margin: 0;">
                <i class="fas fa-search"></i> نتائج البحث عن: ${searchTerm}
            </h2>
            <button onclick="this.closest('div').parentElement.parentElement.remove()" style="background: #f44336; color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">
                <i class="fas fa-times"></i> إغلاق
            </button>
        </div>
        <p style="color: #666; margin-bottom: 20px;">تم العثور على ${results.length} نتيجة</p>
    `;
    
    results.forEach((result, index) => {
        html += `
            <div style="background: #f5f5f5; border-radius: 15px; padding: 20px; margin-bottom: 15px; border-right: 4px solid #2D5F3F;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div>
                        <strong style="color: #2D5F3F;">رقم اللوحة:</strong><br>
                        <span style="font-size: 20px; font-weight: bold;">${result.plateNumber || 'غير محدد'}</span>
                    </div>
                    <div>
                        <strong style="color: #2D5F3F;">نوع السيارة:</strong><br>
                        ${result.vehicleType || 'غير محدد'}
                    </div>
                    <div>
                        <strong style="color: #2D5F3F;">اللون:</strong><br>
                        ${result.vehicleColor || 'غير محدد'}
                    </div>
                    <div>
                        <strong style="color: #2D5F3F;">نسبة الثقة:</strong><br>
                        ${result.confidence || 0}%
                    </div>
                    <div>
                        <strong style="color: #2D5F3F;">تاريخ المعالجة:</strong><br>
                        ${new Date(result.processingDate).toLocaleString('ar-SA')}
                    </div>
                </div>
                ${result.resident && result.resident.name ? `
                    <div style="background: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 15px;">
                        <strong style="color: #2D5F3F;"><i class="fas fa-user"></i> معلومات الساكن:</strong><br>
                        <div style="margin-top: 10px; display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
                            <div>الاسم: ${result.resident.name}</div>
                            <div>المبنى: ${result.resident.building || '-'}</div>
                            <div>الوحدة: ${result.resident.unit || '-'}</div>
                            <div>الهاتف: ${result.resident.phone || '-'}</div>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    modalContent.innerHTML = html;
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    // إغلاق عند النقر خارج النافذة
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}
