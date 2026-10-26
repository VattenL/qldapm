@echo off
if "%~1"=="" (
    echo ========================================================
    echo HUONG DAN DUNG: export_word.bat ^<duong_dan_file_markdown^>
    echo Vi du: export_word.bat docs\forms\2-27-team-charter.en.md
    echo ========================================================
    pause
    exit /b
)
echo ========================================================
echo DANG XUAT FILE WORD (.DOCX)...
echo ========================================================
py .claude/skills/pm/scripts/md_to_docx.py %*
echo.
echo ========================================================
echo HOAN TAT XUAT FILE WORD!
echo ========================================================
pause
