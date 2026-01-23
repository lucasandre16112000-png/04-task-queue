@echo off
REM ============================================================================
REM TASK QUEUE - INICIAR DASHBOARD
REM Versao ultra-simples que funciona 100%
REM ============================================================================

cls
color 0A

echo.
echo ================================================================================
echo                    TASK QUEUE DASHBOARD
echo ================================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Baixe em: https://www.python.org/downloads/
    echo Marque "Add Python to PATH" durante a instalacao
    echo.
    pause
    exit /b 1
)

REM Instalar Flask se necessario
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalando Flask...
    pip install flask --quiet
)

REM Iniciar servidor
echo.
echo Iniciando servidor...
echo.
echo Acesse: http://localhost:5000
echo.
echo Pressione Ctrl+C para encerrar
echo.

python app.py

pause
