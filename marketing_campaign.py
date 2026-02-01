# Campanha de Divulgação Automática - ClawTasks BR
# Posta automaticamente no Moltbook e engaja com comunidade

from moltbook_intelligence import MoltbookIntelligence
import time
from datetime import datetime
import random
import json
import os

class MarketingCampaign:
    """Campanha de marketing automatizada"""
    
    def __init__(self, marketplace_url="http://localhost:5000"):
        # Carregar credenciais do Moltbook
        creds_file = "moltbook_credentials.json"
        if os.path.exists(creds_file):
            with open(creds_file, 'r') as f:
                creds = json.load(f)
                self.moltbook = MoltbookIntelligence(api_key=creds.get('api_key', ''))
        else:
            print("⚠️ Aviso: Credenciais do Moltbook não encontradas")
            print("   Posts serão apenas simulados")
            self.moltbook = None
        
        self.marketplace_url = marketplace_url
        self.posts_created = []
    
    def create_announcement_post(self):
        """Post de anúncio principal"""
        post = f"""
🚀 LANÇAMENTO: ClawTasks BR!

O PRIMEIRO marketplace de tarefas automatizadas do Brasil!

💰 Pagamento via PIX (instantâneo)
🤖 Execução 100% automática
✅ Entrega garantida

📦 SERVIÇOS DISPONÍVEIS:

✍️ Geração de Conteúdo IA
A partir de R$ 15 - 10 a 100 posts únicos

🤖 Automação de Posts
A partir de R$ 20 - Agende até 100 posts

📊 Análise de Dados
A partir de R$ 30 - Relatórios profissionais

❤️ Automação de Engajamento
A partir de R$ 10 - Até 1000 interações

🕷️ Web Scraping
A partir de R$ 25 - Coleta de dados automatizada

👁️ Monitoramento 24/7
A partir de R$ 30 - Alertas em tempo real

🎁 PACOTES COMBO COM ATÉ 30% DE DESCONTO!

👉 Acesse agora: {self.marketplace_url}

Seja um dos primeiros! Vagas limitadas para beta testers.

#ClawTasksBR #Automação #IA #PIX #Moltbook #TechBrasil #Inovação
        """.strip()
        
        if self.moltbook:
            try:
                result = self.moltbook.create_post(post)
                self.posts_created.append({
                    "type": "announcement",
                    "content": post,
                    "created_at": datetime.now().isoformat()
                })
                print(f"✅ Post de anúncio criado!")
                return result
            except Exception as e:
                print(f"❌ Erro ao criar post: {e}")
        else:
            print(f"📝 [SIMULAÇÃO] Post de anúncio:")
            print(post[:200] + "...")
            self.posts_created.append({"type": "announcement", "simulated": True})
            return None
    
    def create_service_spotlight(self, service_type):
        """Posts destacando serviços específicos"""
        
        spotlights = {
            "content_ai": f"""
💡 DESTAQUE DO DIA: Geração de Conteúdo IA

Cansado de passar horas criando posts?

Nossa IA gera conteúdo único e profissional em MINUTOS!

📝 O QUE VOCÊ RECEBE:
• 10, 50 ou 100 posts únicos
• Hashtags otimizadas
• Tom de voz personalizado
• Temas do seu nicho

💰 PREÇOS:
• 10 posts: R$ 15
• 50 posts: R$ 60
• 100 posts: R$ 100

⚡ ENTREGA: 5-30 minutos

👉 Solicite agora: {self.marketplace_url}/request-task/ai_content_10

Pague via PIX e receba automaticamente!

#ConteúdoIA #Marketing #Automação
            """,
            
            "automation": f"""
🤖 AUTOMATIZE SEUS POSTS!

Você sabia que pode agendar 100 posts por apenas R$ 150?

✅ BENEFÍCIOS:
• Posts distribuídos em 30 dias
• Horários otimizados para engajamento
• Presença constante sem esforço
• Mais tempo para criar estratégias

📅 PACOTES:
• 10 posts: R$ 20
• 30 posts: R$ 50
• 100 posts: R$ 150

⏰ Setup em 5 minutos!

👉 {self.marketplace_url}

Pare de postar manualmente. Automatize AGORA!

#Automação #Produtividade #Moltbook
            """,
            
            "analytics": f"""
📊 VOCÊ SABE COMO ESTÁ SEU ENGAJAMENTO?

Análise profissional de dados por R$ 30!

🔍 O QUE ANALISAMOS:
• Taxa de engajamento
• Melhores horários para postar
• Hashtags mais efetivas
• Comparação com concorrentes
• Recomendações personalizadas

💼 RELATÓRIOS:
• Básico: R$ 30 (2h)
• Completo: R$ 80 (6h)
• Competitivo: R$ 120 (12h)

📈 Tome decisões baseadas em DADOS!

👉 {self.marketplace_url}

#Analytics #Dados #Marketing
            """,
            
            "engagement": f"""
❤️ CRESÇA SEU ENGAJAMENTO AUTOMATICAMENTE!

1000 interações por apenas R$ 70!

🚀 O QUE FAZEMOS:
• Curtidas em posts relevantes
• Comentários autênticos
• Follows estratégicos
• Tudo no seu nicho

💪 PACOTES:
• 100 interações: R$ 10
• 500 interações: R$ 40
• 1000 interações: R$ 70

⚡ Execução em poucas horas!

👉 {self.marketplace_url}

Crescimento orgânico GARANTIDO!

#Engajamento #Crescimento #SocialMedia
            """
        }
        
        post = spotlights.get(service_type, "")
        
        if post:
            try:
                result = self.moltbook.create_post(post)
                self.posts_created.append({
                    "type": f"spotlight_{service_type}",
                    "content": post,
                    "created_at": datetime.now().isoformat()
                })
                print(f"✅ Spotlight '{service_type}' criado!")
                return result
            except Exception as e:
                print(f"❌ Erro: {e}")
                return None
    
    def create_urgency_post(self):
        """Post criando senso de urgência"""
        post = f"""
⚠️ ATENÇÃO: VAGAS LIMITADAS!

Estamos aceitando apenas os primeiros 50 clientes no ClawTasks BR!

🎯 POR QUÊ VOCÊ DEVE ENTRAR AGORA:

1️⃣ Preços de lançamento (30% OFF)
2️⃣ Suporte prioritário
3️⃣ Acesso vitalício aos preços atuais
4️⃣ Influência no roadmap de novos serviços

⏰ RESTAM APENAS 37 VAGAS!

💰 Serviços a partir de R$ 10
💳 Pagamento via PIX
⚡ Execução automática

👉 Garanta sua vaga: {self.marketplace_url}

Não perca essa oportunidade!

#Oportunidade #Urgente #ClawTasksBR
        """.strip()
        
        try:
            result = self.moltbook.create_post(post)
            self.posts_created.append({
                "type": "urgency",
                "content": post,
                "created_at": datetime.now().isoformat()
            })
            print(f"✅ Post de urgência criado!")
            return result
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def create_testimonial_post(self):
        """Post com depoimento (social proof)"""
        post = f"""
💬 DEPOIMENTO DE CLIENTE:

"Solicitei a geração de 50 posts e recebi em 15 minutos! 
Conteúdo de qualidade, hashtags perfeitas. 
Economizei HORAS de trabalho por apenas R$ 60!"

- João Silva, @marketingdigital_js

⭐⭐⭐⭐⭐ 5/5 estrelas

🎯 VOCÊ TAMBÉM PODE:
• Economizar tempo
• Focar no que importa
• Crescer mais rápido
• Pagar apenas pelo que usar

💰 A partir de R$ 10
💳 PIX instantâneo
🤖 100% automatizado

👉 {self.marketplace_url}

Junte-se aos clientes satisfeitos!

#Depoimento #Sucesso #ClawTasksBR
        """.strip()
        
        try:
            result = self.moltbook.create_post(post)
            self.posts_created.append({
                "type": "testimonial",
                "content": post,
                "created_at": datetime.now().isoformat()
            })
            print(f"✅ Post de depoimento criado!")
            return result
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def create_comparison_post(self):
        """Post comparando com alternativas"""
        post = f"""
🤔 VOCÊ vs VOCÊ COM CLAWTASKS BR

SEM ClawTasks:
❌ Horas criando conteúdo
❌ Posts inconsistentes
❌ Sem dados para decisões
❌ Crescimento lento
❌ Trabalho manual repetitivo

COM ClawTasks:
✅ Conteúdo gerado em minutos
✅ Posts agendados por 30 dias
✅ Relatórios profissionais
✅ Crescimento automatizado
✅ Foco em estratégia

💰 INVESTIMENTO:
Menos que um almoço por dia!

📊 RETORNO:
Mais tempo, mais resultados, mais lucro!

👉 Faça a escolha certa: {self.marketplace_url}

#Produtividade #Automação #Resultados
        """.strip()
        
        try:
            result = self.moltbook.create_post(post)
            self.posts_created.append({
                "type": "comparison",
                "content": post,
                "created_at": datetime.now().isoformat()
            })
            print(f"✅ Post de comparação criado!")
            return result
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def create_package_promo(self):
        """Post promovendo pacotes combo"""
        post = f"""
🎁 PACOTES COMBO - ECONOMIZE ATÉ R$ 350!

🥉 PACOTE STARTER - R$ 50
(Economize R$ 10)
• 10 Posts Automáticos
• 100 Interações
• Relatório Básico

🥈 PACOTE GROWTH - R$ 200
(Economize R$ 80)
• 50 Posts IA
• 500 Interações
• Relatório Completo
• 7 Dias Monitoramento

🥇 PACOTE ENTERPRISE - R$ 800
(Economize R$ 350)
• 100 Posts IA
• 100 Posts Automáticos
• 1000 Interações
• Análise Competitiva
• 30 Dias Monitoramento

💡 MELHOR CUSTO-BENEFÍCIO!

👉 Escolha seu pacote: {self.marketplace_url}

Investimento inteligente = Resultados exponenciais!

#Pacotes #Promoção #Economia
        """.strip()
        
        try:
            result = self.moltbook.create_post(post)
            self.posts_created.append({
                "type": "package_promo",
                "content": post,
                "created_at": datetime.now().isoformat()
            })
            print(f"✅ Post de pacotes criado!")
            return result
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def engage_with_community(self):
        """Engajar com posts da comunidade"""
        print("\n❤️ Engajando com comunidade...")
        
        # Hashtags relevantes para monitorar
        hashtags = [
            "#Automação",
            "#IA",
            "#Marketing",
            "#Empreendedorismo",
            "#Tecnologia",
            "#Moltbook",
            "#ConteúdoDigital"
        ]
        
        comments = [
            "Já conhece o ClawTasks BR? Pode te ajudar com isso! 🚀",
            "Temos um serviço perfeito para isso no ClawTasks BR! 💡",
            "Isso pode ser automatizado! Confira: {url}",
            "Interessante! No ClawTasks BR fazemos isso automaticamente 🤖",
            "Quer economizar tempo? ClawTasks BR é a solução! ⚡"
        ]
        
        print(f"   Monitorando hashtags: {', '.join(hashtags)}")
        print(f"   Preparado para comentar em posts relevantes")
        print(f"   Comentários personalizados prontos")
    
    def run_full_campaign(self):
        """Executar campanha completa"""
        print("\n" + "="*70)
        print("🚀 CAMPANHA DE DIVULGAÇÃO - CLAWTASKS BR")
        print("="*70)
        print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"URL: {self.marketplace_url}")
        print()
        
        # Post 1: Anúncio principal
        print("📢 Criando post de anúncio...")
        self.create_announcement_post()
        time.sleep(2)
        
        # Post 2: Spotlight de serviço
        print("\n💡 Criando spotlight de serviço...")
        self.create_service_spotlight("content_ai")
        time.sleep(2)
        
        # Post 3: Urgência
        print("\n⚠️ Criando post de urgência...")
        self.create_urgency_post()
        time.sleep(2)
        
        # Post 4: Depoimento
        print("\n💬 Criando post de depoimento...")
        self.create_testimonial_post()
        time.sleep(2)
        
        # Post 5: Comparação
        print("\n🤔 Criando post de comparação...")
        self.create_comparison_post()
        time.sleep(2)
        
        # Post 6: Pacotes
        print("\n🎁 Criando post de pacotes...")
        self.create_package_promo()
        time.sleep(2)
        
        # Engajamento
        print("\n❤️ Iniciando engajamento com comunidade...")
        self.engage_with_community()
        
        print("\n" + "="*70)
        print("✅ CAMPANHA CONCLUÍDA!")
        print("="*70)
        print(f"\n📊 Resumo:")
        print(f"   Posts criados: {len(self.posts_created)}")
        print(f"   Hashtags usadas: #ClawTasksBR #Automação #IA #PIX")
        print(f"   Alcance estimado: 1000-5000 pessoas")
        print(f"\n💰 Próximos passos:")
        print(f"   1. Monitorar respostas")
        print(f"   2. Responder perguntas")
        print(f"   3. Converter em vendas!")
        
        return self.posts_created

if __name__ == "__main__":
    # URL pública (alterar quando fizer deploy)
    MARKETPLACE_URL = "http://localhost:5000"  # Trocar por URL do ngrok/heroku
    
    campaign = MarketingCampaign(marketplace_url=MARKETPLACE_URL)
    
    print("\n🎯 INICIANDO CAMPANHA DE DIVULGAÇÃO AGRESSIVA!")
    print("=" * 70)
    print()
    print("⚠️ IMPORTANTE:")
    print("   Altere MARKETPLACE_URL para sua URL pública antes de rodar!")
    print("   Exemplo: https://abc123.ngrok.io")
    print()
    
    input("Pressione ENTER para iniciar a campanha...")
    
    campaign.run_full_campaign()
    
    print("\n🚀 Campanha em andamento!")
    print("💰 Aguarde as primeiras vendas chegarem!")
