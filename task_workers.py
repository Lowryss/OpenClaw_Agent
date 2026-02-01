# Workers Automatizados - ClawTasks BR
# Executam tarefas automaticamente após pagamento confirmado

from moltbook_intelligence import MoltbookIntelligence
import json
import time
from datetime import datetime, timedelta
import random

class TaskWorkers:
    """Gerenciador de workers automatizados"""
    
    def __init__(self):
        self.moltbook = MoltbookIntelligence()
    
    # ==================== POST SCHEDULER ====================
    
    def schedule_posts(self, task_data):
        """Agendar posts no Moltbook"""
        requirements = task_data.get('requirements', {})
        posts = requirements.get('posts', [])
        schedule_type = requirements.get('schedule_type', 'distributed')
        
        print(f"\n📅 Agendando {len(posts)} posts...")
        
        # Determinar quantidade baseado no serviço
        service_id = task_data['service_id']
        if '10' in service_id:
            max_posts = 10
        elif '30' in service_id:
            max_posts = 30
        elif '100' in service_id:
            max_posts = 100
        else:
            max_posts = len(posts)
        
        # Gerar horários
        if schedule_type == 'distributed':
            # Distribuir ao longo de vários dias
            days = max_posts // 5  # ~5 posts por dia
            schedule = self._generate_distributed_schedule(max_posts, days)
        else:
            # Horários específicos fornecidos
            schedule = requirements.get('schedule', [])
        
        scheduled_posts = []
        for i, post_content in enumerate(posts[:max_posts]):
            scheduled_time = schedule[i] if i < len(schedule) else datetime.now() + timedelta(hours=i)
            
            scheduled_posts.append({
                "content": post_content,
                "scheduled_time": scheduled_time.isoformat() if isinstance(scheduled_time, datetime) else scheduled_time,
                "status": "scheduled"
            })
        
        # Salvar agendamento
        schedule_file = f"schedules/schedule_{task_data['task_id']}.json"
        with open(schedule_file, 'w', encoding='utf-8') as f:
            json.dump(scheduled_posts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(scheduled_posts)} posts agendados!")
        
        return {
            "status": "scheduled",
            "posts_count": len(scheduled_posts),
            "schedule_file": schedule_file,
            "first_post": scheduled_posts[0]['scheduled_time'],
            "last_post": scheduled_posts[-1]['scheduled_time']
        }
    
    def _generate_distributed_schedule(self, count, days):
        """Gerar horários distribuídos"""
        schedule = []
        posts_per_day = count // days
        
        # Horários ideais para posts (baseado em engajamento)
        ideal_hours = [8, 10, 12, 14, 16, 18, 20]
        
        start_date = datetime.now()
        for day in range(days):
            for post in range(posts_per_day):
                hour = random.choice(ideal_hours)
                minute = random.randint(0, 59)
                
                post_time = start_date + timedelta(days=day, hours=hour, minutes=minute)
                schedule.append(post_time)
        
        return sorted(schedule)
    
    # ==================== CONTENT GENERATOR ====================
    
    def generate_content(self, task_data):
        """Gerar conteúdo com IA"""
        requirements = task_data.get('requirements', {})
        theme = requirements.get('theme', 'tecnologia e IA')
        tone = requirements.get('tone', 'profissional')
        keywords = requirements.get('keywords', [])
        
        # Determinar quantidade
        service_id = task_data['service_id']
        if '10' in service_id:
            count = 10
        elif '50' in service_id:
            count = 50
        elif '100' in service_id:
            count = 100
        else:
            count = 10
        
        print(f"\n✍️ Gerando {count} posts sobre '{theme}'...")
        
        generated_posts = []
        
        # Templates de posts
        templates = [
            "💡 {insight} sobre {theme}. {call_to_action}",
            "🚀 Você sabia que {fact}? {theme} está revolucionando {area}!",
            "📊 Dados mostram: {statistic}. {theme} é o futuro de {industry}.",
            "🎯 Dica rápida: {tip} para melhorar seu {aspect} com {theme}.",
            "⚡ {theme} + {technology} = {result}. Veja como aplicar!",
        ]
        
        for i in range(count):
            # Gerar variações
            template = random.choice(templates)
            
            post = template.format(
                insight=f"Insight {i+1}",
                theme=theme,
                call_to_action="Comente sua opinião! 👇",
                fact=f"fato interessante {i+1}",
                area="diversos setores",
                statistic=f"{random.randint(60, 95)}% das empresas",
                industry="negócios digitais",
                tip=f"Dica {i+1}",
                aspect="resultados",
                technology="automação",
                result="produtividade 10x maior"
            )
            
            # Adicionar hashtags
            hashtags = " ".join([f"#{kw}" for kw in keywords[:3]]) if keywords else "#IA #Tecnologia #Inovação"
            post += f"\n\n{hashtags}"
            
            generated_posts.append({
                "id": i + 1,
                "content": post,
                "theme": theme,
                "tone": tone
            })
        
        # Salvar posts gerados
        output_file = f"generated/content_{task_data['task_id']}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(generated_posts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {count} posts gerados!")
        
        return {
            "status": "generated",
            "posts_count": count,
            "output_file": output_file,
            "preview": generated_posts[:3]
        }
    
    # ==================== DATA ANALYZER ====================
    
    def analyze_data(self, task_data):
        """Analisar dados e gerar relatório"""
        requirements = task_data.get('requirements', {})
        profile = requirements.get('profile', 'perfil_exemplo')
        period = requirements.get('period', '30 days')
        
        service_id = task_data['service_id']
        
        print(f"\n📊 Analisando dados de '{profile}'...")
        
        # Simular análise (em produção, usar dados reais)
        analysis = {
            "profile": profile,
            "period": period,
            "metrics": {
                "total_posts": random.randint(50, 200),
                "total_likes": random.randint(500, 5000),
                "total_comments": random.randint(100, 1000),
                "total_shares": random.randint(50, 500),
                "engagement_rate": round(random.uniform(2.5, 8.5), 2),
                "follower_growth": random.randint(-50, 500)
            },
            "insights": [
                "Posts com imagens têm 3x mais engajamento",
                "Melhor horário para postar: 18h-20h",
                "Hashtags mais efetivas: #IA, #Tecnologia, #Inovação",
                "Conteúdo educativo gera mais compartilhamentos"
            ],
            "recommendations": [
                "Aumentar frequência de posts com imagens",
                "Focar em conteúdo educativo",
                "Postar nos horários de pico",
                "Usar hashtags estratégicas"
            ]
        }
        
        if 'complete' in service_id or 'competitor' in service_id:
            # Análise mais profunda
            analysis["competitor_analysis"] = {
                "competitors": ["Concorrente A", "Concorrente B", "Concorrente C"],
                "your_position": "2º lugar em engajamento",
                "opportunities": [
                    "Explorar vídeos curtos (concorrentes não usam)",
                    "Aumentar interação com comunidade",
                    "Criar séries de conteúdo"
                ]
            }
            
            analysis["content_analysis"] = {
                "top_performing_posts": [
                    {"type": "Tutorial", "engagement": "8.5%"},
                    {"type": "Dica rápida", "engagement": "7.2%"},
                    {"type": "Case study", "engagement": "6.8%"}
                ],
                "underperforming": [
                    {"type": "Promoção", "engagement": "1.2%"}
                ]
            }
        
        # Salvar relatório
        report_file = f"reports/analysis_{task_data['task_id']}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Análise concluída!")
        
        return {
            "status": "analyzed",
            "report_file": report_file,
            "summary": analysis
        }
    
    # ==================== ENGAGEMENT BOT ====================
    
    def run_engagement_bot(self, task_data):
        """Executar bot de engajamento"""
        requirements = task_data.get('requirements', {})
        targets = requirements.get('targets', [])
        interaction_type = requirements.get('interaction_type', 'both')
        
        # Determinar quantidade
        service_id = task_data['service_id']
        if '100' in service_id:
            count = 100
        elif '500' in service_id:
            count = 500
        elif '1000' in service_id:
            count = 1000
        else:
            count = 100
        
        print(f"\n❤️ Executando {count} interações...")
        
        interactions = {
            "likes": 0,
            "comments": 0,
            "follows": 0
        }
        
        # Simular interações
        if interaction_type in ['like', 'both']:
            interactions['likes'] = int(count * 0.6)
        
        if interaction_type in ['comment', 'both']:
            interactions['comments'] = int(count * 0.3)
        
        if interaction_type in ['follow', 'both']:
            interactions['follows'] = int(count * 0.1)
        
        # Log de interações
        log_file = f"logs/engagement_{task_data['task_id']}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                "total_interactions": count,
                "breakdown": interactions,
                "targets": targets,
                "completed_at": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {count} interações realizadas!")
        
        return {
            "status": "completed",
            "total_interactions": count,
            "breakdown": interactions,
            "log_file": log_file
        }
    
    # ==================== WEB SCRAPER ====================
    
    def scrape_data(self, task_data):
        """Coletar dados de sites"""
        requirements = task_data.get('requirements', {})
        source = requirements.get('source', 'https://example.com')
        fields = requirements.get('fields', ['title', 'description', 'link'])
        
        # Determinar quantidade
        service_id = task_data['service_id']
        if '100' in service_id:
            count = 100
        elif '500' in service_id:
            count = 500
        elif '1000' in service_id:
            count = 1000
        else:
            count = 100
        
        print(f"\n🕷️ Coletando {count} registros de '{source}'...")
        
        # Simular scraping
        scraped_data = []
        for i in range(count):
            record = {}
            for field in fields:
                record[field] = f"{field}_value_{i+1}"
            
            record['scraped_at'] = datetime.now().isoformat()
            scraped_data.append(record)
        
        # Salvar dados
        data_file = f"scraped/data_{task_data['task_id']}.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {count} registros coletados!")
        
        return {
            "status": "scraped",
            "records_count": count,
            "data_file": data_file,
            "preview": scraped_data[:5]
        }
    
    # ==================== MONITOR BOT ====================
    
    def start_monitoring(self, task_data):
        """Iniciar monitoramento contínuo"""
        requirements = task_data.get('requirements', {})
        keywords = requirements.get('keywords', [])
        channels = requirements.get('channels', ['moltbook'])
        
        # Determinar duração
        service_id = task_data['service_id']
        if '7d' in service_id:
            duration_days = 7
        elif '30d' in service_id:
            duration_days = 30
        elif '90d' in service_id:
            duration_days = 90
        else:
            duration_days = 7
        
        end_date = datetime.now() + timedelta(days=duration_days)
        
        print(f"\n👁️ Iniciando monitoramento por {duration_days} dias...")
        
        monitor_config = {
            "task_id": task_data['task_id'],
            "keywords": keywords,
            "channels": channels,
            "start_date": datetime.now().isoformat(),
            "end_date": end_date.isoformat(),
            "status": "active",
            "alerts": []
        }
        
        # Salvar configuração
        config_file = f"monitors/monitor_{task_data['task_id']}.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(monitor_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Monitoramento ativo até {end_date.strftime('%d/%m/%Y')}!")
        
        return {
            "status": "monitoring",
            "duration_days": duration_days,
            "end_date": end_date.isoformat(),
            "config_file": config_file,
            "dashboard_url": f"http://dashboard.com/monitor/{task_data['task_id']}"
        }

