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

def main():
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
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "--quiet"], check=True)
        print("    Flask instalado OK\n")
    
    # Iniciar servidor
    print("[3] Iniciando servidor...\n")
    print("    Acesse: http://localhost:5000")
    print("    Pressione Ctrl+C para encerrar\n")
    print("="*70 + "\n")
    
    # Abrir navegador
    time.sleep(2)
    try:
        webbrowser.open("http://localhost:5000")
    except:
        pass
    
    # Iniciar Flask
    try:
        subprocess.run([sys.executable, "app.py"], check=False)
    except KeyboardInterrupt:
        print("\n\nEncerrando...")
        sys.exit(0)

if __name__ == "__main__":
    main()
