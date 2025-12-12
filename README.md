# ⚙️ App 4: Sistema de Fila de Tarefas (Task Queue)

Este projeto simula um sistema de **fila de tarefas assíncronas**, uma arquitetura fundamental em sistemas distribuídos e aplicações web modernas. Ele demonstra como gerenciar, processar e monitorar tarefas em segundo plano, garantindo que operações demoradas não bloqueiem a aplicação principal.

## ✨ Funcionalidades Principais

- **Criação e Enfileiramento de Tarefas**: Permite a criação de diferentes tipos de tarefas com cargas de dados (`payload`) específicas.
- **Processamento Baseado em Handlers**: Arquitetura modular onde cada tipo de tarefa é associado a uma função (handler) específica.
- **Priorização de Tarefas**: Suporte para definir prioridades (Alta, Média, Baixa).
- **Retry Automático com Exponential Backoff**: Se uma tarefa falhar, o sistema tenta executá-la novamente automaticamente.

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
| :--- | :--- |
| **Python** | Linguagem principal (utiliza apenas bibliotecas padrão) |

## 📋 Guia de Instalação e Execução (Para Qualquer Pessoa)

### Pré-requisitos

1.  **Git**: [**Download aqui**](https://git-scm.com/downloads)
2.  **Python**: [**Download aqui**](https://www.python.org/downloads/) (versão 3.8+)

### Passo 1: Baixar o Projeto

```bash
git clone https://github.com/lucasandre16112000-png/04-task-queue.git
cd 04-task-queue
```

### Passo 2: Executar o Worker

Este projeto não precisa de instalação de bibliotecas. Basta executar o script:

```bash
python worker.py
```

### Passo 3: Observar a Saída

- O terminal mostrará o log de cada tarefa sendo processada.
- Ao final, um relatório com as estatísticas gerais do sistema será exibido.

## 👨‍💻 Autor

Lucas André S - [GitHub](https://github.com/lucasandre16112000-png)
