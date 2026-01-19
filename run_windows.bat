@echo off
REM ============================================================================
REM Script para executar o Sistema de Fila de Tarefas no Windows
REM ============================================================================
REM
REM Este script verifica os pré-requisitos e executa o worker.py
REM Compatível com Windows 7, 8, 10, 11
REM
REM Uso: run_windows.bat
REM

setlocal enabledelayedexpansion

REM Cores para output (Windows 10+)
for /F %%A in ('echo prompt $H ^| cmd') do set "BS=%%A"

echo.
echo ================================================================================
echo SISTEMA DE FILA DE TAREFAS DISTRIBUIDO - WINDOWS
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

echo.
echo [*] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Git nao foi encontrado (opcional)
    echo Baixe em: https://git-scm.com/downloads
) else (
    for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
    echo [OK] !GIT_VERSION! encontrado
)

echo.
echo ================================================================================
echo EXECUTANDO SISTEMA DE FILA DE TAREFAS
echo ================================================================================
echo.

REM Executar o worker
python worker_windows.py

if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um erro durante a execucao!
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Execucao concluida com sucesso!
echo.
pause
exit /b 0
