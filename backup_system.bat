@echo off
REM نسخ احتياطي شامل لنظام إدارة الإسكان
REM Comprehensive Backup Script for Housing Management System

chcp 65001 >nul
echo ==========================================
echo نسخ احتياطي للنظام - System Backup
echo ==========================================
echo.

REM تحديد اسم النسخة الاحتياطية مع التاريخ والوقت
set DATETIME=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATETIME=%DATETIME: =0%
set BACKUP_NAME=housing_system_backup_%DATETIME%
set BACKUP_DIR=%USERPROFILE%\%BACKUP_NAME%

echo 📦 إنشاء مجلد النسخ الاحتياطي...
echo Creating backup directory: %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul

REM نسخ الملفات الأساسية
echo.
echo 📄 نسخ الملفات الأساسية...
echo Copying core files...

REM نسخ ملفات Python
xcopy /Y *.py "%BACKUP_DIR%\" >nul 2>&1
echo   ✓ Python files copied

REM نسخ قاعدة البيانات
xcopy /Y *.db "%BACKUP_DIR%\" >nul 2>&1
echo   ✓ Database files copied

REM نسخ ملفات التكوين
xcopy /Y requirements.txt "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y Procfile "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y runtime.txt "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y render.yaml "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y railway.json "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y vercel.json "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y config.py "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y .env.example "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y environment.yml "%BACKUP_DIR%\" >nul 2>&1
echo   ✓ Configuration files copied

REM نسخ ملفات Excel والبيانات
xcopy /Y *.xlsx "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y *.csv "%BACKUP_DIR%\" >nul 2>&1
echo   ✓ Data files (Excel, CSV) copied

REM نسخ سكريبتات التشغيل
xcopy /Y *.sh "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y *.bat "%BACKUP_DIR%\" >nul 2>&1
echo   ✓ Startup scripts copied

REM نسخ مجلد static
if exist "static\" (
    xcopy /E /I /Y "static\*" "%BACKUP_DIR%\static\" >nul 2>&1
    echo   ✓ Static files copied
)

REM نسخ مجلدات البيانات
if exist "uploads\" (
    xcopy /E /I /Y "uploads\*" "%BACKUP_DIR%\uploads\" >nul 2>&1
    echo   ✓ Uploads folder copied
)

if exist "processed_images\" (
    xcopy /E /I /Y "processed_images\*" "%BACKUP_DIR%\processed_images\" >nul 2>&1
    echo   ✓ Processed images copied
)

REM نسخ الوثائق المهمة
echo.
echo 📚 نسخ الوثائق...
echo Copying documentation...
xcopy /Y README*.md "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y QUICK_START.md "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y DEPLOYMENT*.md "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y SYSTEM_REVIEW_REPORT.md "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y TASK_COMPLETION_SUMMARY_AR.md "%BACKUP_DIR%\" >nul 2>&1
xcopy /Y LOCAL_SETUP_GUIDE.md "%BACKUP_DIR%\" >nul 2>&1
echo   ✓ Documentation copied

REM إنشاء ملف معلومات النسخة الاحتياطية
echo.
echo 📝 إنشاء ملف معلومات النسخة...
echo Creating backup info file...

(
echo نسخة احتياطية لنظام إدارة الإسكان الجامعي
echo Housing Management System Backup
echo.
echo التاريخ / Date: %date% %time%
echo الاسم / Name: %BACKUP_NAME%
echo المسار / Path: %BACKUP_DIR%
echo.
echo محتويات النسخة / Backup Contents:
echo - Python source files (*.py^)
echo - Database files (*.db^)
echo - Configuration files
echo - Data files (Excel, CSV^)
echo - Static files (HTML, CSS, JS^)
echo - Uploads and processed images
echo - Documentation files
echo.
echo لاستعادة النظام / To restore:
echo 1. انسخ جميع الملفات إلى مجلد جديد
echo    Copy all files to a new directory
echo.   
echo 2. ثبت المتطلبات:
echo    Install requirements:
echo    pip install -r requirements.txt
echo.   
echo 3. شغل التطبيق:
echo    Run the application:
echo    python app.py
echo.   
echo للمزيد من المعلومات، راجع:
echo For more information, see:
echo - README.md
echo - LOCAL_SETUP_GUIDE.md
echo - DEPLOYMENT.md
) > "%BACKUP_DIR%\BACKUP_INFO.txt"

echo   ✓ Backup info created

echo.
echo ==========================================
echo ✅ اكتملت النسخة الاحتياطية بنجاح!
echo ✅ Backup completed successfully!
echo ==========================================
echo.
echo 📍 الموقع / Location: %BACKUP_DIR%
echo.
echo فتح المجلد؟ / Open folder? (y/n^)
set /p OPEN_FOLDER=
if /i "%OPEN_FOLDER%"=="y" (
    explorer "%BACKUP_DIR%"
)

echo.
pause
