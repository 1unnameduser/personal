@echo off
pushd "%~dp0"
rem SFK is required -- https://www.stahlworks.com/

python -m pip install --force-reinstall --upgrade pip
pip freeze > "%temp%\requirements.txt"
sfk rep "%temp%\requirements.txt" "/==/>=/" -yes
pip install -r "%temp%\requirements.txt" --upgrade
del /f /q "%temp%\requirements.txt"
rem опционально, если хочется очистить кеш пип
rem pip cache purge