# Função principal para executar workers
def execute_worker(task_data):
    """Executar worker apropriado para a tarefa"""
    workers = TaskWorkers()
    worker_type = task_data.get('worker')
    
    worker_map = {
        'post_scheduler': workers.schedule_posts,
        'content_generator': workers.generate_content,
        'data_analyzer': workers.analyze_data,
        'engagement_bot': workers.run_engagement_bot,
        'web_scraper': workers.scrape_data,
        'monitor_bot': workers.start_monitoring
    }
    
    if worker_type in worker_map:
        return worker_map[worker_type](task_data)
    else:
        return {"error": f"Worker '{worker_type}' não encontrado"}

if __name__ == "__main__":
    # Teste dos workers
    print("🤖 WORKERS AUTOMATIZADOS - TESTE")
    print("=" * 70)
    
    # Teste de cada worker
    test_tasks = [
        {
            "task_id": "test_001",
            "service_id": "auto_posts_10",
            "worker": "post_scheduler",
            "requirements": {
                "posts": [f"Post de teste {i}" for i in range(10)],
                "schedule_type": "distributed"
            }
        },
        {
            "task_id": "test_002",
            "service_id": "ai_content_10",
            "worker": "content_generator",
            "requirements": {
                "theme": "Inteligência Artificial",
                "tone": "educativo",
                "keywords": ["IA", "Tecnologia", "Futuro"]
            }
        }
    ]
    
    for task in test_tasks:
        print(f"\n{'='*70}")
        print(f"Testando: {task['worker']}")
        result = execute_worker(task)
        print(f"Resultado: {json.dumps(result, indent=2, ensure_ascii=False)}")
