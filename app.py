"""
Sistema de Fila de Tarefas - Dashboard Web
Backend Flask com API REST

Desenvolvido por Lucas André S
GitHub: https://github.com/lucasandre16112000-png
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
import json
import time
import threading
import os
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

app = Flask(__name__, static_folder='static', template_folder='templates')

# ============================================================================
# ENUMS E MODELOS
# ============================================================================

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class TaskPriority(Enum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


@dataclass
class Task:
    id: str
    name: str
    payload: Dict[str, Any]
    priority: str = "MEDIUM"
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    execution_time: float = 0.0


# ============================================================================
# ARMAZENAMENTO EM MEMÓRIA
# ============================================================================

tasks_db: Dict[str, Task] = {}
processing_lock = threading.Lock()


# ============================================================================
# HANDLERS DE TAREFAS
# ============================================================================

def handle_send_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simula envio de email"""
    time.sleep(1.5)
    return {
        'status': 'sent',
        'to': payload.get('to', 'user@example.com'),
        'subject': payload.get('subject', 'Sem assunto'),
        'message': f"Email enviado com sucesso para {payload.get('to', 'user@example.com')}",
        'timestamp': datetime.now().isoformat()
    }


def handle_generate_report(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simula geração de relatório"""
    time.sleep(2)
    return {
        'status': 'generated',
        'report_type': payload.get('report_type', 'geral'),
        'filename': f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        'pages': 15,
        'size_mb': 2.5,
        'message': f"Relatório '{payload.get('report_type', 'geral')}' gerado com sucesso!",
        'timestamp': datetime.now().isoformat()
    }


def handle_process_image(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simula processamento de imagem"""
    time.sleep(2.5)
    filters = payload.get('filters', ['resize', 'optimize'])
    return {
        'status': 'processed',
        'original': payload.get('image_name', 'imagem.jpg'),
        'output': f"processed_{payload.get('image_name', 'imagem.jpg')}",
        'filters_applied': filters,
        'message': f"Imagem processada com {len(filters)} filtros aplicados!",
        'timestamp': datetime.now().isoformat()
    }


def handle_sync_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simula sincronização de dados"""
    time.sleep(2)
    return {
        'status': 'synced',
        'source': payload.get('source', 'database_a'),
        'destination': payload.get('destination', 'database_b'),
        'records_synced': 1250,
        'message': f"1250 registros sincronizados de {payload.get('source', 'database_a')} para {payload.get('destination', 'database_b')}!",
        'timestamp': datetime.now().isoformat()
    }


def handle_cleanup(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simula limpeza de dados"""
    time.sleep(1)
    return {
        'status': 'cleaned',
        'target': payload.get('target', 'cache'),
        'items_removed': 847,
        'space_freed_mb': 156.3,
        'message': f"847 itens removidos do {payload.get('target', 'cache')}, liberando 156.3 MB!",
        'timestamp': datetime.now().isoformat()
    }


HANDLERS = {
    'send_email': handle_send_email,
    'generate_report': handle_generate_report,
    'process_image': handle_process_image,
    'sync_data': handle_sync_data,
    'cleanup': handle_cleanup,
}


# ============================================================================
# PROCESSAMENTO DE TAREFAS
# ============================================================================

def process_task(task_id: str):
    """Processa uma tarefa em background"""
    with processing_lock:
        if task_id not in tasks_db:
            return
        
        task = tasks_db[task_id]
        task.status = "processing"
        task.started_at = datetime.now().isoformat()
    
    start_time = time.time()
    
    try:
        handler = HANDLERS.get(task.name)
        if handler is None:
            raise ValueError(f"Handler não encontrado para: {task.name}")
        
        result = handler(task.payload)
        
        with processing_lock:
            task.status = "completed"
            task.completed_at = datetime.now().isoformat()
            task.result = result
            task.execution_time = round(time.time() - start_time, 2)
            
    except Exception as e:
        with processing_lock:
            task.status = "failed"
            task.completed_at = datetime.now().isoformat()
            task.error = str(e)
            task.execution_time = round(time.time() - start_time, 2)


# ============================================================================
# ROTAS DA API
# ============================================================================

@app.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Retorna todas as tarefas"""
    tasks_list = []
    for task in tasks_db.values():
        task_dict = asdict(task)
        tasks_list.append(task_dict)
    
    # Ordenar por data de criação (mais recente primeiro)
    tasks_list.sort(key=lambda x: x['created_at'], reverse=True)
    return jsonify(tasks_list)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Cria uma nova tarefa"""
    data = request.json
    
    task_id = str(uuid.uuid4())[:8]
    task = Task(
        id=task_id,
        name=data.get('name', 'send_email'),
        payload=data.get('payload', {}),
        priority=data.get('priority', 'MEDIUM')
    )
    
    tasks_db[task_id] = task
    
    # Processar em background
    thread = threading.Thread(target=process_task, args=(task_id,))
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id, 'message': 'Tarefa criada e iniciada!'})


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Retorna uma tarefa específica"""
    if task_id not in tasks_db:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    return jsonify(asdict(tasks_db[task_id]))


@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Remove uma tarefa"""
    if task_id not in tasks_db:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    del tasks_db[task_id]
    return jsonify({'success': True, 'message': 'Tarefa removida!'})


@app.route('/api/tasks/clear', methods=['POST'])
def clear_tasks():
    """Limpa todas as tarefas"""
    tasks_db.clear()
    return jsonify({'success': True, 'message': 'Todas as tarefas foram removidas!'})


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Retorna estatísticas do sistema"""
    total = len(tasks_db)
    pending = sum(1 for t in tasks_db.values() if t.status == 'pending')
    processing = sum(1 for t in tasks_db.values() if t.status == 'processing')
    completed = sum(1 for t in tasks_db.values() if t.status == 'completed')
    failed = sum(1 for t in tasks_db.values() if t.status == 'failed')
    
    # Calcular tempo médio
    completed_tasks = [t for t in tasks_db.values() if t.status == 'completed']
    avg_time = 0
    if completed_tasks:
        avg_time = round(sum(t.execution_time for t in completed_tasks) / len(completed_tasks), 2)
    
    # Taxa de sucesso
    finished = completed + failed
    success_rate = round((completed / finished * 100) if finished > 0 else 0, 1)
    
    return jsonify({
        'total': total,
        'pending': pending,
        'processing': processing,
        'completed': completed,
        'failed': failed,
        'average_time': avg_time,
        'success_rate': success_rate
    })


# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 SISTEMA DE FILA DE TAREFAS - DASHBOARD WEB")
    print("=" * 60)
    print("\n📊 Acesse o painel em: http://localhost:5000")
    print("\n💡 Pressione Ctrl+C para encerrar\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
