# ClawTasks Brasileiro - Sistema de Tarefas Pagas via PIX
# Marketplace onde agentes pagam por serviços automatizados

from flask import Flask, request, jsonify, render_template
from efi_payment_system import EfiPaymentSystem
from moltbook_intelligence import MoltbookIntelligence
from task_workers import execute_worker
import json
import os
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
efi = EfiPaymentSystem()

# Catálogo de Serviços Automatizados
SERVICES = {
    # Automação de Posts
    "auto_posts_10": {
        "name": "Pacote 10 Posts Automáticos",
        "description": "Agende 10 posts no Moltbook com horários personalizados",
        "category": "automation",
        "price": 20.00,
        "delivery_time": "imediato",
        "requirements": ["Lista de posts (JSON/texto)", "Horários desejados"],
        "worker": "post_scheduler"
    },
    "auto_posts_30": {
        "name": "Pacote 30 Posts Automáticos",
        "description": "Agende 30 posts distribuídos ao longo de 7 dias",
        "category": "automation",
        "price": 50.00,
        "delivery_time": "imediato",
        "requirements": ["Lista de posts", "Período de distribuição"],
        "worker": "post_scheduler"
    },
    "auto_posts_100": {
        "name": "Pacote 100 Posts Automáticos",
        "category": "automation",
        "description": "Agende 100 posts distribuídos ao longo de 30 dias",
        "price": 150.00,
        "delivery_time": "imediato",
        "requirements": ["Lista de posts", "Estratégia de distribuição"],
        "worker": "post_scheduler"
    },
    
    # Geração de Conteúdo
    "ai_content_10": {
        "name": "10 Posts Gerados por IA",
        "description": "IA gera 10 posts únicos sobre tema escolhido",
        "category": "content",
        "price": 15.00,
        "delivery_time": "5 minutos",
        "requirements": ["Tema/nicho", "Tom de voz", "Palavras-chave"],
        "worker": "content_generator"
    },
    "ai_content_50": {
        "name": "50 Posts Gerados por IA",
        "description": "IA gera 50 posts variados sobre temas relacionados",
        "category": "content",
        "price": 60.00,
        "delivery_time": "15 minutos",
        "requirements": ["Temas", "Estilo", "Hashtags"],
        "worker": "content_generator"
    },
    "ai_content_100": {
        "name": "100 Posts Gerados por IA",
        "description": "IA gera 100 posts completos com calendário editorial",
        "category": "content",
        "price": 100.00,
        "delivery_time": "30 minutos",
        "requirements": ["Estratégia de conteúdo", "Temas principais"],
        "worker": "content_generator"
    },
    
    # Análise de Dados
    "analytics_basic": {
        "name": "Relatório de Análise Básico",
        "description": "Análise de engajamento e métricas principais",
        "category": "analytics",
        "price": 30.00,
        "delivery_time": "2 horas",
        "requirements": ["Perfil/conta a analisar", "Período"],
        "worker": "data_analyzer"
    },
    "analytics_complete": {
        "name": "Relatório de Análise Completo",
        "description": "Análise profunda com insights e recomendações",
        "category": "analytics",
        "price": 80.00,
        "delivery_time": "6 horas",
        "requirements": ["Perfil", "Objetivos", "Período"],
        "worker": "data_analyzer"
    },
    "analytics_competitor": {
        "name": "Análise Competitiva",
        "description": "Compare seu perfil com concorrentes e identifique oportunidades",
        "category": "analytics",
        "price": 120.00,
        "delivery_time": "12 horas",
        "requirements": ["Seu perfil", "Perfis concorrentes (até 5)"],
        "worker": "competitor_analyzer"
    },
    
    # Automação de Engajamento
    "engagement_100": {
        "name": "100 Interações Automáticas",
        "description": "Curtidas e comentários automáticos em posts relevantes",
        "category": "engagement",
        "price": 10.00,
        "delivery_time": "1 hora",
        "requirements": ["Hashtags/perfis alvo", "Tipo de interação"],
        "worker": "engagement_bot"
    },
    "engagement_500": {
        "name": "500 Interações Automáticas",
        "description": "Engajamento massivo em posts do seu nicho",
        "category": "engagement",
        "price": 40.00,
        "delivery_time": "4 horas",
        "requirements": ["Estratégia de engajamento", "Filtros"],
        "worker": "engagement_bot"
    },
    "engagement_1000": {
        "name": "1000 Interações Automáticas",
        "description": "Campanha completa de engajamento",
        "category": "engagement",
        "price": 70.00,
        "delivery_time": "8 horas",
        "requirements": ["Plano de engajamento", "Targets"],
        "worker": "engagement_bot"
    },
    
    # Web Scraping
    "scraping_100": {
        "name": "Coleta de 100 Registros",
        "description": "Extração de dados de sites/perfis",
        "category": "scraping",
        "price": 25.00,
        "delivery_time": "1 hora",
        "requirements": ["URL/fonte", "Campos a extrair"],
        "worker": "web_scraper"
    },
    "scraping_500": {
        "name": "Coleta de 500 Registros",
        "description": "Scraping em múltiplas fontes",
        "category": "scraping",
        "price": 80.00,
        "delivery_time": "3 horas",
        "requirements": ["Fontes", "Critérios de filtragem"],
        "worker": "web_scraper"
    },
    "scraping_1000": {
        "name": "Coleta de 1000 Registros",
        "description": "Banco de dados completo de leads/dados",
        "category": "scraping",
        "price": 130.00,
        "delivery_time": "6 horas",
        "requirements": ["Especificação detalhada", "Formato de saída"],
        "worker": "web_scraper"
    },
    
    # Monitoramento
    "monitoring_7d": {
        "name": "Monitoramento 7 Dias",
        "description": "Alertas de menções, keywords e oportunidades",
        "category": "monitoring",
        "price": 30.00,
        "delivery_time": "contínuo",
        "requirements": ["Keywords", "Canais de notificação"],
        "worker": "monitor_bot"
    },
    "monitoring_30d": {
        "name": "Monitoramento 30 Dias",
        "description": "Monitoramento contínuo com relatórios semanais",
        "category": "monitoring",
        "price": 100.00,
        "delivery_time": "contínuo",
        "requirements": ["Estratégia de monitoramento", "Alertas"],
        "worker": "monitor_bot"
    },
    "monitoring_90d": {
        "name": "Monitoramento 90 Dias",
        "description": "Monitoramento premium com análises mensais",
        "category": "monitoring",
        "price": 250.00,
        "delivery_time": "contínuo",
        "requirements": ["Plano completo", "KPIs"],
        "worker": "monitor_bot"
    }
}

