# ⚙️ Sistema de Fila de Tarefas Distribuído (Task Queue)

Um sistema robusto e profissional de **fila de tarefas assíncronas** com **Dashboard Web Visual**, demonstrando as melhores práticas em arquitetura de sistemas distribuídos.

![Dashboard Screenshot](dashboard_screenshot.webp)

---

## 🎯 O que é?

Um **sistema de fila de tarefas** que:
- ✅ Recebe tarefas para executar
- ✅ Coloca na fila para processar
- ✅ Executa uma por uma em background
- ✅ Mostra o status em tempo real
- ✅ Tenta novamente se falhar

Muito usado em aplicações web para processar tarefas pesadas sem travar a interface!

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|:---|:---|
| **Dashboard Web** | Interface visual para criar e monitorar tarefas |
| **5 Tipos de Tarefas** | Email, Relatório, Imagem, Sincronização, Limpeza |
| **Estatísticas em Tempo Real** | Total, Pendentes, Processando, Concluídas, Falhadas |
| **Taxa de Sucesso** | Cálculo automático da taxa de sucesso |
| **Botão "Executar Todas"** | Cria todas as tarefas de uma vez para teste |

---

## 🚀 Como Usar (Guia Completo do Zero)

### ⚠️ Pré-requisito: Python 3.8+

**Você PRECISA ter Python instalado!**

#### Passo 1: Instalar Python

1. Acesse: https://www.python.org/downloads/
2. Baixe a versão mais recente (3.10 ou superior)
3. Execute o instalador
4. **⚠️ IMPORTANTE:** Durante a instalação, marque a opção **"Add Python to PATH"**
5. Clique em "Install Now"
6. Reinicie o computador

#### Verificar se Python está instalado:

Abra **CMD** ou **PowerShell** e digite:
```bash
python --version
```

Se aparecer a versão (ex: `Python 3.12.10`), Python está pronto! ✓

---

### 📥 Passo 1: Baixar o Projeto

**Opção A - Sem Git (Mais Fácil):**

1. Acesse: https://github.com/lucasandre16112000-png/04-task-queue
2. Clique no botão verde **"Code"**
3. Clique em **"Download ZIP"**
4. Extraia o arquivo em uma pasta (ex: `C:\Users\[seu_usuario]\Desktop\04-task-queue`)

**Opção B - Com Git:**

Abra PowerShell/CMD e execute:
```bash
git clone https://github.com/lucasandre16112000-png/04-task-queue.git
cd 04-task-queue
```

---

### ▶️ Passo 2: Executar (2 Cliques!)

**Opção A - Recomendada (Automática):**

1. Navegue até a pasta do projeto
2. Dê **duplo clique** em **`TaskQueueLauncher_v2.bat`**
3. Aguarde alguns segundos
4. **Dashboard abre automaticamente!**

O script vai:
- ✅ Verificar Python
- ✅ Instalar Flask (se necessário)
- ✅ Baixar projeto (se necessário)
- ✅ Iniciar servidor
- ✅ Abrir navegador

**Opção B - Simples:**

1. Navegue até a pasta do projeto
2. Dê **duplo clique** em **`INICIAR.bat`**
3. Aguarde alguns segundos
4. **Dashboard abre automaticamente!**

**Opção C - Manual (Para Programadores):**

Abra PowerShell/CMD na pasta do projeto e execute:
```bash
pip install flask
python app.py
```

Depois abra o navegador em: http://localhost:5000

---

### 🌐 Passo 3: Acessar a Dashboard

Se o navegador não abrir automaticamente, abra manualmente:

```
http://localhost:5000
```

---

## 📊 Como Usar a Dashboard

### Criar Tarefas

Clique em um dos botões para criar tarefas:

| Botão | O que faz |
|:---|:---|
| 📧 **Enviar Email** | Simula envio de email |
| 📄 **Gerar Relatório** | Simula criação de PDF |
| 🖼️ **Processar Imagem** | Simula aplicação de filtros |
| 🔄 **Sincronizar Dados** | Simula sincronização de banco |
| 🧹 **Limpar Cache** | Simula limpeza de dados |
| ⚡ **Executar Todas** | Cria todas as 5 tarefas |

### Monitorar Tarefas

A dashboard mostra em tempo real:

- **Total** - Quantidade total de tarefas criadas
- **Pendentes** - Tarefas aguardando processamento
- **Processando** - Tarefas sendo executadas agora
- **Concluídas** - Tarefas finalizadas com sucesso
- **Falhadas** - Tarefas que falharam
- **Taxa de Sucesso** - Porcentagem de sucesso

---

## 📁 Estrutura do Projeto

```
04-task-queue/
├── 📜 app.py                    # Servidor Flask (Backend)
├── 📜 TaskQueueLauncher_v2.bat  # Executável principal ⭐
├── 📜 INICIAR.bat               # Executável simples
├── 📜 requirements.txt          # Dependências
├── 📜 README.md                 # Este arquivo
│
├── 📂 templates/
│   └── index.html               # Interface da dashboard
│
├── 📂 static/
│   ├── css/style.css            # Estilos visuais
│   └── js/app.js                # Interatividade
│
└── 📂 (Arquivos de teste)
    ├── execution_output.txt
    ├── generate_screenshot.py
    └── screenshots/
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Propósito |
|:---|:---|
| **Python 3.8+** | Backend e processamento |
| **Flask** | Servidor web e API REST |
| **HTML5/CSS3** | Interface visual |
| **JavaScript** | Interatividade |
| **Threading** | Processamento assíncrono |

---

## ❌ Solução de Problemas

### ❌ Erro: "Python não foi encontrado"

**Solução:**
1. Instale Python: https://www.python.org/downloads/
2. **IMPORTANTE:** Marque "Add Python to PATH" durante a instalação
3. Reinicie o computador
4. Execute o launcher novamente

### ❌ Erro: "Porta 5000 em uso"

**Solução:**
1. Feche outros programas que possam estar usando a porta 5000
2. Ou edite `app.py` e mude `port=5000` para outra porta (ex: 5001)
3. Salve e execute novamente

### ❌ O navegador não abre automaticamente

**Solução:**
1. Abra seu navegador manualmente
2. Acesse: http://localhost:5000

### ❌ Erro: "No module named 'flask'"

**Solução:**
Abra PowerShell/CMD e execute:
```bash
pip install flask
```

### ❌ Erro de permissão no PowerShell

**Solução:**
Abra PowerShell como administrador e execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `TaskQueueLauncher_v2.bat` | ⭐ **Executável principal** - Com download automático |
| `INICIAR.bat` | Executável simples - Pasta atual |
| `app.py` | Servidor Flask |
| `requirements.txt` | Dependências do projeto |
| `templates/index.html` | Interface da dashboard |
| `static/css/style.css` | Estilos CSS |
| `static/js/app.js` | JavaScript |

---

## 🎓 Resumo Rápido

**Para o cliente usar:**

1. ✅ Instalar Python (https://www.python.org/downloads/)
2. ✅ Baixar o projeto do GitHub
3. ✅ Dê duplo clique em `TaskQueueLauncher_v2.bat`
4. ✅ **Pronto! Tudo funciona sozinho!**

---

## 👨‍💻 Autor

**Lucas André S**

- GitHub: [@lucasandre16112000-png](https://github.com/lucasandre16112000-png)

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ por Lucas André S**

**Versão:** 1.0.0  
**Última atualização:** Janeiro 2026
