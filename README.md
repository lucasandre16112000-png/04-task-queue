# ⚙️ Sistema de Fila de Tarefas Distribuído (Task Queue)

Um sistema robusto e profissional de **fila de tarefas assíncronas**, demonstrando as melhores práticas em arquitetura de sistemas distribuídos. Este projeto implementa processamento de tarefas em segundo plano com retry automático, priorização e monitoramento completo.

---

## 🎯 Visão Geral

Este projeto simula um sistema de fila de tarefas que é fundamental em aplicações web modernas, permitindo que operações demoradas sejam processadas sem bloquear a aplicação principal. Implementa padrões profissionais como exponential backoff, priorização de tarefas e logging estruturado.

**Casos de Uso:**
- Envio de emails em background
- Processamento de imagens
- Geração de relatórios
- Sincronização de dados
- Operações de longa duração

---

## ✨ Funcionalidades Principais

| Funcionalidade | Descrição |
|:---|:---|
| **Criação de Tarefas** | Enfileiramento de diferentes tipos de tarefas com payloads customizados |
| **Handlers Modulares** | Arquitetura extensível com handlers específicos para cada tipo de tarefa |
| **Priorização** | Suporte para prioridades (Alta, Média, Baixa) com processamento ordenado |
| **Retry Automático** | Tentativas automáticas com exponential backoff em caso de falha |
| **Logging Estruturado** | Rastreamento completo de cada tarefa com timestamps |
| **Monitoramento** | Estatísticas detalhadas sobre execução e performance |
| **Status Tracking** | Estados: PENDING → PROCESSING → COMPLETED/FAILED/RETRYING |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|:---|:---|:---|
| **Python** | 3.8+ | Linguagem principal (apenas bibliotecas padrão) |
| **Logging** | Built-in | Rastreamento estruturado de operações |
| **JSON** | Built-in | Serialização de dados e resultados |
| **Dataclasses** | Built-in | Modelos de dados tipados |

---

## 📋 Guia Completo de Instalação e Execução

### Pré-requisitos

Antes de começar, certifique-se de ter:

