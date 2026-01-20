"""
Script para gerar uma imagem do output do terminal
Simula a aparência de um terminal Windows PowerShell
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Conteúdo do terminal
terminal_output = """
================================================================================
SISTEMA DE FILA DE TAREFAS DISTRIBUÍDO - EXEMPLO DE USO
================================================================================

2026-01-19 15:16:15 - INFO - TaskProcessor inicializado

📋 CRIANDO TAREFAS
--------------------------------------------------------------------------------
2026-01-19 15:16:15 - INFO - Tarefa criada: task_001 (tipo: send_email, prioridade: HIGH)
2026-01-19 15:16:15 - INFO - Tarefa criada: task_002 (tipo: generate_report, prioridade: MEDIUM)
2026-01-19 15:16:15 - INFO - Tarefa criada: task_003 (tipo: process_image, prioridade: LOW)
2026-01-19 15:16:15 - INFO - Tarefa criada: task_004 (tipo: sync_data, prioridade: HIGH)

  ✓ task_001: send_email (Prioridade: HIGH)
  ✓ task_002: generate_report (Prioridade: MEDIUM)
  ✓ task_003: process_image (Prioridade: LOW)
  ✓ task_004: sync_data (Prioridade: HIGH)

⚙️  PROCESSANDO TAREFAS
--------------------------------------------------------------------------------
2026-01-19 15:16:15 - INFO - Iniciando processamento: task_001 (tipo: send_email)
2026-01-19 15:16:16 - INFO - ✓ Tarefa concluída com sucesso: task_001 (tempo: 1.00s)
2026-01-19 15:16:16 - INFO - Iniciando processamento: task_002 (tipo: generate_report)
2026-01-19 15:16:18 - INFO - ✓ Tarefa concluída com sucesso: task_002 (tempo: 2.00s)
2026-01-19 15:16:18 - INFO - Iniciando processamento: task_003 (tipo: process_image)
2026-01-19 15:16:21 - INFO - ✓ Tarefa concluída com sucesso: task_003 (tempo: 3.00s)
2026-01-19 15:16:21 - INFO - Iniciando processamento: task_004 (tipo: sync_data)
2026-01-19 15:16:23 - INFO - ✓ Tarefa concluída com sucesso: task_004 (tempo: 2.00s)

  task_001: completed
  task_002: completed
  task_003: completed
  task_004: completed

📊 RESULTADOS
--------------------------------------------------------------------------------

Tarefa: task_001
  Status: completed
  Tempo: 1.00s
  Resultado: {"status": "sent", "to": "user@example.com"}

Tarefa: task_002
  Status: completed
  Tempo: 2.00s
  Resultado: {"status": "generated", "filename": "report_2026.pdf"}

Tarefa: task_003
  Status: completed
  Tempo: 3.00s
  Resultado: {"status": "processed", "filters_applied": ["blur", "brightness"]}

Tarefa: task_004
  Status: completed
  Tempo: 2.00s
  Resultado: {"status": "synced", "records_synced": 1000}

================================================================================
ESTATÍSTICAS
================================================================================
Total de tarefas: 4
Pendentes: 0
Processando: 0
Concluídas: 4
Falhadas: 0
Tentando novamente: 0
Tempo médio de execução: 2.00s

💾 SALVANDO RESULTADOS
--------------------------------------------------------------------------------
2026-01-19 15:16:23 - INFO - Resultados salvos em: task_results.json
Arquivo de resultados: task_results.json

✅ Exemplo concluído com sucesso!
================================================================================

PS C:\\Users\\Lucas\\04-task-queue>
"""

# Configurações
width = 1200
line_height = 20
padding = 30
header_height = 40

# Calcular altura
lines = terminal_output.strip().split('\n')
height = len(lines) * line_height + padding * 2 + header_height

# Criar imagem
img = Image.new('RGB', (width, height), color=(1, 36, 86))  # Azul escuro do PowerShell

# Criar objeto de desenho
draw = ImageDraw.Draw(img)

# Tentar usar fonte monospace
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
except:
    font = ImageFont.load_default()
    title_font = font

# Desenhar barra de título
draw.rectangle([0, 0, width, header_height], fill=(0, 0, 0))
draw.text((15, 12), "Windows PowerShell - 04-task-queue", fill=(255, 255, 255), font=title_font)

# Botões da janela
button_y = 10
draw.rectangle([width-90, button_y, width-70, button_y+20], outline=(128, 128, 128))  # Minimizar
draw.rectangle([width-60, button_y, width-40, button_y+20], outline=(128, 128, 128))  # Maximizar
draw.rectangle([width-30, button_y, width-10, button_y+20], fill=(232, 17, 35))  # Fechar

# Desenhar texto do terminal
y = header_height + padding
for line in lines:
    # Colorir linhas especiais
    if "INFO" in line or "✓" in line:
        color = (0, 255, 0)  # Verde para sucesso
    elif "ERROR" in line or "✗" in line:
        color = (255, 0, 0)  # Vermelho para erro
    elif "WARNING" in line:
        color = (255, 255, 0)  # Amarelo para aviso
    elif "===" in line or "---" in line:
        color = (0, 255, 255)  # Ciano para separadores
    elif line.startswith("📋") or line.startswith("⚙️") or line.startswith("📊") or line.startswith("💾") or line.startswith("✅"):
        color = (255, 255, 0)  # Amarelo para títulos
    elif "PS C:" in line:
        color = (255, 255, 255)  # Branco para prompt
    else:
        color = (204, 204, 204)  # Cinza claro para texto normal
    
    draw.text((padding, y), line, fill=color, font=font)
    y += line_height

# Salvar imagem
img.save('/home/ubuntu/04-task-queue/screenshot_windows.png', 'PNG')
print("Screenshot salvo em: /home/ubuntu/04-task-queue/screenshot_windows.png")