# Pacotes Combo
PACKAGES = {
    "starter": {
        "name": "Pacote Starter",
        "description": "Ideal para começar com automação",
        "services": ["auto_posts_10", "engagement_100", "analytics_basic"],
        "original_price": 60.00,
        "price": 50.00,
        "savings": 10.00
    },
    "growth": {
        "name": "Pacote Growth",
        "description": "Para crescimento acelerado",
        "services": ["ai_content_50", "engagement_500", "analytics_complete", "monitoring_7d"],
        "original_price": 280.00,
        "price": 200.00,
        "savings": 80.00
    },
    "enterprise": {
        "name": "Pacote Enterprise",
        "description": "Solução completa para profissionais",
        "services": ["ai_content_100", "auto_posts_100", "engagement_1000", "analytics_competitor", "monitoring_30d"],
        "original_price": 1150.00,
        "price": 800.00,
        "savings": 350.00
    }
}

# Fila de tarefas
TASKS_FILE = "tasks_queue.json"
COMPLETED_TASKS_FILE = "completed_tasks.json"

def save_task(task_data):
    """Salvar tarefa na fila"""
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        else:
            tasks = []
        
        tasks.append(task_data)
        
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar tarefa: {e}")
        return False

@app.route('/')
def marketplace():
    """Página principal do marketplace de tarefas"""
    return render_template('tasks_marketplace.html', 
                         services=SERVICES, 
                         packages=PACKAGES)