1. **Git** - [Download aqui](https://git-scm.com/downloads)
2. **Python 3.8 ou superior** - [Download aqui](https://www.python.org/downloads/)

#### Verificar se Python está instalado:

**Windows (PowerShell ou CMD):**
```bash
python --version
```

**macOS/Linux (Terminal):**
```bash
python3 --version
```

Se o comando não funcionar, instale Python através do link acima.

---

### Passo 1: Clonar o Repositório

**Windows (PowerShell ou CMD):**
```bash
git clone https://github.com/lucasandre16112000-png/04-task-queue.git
cd 04-task-queue
```

**macOS/Linux (Terminal):**
```bash
git clone https://github.com/lucasandre16112000-png/04-task-queue.git
cd 04-task-queue
```

---

### Passo 2: Executar o Worker

Este projeto **não requer instalação de dependências externas** - usa apenas bibliotecas padrão do Python!

**Windows (PowerShell ou CMD):**
```bash
python worker.py
```

**macOS/Linux (Terminal):**
```bash
python3 worker.py
```

---

### Passo 3: Observar a Execução

O terminal mostrará:

```
2025-12-12 18:30:45,123 - __main__ - INFO - ================================================================================
2025-12-12 18:30:45,123 - __main__ - INFO - INICIANDO SISTEMA DE FILA DE TAREFAS
2025-12-12 18:30:45,123 - __main__ - INFO - ================================================================================
2025-12-12 18:30:45,234 - __main__ - INFO - [TAREFA 1] Status: processing
2025-12-12 18:30:45,456 - __main__ - INFO - [TAREFA 1] Status: completed
...
```

---

## 📊 Estrutura do Projeto

```
04-task-queue/
├── README.md              # Este arquivo
├── worker.py              # Script principal com toda a lógica
├── requirements.txt       # Dependências (vazio - usa stdlib)
└── .gitignore             # Arquivos a ignorar no Git
```

---

## 🔧 Como Funciona

### 1. Enfileiramento de Tarefas

```python
processor = TaskProcessor()
task = Task(
    id="task-001",
    name="send_email",
    payload={"email": "user@example.com", "subject": "Hello"},
    priority=TaskPriority.HIGH
)
processor.enqueue(task)
```

### 2. Processamento

O sistema processa tarefas na ordem de prioridade:
- **HIGH (1)** - Processadas primeiro
- **MEDIUM (2)** - Processadas depois
- **LOW (3)** - Processadas por último

### 3. Retry Automático

Se uma tarefa falhar:
- Tenta novamente automaticamente (máximo 3 tentativas)
- Aguarda exponencialmente mais tempo a cada tentativa
- Registra cada tentativa no log

### 4. Monitoramento

Ao final, exibe estatísticas:
```
Total de tarefas: 10
Concluídas: 8
Falhadas: 2
Taxa de sucesso: 80%
Tempo total: 5.23s
```

---

## 📝 Tipos de Tarefas Suportadas

O sistema inclui handlers para:

| Tipo | Descrição |
|:---|:---|
| `send_email` | Simula envio de email |
| `process_image` | Simula processamento de imagem |
| `generate_report` | Simula geração de relatório |
| `sync_data` | Simula sincronização de dados |
| `heavy_computation` | Simula computação pesada |

---

## 🧪 Testando Manualmente

Para testar o sistema com tarefas customizadas, edite o arquivo `worker.py` na função `main()`:

```python
def main():
    processor = TaskProcessor()
    
    # Crie suas próprias tarefas aqui
    task = Task(
        id="custom-001",
        name="send_email",
        payload={"email": "seu@email.com", "subject": "Teste"},
        priority=TaskPriority.HIGH
    )
    
    processor.enqueue(task)
    processor.process_all()
```

---

## 📊 Saída Esperada

Quando executado, o programa gera:

1. **Logs em tempo real** - Mostra o progresso de cada tarefa
2. **Relatório final** - Estatísticas de execução
3. **Arquivo JSON** - `task_results.json` com detalhes de cada tarefa

---

## ⚙️ Configurações Avançadas

### Alterar Número Máximo de Retries

No arquivo `worker.py`, procure por:
```python
max_retries: int = 3
```

Altere o número conforme necessário.

### Alterar Timeout de Tarefas

Procure por:
```python
timeout: int = 5
```

Altere para o número de segundos desejado.

---

## 🐛 Troubleshooting

### Erro: "python: command not found"

**Solução:** Python não está instalado ou não está no PATH. Instale Python através de: https://www.python.org/downloads/

### Erro: "No module named 'worker'"

**Solução:** Certifique-se de estar no diretório correto:
```bash
cd 04-task-queue
python worker.py
```

### Tarefas não estão sendo processadas

**Solução:** Verifique se o script está rodando completamente. Algumas tarefas podem falhar propositalmente para demonstrar o retry automático.

---

## 📚 Conceitos Aprendidos

Este projeto demonstra:

- ✅ Padrão de Fila de Tarefas (Task Queue Pattern)
- ✅ Processamento Assíncrono
- ✅ Retry com Exponential Backoff
- ✅ Priorização de Tarefas
- ✅ Logging Estruturado
- ✅ Tratamento de Erros
- ✅ Serialização JSON
- ✅ Dataclasses em Python
- ✅ Enums para Estados
- ✅ Monitoramento e Estatísticas

---

## 🤝 Contribuições

Este é um projeto de portfólio. Sugestões e melhorias são bem-vindas!

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## 👨‍💻 Autor

**Lucas André S**

- GitHub: [@lucasandre16112000-png](https://github.com/lucasandre16112000-png)
- Portfólio: [Meus Projetos](https://github.com/lucasandre16112000-png?tab=repositories)

---

## 🎓 Próximos Passos

Para aprofundar seus conhecimentos:

1. Implemente persistência com banco de dados (SQLite, PostgreSQL)
2. Adicione suporte a Redis para fila distribuída
3. Implemente Celery para processamento distribuído
4. Crie uma API REST para gerenciar tarefas
5. Adicione dashboard web para monitoramento

---

**Desenvolvido por Lucas André S** ❤️

