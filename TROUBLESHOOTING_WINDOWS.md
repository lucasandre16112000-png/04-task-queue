# 🔧 Guia de Troubleshooting - Windows

Se você encontrar algum problema ao executar o projeto no Windows, consulte este guia para soluções rápidas.

---

## ❌ Erro: "python: command not found"

### Sintomas
Ao tentar rodar `python --version`, você recebe uma mensagem de erro.

### Causa
Python não está instalado ou não está no PATH do Windows.

### Solução

1. **Verificar se Python está instalado:**
   - Abra o PowerShell e digite: `python --version`
   - Se funcionar, pule para a próxima seção.

2. **Se Python não está instalado:**
   - Baixe Python em: [python.org](https://www.python.org/downloads/)
   - **Importante:** Durante a instalação, marque a caixa **"Add Python to PATH"**
   - Clique em "Install Now"
   - Reinicie o PowerShell/CMD
   - Teste novamente: `python --version`

3. **Se Python está instalado mas não aparece no PATH:**
   - Procure por "Variáveis de Ambiente" no Windows
   - Clique em "Editar as variáveis de ambiente do sistema"
   - Clique em "Variáveis de Ambiente"
   - Em "Variáveis do sistema", procure por "Path"
   - Clique em "Editar"
   - Clique em "Novo"
   - Adicione o caminho do Python (ex: `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311`)
   - Clique em "OK" em todas as janelas
   - Reinicie o PowerShell/CMD

---

## ❌ Erro: "Cannot be loaded because running scripts is disabled on this system"

### Sintomas
Ao tentar executar `.\run_windows.ps1`, você recebe um erro sobre política de execução.

### Causa
O PowerShell está bloqueando a execução de scripts por razões de segurança.

### Solução

Execute este comando uma única vez no PowerShell (como administrador):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois, tente novamente:

```powershell
.\run_windows.ps1
```

---

## ❌ Erro: "No module named 'worker_windows'"

### Sintomas
Ao tentar rodar o script, você recebe uma mensagem de erro sobre módulo não encontrado.

### Causa
Você não está no diretório correto ou o arquivo `worker_windows.py` não existe.

### Solução

1. **Verificar o diretório atual:**
   - No PowerShell, digite: `pwd` (ou `cd` sem argumentos)
   - Certifique-se de que você está em `04-task-queue`

2. **Se não estiver no diretório correto:**
   - Navegue até o diretório: `cd 04-task-queue`

3. **Verificar se o arquivo existe:**
   - Digite: `ls worker_windows.py` (PowerShell) ou `dir worker_windows.py` (CMD)
   - Se o arquivo não aparecer, você pode ter baixado uma versão antiga do projeto

---

## ❌ Erro: "UnicodeDecodeError" ou caracteres estranhos no output

### Sintomas
O programa roda, mas mostra caracteres estranhos ou símbolos incorretos no terminal.

### Causa
Problema de codificação de caracteres (encoding) no Windows.

### Solução

A versão `worker_windows.py` que preparei já resolve este problema automaticamente. Se você ainda tiver problemas:

1. **Abra o PowerShell como Administrador**
2. **Execute este comando:**
   ```powershell
   chcp 65001
   ```
   Isto muda o encoding para UTF-8.

3. **Tente rodar o script novamente:**
   ```powershell
   python worker_windows.py
   ```

---

## ❌ Erro: "Permission denied" ou "Access is denied"

### Sintomas
Ao tentar executar o script, você recebe uma mensagem de permissão negada.

### Causa
O arquivo não tem permissão de execução ou você não tem permissão para acessar o diretório.

### Solução

1. **Verifique se você tem permissão de escrita no diretório:**
   - Clique com botão direito na pasta `04-task-queue`
   - Selecione "Propriedades"
   - Vá para a aba "Segurança"
   - Clique em "Editar"
   - Selecione seu usuário
   - Marque "Controle Total"
   - Clique em "Aplicar" e "OK"

2. **Tente novamente:**
   ```powershell
   python worker_windows.py
   ```

---

## ❌ Erro: "ModuleNotFoundError: No module named 'json'" ou similar

### Sintomas
O programa reclama que não consegue importar módulos padrão do Python.

### Causa
Instalação corrompida do Python ou versão muito antiga.

### Solução

1. **Reinstale Python:**
   - Desinstale Python completamente
   - Baixe a versão mais recente em [python.org](https://www.python.org/downloads/)
   - Instale novamente, marcando "Add Python to PATH"

2. **Verifique a versão:**
   ```powershell
   python --version
   ```
   Deve ser Python 3.8 ou superior.

---

## ❌ O script roda mas não cria o arquivo `task_results.json`

### Sintomas
O programa executa com sucesso, mas o arquivo de resultados não é criado.

### Causa
O diretório `results/` não existe ou não tem permissão de escrita.

### Solução

1. **Crie o diretório manualmente:**
   ```powershell
   mkdir results
   ```

2. **Verifique permissões:**
   - Clique com botão direito na pasta `results`
   - Selecione "Propriedades"
   - Vá para "Segurança"
   - Certifique-se de que você tem permissão de "Modificar"

3. **Tente novamente:**
   ```powershell
   python worker_windows.py
   ```

---

## ❌ O script roda muito lentamente

### Sintomas
O programa demora muito tempo para processar as tarefas.

### Causa
Tarefas com `time.sleep()` ou antivírus verificando arquivos.

### Solução

1. **Isto é normal:** O script contém `time.sleep()` para simular processamento real. Cada tarefa leva alguns segundos.

2. **Se for muito lento:**
   - Desabilite temporariamente o antivírus
   - Feche outros programas que estejam usando muitos recursos
   - Tente novamente

---

## ❌ Erro: "FileNotFoundError" ao salvar resultados

### Sintomas
Ao final da execução, você recebe um erro sobre arquivo não encontrado.

### Causa
O caminho do arquivo está incorreto ou o diretório não existe.

### Solução

1. **Crie o diretório `results`:**
   ```powershell
   mkdir results
   ```

2. **Verifique o arquivo `worker_windows.py`:**
   - Procure pela linha: `processor = TaskProcessor()`
   - Altere para: `processor = TaskProcessor(output_dir="results")`

3. **Tente novamente**

---

## ✅ Tudo funcionando? Ótimo!

Se o seu problema não está listado aqui, ou se você conseguiu resolver, parabéns! O projeto está pronto para uso.

Para mais informações, consulte o arquivo `README_WINDOWS.md`.