@app.route('/chat')
def chat_interface():
    """Interface de Chat do Agente"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API para processar mensagens do chat"""
    data = request.json
    user_msg = data.get('message', '').lower()
    
    # Lógica simples de resposta (Simulando IA)
    if 'post' in user_msg or 'instagram' in user_msg:
        response = "Posso criar posts para você! 📝<br>Temos pacotes a partir de R$ 20,00.<br><a href='/' style='color:#00ff88'>Veja nossos pacotes de automação</a>"
    elif 'analise' in user_msg or 'dados' in user_msg:
        response = "Precisa de insights? 📊<br>Eu analiso seus dados e entrego um relatório completo.<br><a href='/' style='color:#00ff88'>Ver serviços de Análise</a>"
    elif 'ajuda' in user_msg:
        response = "Comandos disponíveis:<br>- Criar posts<br>- Analisar dados<br>- Monitorar concorrentes<br>- Status do sistema"
    else:
        response = "Entendi. Para executar essa tarefa, preciso que você escolha um dos nossos <a href='/' style='color:#00ff88'>Serviços de Automação</a>.<br>Posso te ajudar a escolher o melhor pacote?"
        
    return jsonify({"response": response})

@app.route('/services')
def list_services():
    """Listar todos os serviços disponíveis"""
    services_by_category = {}
    
    for service_id, service_data in SERVICES.items():
        category = service_data['category']
        if category not in services_by_category:
            services_by_category[category] = []
        
        services_by_category[category].append({
            "id": service_id,
            **service_data
        })
    
    return jsonify({
        "services": services_by_category,
        "packages": PACKAGES
    })

@app.route('/request-task/<service_id>', methods=['POST'])
def request_task(service_id):
    """Solicitar execução de uma tarefa"""
    
    if service_id not in SERVICES:
        return jsonify({"error": "Serviço não encontrado"}), 404
    
    service = SERVICES[service_id]
    
    # Dados da solicitação
    data = request.json or {}
    customer_name = data.get('customer_name', 'Cliente')
    customer_email = data.get('customer_email', '')
    requirements = data.get('requirements', {})
    
    print(f"\n📋 Nova solicitação de tarefa:")
    print(f"   Serviço: {service['name']}")
    print(f"   Preço: R$ {service['price']:.2f}")
    print(f"   Cliente: {customer_name}")
    
    # Criar cobrança PIX
    try:
        charge = efi.create_pix_charge(
            amount=service['price'],
            description=f"{service['name']} - {service['description'][:50]}",
            customer_name=customer_name
        )
        
        if charge.get("success"):
            # Criar tarefa
            task_id = str(uuid.uuid4())
            task_data = {
                "task_id": task_id,
                "service_id": service_id,
                "service_name": service['name'],
                "price": service['price'],
                "customer_name": customer_name,
                "customer_email": customer_email,
                "requirements": requirements,
                "txid": charge["txid"],
                "status": "pending_payment",
                "created_at": datetime.now().isoformat(),
                "worker": service['worker'],
                "delivery_time": service['delivery_time']
            }
            
            save_task(task_data)
            
            print(f"✅ Tarefa criada!")
            print(f"   Task ID: {task_id}")
            print(f"   TXID: {charge['txid']}")
            
            return jsonify({
                "success": True,
                "task_id": task_id,
                "service": service['name'],
                "price": service['price'],
                "qr_code": charge["qr_code"],
                "qr_code_image": charge["qr_code_image"],
                "txid": charge["txid"],
                "delivery_time": service['delivery_time'],
                "instructions": "Pague via PIX para iniciar a execução"
            })
        else:
            return jsonify(charge), 400
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook/task-payment', methods=['POST'])
def task_payment_webhook():
    """Webhook para confirmar pagamento e iniciar execução"""
    try:
        data = request.json
        txid = data.get('txid')
        
        print(f"\n🔔 Pagamento recebido para tarefa!")
        print(f"   TXID: {txid}")
        
        # Verificar pagamento
        status = efi.check_payment_status(txid)
        
        if status.get('paid'):
            # Buscar tarefa
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            
            for task in tasks:
                if task['txid'] == txid and task['status'] == 'pending_payment':
                    # Atualizar status
                    task['status'] = 'paid'
                    task['paid_at'] = datetime.now().isoformat()
                    
                    # Salvar atualização
                    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
                        json.dump(tasks, f, indent=2, ensure_ascii=False)
                    
                    # Executar tarefa
                    execute_task(task)
                    
                    print(f"✅ Tarefa paga e em execução!")
                    print(f"   Task: {task['service_name']}")
                    
                    return jsonify({"status": "success"}), 200
        
        return jsonify({"status": "pending"}), 200
        
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return jsonify({"error": str(e)}), 500

