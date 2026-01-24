@echo off
cls
color 0A

echo.
echo ================================================================================
echo                    TASK QUEUE DASHBOARD
echo ================================================================================
echo.

cd /d "%~dp0"

echo [1] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK]
echo.

echo [2] Verificando Flask...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalando Flask...
    pip install flask --quiet
)
echo [OK]
echo.

echo [3] Iniciando servidor...
start "" /B python app.py

echo [OK] Servidor iniciado
echo.

echo Abrindo navegador em 2 segundos...
timeout /t 2 /nobreak >nul

start http://localhost:5000

echo.
echo ================================================================================
echo Dashboard: http://localhost:5000
echo ================================================================================
echo.

pause
