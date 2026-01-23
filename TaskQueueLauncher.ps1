#!/usr/bin/env powershell
<#
.SYNOPSIS
    Task Queue Launcher - Executável para Windows
    Instala tudo automaticamente e inicia a dashboard

.DESCRIPTION
    Script PowerShell que automatiza a instalação e execução do Task Queue
    Compatível com Windows 7, 8, 10, 11

.AUTHOR
    Lucas André S
    GitHub: https://github.com/lucasandre16112000-png

.VERSION
    1.0.0
#>

param(
    [switch]$NoOpen = $false
)

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

$ProjectName = "04-task-queue"
$GitHubRepo = "https://github.com/lucasandre16112000-png/04-task-queue.git"
$GitHubZip = "https://github.com/lucasandre16112000-png/04-task-queue/archive/refs/heads/main.zip"
$LocalhostUrl = "http://localhost:5000"
$InstallDir = Join-Path $env:USERPROFILE "TaskQueue"
$ProjectDir = Join-Path $InstallDir $ProjectName

# ============================================================================
# CORES E FORMATAÇÃO
# ============================================================================

function Write-Header {
    param([string]$Text)
    Clear-Host
    Write-Host "`n" -NoNewline
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host $Text.PadLeft(35 + $Text.Length / 2) -ForegroundColor Cyan -BackgroundColor Black
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "`n" -NoNewline
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor Green
}

function Write-Error {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor Red
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ $Text" -ForegroundColor Blue
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor Yellow
}

# ============================================================================
# FUNÇÕES DE VERIFICAÇÃO
# ============================================================================

function Check-Python {
    Write-Info "Verificando Python..."
    
    try {
        $version = python --version 2>&1
        Write-Success "Python encontrado: $version"
        return $true
    }
    catch {
        Write-Error "Python não foi encontrado!"
        Write-Warning "Você precisa instalar Python 3.8 ou superior"
        Write-Info "Baixe em: https://www.python.org/downloads/"
        Write-Warning "IMPORTANTE: Marque 'Add Python to PATH' durante a instalação"
        return $false
    }
}

function Check-Pip {
    Write-Info "Verificando pip..."
    
    try {
        $version = pip --version 2>&1
        Write-Success "pip encontrado: $version"
        return $true
    }
    catch {
        Write-Error "pip não foi encontrado!"
        return $false
    }
}

function Check-Git {
    Write-Info "Verificando Git..."
    
    try {
        $version = git --version 2>&1
        Write-Success "Git encontrado: $version"
        return $true
    }
    catch {
        Write-Warning "Git não foi encontrado (opcional)"
        return $false
    }
}

function Install-Flask {
    Write-Info "Verificando Flask..."
    
    try {
        python -c "import flask" 2>&1 | Out-Null
        Write-Success "Flask já está instalado"
        return $true
    }
    catch {
        Write-Info "Instalando Flask..."
        
        try {
            pip install flask --quiet
            Write-Success "Flask instalado com sucesso!"
            return $true
        }
        catch {
            Write-Error "Erro ao instalar Flask: $_"
            return $false
        }
    }
}

# ============================================================================
# FUNÇÕES DE DOWNLOAD E INSTALAÇÃO
# ============================================================================

function Download-Project {
    Write-Info "Verificando se projeto já existe..."
    
    if (Test-Path $ProjectDir) {
        Write-Success "Projeto já existe em $ProjectDir"
        return $true
    }
    
    Write-Info "Criando diretório de instalação..."
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }
    
    # Tentar com Git primeiro
    $gitAvailable = Check-Git
    
    if ($gitAvailable) {
        Write-Info "Clonando repositório com Git..."
        try {
            Push-Location $InstallDir
            git clone $GitHubRepo $ProjectDir 2>&1 | Out-Null
            Pop-Location
            Write-Success "Projeto clonado com sucesso!"
            return $true
        }
        catch {
            Write-Warning "Falha ao clonar com Git, tentando download ZIP..."
            Pop-Location
        }
    }
    
    # Fallback: download ZIP
    return Download-ProjectZip
}

function Download-ProjectZip {
    Write-Info "Baixando arquivo ZIP..."
    
    try {
        $zipPath = Join-Path $InstallDir "project.zip"
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($GitHubZip, $zipPath)
        
        Write-Success "Arquivo baixado!"
        Write-Info "Extraindo arquivos..."
        
        Expand-Archive -Path $zipPath -DestinationPath $InstallDir -Force
        
        # Renomear pasta extraída
        $extractedPath = Join-Path $InstallDir "04-task-queue-main"
        if (Test-Path $extractedPath) {
            if (Test-Path $ProjectDir) {
                Remove-Item -Path $ProjectDir -Recurse -Force
            }
            Rename-Item -Path $extractedPath -NewName $ProjectName
        }
        
        # Deletar ZIP
        Remove-Item -Path $zipPath -Force
        
        Write-Success "Projeto extraído com sucesso!"
        return $true
    }
    catch {
        Write-Error "Erro ao baixar/extrair projeto: $_"
        return $false
    }
}

