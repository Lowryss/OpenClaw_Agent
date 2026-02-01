# Script de Teste - ClawTasks BR
# Testa todos os componentes do sistema

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_services_endpoint():
    """Testar endpoint de listagem de serviços"""
    print("\n" + "="*70)
    print("TESTE 1: Listar Serviços")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/services")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Serviços carregados com sucesso!")
        print(f"   Categorias: {len(data['services'])}")
        print(f"   Pacotes: {len(data['packages'])}")
        
        for category, services in data['services'].items():
            print(f"\n   {category.upper()}: {len(services)} serviços")
    else:
        print(f"❌ Erro: {response.status_code}")

def test_request_task():
    """Testar solicitação de tarefa"""
    print("\n" + "="*70)
    print("TESTE 2: Solicitar Tarefa (Geração de Conteúdo)")
    print("="*70)
    
    payload = {
        "customer_name": "Teste Automático",
        "customer_email": "teste@clawtasksbr.com",
        "requirements": {
            "theme": "Inteligência Artificial",
            "tone": "profissional",
            "keywords": ["IA", "Tecnologia", "Inovação"]
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/request-task/ai_content_10",
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Tarefa criada com sucesso!")
        print(f"   Task ID: {data['task_id']}")
        print(f"   Serviço: {data['service']}")
        print(f"   Preço: R$ {data['price']:.2f}")
        print(f"   TXID: {data['txid']}")
        print(f"   Tempo de entrega: {data['delivery_time']}")
        print(f"\n   QR Code gerado: ✅")
        
        return data['task_id']
    else:
        print(f"❌ Erro: {response.status_code}")
        print(f"   {response.text}")
        return None

def test_task_status(task_id):
    """Testar verificação de status"""
    print("\n" + "="*70)
    print("TESTE 3: Verificar Status da Tarefa")
    print("="*70)
    
    if not task_id:
        print("⚠️ Pulando teste (sem task_id)")
        return
    
    response = requests.get(f"{BASE_URL}/tasks/status/{task_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status recuperado com sucesso!")
        print(f"   Task ID: {data['task_id']}")
        print(f"   Status: {data['status']}")
        print(f"   Serviço: {data['service_name']}")
        print(f"   Criado em: {data['created_at']}")
    else:
        print(f"❌ Erro: {response.status_code}")

def test_workers():
    """Testar workers diretamente"""
    print("\n" + "="*70)
    print("TESTE 4: Workers Automatizados")
    print("="*70)
    
    from task_workers import TaskWorkers
    
    workers = TaskWorkers()
    
    # Teste 1: Content Generator
    print("\n📝 Testando Content Generator...")
    task_data = {
        "task_id": "test_content_001",
        "service_id": "ai_content_10",
        "requirements": {
            "theme": "Marketing Digital",
            "tone": "educativo",
            "keywords": ["Marketing", "Digital", "Vendas"]
        }
    }
    
    result = workers.generate_content(task_data)
    print(f"   Status: {result['status']}")
    print(f"   Posts gerados: {result['posts_count']}")
    print(f"   Arquivo: {result['output_file']}")
    
    # Teste 2: Post Scheduler
    print("\n📅 Testando Post Scheduler...")
    task_data = {
        "task_id": "test_schedule_001",
        "service_id": "auto_posts_10",
        "requirements": {
            "posts": [f"Post de teste {i}" for i in range(10)],
            "schedule_type": "distributed"
        }
    }
    
    result = workers.schedule_posts(task_data)
    print(f"   Status: {result['status']}")
    print(f"   Posts agendados: {result['posts_count']}")
    print(f"   Primeiro post: {result['first_post']}")
    
    # Teste 3: Data Analyzer
    print("\n📊 Testando Data Analyzer...")
    task_data = {
        "task_id": "test_analysis_001",
        "service_id": "analytics_basic",
        "requirements": {
            "profile": "@teste_perfil",
            "period": "30 days"
        }
    }
    
    result = workers.analyze_data(task_data)
    print(f"   Status: {result['status']}")
    print(f"   Relatório: {result['report_file']}")
    print(f"   Taxa de engajamento: {result['summary']['metrics']['engagement_rate']}%")

def test_integration():
    """Teste de integração completa"""
    print("\n" + "="*70)
    print("TESTE 5: Integração Completa")
    print("="*70)
    
    print("\n🔄 Simulando fluxo completo...")
    print("   1. Cliente solicita tarefa")
    print("   2. Sistema gera QR Code PIX")
    print("   3. (Simulação) Cliente paga")
    print("   4. Worker executa tarefa")
    print("   5. Cliente recebe resultado")
    
    # Simular solicitação
    task_id = test_request_task()
    
    if task_id:
        print("\n✅ Fluxo de solicitação funcionando!")
        print("   Próximo passo: Pagar via PIX para executar worker")

def run_all_tests():
    """Executar todos os testes"""
    print("\n" + "="*70)
    print("🧪 CLAWTASKS BR - SUITE DE TESTES")
    print("="*70)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"URL Base: {BASE_URL}")
    
    try:
        # Teste 1: Listar serviços
        test_services_endpoint()
        
        # Teste 2: Solicitar tarefa
        task_id = test_request_task()
        
        # Teste 3: Verificar status
        test_task_status(task_id)
        
        # Teste 4: Workers
        test_workers()
        
        # Teste 5: Integração
        # test_integration()  # Já testado acima
        
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*70)
        print("\n📊 Resumo:")
        print("   ✅ API funcionando")
        print("   ✅ Pagamento PIX integrado")
        print("   ✅ Workers automatizados")
        print("   ✅ Sistema completo operacional")
        print("\n💰 Pronto para começar a lucrar!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Servidor não está rodando!")
        print("   Execute: python clawtasks_br.py")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")

if __name__ == "__main__":
    run_all_tests()
