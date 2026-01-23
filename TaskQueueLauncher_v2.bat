@echo off
REM ============================================================================
REM TASK QUEUE LAUNCHER v2 - VERSAO FINAL
REM Executável para Windows - Instala e roda tudo automaticamente
REM ============================================================================

setlocal enabledelayedexpansion

REM Cores
cls
color 0A

echo.
echo ================================================================================
echo.
echo                    TASK QUEUE LAUNCHER - INICIANDO...
echo.
echo ================================================================================
echo.

REM Ir para a pasta do script
cd /d "%~dp0"

REM Passo 1: Verificar Python
echo [PASSO 1] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao foi encontrado!
    echo.
    echo Solucao:
    echo 1. Baixe Python em: https://www.python.org/downloads/
    echo 2. MARQUE "Add Python to PATH" durante a instalacao
    echo 3. Reinicie o computador
    echo 4. Tente novamente
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% encontrado
echo.

REM Passo 2: Instalar Flask
echo [PASSO 2] Verificando/Instalando Flask...
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

REM Passo 3: Criar diretorio de instalacao
echo [PASSO 3] Preparando arquivos...
set INSTALL_DIR=%USERPROFILE%\TaskQueue
set PROJECT_DIR=%INSTALL_DIR%\04-task-queue

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo [OK] Diretorio criado
echo.

REM Passo 4: Verificar se projeto existe
if exist "%PROJECT_DIR%" (
    echo [OK] Projeto ja existe
    goto :start_server
)

REM Passo 5: Baixar projeto
echo [PASSO 4] Baixando projeto do GitHub...

REM Tentar com Git
git --version >nul 2>&1
if errorlevel 0 (
    cd /d "%INSTALL_DIR%"
    git clone https://github.com/lucasandre16112000-png/04-task-queue.git "%PROJECT_DIR%" >nul 2>&1
    if errorlevel 0 (
        echo [OK] Projeto clonado com Git
        goto :start_server
    )
)

REM Fallback: Baixar ZIP
echo Baixando arquivo ZIP...
cd /d "%INSTALL_DIR%"

powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/lucasandre16112000-png/04-task-queue/archive/refs/heads/main.zip', '%INSTALL_DIR%\project.zip')" >nul 2>&1

if errorlevel 1 (
    echo [ERRO] Falha ao baixar projeto!
    pause
    exit /b 1
)

echo Extraindo arquivos...
powershell -Command "Expand-Archive -Path '%INSTALL_DIR%\project.zip' -DestinationPath '%INSTALL_DIR%' -Force" >nul 2>&1

if exist "%INSTALL_DIR%\04-task-queue-main" (
    ren "%INSTALL_DIR%\04-task-queue-main" "04-task-queue"
)

del "%INSTALL_DIR%\project.zip" >nul 2>&1
echo [OK] Projeto extraido
echo.

REM Passo 6: Iniciar servidor
:start_server
echo [PASSO 5] Iniciando servidor...
cd /d "%PROJECT_DIR%"

REM Iniciar Flask em background (sem janela)
start "" /B python app.py

echo Aguardando servidor iniciar...

REM Aguardar servidor ficar online (máximo 30 segundos)
set /a count=0
:wait_loop
set /a count=!count!+1

if !count! gtr 30 (
    echo [AVISO] Timeout ao aguardar servidor
    goto :open_browser
)

REM Tentar conectar ao servidor usando PowerShell
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000' -TimeoutSec 1 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1

if errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto :wait_loop
)

echo [OK] Servidor esta online!
echo.

REM Passo 7: Abrir navegador
:open_browser
echo [PASSO 6] Abrindo dashboard...
start http://localhost:5000

echo.
echo ================================================================================
echo.
echo                    PRONTO! Dashboard abrindo...
echo.
echo                    Acesse: http://localhost:5000
echo.
echo ================================================================================
echo.

timeout /t 2 /nobreak >nul

exit /b 0
