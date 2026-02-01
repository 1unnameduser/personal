@echo off
pushd "%~dp0"

:bkp
    rem For /f "delims=" %%a in ('sfk time') do sfk list . .TwoWorldsSave +zipto _bkp\TwoWorldsSave_%%~a.zip -yes
    for /f "delims=" %%a in ('dir /b 02*.TwoWorldsSave') do set file=%%~a
    if %errorlevel%==0 (
        for /f "delims= " %%a in ('busybox md5sum %file%') do (
            if not exist _bkp\%%~a.zip (
                sfk list %file% +zipto _bkp\%%~a.zip -yes
                for /F "skip=3 delims=" %%a in ('dir /O-D /A-D /B "_bkp\*"') do del /f /q "_bkp\%%a"
            )
        )
    ) else (
        echo ФАЙЛ БЫСТРОГО СОХРАНЕНИЯ НЕ НАЙДЕН
    )
    timeout /t 30
goto bkp
