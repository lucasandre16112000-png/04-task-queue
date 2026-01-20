/**
 * Task Queue Dashboard - JavaScript
 * Interatividade e comunicação com a API
 */

// ============================================================================
// Configuração
// ============================================================================

const API_BASE = '';
let refreshInterval = null;

// Mapeamento de ícones por tipo de tarefa
const TASK_ICONS = {
    'send_email': '📧',
    'generate_report': '📄',
    'process_image': '🖼️',
    'sync_data': '🔄',
    'cleanup': '🧹'
};

// Mapeamento de nomes amigáveis
const TASK_NAMES = {
    'send_email': 'Enviar Email',
    'generate_report': 'Gerar Relatório',
    'process_image': 'Processar Imagem',
    'sync_data': 'Sincronizar Dados',
    'cleanup': 'Limpar Cache'
};

// Payloads padrão para cada tipo de tarefa
const DEFAULT_PAYLOADS = {
    'send_email': {
        to: 'usuario@exemplo.com',
        subject: 'Notificação do Sistema',
        body: 'Esta é uma mensagem de teste.'
    },
    'generate_report': {
        report_type: 'vendas_mensal',
        format: 'PDF',
        include_charts: true
    },
    'process_image': {
        image_name: 'foto_perfil.jpg',
        filters: ['resize', 'optimize', 'watermark']
    },
    'sync_data': {
        source: 'database_producao',
        destination: 'database_backup'
    },
    'cleanup': {
        target: 'cache_temporario',
        older_than_days: 7
    }
};

// ============================================================================
// Inicialização
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    loadTasks();
    
    // Atualizar automaticamente a cada 2 segundos
    refreshInterval = setInterval(() => {
        loadStatistics();
        loadTasks();
    }, 2000);
});

// ============================================================================
// Funções de API
// ============================================================================

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/api/statistics`);
        const stats = await response.json();
        
        document.getElementById('stat-total').textContent = stats.total;
        document.getElementById('stat-pending').textContent = stats.pending;
        document.getElementById('stat-processing').textContent = stats.processing;
        document.getElementById('stat-completed').textContent = stats.completed;
        document.getElementById('stat-failed').textContent = stats.failed;
        document.getElementById('stat-success-rate').textContent = `${stats.success_rate}%`;
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE}/api/tasks`);
        const tasks = await response.json();
        
        const container = document.getElementById('tasks-container');
        const emptyState = document.getElementById('empty-state');
        
        if (tasks.length === 0) {
            container.innerHTML = '';
            container.appendChild(createEmptyState());
            return;
        }
        
        container.innerHTML = tasks.map(task => createTaskCard(task)).join('');
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
    }
}

async function createTask(taskType) {
    try {
        const payload = DEFAULT_PAYLOADS[taskType] || {};
        
        const response = await fetch(`${API_BASE}/api/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: taskType,
                payload: payload,
                priority: 'HIGH'
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('✅', `Tarefa "${TASK_NAMES[taskType]}" criada com sucesso!`);
            loadStatistics();
            loadTasks();
        } else {
            showToast('❌', 'Erro ao criar tarefa');
        }
    } catch (error) {
        console.error('Erro ao criar tarefa:', error);
        showToast('❌', 'Erro ao criar tarefa');
    }
}

async function createAllTasks() {
    const taskTypes = ['send_email', 'generate_report', 'process_image', 'sync_data', 'cleanup'];
    
    showToast('⚡', 'Criando todas as tarefas...');
    
    for (const taskType of taskTypes) {
        await createTask(taskType);
        await sleep(300); // Pequeno delay entre criações
    }
    
    showToast('✅', 'Todas as 5 tarefas foram criadas!');
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_BASE}/api/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('🗑️', 'Tarefa removida!');
            loadStatistics();
            loadTasks();
        }
    } catch (error) {
        console.error('Erro ao deletar tarefa:', error);
    }
}

async function clearAllTasks() {
    if (!confirm('Tem certeza que deseja remover todas as tarefas?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/tasks/clear`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('🗑️', 'Todas as tarefas foram removidas!');
            loadStatistics();
            loadTasks();
        }
    } catch (error) {
        console.error('Erro ao limpar tarefas:', error);
    }
}

// ============================================================================
// Funções de UI
// ============================================================================

function createEmptyState() {
    const div = document.createElement('div');
    div.className = 'empty-state';
    div.id = 'empty-state';
    div.innerHTML = `
        <span class="empty-icon">📭</span>
        <p>Nenhuma tarefa criada ainda.</p>
        <p class="empty-hint">Clique em um dos botões acima para criar uma tarefa!</p>
    `;
    return div;
}

function createTaskCard(task) {
    const icon = TASK_ICONS[task.name] || '📋';
    const name = TASK_NAMES[task.name] || task.name;
    const statusClass = task.status;
    const statusText = getStatusText(task.status);
    
    // Formatar data
    const createdAt = new Date(task.created_at).toLocaleString('pt-BR');
    
    // Resultado ou erro
    let resultHtml = '';
    if (task.status === 'completed' && task.result) {
        const message = task.result.message || 'Tarefa concluída com sucesso!';
        resultHtml = `
            <div class="task-result">
                <div class="result-message">
                    ✅ ${message}
                </div>
            </div>
        `;
    } else if (task.status === 'failed' && task.error) {
        resultHtml = `
            <div class="task-result">
                <div class="error-message">
                    ❌ ${task.error}
                </div>
            </div>
        `;
    }
    
    return `
        <div class="task-card status-${statusClass}">
            <div class="task-header">
                <div class="task-title">
                    <span class="task-icon">${icon}</span>
                    <div>
                        <div class="task-name">${name}</div>
                        <div class="task-id">ID: ${task.id}</div>
                    </div>
                </div>
                <div class="task-status">
                    <span class="status-badge ${statusClass}">${statusText}</span>
                    <button class="delete-btn" onclick="deleteTask('${task.id}')" title="Remover tarefa">
                        🗑️
                    </button>
                </div>
            </div>
            <div class="task-details">
                <div class="task-detail">
                    <span class="detail-label">Prioridade</span>
                    <span class="detail-value">${task.priority}</span>
                </div>
                <div class="task-detail">
                    <span class="detail-label">Criada em</span>
                    <span class="detail-value">${createdAt}</span>
                </div>
                <div class="task-detail">
                    <span class="detail-label">Tempo de Execução</span>
                    <span class="detail-value">${task.execution_time > 0 ? task.execution_time + 's' : '-'}</span>
                </div>
            </div>
            ${resultHtml}
        </div>
    `;
}

function getStatusText(status) {
    const statusMap = {
        'pending': '⏳ Pendente',
        'processing': '🔄 Processando',
        'completed': '✅ Concluída',
        'failed': '❌ Falhou',
        'retrying': '🔁 Tentando novamente'
    };
    return statusMap[status] || status;
}

function showToast(icon, message) {
    const toast = document.getElementById('toast');
    const toastIcon = document.getElementById('toast-icon');
    const toastMessage = document.getElementById('toast-message');
    
    toastIcon.textContent = icon;
    toastMessage.textContent = message;
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
