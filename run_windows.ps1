# ============================================================================
# Script PowerShell para executar o Sistema de Fila de Tarefas no Windows
# ============================================================================
#
# Este script verifica os pré-requisitos e executa o worker.py
# Compatível com Windows PowerShell 5.0+
#
# Uso: .\run_windows.ps1
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

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "[AVISO] $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "[*] $Message" -ForegroundColor Cyan
}

# Limpar tela
Clear-Host

Write-Host ""
Write-Host "================================================================================`n" -ForegroundColor Cyan
Write-Host "SISTEMA DE FILA DE TAREFAS DISTRIBUÍDO - WINDOWS`n" -ForegroundColor Cyan
Write-Host "================================================================================`n" -ForegroundColor Cyan

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

# Verificar Git (opcional)
Write-Host ""
Write-Info "Verificando Git..."
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "$gitVersion encontrado"
} else {
    Write-Warning-Custom "Git não foi encontrado (opcional)"
    Write-Host "Baixe em: https://git-scm.com/downloads" -ForegroundColor Yellow
}

# Verificar se o arquivo worker_windows.py existe
Write-Host ""
Write-Info "Verificando arquivo worker_windows.py..."
if (-not (Test-Path "worker_windows.py")) {
    Write-Error-Custom "Arquivo worker_windows.py não encontrado!"
    Write-Host "Certifique-se de estar no diretório correto: 04-task-queue" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione ENTER para sair"
    exit 1
}
Write-Success "worker_windows.py encontrado"

# Executar o worker
Write-Host ""
Write-Host "================================================================================`n" -ForegroundColor Cyan
Write-Host "EXECUTANDO SISTEMA DE FILA DE TAREFAS`n" -ForegroundColor Cyan
Write-Host "================================================================================`n" -ForegroundColor Cyan

python worker_windows.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Error-Custom "Ocorreu um erro durante a execução!"
    Write-Host ""
    Read-Host "Pressione ENTER para sair"
    exit 1
}

Write-Host ""
Write-Success "Execução concluída com sucesso!"
Write-Host ""
Read-Host "Pressione ENTER para sair"
exit 0
