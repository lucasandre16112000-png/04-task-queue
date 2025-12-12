"""
Sistema de Fila de Tarefas Distribuído (Task Queue)

Um sistema robusto e profissional de processamento assíncrono de tarefas,
demonstrando as melhores práticas em arquitetura de sistemas distribuídos.

Funcionalidades:
- Enfileiramento de tarefas com priorização
- Processamento assíncrono com handlers modulares
- Retry automático com exponential backoff
- Logging estruturado e monitoramento
- Estatísticas detalhadas de execução

Desenvolvido por Lucas André S
GitHub: https://github.com/lucasandre16112000-png
"""

import json
import logging
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================

def _configure_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configurar logging estruturado para o sistema.
    
    Args:
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Logger configurado
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


logger = _configure_logging()


# ============================================================================
# ENUMS E TIPOS
# ============================================================================

class TaskStatus(Enum):
    """Estados possíveis de uma tarefa no sistema."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Níveis de prioridade para processamento de tarefas."""
    LOW = 3
    MEDIUM = 2
    HIGH = 1


# ============================================================================
# MODELOS DE DADOS
# ============================================================================

@dataclass
class Task:
    """
    Modelo representando uma tarefa no sistema.
    
    Attributes:
        id: Identificador único da tarefa
        name: Nome/tipo da tarefa
        payload: Dados específicos para processamento
        priority: Nível de prioridade (HIGH, MEDIUM, LOW)
        status: Estado atual da tarefa
        created_at: Timestamp de criação
        started_at: Timestamp de início do processamento
        completed_at: Timestamp de conclusão
        result: Resultado do processamento
        error: Mensagem de erro (se houver)
        retry_count: Número de tentativas realizadas
        max_retries: Número máximo de tentativas
    """
    id: str
    name: str
    payload: Dict[str, Any]
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class TaskResult:
    """
    Modelo representando o resultado de uma tarefa processada.
    
    Attributes:
        task_id: ID da tarefa processada
        status: Status final da tarefa
        result: Dados retornados pelo handler
        error: Mensagem de erro (se houver)
        execution_time: Tempo de execução em segundos
        completed_at: Timestamp de conclusão
    """
    task_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    completed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# PROCESSADOR DE TAREFAS
# ============================================================================

