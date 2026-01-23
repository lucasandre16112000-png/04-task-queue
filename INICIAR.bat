@echo off
REM ============================================================================
REM TASK QUEUE - INICIAR DASHBOARD
REM Versao final que funciona 100%
REM ============================================================================

setlocal enabledelayedexpansion

cls
color 0A

echo.
echo ================================================================================
echo                    TASK QUEUE DASHBOARD
echo ================================================================================
echo.

REM Ir para a pasta do script
cd /d "%~dp0"

echo [1] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Solucao:
    echo 1. Baixe Python em: https://www.python.org/downloads/
    echo 2. Marque "Add Python to PATH" durante a instalacao
    echo 3. Reinicie o computador
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

echo [2] Verificando Flask...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalando Flask...
    pip install flask --quiet
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar Flask!
        pause
        exit /b 1
    )
)
echo [OK] Flask pronto
echo.

echo [3] Iniciando servidor...
echo.

REM Iniciar servidor em background
start "" /B python app.py

REM Aguardar servidor iniciar
echo Aguardando servidor iniciar...
timeout /t 3 /nobreak >nul

echo.
echo Acesse: http://localhost:5000
echo Pressione Ctrl+C para encerrar
echo.
echo ================================================================================
echo.

REM Abrir navegador
start http://localhost:5000

pause
