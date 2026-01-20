# ============================================================================
# Script PowerShell para executar a Dashboard do Sistema de Fila de Tarefas
# ============================================================================
#
# Este script verifica os pré-requisitos e inicia o servidor web
# Compatível com Windows PowerShell 5.0+
#
# Uso: .\run_dashboard.ps1
#
# NOTA: Se receber erro de execução, execute primeiro:
#       Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#

# Cores para output
function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERRO] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[*] $Message" -ForegroundColor Cyan
}

# Limpar tela
Clear-Host

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "   TASK QUEUE DASHBOARD - SISTEMA DE FILA DE TAREFAS" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
Write-Info "Verificando Python..."
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Python não foi encontrado!"
    Write-Host ""
    Write-Host "Solução:" -ForegroundColor Yellow
    Write-Host "1. Baixe Python em: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "2. Durante a instalação, MARQUE 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host "3. Reinicie o PowerShell e tente novamente" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione ENTER para sair"
    exit 1
}
Write-Success "$pythonVersion encontrado"

# Verificar se Flask está instalado
Write-Host ""
Write-Info "Verificando Flask..."
$flaskCheck = python -c "import flask" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Info "Instalando Flask..."
    pip install flask
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Falha ao instalar Flask!"
        Read-Host "Pressione ENTER para sair"
        exit 1
    }
}
Write-Success "Flask instalado"

# Verificar se o arquivo app.py existe
Write-Host ""
Write-Info "Verificando arquivo app.py..."
if (-not (Test-Path "app.py")) {
    Write-Error-Custom "Arquivo app.py não encontrado!"
    Write-Host "Certifique-se de estar no diretório correto: 04-task-queue" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione ENTER para sair"
    exit 1
}
Write-Success "app.py encontrado"

# Iniciar o servidor
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "   INICIANDO SERVIDOR WEB" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Acesse o painel em: " -NoNewline
Write-Host "http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "   Pressione Ctrl+C para encerrar o servidor" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Abrir navegador automaticamente (opcional)
Start-Process "http://localhost:5000"

# Executar o servidor
python app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Error-Custom "Ocorreu um erro durante a execução!"
    Write-Host ""
    Read-Host "Pressione ENTER para sair"
    exit 1
}

Read-Host "Pressione ENTER para sair"
exit 0
