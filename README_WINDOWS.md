# ⚙️ Sistema de Fila de Tarefas - Guia Completo para Windows

Olá! Conforme solicitado, analisei 100% do seu projeto e preparei uma versão totalmente compatível e otimizada para rodar no **Windows PowerShell** ou **CMD**. Abaixo estão as instruções detalhadas e todos os arquivos necessários.

---

## 🎯 Objetivo Cumprido

O projeto original já era de alta qualidade e usava apenas bibliotecas padrão do Python, o que facilitou a adaptação. A versão que preparei inclui:

- **Compatibilidade Total:** Garante que o código rode sem problemas de codificação de caracteres (UTF-8) no Windows.
- **Scripts de Execução Fácil:** Criei os arquivos `run_windows.bat` e `run_windows.ps1` para você executar tudo com um único clique.
- **Gerenciamento de Arquivos Melhorado:** Otimizei o código para salvar os resultados em um diretório específico (`./results/`), mantendo o projeto organizado.
- **Documentação Detalhada:** Este guia completo para Windows.

---

## 📦 Arquivos no Pacote

Preparei um pacote completo para você. Aqui está a estrutura de arquivos que você receberá:

```
04-task-queue/
├── 📂 results/                  # Novo: Diretório para salvar os resultados
│
├── 📜 README_WINDOWS.md         # Novo: Este guia completo para Windows
├── 📜 worker_windows.py          # Novo: Versão do script otimizada para Windows
├── 📜 run_windows.bat            # Novo: Script para rodar com 1 clique no CMD
├── 📜 run_windows.ps1            # Novo: Script para rodar com 1 clique no PowerShell
│
├── 📜 worker.py                  # Script original
├── 📜 README.md                  # Documentação original
├── 📜 requirements.txt           # Dependências (não são necessárias para rodar)
└── 📜 .gitignore                 # Arquivos a ignorar no Git
```

---

## 📋 Guia de Instalação e Execução no Windows

Siga estes 3 passos simples para rodar o projeto.

### Pré-requisitos

Antes de começar, certifique-se de ter o **Python** instalado. O Git é opcional, mas recomendado.

1.  **Python 3.8 ou superior:**
    - **Como verificar:** Abra o PowerShell ou CMD e digite `python --version`.
    - **Se não tiver:** Baixe em [python.org](https://www.python.org/downloads/). **Importante:** Durante a instalação, marque a caixa que diz **"Add Python to PATH"**.

2.  **Git (Opcional):**
    - **Como verificar:** Digite `git --version`.
    - **Se não tiver:** Baixe em [git-scm.com](https://git-scm.com/downloads).

### Passo 1: Baixar o Projeto

Se você já tem o projeto no seu computador, pode pular este passo. Caso contrário, clone o repositório:

```powershell
# Abra o PowerShell ou CMD
git clone https://github.com/lucasandre16112000-png/04-task-queue.git

# Navegue para o diretório do projeto
cd 04-task-queue
```

### Passo 2: Executar o Script

Criei dois scripts para facilitar sua vida. Você pode usar qualquer um dos dois.

#### Opção A: Usando o PowerShell (Recomendado)

1.  Abra o **PowerShell** no diretório `04-task-queue`.
2.  Execute o seguinte comando:

    ```powershell
    .\run_windows.ps1
    ```

    > **Nota sobre Segurança:** Se o PowerShell bloquear a execução, rode este comando uma vez para permitir scripts locais:
    > `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### Opção B: Usando o CMD (Duplo Clique)

1.  Abra o **Explorador de Arquivos** na pasta `04-task-queue`.
2.  Dê um **duplo clique** no arquivo `run_windows.bat`.

### Passo 3: Observar os Resultados

Após a execução, o terminal mostrará o processamento das tarefas em tempo real. Ao final, você encontrará os resultados no novo diretório `results/`.

1.  **Logs no Terminal:** Acompanhe o status de cada tarefa (pending → processing → completed).
2.  **Arquivo de Resultados:** Um arquivo chamado `task_results.json` será criado dentro da pasta `results/`. Ele contém um relatório completo com:
    - Estatísticas gerais (total de tarefas, falhas, sucesso, tempo médio).
    - Detalhes de cada tarefa executada.
    - O resultado específico de cada operação.

---

## 🔧 Como Customizar e Testar

Para testar o sistema com suas próprias tarefas, edite o arquivo `worker_windows.py`.

1.  Abra o arquivo `worker_windows.py` em um editor de código (como o VS Code).
2.  Vá até o final do arquivo, na função `main()`.
3.  Adicione ou modifique as tarefas dentro da lista `tasks`.

**Exemplo de como adicionar uma nova tarefa de email com alta prioridade:**

```python
# Dentro da função main(), localize a lista de tarefas
tasks = [
    # ... tarefas existentes

    # Adicione sua nova tarefa aqui
    processor.create_task(
        name='send_email',
        payload={
            'to': 'seu-email@provedor.com',
            'subject': 'Teste de Nova Tarefa',
            'body': 'Este é um teste customizado.'
        },
        priority=TaskPriority.HIGH
    ),
]
```

Salve o arquivo e execute novamente com `run_windows.ps1` ou `run_windows.bat` para ver sua nova tarefa em ação.

---

## ✅ Conclusão

O projeto agora está 100% pronto para ser executado e modificado no seu ambiente Windows. Os scripts de automação e as otimizações de código garantem uma experiência fluida e sem erros.

Se tiver qualquer outra dúvida ou precisar de mais alguma ajuda, estou à disposição!