class TaskProcessor:
    """
    Processador central de tarefas com suporte a priorização e retry.
    
    Gerencia o ciclo de vida completo das tarefas, desde criação até
    processamento, incluindo tratamento de erros e retry automático.
    """
    
    def __init__(self) -> None:
        """Inicializar o processador de tarefas."""
        self._tasks: Dict[str, Task] = {}
        self._results: Dict[str, TaskResult] = {}
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
            'send_email': self._handle_send_email,
            'generate_report': self._handle_generate_report,
            'process_image': self._handle_process_image,
            'sync_data': self._handle_sync_data,
            'cleanup': self._handle_cleanup,
        }
        logger.info("TaskProcessor inicializado")
    
    def register_handler(
        self,
        task_name: str,
        handler: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> None:
        """
        Registrar um handler customizado para um tipo de tarefa.
        
        Args:
            task_name: Nome do tipo de tarefa
            handler: Função que processa a tarefa
            
        Raises:
            ValueError: Se task_name ou handler for inválido
        """
        if not task_name or not callable(handler):
            raise ValueError("task_name e handler devem ser válidos")
        
        self._handlers[task_name] = handler
        logger.info(f"Handler registrado para tarefa: {task_name}")
    
    def create_task(
        self,
        name: str,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.MEDIUM,
        task_id: Optional[str] = None
    ) -> Task:
        """
        Criar uma nova tarefa no sistema.
        
        Args:
            name: Tipo/nome da tarefa
            payload: Dados para processamento
            priority: Nível de prioridade
            task_id: ID customizado (gerado automaticamente se não fornecido)
            
        Returns:
            Task criada
            
        Raises:
            ValueError: Se name ou payload for inválido
        """
        if not name or not isinstance(payload, dict):
            raise ValueError("name e payload devem ser válidos")
        
        if task_id is None:
            task_id = f"task_{int(time.time() * 1000)}"
        
        task = Task(
            id=task_id,
            name=name,
            payload=payload,
            priority=priority
        )
        
        self._tasks[task_id] = task
        logger.info(f"Tarefa criada: {task_id} (tipo: {name}, prioridade: {priority.name})")
        
        return task
    
    def process_task(self, task_id: str) -> TaskResult:
        """
        Processar uma tarefa usando seu handler correspondente.
        
        Implementa lógica de retry com exponential backoff em caso de falha.
        
        Args:
            task_id: ID da tarefa a processar
            
        Returns:
            TaskResult com resultado ou erro
        """
        if task_id not in self._tasks:
            logger.error(f"Tarefa não encontrada: {task_id}")
            return TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error="Tarefa não encontrada"
            )
        
        task = self._tasks[task_id]
        
        # Evitar reprocessamento
        if task.status == TaskStatus.COMPLETED:
            logger.warning(f"Tarefa já foi processada: {task_id}")
            return self._results.get(task_id)
        
        logger.info(f"Iniciando processamento: {task_id} (tipo: {task.name})")
        
        task.status = TaskStatus.PROCESSING
        task.started_at = datetime.utcnow().isoformat()
        
        start_time = time.time()
        
        try:
            # Obter handler para tipo de tarefa
            handler = self._handlers.get(task.name)
            
            if handler is None:
                raise ValueError(f"Handler não encontrado para tipo: {task.name}")
            
            # Executar handler
            result = handler(task.payload)
            
            execution_time = time.time() - start_time
            
            # Atualizar tarefa com sucesso
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow().isoformat()
            task.result = result
            
            task_result = TaskResult(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                result=result,
                execution_time=execution_time
            )
            
            self._results[task_id] = task_result
            
            logger.info(
                f"✓ Tarefa concluída com sucesso: {task_id} "
                f"(tempo: {execution_time:.2f}s)"
            )
            
            return task_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            logger.error(f"✗ Erro ao processar tarefa {task_id}: {error_msg}")
            
            # Tentar retry com exponential backoff
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING
                
                wait_time = 2 ** task.retry_count
                logger.info(
                    f"Tentando novamente ({task.retry_count}/{task.max_retries}): "
                    f"{task_id} (aguardando {wait_time}s)"
                )
                
                time.sleep(wait_time)
                return self.process_task(task_id)
            else:
                # Marcar como falhada após todas as tentativas
                task.status = TaskStatus.FAILED
                task.error = error_msg
                task.completed_at = datetime.utcnow().isoformat()
                
                task_result = TaskResult(
                    task_id=task_id,
                    status=TaskStatus.FAILED,
                    error=error_msg,
                    execution_time=execution_time
                )
                
                self._results[task_id] = task_result
                
                logger.error(
                    f"Tarefa falhou permanentemente: {task_id} "
                    f"(tentativas: {task.retry_count}/{task.max_retries})"
                )
                
                return task_result
    
    # ========================================================================
    # HANDLERS DE TAREFAS
    # ========================================================================
    
    def _handle_send_email(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler para envio de email.
        
        Args:
            payload: Deve conter 'to' e 'subject'
            
        Returns:
            Resultado do envio
        """
        logger.debug(f"Processando envio de email para: {payload.get('to')}")
        time.sleep(1)  # Simular processamento
        
        return {
            'status': 'sent',
            'to': payload.get('to'),
            'subject': payload.get('subject'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_generate_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler para geração de relatório.
        
        Args:
            payload: Deve conter 'report_type'
            
        Returns:
            Metadados do relatório gerado
        """
        logger.debug(f"Gerando relatório: {payload.get('report_type')}")
        time.sleep(2)  # Simular processamento
        
        return {
            'status': 'generated',
            'report_type': payload.get('report_type'),
            'filename': f"report_{int(time.time())}.pdf",
            'size_mb': 2.5,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_process_image(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler para processamento de imagem.
        
        Args:
            payload: Deve conter 'image_path' e opcionalmente 'filters'
            
        Returns:
            Resultado do processamento
        """
        logger.debug(f"Processando imagem: {payload.get('image_path')}")
        time.sleep(3)  # Simular processamento
        
        return {
            'status': 'processed',
            'original_path': payload.get('image_path'),
            'output_path': f"processed_{payload.get('image_path')}",
            'filters_applied': payload.get('filters', []),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_sync_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler para sincronização de dados.
        
        Args:
            payload: Deve conter 'source' e 'destination'
            
        Returns:
            Resultado da sincronização
        """
        logger.debug(f"Sincronizando dados de: {payload.get('source')}")
        time.sleep(2)  # Simular processamento
        
        return {
            'status': 'synced',
            'source': payload.get('source'),
            'destination': payload.get('destination'),
            'records_synced': 1000,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _handle_cleanup(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler para limpeza de dados.
        
        Args:
            payload: Deve conter 'target'
            
        Returns:
            Resultado da limpeza
        """
        logger.debug(f"Limpando dados: {payload.get('target')}")
        time.sleep(1)  # Simular processamento
        
        return {
            'status': 'cleaned',
            'target': payload.get('target'),
            'items_removed': 500,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    # ========================================================================
    # MÉTODOS DE CONSULTA
    # ========================================================================
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """
        Obter status atual de uma tarefa.
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            Task ou None se não encontrada
        """
        return self._tasks.get(task_id)
    
    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """
        Obter resultado de uma tarefa processada.
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            TaskResult ou None se não processada
        """
        return self._results.get(task_id)
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """
        Listar tarefas, opcionalmente filtradas por status.
        
        Args:
            status: Status para filtrar (opcional)
            
        Returns:
            Lista de tarefas ordenadas por prioridade
        """
        tasks = list(self._tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        return sorted(tasks, key=lambda t: t.priority.value)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obter estatísticas de processamento do sistema.
        
        Returns:
            Dicionário com estatísticas detalhadas
        """
        all_tasks = list(self._tasks.values())
        
        stats = {
            'total_tasks': len(all_tasks),
            'pending': len([t for t in all_tasks if t.status == TaskStatus.PENDING]),
            'processing': len([t for t in all_tasks if t.status == TaskStatus.PROCESSING]),
            'completed': len([t for t in all_tasks if t.status == TaskStatus.COMPLETED]),
            'failed': len([t for t in all_tasks if t.status == TaskStatus.FAILED]),
            'retrying': len([t for t in all_tasks if t.status == TaskStatus.RETRYING]),
        }
        
        # Calcular tempo médio de execução
        completed_results = [
            r for r in self._results.values()
            if r.status == TaskStatus.COMPLETED
        ]
        
        if completed_results:
            avg_time = sum(r.execution_time for r in completed_results) / len(completed_results)
            stats['average_execution_time'] = avg_time
        
        return stats


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def main() -> None:
    """
    Exemplo de uso do sistema de fila de tarefas.
    
    Demonstra criação, processamento e monitoramento de tarefas.
    """
    
    print("\n" + "=" * 80)
    print("SISTEMA DE FILA DE TAREFAS DISTRIBUÍDO - EXEMPLO DE USO")
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
    
    for task_id, result in processor._results.items():
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
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
