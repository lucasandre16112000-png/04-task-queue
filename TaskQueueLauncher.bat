@echo off
REM ============================================================================
REM TASK QUEUE LAUNCHER - Executável para Windows
REM Instala tudo automaticamente e inicia a dashboard com 1 clique
REM ============================================================================
REM
REM Compatível com: Windows 7, 8, 10, 11
REM Desenvolvido por: Lucas André S
REM GitHub: https://github.com/lucasandre16112000-png
REM
REM ============================================================================

setlocal enabledelayedexpansion

REM Configurações
set PROJECT_NAME=04-task-queue
set GITHUB_REPO=https://github.com/lucasandre16112000-png/04-task-queue.git
set GITHUB_ZIP=https://github.com/lucasandre16112000-png/04-task-queue/archive/refs/heads/main.zip
set LOCALHOST_URL=http://localhost:5000
set INSTALL_DIR=%USERPROFILE%\TaskQueue
set PROJECT_DIR=%INSTALL_DIR%\%PROJECT_NAME%

REM Cores (usando códigos ANSI)
set GREEN=[92m
set RED=[91m
set YELLOW=[93m
set BLUE=[94m
set CYAN=[96m
set BOLD=[1m
set RESET=[0m

REM ============================================================================
REM FUNÇÕES
REM ============================================================================

:print_header
    cls
    echo.
    echo ================================================================================
    echo    TASK QUEUE LAUNCHER
    echo ================================================================================
    echo.
    goto :eof

:print_success
    echo [OK] %~1
    goto :eof

:print_error
    echo [ERRO] %~1
    goto :eof

:print_info
    echo [*] %~1
    goto :eof

:print_warning
    echo [!] %~1
    goto :eof

:check_python
    call :print_info "Verificando Python..."
    python --version >nul 2>&1
    if errorlevel 1 (
        call :print_error "Python nao foi encontrado!"
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
    call :print_success "%PYTHON_VERSION% encontrado"
    goto :eof

:check_pip
    call :print_info "Verificando pip..."
    pip --version >nul 2>&1
    if errorlevel 1 (
        call :print_error "pip nao foi encontrado!"
        pause
        exit /b 1
    )
    call :print_success "pip encontrado"
    goto :eof

:install_flask
    call :print_info "Verificando Flask..."
    python -c "import flask" >nul 2>&1
    if errorlevel 1 (
        call :print_info "Instalando Flask..."
        pip install flask --quiet
        if errorlevel 1 (
            call :print_error "Erro ao instalar Flask!"
            pause
            exit /b 1
        )
    )
    call :print_success "Flask instalado"
    goto :eof

:download_project
    call :print_info "Verificando se projeto ja existe..."
    if exist "%PROJECT_DIR%" (
        call :print_success "Projeto ja existe em %PROJECT_DIR%"
        goto :eof
    )
    
    call :print_info "Criando diretorio de instalacao..."
    if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
    
    call :print_info "Baixando projeto do GitHub..."
    call :print_info "Tentando com Git..."
    
    git --version >nul 2>&1
    if errorlevel 1 (
        call :print_warning "Git nao encontrado, usando download ZIP..."
        goto :download_zip
    )
    
    cd /d "%INSTALL_DIR%"
    git clone %GITHUB_REPO% "%PROJECT_DIR%" >nul 2>&1
    if errorlevel 1 (
        call :print_warning "Falha ao clonar com Git, tentando ZIP..."
        goto :download_zip
    )
    
    call :print_success "Projeto clonado com sucesso!"
    goto :eof

:download_zip
    call :print_info "Baixando arquivo ZIP..."
    
    REM Usar PowerShell para baixar arquivo
    powershell -Command "try { (New-Object System.Net.WebClient).DownloadFile('%GITHUB_ZIP%', '%INSTALL_DIR%\project.zip'); Write-Host 'OK' } catch { exit 1 }" >nul 2>&1
    
    if errorlevel 1 (
        call :print_error "Erro ao baixar projeto!"
        pause
        exit /b 1
    )
    
    call :print_success "Arquivo baixado!"
    call :print_info "Extraindo arquivos..."
    
    REM Usar PowerShell para extrair ZIP
    powershell -Command "Expand-Archive -Path '%INSTALL_DIR%\project.zip' -DestinationPath '%INSTALL_DIR%' -Force" >nul 2>&1
    
    if errorlevel 1 (
        call :print_error "Erro ao extrair arquivo!"
        pause
        exit /b 1
    )
    
    REM Renomear pasta extraída
    if exist "%INSTALL_DIR%\04-task-queue-main" (
        if exist "%PROJECT_DIR%" rmdir /s /q "%PROJECT_DIR%"
        ren "%INSTALL_DIR%\04-task-queue-main" "%PROJECT_NAME%"
    )
    
    REM Deletar ZIP
    if exist "%INSTALL_DIR%\project.zip" del "%INSTALL_DIR%\project.zip"
    
    call :print_success "Projeto extraido com sucesso!"
    goto :eof

:start_server
    call :print_info "Iniciando servidor Flask..."
    
    cd /d "%PROJECT_DIR%"
    
    REM Iniciar servidor em background
    start /B python app.py >nul 2>&1
    
    call :print_info "Aguardando servidor iniciar..."
    
    REM Aguardar servidor ficar online (máximo 30 tentativas)
    setlocal enabledelayedexpansion
    set /a attempts=0
    :wait_loop
    set /a attempts=!attempts!+1
    
    if !attempts! gtr 30 (
        call :print_warning "Timeout ao aguardar servidor"
        goto :open_browser
    )
    
    REM Verificar se servidor está respondendo
    powershell -Command "try { $response = Invoke-WebRequest -Uri '%LOCALHOST_URL%' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
    
    if errorlevel 1 (
        timeout /t 1 /nobreak >nul
        goto :wait_loop
    )
    
    call :print_success "Servidor esta online!"
    goto :eof

:open_browser
    call :print_info "Abrindo navegador..."
    
    REM Abrir URL no navegador padrão
    start %LOCALHOST_URL%
    
    call :print_success "Navegador aberto!"
    goto :eof

REM ============================================================================
REM PROGRAMA PRINCIPAL
REM ============================================================================

:main
    call :print_header
    
    REM Passo 1: Verificar pré-requisitos
    echo [PASSO 1] Verificando Pre-requisitos
    echo.
    call :check_python
    call :check_pip
    echo.
    
    REM Passo 2: Instalar dependências
    echo [PASSO 2] Instalando Dependencias
    echo.
    call :install_flask
    echo.
    
    REM Passo 3: Baixar projeto
    echo [PASSO 3] Baixando Projeto
    echo.
    call :download_project
    echo.
    
    REM Passo 4: Iniciar servidor
    echo [PASSO 4] Iniciando Servidor
    echo.
    call :start_server
    echo.
    
    REM Passo 5: Abrir navegador
    echo [PASSO 5] Abrindo Dashboard
    echo.
    call :open_browser
    echo.
    
    REM Mensagem final
    cls
    echo.
    echo ================================================================================
    echo    TASK QUEUE - PRONTO PARA USAR!
    echo ================================================================================
    echo.
    echo    Dashboard: %LOCALHOST_URL%
    echo.
    echo    A janela pode ser minimizada. Para encerrar, feche a janela do servidor.
    echo.
    echo ================================================================================
    echo.
    
    REM Manter janela aberta
    pause
    
    goto :eof

REM ============================================================================
REM EXECUÇÃO
REM ============================================================================

call :main
exit /b 0
