REM filepath: d:\source\SGA\Product\Selenium_gitlab_automation\PytestSelenium.bat
@echo off

REM Kích hoạt môi trường ảo
call .\Scripts\activate.bat
IF ERRORLEVEL 1 (
    echo "Không thể kích hoạt môi trường ảo. Kiểm tra lại đường dẫn hoặc môi trường Python."
    exit /b 1
)

REM Chạy các lệnh pytest
pytest .\test\testrpa_finish_testcaseFB.py
pytest .\test\testrpa_create_testcaseFB.py

exit 0