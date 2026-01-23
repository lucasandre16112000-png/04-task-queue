#!/usr/bin/env python3
"""
Task Queue Launcher - Executável para Windows
Instala dependências, clona o projeto e inicia o servidor automaticamente
Compatível com Windows 7, 8, 10, 11

Desenvolvido por Lucas André S
GitHub: https://github.com/lucasandre16112000-png
"""

import os
import sys
import subprocess
import webbrowser
import time
import shutil
import json
from pathlib import Path
import threading
import socket
from urllib.request import urlopen
from urllib.error import URLError

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

PROJECT_NAME = "04-task-queue"
GITHUB_REPO = "https://github.com/lucasandre16112000-png/04-task-queue.git"
GITHUB_ZIP = "https://github.com/lucasandre16112000-png/04-task-queue/archive/refs/heads/main.zip"
LOCALHOST_URL = "http://localhost:5000"
INSTALL_DIR = Path.home() / "TaskQueue"
PROJECT_DIR = INSTALL_DIR / PROJECT_NAME

# ============================================================================
# CORES PARA TERMINAL
# ============================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def print_header(text):
    """Imprime cabeçalho"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    """Imprime mensagem informativa"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def print_warning(text):
    """Imprime aviso"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def run_command(cmd, shell=True, check=True):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python():
    """Verifica se Python está instalado"""
    print_info("Verificando Python...")
    success, stdout, stderr = run_command("python --version")
    
    if success:
        version = stdout.strip()
        print_success(f"Python encontrado: {version}")
        return True
    else:
        print_error("Python não foi encontrado!")
        print_warning("Você precisa instalar Python 3.8 ou superior")
        print_info("Baixe em: https://www.python.org/downloads/")
        print_warning("IMPORTANTE: Marque 'Add Python to PATH' durante a instalação")
        return False

def check_pip():
    """Verifica se pip está instalado"""
    print_info("Verificando pip...")
    success, stdout, stderr = run_command("pip --version")
    
    if success:
        print_success(f"pip encontrado: {stdout.strip()}")
        return True
    else:
        print_error("pip não foi encontrado!")
        return False

def check_git():
    """Verifica se Git está instalado"""
    print_info("Verificando Git...")
    success, stdout, stderr = run_command("git --version")
    
    if success:
        print_success(f"Git encontrado: {stdout.strip()}")
        return True
    else:
        print_warning("Git não foi encontrado (opcional)")
        return False

def install_flask():
    """Instala Flask"""
    print_info("Verificando Flask...")
    success, stdout, stderr = run_command("python -m pip show flask")
    
    if success:
        print_success("Flask já está instalado")
        return True
    
    print_info("Instalando Flask...")
    success, stdout, stderr = run_command("pip install flask --quiet")
    
    if success:
        print_success("Flask instalado com sucesso!")
        return True
    else:
        print_error(f"Erro ao instalar Flask: {stderr}")
        return False

def download_project():
    """Baixa o projeto do GitHub"""
    print_info(f"Baixando projeto de {GITHUB_REPO}...")
    
    # Criar diretório se não existir
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Tentar com Git primeiro
    git_available = check_git()
    
    if git_available:
        success, stdout, stderr = run_command(
            f"git clone {GITHUB_REPO} \"{PROJECT_DIR}\"",
            check=False
        )
        if success:
            print_success("Projeto clonado com sucesso!")
            return True
        else:
            print_warning("Falha ao clonar com Git, tentando download ZIP...")
    
    # Fallback: baixar ZIP
    try:
        import urllib.request
        import zipfile
        
        zip_path = INSTALL_DIR / "project.zip"
        print_info(f"Baixando arquivo ZIP...")
        
        urllib.request.urlretrieve(GITHUB_ZIP, zip_path)
        print_success("Arquivo baixado!")
        
        print_info("Extraindo arquivos...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(INSTALL_DIR)
        
        # Renomear pasta extraída
        extracted = INSTALL_DIR / "04-task-queue-main"
        if extracted.exists():
            if PROJECT_DIR.exists():
                shutil.rmtree(PROJECT_DIR)
            extracted.rename(PROJECT_DIR)
        
        zip_path.unlink()
        print_success("Projeto extraído com sucesso!")
        return True
        
    except Exception as e:
        print_error(f"Erro ao baixar projeto: {str(e)}")
        return False

def check_port_available(port=5000):
    """Verifica se a porta está disponível"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def wait_for_server(max_attempts=30):
    """Aguarda o servidor ficar online"""
    print_info("Aguardando servidor iniciar...")
    
    for attempt in range(max_attempts):
        try:
            response = urlopen(LOCALHOST_URL, timeout=2)
            if response.status == 200:
                print_success("Servidor está online!")
                return True
        except URLError:
            pass
        except Exception:
            pass
        
        time.sleep(1)
        print(f"  Tentativa {attempt + 1}/{max_attempts}...", end='\r')
    
    print_warning("Timeout ao aguardar servidor")
    return False

def start_server():
    """Inicia o servidor Flask"""
    print_info("Iniciando servidor Flask...")
    
    if not check_port_available(5000):
        print_warning("Porta 5000 já está em uso!")
        print_info("Tentando usar porta alternativa...")
        # Poderia tentar outra porta aqui
    
    # Mudar para diretório do projeto
    os.chdir(PROJECT_DIR)
    
    # Iniciar servidor em thread separada
    def run_server():
        try:
            subprocess.Popen(
                [sys.executable, "app.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
        except Exception as e:
            print_error(f"Erro ao iniciar servidor: {str(e)}")
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    
    return wait_for_server()

def open_browser():
    """Abre o navegador na dashboard"""
    print_info("Abrindo navegador...")
    try:
        webbrowser.open(LOCALHOST_URL)
        print_success(f"Navegador aberto em {LOCALHOST_URL}")
        return True
    except Exception as e:
        print_error(f"Erro ao abrir navegador: {str(e)}")
        print_info(f"Acesse manualmente: {LOCALHOST_URL}")
        return False

def main():
    """Função principal"""
    print_header("🚀 TASK QUEUE - LAUNCHER")
    
    # Passo 1: Verificar Python
    print_header("PASSO 1: Verificando Pré-requisitos")
    if not check_python():
        print_error("Python é obrigatório!")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
    
    if not check_pip():
        print_error("pip é obrigatório!")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
    
    # Passo 2: Instalar dependências
    print_header("PASSO 2: Instalando Dependências")
    if not install_flask():
        print_error("Falha ao instalar dependências!")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
    
    # Passo 3: Baixar projeto
    print_header("PASSO 3: Baixando Projeto")
    if not PROJECT_DIR.exists():
        if not download_project():
            print_error("Falha ao baixar projeto!")
            input("\nPressione ENTER para sair...")
            sys.exit(1)
    else:
        print_success(f"Projeto já existe em {PROJECT_DIR}")
    
    # Passo 4: Iniciar servidor
    print_header("PASSO 4: Iniciando Servidor")
    if not start_server():
        print_error("Falha ao iniciar servidor!")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
    
    # Passo 5: Abrir navegador
    print_header("PASSO 5: Abrindo Dashboard")
    open_browser()
    
    # Mensagem final
    print_header("✓ TUDO PRONTO!")
    print(f"{Colors.GREEN}A Dashboard está rodando em {LOCALHOST_URL}{Colors.ENDC}")
    print(f"{Colors.BLUE}Pressione Ctrl+C para encerrar{Colors.ENDC}\n")
    
    # Manter executável aberto
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Encerrando...{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"Erro inesperado: {str(e)}")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
