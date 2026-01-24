@echo off
cls
color 0A

echo.
echo ================================================================================
echo                    TASK QUEUE LAUNCHER - INICIANDO...
echo ================================================================================
echo.

cd /d "%~dp0"

echo [PASSO 1] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK]
echo.

echo [PASSO 2] Verificando Flask...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalando Flask...
    pip install flask --quiet
)
echo [OK]
echo.

echo [PASSO 3] Preparando arquivos...
set INSTALL_DIR=%USERPROFILE%\TaskQueue
set PROJECT_DIR=%INSTALL_DIR%\04-task-queue

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

if exist "%PROJECT_DIR%" (
    echo [OK] Projeto ja existe
    goto :start
)

echo Baixando projeto...
cd /d "%INSTALL_DIR%"

git --version >nul 2>&1
if errorlevel 0 (
    git clone https://github.com/lucasandre16112000-png/04-task-queue.git "%PROJECT_DIR%" >nul 2>&1
    if errorlevel 0 goto :start
)

powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/lucasandre16112000-png/04-task-queue/archive/refs/heads/main.zip', '%INSTALL_DIR%\project.zip')" >nul 2>&1
powershell -Command "Expand-Archive -Path '%INSTALL_DIR%\project.zip' -DestinationPath '%INSTALL_DIR%' -Force" >nul 2>&1

if exist "%INSTALL_DIR%\04-task-queue-main" (
    ren "%INSTALL_DIR%\04-task-queue-main" "04-task-queue"
)
del "%INSTALL_DIR%\project.zip" >nul 2>&1
echo [OK] Projeto extraido
echo.

:start
echo [PASSO 4] Iniciando servidor...
cd /d "%PROJECT_DIR%"
start "" /B python app.py
echo [OK] Servidor iniciado
echo.

echo Abrindo navegador em 2 segundos...
timeout /t 2 /nobreak >nul

start http://localhost:5000

echo.
echo ================================================================================
echo                    PRONTO! Dashboard abrindo...
echo                    Acesse: http://localhost:5000
echo ================================================================================
echo.

timeout /t 2 /nobreak >nul

exit /b 0