# ============================================================================
# FUNÇÕES DE SERVIDOR
# ============================================================================

function Start-Server {
    Write-Info "Iniciando servidor Flask..."
    
    try {
        Push-Location $ProjectDir
        
        # Iniciar servidor em background
        $process = Start-Process python -ArgumentList "app.py" -WindowStyle Hidden -PassThru
        
        Write-Info "Aguardando servidor iniciar..."
        
        # Aguardar servidor ficar online
        $maxAttempts = 30
        $attempt = 0
        
        while ($attempt -lt $maxAttempts) {
            $attempt++
            
            try {
                $response = Invoke-WebRequest -Uri $LocalhostUrl -TimeoutSec 2 -ErrorAction Stop
                if ($response.StatusCode -eq 200) {
                    Write-Success "Servidor está online!"
                    Pop-Location
                    return $true
                }
            }
            catch {
                Start-Sleep -Seconds 1
            }
        }
        
        Write-Warning "Timeout ao aguardar servidor"
        Pop-Location
        return $false
    }
    catch {
        Write-Error "Erro ao iniciar servidor: $_"
        Pop-Location
        return $false
    }
}

function Open-Browser {
    Write-Info "Abrindo navegador..."
    
    try {
        Start-Process $LocalhostUrl
        Write-Success "Navegador aberto!"
        return $true
    }
    catch {
        Write-Error "Erro ao abrir navegador: $_"
        Write-Info "Acesse manualmente: $LocalhostUrl"
        return $false
    }
}

# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

function Main {
    Write-Header "🚀 TASK QUEUE LAUNCHER"
    
    # Passo 1: Verificar pré-requisitos
    Write-Host "[PASSO 1] Verificando Pré-requisitos" -ForegroundColor Cyan
    Write-Host ""
    
    if (-not (Check-Python)) {
        Write-Error "Python é obrigatório!"
        Read-Host "Pressione ENTER para sair"
        exit 1
    }
    
    if (-not (Check-Pip)) {
        Write-Error "pip é obrigatório!"
        Read-Host "Pressione ENTER para sair"
        exit 1
    }
    
    Write-Host ""
    
    # Passo 2: Instalar dependências
    Write-Host "[PASSO 2] Instalando Dependências" -ForegroundColor Cyan
    Write-Host ""
    
    if (-not (Install-Flask)) {
        Write-Error "Falha ao instalar dependências!"
        Read-Host "Pressione ENTER para sair"
        exit 1
    }
    
    Write-Host ""
    
    # Passo 3: Baixar projeto
    Write-Host "[PASSO 3] Baixando Projeto" -ForegroundColor Cyan
    Write-Host ""
    
    if (-not (Download-Project)) {
        Write-Error "Falha ao baixar projeto!"
        Read-Host "Pressione ENTER para sair"
        exit 1
    }
    
    Write-Host ""
    
    # Passo 4: Iniciar servidor
    Write-Host "[PASSO 4] Iniciando Servidor" -ForegroundColor Cyan
    Write-Host ""
    
    if (-not (Start-Server)) {
        Write-Error "Falha ao iniciar servidor!"
        Read-Host "Pressione ENTER para sair"
        exit 1
    }
    
    Write-Host ""
    
    # Passo 5: Abrir navegador
    if (-not $NoOpen) {
        Write-Host "[PASSO 5] Abrindo Dashboard" -ForegroundColor Cyan
        Write-Host ""
        Open-Browser
        Write-Host ""
    }
    
    # Mensagem final
    Clear-Host
    Write-Host "`n" -NoNewline
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "✓ TASK QUEUE - PRONTO PARA USAR!" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "`n" -NoNewline
    Write-Host "Dashboard: $LocalhostUrl" -ForegroundColor Green
    Write-Host "`n" -NoNewline
    Write-Host "A janela pode ser minimizada. Para encerrar, feche a janela do servidor." -ForegroundColor Blue
    Write-Host "`n" -NoNewline
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "`n" -NoNewline
    
    # Manter janela aberta
    Read-Host "Pressione ENTER para sair"
}

# ============================================================================
# EXECUÇÃO
# ============================================================================

try {
    Main
}
catch {
    Write-Error "Erro inesperado: $_"
    Read-Host "Pressione ENTER para sair"
    exit 1
}
