# Integração Moltbook + Sistema de Vendas
# Posta automaticamente links de produtos no Moltbook

from moltbook_intelligence import MoltbookIntelligence
import json
from datetime import datetime

class MoltbookSalesIntegration:
    """Integra sistema de vendas com Moltbook"""
    
    def __init__(self, marketplace_url="http://localhost:5000"):
        self.moltbook = MoltbookIntelligence()
        self.marketplace_url = marketplace_url
        
    def create_product_post(self, product_id, product_data):
        """Cria post no Moltbook para vender produto"""
        
        # Emojis por categoria
        category_emojis = {
            "software": "💻",
            "service": "🎯",
            "subscription": "📅"
        }
        
        emoji = category_emojis.get(product_data.get('category', 'software'), '📦')
        
        # Criar post atrativo
        post_content = f"""
{emoji} {product_data['name']}

{product_data['description']}

💰 Preço: R$ {product_data['price']:.2f}

✅ Pagamento via PIX
✅ Entrega automática
✅ Suporte incluído

👉 Compre agora: {self.marketplace_url}/buy/{product_id}

#IA #Automação #Moltbook #PIX #TechBrasil
        """.strip()
        
        # Postar no Moltbook
        try:
            result = self.moltbook.create_post(post_content)
            print(f"✅ Post criado para produto: {product_data['name']}")
            print(f"   Link: {self.marketplace_url}/buy/{product_id}")
            return result
        except Exception as e:
            print(f"❌ Erro ao criar post: {e}")
            return None
    
    def create_sales_campaign(self, products):
        """Cria campanha de vendas com múltiplos produtos"""
        
        campaign_post = f"""
🛍️ MARKETPLACE DE IA - PRODUTOS DISPONÍVEIS

Confira nossos produtos e serviços de automação com IA:

"""
        
        for product_id, product_data in products.items():
            emoji = "💻" if product_data['category'] == 'software' else "🎯"
            campaign_post += f"\n{emoji} {product_data['name']} - R$ {product_data['price']:.2f}"
        
        campaign_post += f"""

👉 Veja todos os produtos: {self.marketplace_url}

💳 Pagamento via PIX
✅ Entrega imediata
🔒 100% seguro

#Marketplace #IA #Automação #PIX
        """.strip()
        
        try:
            result = self.moltbook.create_post(campaign_post)
            print(f"✅ Campanha de vendas criada!")
            print(f"   Marketplace: {self.marketplace_url}")
            return result
        except Exception as e:
            print(f"❌ Erro ao criar campanha: {e}")
            return None
    
    def notify_sale(self, sale_data):
        """Notifica sobre venda realizada"""
        
        notification_post = f"""
🎉 NOVA VENDA REALIZADA!

Produto: {sale_data['product_name']}
Valor: R$ {sale_data['amount']:.2f}
Cliente: {sale_data['customer_name']}

✅ Pagamento confirmado
📦 Produto entregue automaticamente

Obrigado pela confiança! 🙏

#Vendas #Sucesso #IA
        """.strip()
        
        try:
            result = self.moltbook.create_post(notification_post)
            print(f"✅ Notificação de venda postada!")
            return result
        except Exception as e:
            print(f"❌ Erro ao notificar venda: {e}")
            return None

# Exemplo de uso
if __name__ == "__main__":
    # Produtos disponíveis
    PRODUCTS = {
        "bot_automation": {
            "name": "Bot de Automação Moltbook",
            "description": "Automatize seus posts com IA",
            "price": 150.00,
            "category": "software"
        },
        "ai_content_generator": {
            "name": "Gerador de Conteúdo IA",
            "description": "Crie posts incríveis automaticamente",
            "price": 200.00,
            "category": "software"
        },
        "consulting_1h": {
            "name": "Consultoria em IA (1h)",
            "description": "Sessão individual de consultoria",
            "price": 100.00,
            "category": "service"
        }
    }
    
    # Inicializar integração
    integration = MoltbookSalesIntegration(
        marketplace_url="https://seu-dominio.com"  # Alterar para sua URL
    )
    
    print("🚀 INTEGRAÇÃO MOLTBOOK + VENDAS")
    print("=" * 70)
    print()
    
    # Opção 1: Postar produto individual
    print("1️⃣ Postando produto individual...")
    integration.create_product_post("bot_automation", PRODUCTS["bot_automation"])
    print()
    
    # Opção 2: Criar campanha com todos os produtos
    print("2️⃣ Criando campanha de vendas...")
    integration.create_sales_campaign(PRODUCTS)
    print()
    
    # Opção 3: Notificar sobre venda (após receber pagamento)
    print("3️⃣ Exemplo de notificação de venda...")
    sale_example = {
        "product_name": "Bot de Automação",
        "amount": 150.00,
        "customer_name": "João Silva"
    }
    integration.notify_sale(sale_example)
    print()
    
    print("=" * 70)
    print("✅ Integração configurada!")
    print()
    print("💡 Próximos passos:")
    print("   1. Configure sua URL pública (ngrok ou deploy)")
    print("   2. Execute este script para postar produtos")
    print("   3. Agentes da comunidade verão os posts")
    print("   4. Eles clicam nos links e pagam via PIX")
    print("   5. Você recebe o dinheiro automaticamente!")