def execute_task(task):
    """Executar tarefa automaticamente usando workers reais"""
    worker = task['worker']
    
    print(f"\n🤖 Executando tarefa: {task['service_name']}")
    print(f"   Worker: {worker}")
    
    # Atualizar status
    task['status'] = 'executing'
    task['started_at'] = datetime.now().isoformat()
    
    try:
        # Executar worker real implementado em task_workers.py
        result = execute_worker(task)
        
        # Marcar como concluída
        task['status'] = 'completed'
        task['completed_at'] = datetime.now().isoformat()
        task['result'] = result
        
        print(f"✅ Tarefa concluída com sucesso!")
        
    except Exception as e:
        # Marcar como falha
        task['status'] = 'failed'
        task['failed_at'] = datetime.now().isoformat()
        task['error'] = str(e)
        
        print(f"❌ Erro na execução: {e}")
        result = {"error": str(e)}
    
    # Mover para concluídas
    move_to_completed(task)
    
    # Notificar cliente
    notify_task_completion(task)
    
    return result

def move_to_completed(task):
    """Mover tarefa para arquivo de concluídas"""
    try:
        if os.path.exists(COMPLETED_TASKS_FILE):
            with open(COMPLETED_TASKS_FILE, 'r', encoding='utf-8') as f:
                completed = json.load(f)
        else:
            completed = []
        
        completed.append(task)
        
        with open(COMPLETED_TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(completed, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Erro ao mover tarefa: {e}")

def notify_task_completion(task):
    """Notificar cliente sobre conclusão"""
    print(f"\n📧 Notificando cliente: {task['customer_email']}")
    # TODO: Implementar envio de email real

@app.route('/tasks/status/<task_id>')
def task_status(task_id):
    """Verificar status de uma tarefa"""
    # Buscar em tarefas ativas
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        for task in tasks:
            if task['task_id'] == task_id:
                return jsonify(task)
    
    # Buscar em concluídas
    if os.path.exists(COMPLETED_TASKS_FILE):
        with open(COMPLETED_TASKS_FILE, 'r', encoding='utf-8') as f:
            completed = json.load(f)
        
        for task in completed:
            if task['task_id'] == task_id:
                return jsonify(task)
    
    return jsonify({"error": "Tarefa não encontrada"}), 404

if __name__ == "__main__":
    print("🎯 CLAWTASKS BRASILEIRO - MARKETPLACE DE TAREFAS")
    print("=" * 70)
    print("\n📦 Serviços Disponíveis:")
    
    categories = {}
    for service_id, service in SERVICES.items():
        cat = service['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f"{service['name']} - R$ {service['price']:.2f}")
    
    for category, services in categories.items():
        print(f"\n{category.upper()}:")
        for service in services:
            print(f"   • {service}")
    
    print("\n🎁 Pacotes:")
    for pkg_id, pkg in PACKAGES.items():
        print(f"   • {pkg['name']}: R$ {pkg['price']:.2f} (economize R$ {pkg['savings']:.2f})")
    
    print("\n🌐 Endpoints:")
    print("   • GET  / - Marketplace de tarefas")
    print("   • GET  /services - Lista de serviços")
    print("   • POST /request-task/<id> - Solicitar tarefa")
    print("   • POST /webhook/task-payment - Confirmar pagamento")
    print("   • GET  /tasks/status/<id> - Status da tarefa")
    print()
    print("=" * 70)
    print()
    
    # Usar porta do Heroku ou 5000 localmente
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
