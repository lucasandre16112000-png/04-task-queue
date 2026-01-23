# 🚀 Task Queue Launcher - Instruções de Uso

## O que é o Launcher?

O **Task Queue Launcher** é um executável que automatiza completamente a instalação e execução do sistema de fila de tarefas. Com apenas **2 cliques**, o cliente consegue:

✅ Verificar se Python está instalado  
✅ Instalar Flask automaticamente  
✅ Baixar o projeto do GitHub  
✅ Iniciar o servidor  
✅ Abrir a dashboard no navegador  

**Tudo sem precisar abrir terminal ou digitar comandos!**

---

## 📋 Pré-requisitos

- **Windows 7, 8, 10 ou 11**
- **Python 3.8+** (será verificado automaticamente)
- **Navegador web** (Chrome, Firefox, Edge, etc.)

---

## 🎯 Como Usar

### Opção 1: Usar o Arquivo .BAT (Recomendado)

1. **Baixe o arquivo `TaskQueueLauncher.bat`** do repositório
2. **Dê duplo clique** no arquivo
3. **Pronto!** O servidor inicia automaticamente e abre a dashboard

> **Nota:** A primeira execução pode levar alguns minutos para instalar as dependências

### Opção 2: Usar o PowerShell Script

1. **Baixe o arquivo `TaskQueueLauncher.ps1`** do repositório
2. **Clique com botão direito** no arquivo
3. **Selecione "Run with PowerShell"**
4. **Pronto!** O servidor inicia automaticamente

> **Nota:** Se receber erro de permissão, execute no PowerShell:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## 🔍 O que Acontece Quando Você Clica?

O launcher executa automaticamente:

```
1. Verifica se Python está instalado
   ↓
2. Verifica se pip está instalado
   ↓
3. Instala Flask (se necessário)
   ↓
4. Baixa o projeto do GitHub
   ↓
5. Inicia o servidor Flask
   ↓
6. Abre a dashboard no navegador
```

---

## 🌐 Acessar a Dashboard

Depois que o launcher terminar, a dashboard abrirá automaticamente em:

```
http://localhost:5000
```

Se não abrir automaticamente, acesse manualmente no seu navegador.

---

## 📊 Usando a Dashboard

### Criar Tarefas

Clique em um dos botões para criar tarefas:

- 📧 **Enviar Email** - Simula envio de email
- 📄 **Gerar Relatório** - Simula criação de PDF
- 🖼️ **Processar Imagem** - Simula aplicação de filtros
- 🔄 **Sincronizar Dados** - Simula sync entre bancos
- 🧹 **Limpar Cache** - Simula limpeza de dados
- ⚡ **Executar Todas** - Cria todas as 5 tarefas

### Monitorar Tarefas

A dashboard mostra em tempo real:

- **Total de Tarefas** - Quantidade total criada
- **Pendentes** - Aguardando processamento
- **Processando** - Sendo executadas agora
- **Concluídas** - Finalizadas com sucesso
- **Falhadas** - Que tiveram erro
- **Taxa de Sucesso** - Porcentagem de sucesso

---

## ❌ Solução de Problemas

### Erro: "Python não foi encontrado"

**Solução:**
1. Baixe Python em: https://www.python.org/downloads/
2. **IMPORTANTE:** Durante a instalação, marque a opção "Add Python to PATH"
3. Reinicie o computador
4. Execute o launcher novamente

### Erro: "Porta 5000 já está em uso"

**Solução:**
1. Feche outros programas que possam estar usando a porta 5000
2. Ou edite o arquivo `app.py` e mude `port=5000` para outra porta (ex: 5001)

### O navegador não abre automaticamente

**Solução:**
1. Abra seu navegador manualmente
2. Acesse: http://localhost:5000

### Erro ao instalar Flask

**Solução:**
1. Abra PowerShell como administrador
2. Execute: `pip install flask`
3. Execute o launcher novamente

---

## 🔧 Arquivos Inclusos

| Arquivo | Descrição |
|---------|-----------|
| `TaskQueueLauncher.bat` | Script batch para Windows (recomendado) |
| `TaskQueueLauncher.ps1` | Script PowerShell alternativo |
| `launcher.py` | Script Python original |
| `app.py` | Servidor Flask principal |
| `requirements.txt` | Dependências do projeto |

---

## 📁 Onde os Arquivos São Instalados?

Por padrão, o projeto é instalado em:

```
C:\Users\[seu_usuario]\TaskQueue\04-task-queue
```

Você pode acessar essa pasta para ver os arquivos do projeto.

---

## 🔄 Executar Novamente

Depois da primeira execução, você pode:

1. **Clicar novamente no launcher** - Ele detectará que o projeto já existe e iniciará o servidor diretamente
2. **Ou navegar até a pasta de instalação** e executar `python app.py` manualmente

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique se Python está instalado: `python --version`
2. Verifique se Flask está instalado: `pip show flask`
3. Tente executar o launcher novamente
4. Consulte o arquivo `TROUBLESHOOTING_WINDOWS.md` para mais soluções

---

## 👨‍💻 Desenvolvido por

**Lucas André S**  
GitHub: [@lucasandre16112000-png](https://github.com/lucasandre16112000-png)

---

**Versão:** 1.0.0  
**Última atualização:** Janeiro 2026
