@echo off
python -m PyInstaller --onefile --name organizador organizador/__main__.py
if errorlevel 1 echo ERRO! else echo OK - dist\organizador.exe
