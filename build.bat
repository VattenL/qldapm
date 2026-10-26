@echo off
echo ========================================================
echo DANG BIEN DICH TAI LIEU MARKDOWN SANG HTML VA PDF...
echo ========================================================
py build.py %*
echo.
echo ========================================================
echo HOAN TAT! Kiem tra cac file PDF tai thu muc: build\
echo ========================================================
pause
