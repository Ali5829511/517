// نظام الإشعارات المتقدم
// Advanced Notification System

class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.init();
    }

    init() {
        // إنشاء حاوية الإشعارات
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        const colors = {
            success: '#27ae60',
            error: '#e74c3c',
            warning: '#f39c12',
            info: '#3498db'
        };

        notification.style.cssText = `
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            border-right: 5px solid ${colors[type]};
            display: flex;
            align-items: center;
            gap: 15px;
            animation: slideIn 0.3s ease;
            cursor: pointer;
        `;

        notification.innerHTML = `
            <i class="fas ${icons[type]}" style="color: ${colors[type]}; font-size: 24px;"></i>
            <div style="flex: 1;">
                <div style="font-weight: bold; color: #333; margin-bottom: 5px;">${this.getTitle(type)}</div>
                <div style="color: #666; font-size: 14px;">${message}</div>
            </div>
            <i class="fas fa-times" style="color: #999; cursor: pointer; font-size: 18px;"></i>
        `;

        // إضافة تأثير CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(-100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(-100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        // إضافة حدث الإغلاق
        notification.addEventListener('click', () => {
            this.remove(notification);
        });

        this.container.appendChild(notification);
        this.notifications.push(notification);

        // إزالة تلقائية بعد المدة المحددة
        if (duration > 0) {
            setTimeout(() => {
                this.remove(notification);
            }, duration);
        }

        return notification;
    }

    remove(notification) {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            const index = this.notifications.indexOf(notification);
            if (index > -1) {
                this.notifications.splice(index, 1);
            }
        }, 300);
    }

    getTitle(type) {
        const titles = {
            success: '✓ نجح',
            error: '✗ خطأ',
            warning: '⚠ تحذير',
            info: 'ℹ معلومة'
        };
        return titles[type] || 'إشعار';
    }

    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    error(message, duration) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }

    clear() {
        this.notifications.forEach(notification => this.remove(notification));
    }
}

// إنشاء instance عام
const notify = new NotificationSystem();

// إشعارات تلقائية عند تحميل الصفحة
window.addEventListener('DOMContentLoaded', () => {
    // إشعار ترحيبي
    setTimeout(() => {
        notify.info('مرحباً بك في نظام إدارة الإسكان الجامعي', 6000);
    }, 1000);

    // التحقق من تسجيل الدخول
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('login') === 'success') {
        notify.success('تم تسجيل الدخول بنجاح', 5000);
    }
});
