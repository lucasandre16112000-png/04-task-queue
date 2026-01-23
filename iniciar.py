#!/usr/bin/env python3
"""
Task Queue - Iniciar Dashboard
Script simples que funciona 100%
"""

import subprocess
import sys
import time
import webbrowser
import os
import socket
from urllib.request import urlopen
from urllib.error import URLError

def is_server_running(host='localhost', port=5000, timeout=2):
    """Verifica se o servidor está respondendo"""
    try:
        response = urlopen(f'http://{host}:{port}', timeout=timeout)
        return response.status == 200
    except (URLError, Exception):
        return False

def wait_for_server(max_attempts=30):
    """Aguarda o servidor ficar online"""
    print("Aguardando servidor iniciar...", end='', flush=True)
    
    for attempt in range(max_attempts):
        if is_server_running():
            print("\n[OK] Servidor está online!")
            return True
        
        print(".", end='', flush=True)
        time.sleep(1)
    
    print("\n[AVISO] Timeout ao aguardar servidor")
    return False

def main():
    # Mudar para a pasta do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("\n" + "="*70)
    print("TASK QUEUE DASHBOARD".center(70))
    print("="*70 + "\n")
    
    # Verificar Python
    print("[1] Verificando Python...")
    print(f"    Python {sys.version.split()[0]} OK\n")
    
    # Instalar Flask
    print("[2] Verificando Flask...")
    try:
        import flask
        print(f"    Flask OK\n")
    except ImportError:
        print("    Instalando Flask...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask", "--quiet"], check=True)
            print("    Flask instalado OK\n")
        except:
            print("    [ERRO] Falha ao instalar Flask!")
            input("Pressione ENTER para sair...")
            sys.exit(1)
    
    # Iniciar servidor
    print("[3] Iniciando servidor...\n")
    
    # Iniciar Flask em background
    try:
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar servidor: {e}")
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    # Aguardar servidor ficar online
    if not wait_for_server():
        print("[AVISO] Servidor pode estar iniciando...")
    
    print()
    print("    Acesse: http://localhost:5000")
    print("    Pressione Ctrl+C para encerrar\n")
    print("="*70 + "\n")
    
    # Abrir navegador
    time.sleep(1)
    try:
        webbrowser.open("http://localhost:5000")
        print("[OK] Navegador aberto!")
    except:
        print("[AVISO] Não foi possível abrir navegador automaticamente")
        print("    Acesse manualmente: http://localhost:5000")
    
    print()
    
    # Manter processo vivo
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n\nEncerrando...")
        process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERRO] {e}")
        input("Pressione ENTER para sair...")
        sys.exit(1)
