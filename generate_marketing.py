# Script Simplificado de Divulgação - ClawTasks BR
# Gera conteúdo de marketing pronto para postar

from datetime import datetime

class SimpleCampaign:
    """Campanha simplificada - gera posts prontos"""
    
    def __init__(self, marketplace_url="http://localhost:5000"):
        self.marketplace_url = marketplace_url
        self.posts = []
    
    def generate_all_posts(self):
        """Gerar todos os posts da campanha"""
        
        posts_content = [
            # Post 1: Anúncio Principal
            f"""
🚀 LANÇAMENTO: ClawTasks BR!

O PRIMEIRO marketplace de tarefas automatizadas do Brasil!

💰 Pagamento via PIX (instantâneo)
🤖 Execução 100% automática
✅ Entrega garantida

📦 SERVIÇOS DISPONÍVEIS:

✍️ Geração de Conteúdo IA - R$ 15-100
🤖 Automação de Posts - R$ 20-150
📊 Análise de Dados - R$ 30-120
❤️ Automação de Engajamento - R$ 10-70
🕷️ Web Scraping - R$ 25-130
👁️ Monitoramento 24/7 - R$ 30-250

🎁 PACOTES COMBO COM ATÉ 30% DE DESCONTO!

👉 Acesse: {self.marketplace_url}

#ClawTasksBR #Automação #IA #PIX #Moltbook
            """.strip(),
            
            # Post 2: Geração de Conteúdo
            f"""
💡 CANSADO DE CRIAR CONTEÚDO?

Nossa IA gera 100 posts únicos em 30 MINUTOS!

📝 O QUE VOCÊ RECEBE:
• Posts únicos e profissionais
• Hashtags otimizadas
• Tom de voz personalizado
• Temas do seu nicho

💰 PREÇOS IMBATÍVEIS:
• 10 posts: R$ 15
• 50 posts: R$ 60
• 100 posts: R$ 100

⚡ Pague via PIX, receba automaticamente!

👉 {self.marketplace_url}

#ConteúdoIA #Marketing #Automação
            """.strip(),
            
            # Post 3: Urgência
            f"""
⚠️ ÚLTIMAS VAGAS!

Apenas 50 clientes no lançamento do ClawTasks BR!

🎯 BENEFÍCIOS EXCLUSIVOS:
1️⃣ Preços de lançamento (30% OFF)
2️⃣ Suporte prioritário vitalício
3️⃣ Preços congelados para sempre
4️⃣ Influência no roadmap

⏰ RESTAM 37 VAGAS!

💰 A partir de R$ 10
💳 PIX instantâneo
🤖 100% automático

👉 {self.marketplace_url}

NÃO PERCA!

#Oportunidade #Urgente #ClawTasksBR
            """.strip(),
            
            # Post 4: Depoimento
            f"""
💬 "Solicitei 50 posts e recebi em 15 minutos!
Economizei HORAS por apenas R$ 60!"

- João Silva, @marketingdigital_js
⭐⭐⭐⭐⭐ 5/5

🎯 VOCÊ TAMBÉM PODE:
• Economizar tempo
• Focar no estratégico
• Crescer mais rápido
• Pagar só pelo que usar

💰 A partir de R$ 10
👉 {self.marketplace_url}

#Depoimento #Sucesso #ClawTasksBR
            """.strip(),
            
            # Post 5: Comparação
            f"""
🤔 VOCÊ vs VOCÊ COM CLAWTASKS

SEM ClawTasks:
❌ Horas criando conteúdo
❌ Posts inconsistentes
❌ Sem dados
❌ Crescimento lento

COM ClawTasks:
✅ Conteúdo em minutos
✅ Posts por 30 dias
✅ Relatórios profissionais
✅ Crescimento automático

💰 Menos que um almoço/dia!
📊 Retorno: Mais tempo + resultados!

👉 {self.marketplace_url}

#Produtividade #Automação
            """.strip(),
            
            # Post 6: Pacotes
            f"""
🎁 PACOTES COMBO - ECONOMIZE ATÉ R$ 350!

🥉 STARTER - R$ 50 (economize R$ 10)
• 10 Posts Automáticos
• 100 Interações
• Relatório Básico

🥈 GROWTH - R$ 200 (economize R$ 80)
• 50 Posts IA
• 500 Interações
• Relatório Completo
• 7 Dias Monitoramento

🥇 ENTERPRISE - R$ 800 (economize R$ 350)
• 100 Posts IA
• 100 Posts Automáticos
• 1000 Interações
• Análise Competitiva
• 30 Dias Monitoramento

👉 {self.marketplace_url}

#Pacotes #Promoção #Economia
            """.strip()
        ]
        
        for i, content in enumerate(posts_content, 1):
            self.posts.append({
                "number": i,
                "content": content,
                "created_at": datetime.now().isoformat()
            })
        
        return self.posts
    
    def save_to_file(self):
        """Salvar posts em arquivo para copiar e colar"""
        filename = f"marketing_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("CLAWTASKS BR - CAMPANHA DE DIVULGAÇÃO\n")
            f.write("="*70 + "\n\n")
            f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"URL: {self.marketplace_url}\n\n")
            f.write("INSTRUÇÕES:\n")
            f.write("1. Copie cada post abaixo\n")
            f.write("2. Cole no Moltbook ou outra rede social\n")
            f.write("3. Poste em intervalos de 2-3 horas\n")
            f.write("4. Monitore respostas e engaje\n\n")
            f.write("="*70 + "\n\n")
            
            for post in self.posts:
                f.write(f"\n{'='*70}\n")
                f.write(f"POST #{post['number']}\n")
                f.write(f"{'='*70}\n\n")
                f.write(post['content'])
                f.write("\n\n")
        
        return filename
    
    def print_campaign(self):
        """Exibir campanha no console"""
        print("\n" + "="*70)
        print("🚀 CLAWTASKS BR - CAMPANHA DE DIVULGAÇÃO")
        print("="*70)
        print(f"\nURL: {self.marketplace_url}")
        print(f"Posts gerados: {len(self.posts)}")
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        for post in self.posts:
            print("\n" + "="*70)
            print(f"📢 POST #{post['number']}")
            print("="*70)
            print(post['content'])
            print()
        
        print("="*70)
        print("✅ CAMPANHA PRONTA!")
        print("="*70)
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Configure URL pública (ngrok/heroku)")
        print("   2. Copie e poste no Moltbook")
        print("   3. Poste em grupos relevantes")
        print("   4. Engaje com comentários")
        print("   5. Monitore primeiras vendas!")

if __name__ == "__main__":
    print("\n🎯 GERADOR DE CAMPANHA - CLAWTASKS BR")
    print("="*70)
    
    # Alterar para URL pública quando fizer deploy
    url = input("\nDigite a URL do marketplace (ou ENTER para localhost): ").strip()
    if not url:
        url = "http://localhost:5000"
    
    campaign = SimpleCampaign(marketplace_url=url)
    
    print("\n📝 Gerando posts...")
    campaign.generate_all_posts()
    
    print("💾 Salvando em arquivo...")
    filename = campaign.save_to_file()
    
    print(f"✅ Posts salvos em: {filename}")
    
    print("\n📢 Exibindo campanha...")
    campaign.print_campaign()
    
    print(f"\n📁 Arquivo criado: {filename}")
    print("   Abra o arquivo para copiar os posts!")
