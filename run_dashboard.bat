@echo off
REM ============================================================================
REM Script para executar a Dashboard do Sistema de Fila de Tarefas no Windows
REM ============================================================================
REM
REM Este script verifica os pré-requisitos e inicia o servidor web
REM Compatível com Windows 7, 8, 10, 11
REM
REM Uso: run_dashboard.bat
REM

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo    TASK QUEUE DASHBOARD - SISTEMA DE FILA DE TAREFAS
echo ================================================================================
echo.

REM Verificar se Python está instalado
echo [*] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao foi encontrado!
    echo.
    echo Solucao:
    echo 1. Baixe Python em: https://www.python.org/downloads/
    echo 2. Durante a instalacao, MARQUE "Add Python to PATH"
    echo 3. Reinicie o terminal e tente novamente
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% encontrado

REM Verificar se Flask está instalado
echo.
echo [*] Verificando Flask...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [*] Instalando Flask...
    pip install flask
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar Flask!
        pause
        exit /b 1
    )
)
echo [OK] Flask instalado

echo.
echo ================================================================================
echo    INICIANDO SERVIDOR WEB
echo ================================================================================
echo.
echo    Acesse o painel em: http://localhost:5000
echo.
echo    Pressione Ctrl+C para encerrar o servidor
echo.
echo ================================================================================
echo.

REM Iniciar o servidor
python app.py

if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um erro durante a execucao!
    echo.
    pause
    exit /b 1
)

pause
exit /b 0
