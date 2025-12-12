"""
Task Queue Profissional com Redis e Celery
Exemplo de processamento assíncrono de tarefas com retry, logging e monitoramento.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import time
from dataclasses import dataclass, asdict
from enum import Enum

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Status de uma tarefa"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Prioridade de uma tarefa"""
    LOW = 3
    MEDIUM = 2
    HIGH = 1


@dataclass
class Task:
    """Modelo de tarefa"""
    id: str
    name: str
    payload: Dict[str, Any]
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()


@dataclass
class TaskResult:
    """Resultado de uma tarefa"""
    task_id: str
    status: TaskStatus
    result: Optional[Dict] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    completed_at: str = None
    
    def __post_init__(self):
        if self.completed_at is None:
            self.completed_at = datetime.utcnow().isoformat()


class TaskProcessor:
    """Processador de tarefas"""
    
    def __init__(self):
        self.tasks = {}  # Simulação de armazenamento
        self.results = {}
        self.task_handlers = {
            'send_email': self._handle_send_email,
            'generate_report': self._handle_generate_report,
            'process_image': self._handle_process_image,
            'sync_data': self._handle_sync_data,
            'cleanup': self._handle_cleanup,
        }
    
    def register_handler(self, task_name: str, handler):
        """Registrar handler customizado para tipo de tarefa"""
        self.task_handlers[task_name] = handler
        logger.info(f"Handler registrado para: {task_name}")
    
    def create_task(
        self,
        name: str,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM,
        task_id: Optional[str] = None
    ) -> Task:
        """Criar nova tarefa"""
        if task_id is None:
            task_id = f"task_{int(time.time() * 1000)}"
        
        task = Task(
            id=task_id,
            name=name,
            payload=payload,
            priority=priority
        )
        
        self.tasks[task_id] = task
        logger.info(f"Tarefa criada: {task_id} ({name})")
        
        return task
    
    def process_task(self, task_id: str) -> TaskResult:
        """Processar uma tarefa"""
        if task_id not in self.tasks:
            logger.error(f"Tarefa não encontrada: {task_id}")
            return TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error="Tarefa não encontrada"
            )
        
        task = self.tasks[task_id]
        
        # Verificar se tarefa já foi processada
        if task.status == TaskStatus.COMPLETED:
            logger.warning(f"Tarefa já foi processada: {task_id}")
            return self.results.get(task_id)
        
        logger.info(f"Processando tarefa: {task_id} ({task.name})")
        
        task.status = TaskStatus.PROCESSING
        task.started_at = datetime.utcnow().isoformat()
        
        start_time = time.time()
        
        try:
            # Obter handler para tipo de tarefa
            handler = self.task_handlers.get(task.name)
            
            if handler is None:
                raise ValueError(f"Handler não encontrado para: {task.name}")
            
            # Executar handler
            result = handler(task.payload)
            
            execution_time = time.time() - start_time
            
            # Atualizar tarefa
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow().isoformat()
            task.result = result
            
            # Criar resultado
            task_result = TaskResult(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                result=result,
                execution_time=execution_time
            )
            
            self.results[task_id] = task_result
            
            logger.info(
                f"✓ Tarefa concluída: {task_id} "
                f"({execution_time:.2f}s)"
            )
            
            return task_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            logger.error(f"✗ Erro ao processar tarefa {task_id}: {error_msg}")
            
            # Tentar retry
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING
                logger.info(
                    f"Tentando novamente ({task.retry_count}/{task.max_retries}): {task_id}"
                )
                # Simular espera exponencial
                time.sleep(2 ** task.retry_count)
                return self.process_task(task_id)
            else:
                task.status = TaskStatus.FAILED
                task.error = error_msg
                task.completed_at = datetime.utcnow().isoformat()
                
                task_result = TaskResult(
                    task_id=task_id,
                    status=TaskStatus.FAILED,
                    error=error_msg,
                    execution_time=execution_time
                )
                
                self.results[task_id] = task_result
                
                return task_result
    
    # ========================================================================
    # HANDLERS DE TAREFAS
    # ========================================================================
    
    def _handle_send_email(self, payload: Dict) -> Dict:
        """Handler para envio de email"""
        logger.info(f"Enviando email para: {payload.get('to')}")
        
        # Simular envio de email
        time.sleep(1)
        
        return {
            'status': 'sent',
            'to': payload.get('to'),
            'subject': payload.get('subject'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_generate_report(self, payload: Dict) -> Dict:
        """Handler para geração de relatório"""
        logger.info(f"Gerando relatório: {payload.get('report_type')}")
        
        # Simular geração de relatório
        time.sleep(2)
        
        return {
            'status': 'generated',
            'report_type': payload.get('report_type'),
            'filename': f"report_{int(time.time())}.pdf",
            'size_mb': 2.5,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_process_image(self, payload: Dict) -> Dict:
        """Handler para processamento de imagem"""
        logger.info(f"Processando imagem: {payload.get('image_path')}")
        
        # Simular processamento de imagem
        time.sleep(3)
        
        return {
            'status': 'processed',
            'original_path': payload.get('image_path'),
            'output_path': f"processed_{payload.get('image_path')}",
            'filters_applied': payload.get('filters', []),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_sync_data(self, payload: Dict) -> Dict:
        """Handler para sincronização de dados"""
        logger.info(f"Sincronizando dados de: {payload.get('source')}")
        
        # Simular sincronização
        time.sleep(2)
        
        return {
            'status': 'synced',
            'source': payload.get('source'),
            'destination': payload.get('destination'),
            'records_synced': 1000,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_cleanup(self, payload: Dict) -> Dict:
        """Handler para limpeza de dados"""
        logger.info(f"Limpando dados: {payload.get('target')}")
        
        # Simular limpeza
        time.sleep(1)
        
        return {
            'status': 'cleaned',
            'target': payload.get('target'),
            'items_removed': 500,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Obter status de uma tarefa"""
        return self.tasks.get(task_id)
    
    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """Obter resultado de uma tarefa"""
        return self.results.get(task_id)
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> list:
        """Listar tarefas"""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        return sorted(tasks, key=lambda t: t.priority.value)
    
    def get_statistics(self) -> Dict:
        """Obter estatísticas de processamento"""
        all_tasks = list(self.tasks.values())
        
        stats = {
            'total_tasks': len(all_tasks),
            'pending': len([t for t in all_tasks if t.status == TaskStatus.PENDING]),
            'processing': len([t for t in all_tasks if t.status == TaskStatus.PROCESSING]),
            'completed': len([t for t in all_tasks if t.status == TaskStatus.COMPLETED]),
            'failed': len([t for t in all_tasks if t.status == TaskStatus.FAILED]),
            'retrying': len([t for t in all_tasks if t.status == TaskStatus.RETRYING]),
        }
        
        # Calcular tempo médio de execução
        completed_results = [r for r in self.results.values() if r.status == TaskStatus.COMPLETED]
        if completed_results:
            avg_time = sum(r.execution_time for r in completed_results) / len(completed_results)
            stats['average_execution_time'] = avg_time
        
        return stats


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def main():
    """Exemplo de uso do task queue"""
    
    print("=" * 80)
    print("TASK QUEUE PROFISSIONAL - EXEMPLO DE USO")
    print("=" * 80)
    
    # Criar processador
    processor = TaskProcessor()
    
    # Criar tarefas de exemplo
    print("\n📋 CRIANDO TAREFAS")
    print("-" * 80)
    
    tasks = [
        processor.create_task(
            name='send_email',
            payload={
                'to': 'user@example.com',
                'subject': 'Bem-vindo!',
                'body': 'Obrigado por se registrar'
            },
            priority=TaskPriority.HIGH
        ),
        processor.create_task(
            name='generate_report',
            payload={
                'report_type': 'sales',
                'date_range': '2025-01-01 to 2025-12-31'
            },
            priority=TaskPriority.MEDIUM
        ),
        processor.create_task(
            name='process_image',
            payload={
                'image_path': '/images/photo.jpg',
                'filters': ['blur', 'brightness', 'contrast']
            },
            priority=TaskPriority.LOW
        ),
        processor.create_task(
            name='sync_data',
            payload={
                'source': 'database_a',
                'destination': 'database_b'
            },
            priority=TaskPriority.HIGH
        ),
    ]
    
    for task in tasks:
        print(f"  ✓ {task.id}: {task.name} (Prioridade: {task.priority.name})")
    
    # Processar tarefas
    print("\n⚙️  PROCESSANDO TAREFAS")
    print("-" * 80)
    
    for task in tasks:
        result = processor.process_task(task.id)
        print(f"  {task.id}: {result.status.value}")
    
    # Exibir resultados
    print("\n📊 RESULTADOS")
    print("-" * 80)
    
    for task_id, result in processor.results.items():
        print(f"\nTarefa: {task_id}")
        print(f"  Status: {result.status.value}")
        print(f"  Tempo: {result.execution_time:.2f}s")
        if result.result:
            print(f"  Resultado: {json.dumps(result.result, indent=2, ensure_ascii=False)}")
        if result.error:
            print(f"  Erro: {result.error}")
    
    # Exibir estatísticas
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS")
    print("=" * 80)
    
    stats = processor.get_statistics()
    print(f"Total de tarefas: {stats['total_tasks']}")
    print(f"Pendentes: {stats['pending']}")
    print(f"Processando: {stats['processing']}")
    print(f"Concluídas: {stats['completed']}")
    print(f"Falhadas: {stats['failed']}")
    print(f"Tentando novamente: {stats['retrying']}")
    if 'average_execution_time' in stats:
        print(f"Tempo médio de execução: {stats['average_execution_time']:.2f}s")
    
    print(f"\n✅ Exemplo concluído com sucesso!")


if __name__ == "__main__":
    main()
