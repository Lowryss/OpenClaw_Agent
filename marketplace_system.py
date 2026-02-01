# Sistema de Marketplace - Vendas para Comunidade Moltbook
# Permite que qualquer pessoa compre produtos/serviços via PIX

from flask import Flask, request, jsonify, render_template, redirect, url_for
from efi_payment_system import EfiPaymentSystem
import json
from datetime import datetime
import os

app = Flask(__name__)
efi = EfiPaymentSystem()

# Catálogo de Produtos/Serviços
PRODUCTS = {
    "bot_automation": {
        "name": "Bot de Automação Moltbook",
        "description": "Bot completo para automatizar posts no Moltbook",
        "price": 150.00,
        "category": "software",
        "delivery_type": "download",  # download, access, service
        "delivery_content": {
            "type": "github",
            "url": "https://github.com/seu-repo/bot-automation",
            "instructions": "Acesso ao repositório privado será enviado por email"
        }
    },
    "ai_content_generator": {
        "name": "Gerador de Conteúdo IA",
        "description": "Sistema de IA para gerar posts automaticamente",
        "price": 200.00,
        "category": "software",
        "delivery_type": "access",
        "delivery_content": {
            "type": "api_key",
            "instructions": "API key será enviada por email após pagamento"
        }
    },
    "consulting_1h": {
        "name": "Consultoria em IA (1 hora)",
        "description": "Sessão de consultoria individual sobre IA e automação",
        "price": 100.00,
        "category": "service",
        "delivery_type": "service",
        "delivery_content": {
            "type": "calendar",
            "url": "https://calendly.com/seu-usuario",
            "instructions": "Agende sua sessão no link enviado por email"
        }
    },
    "custom_bot": {
        "name": "Bot Personalizado",
        "description": "Desenvolvimento de bot customizado para suas necessidades",
        "price": 500.00,
        "category": "service",
        "delivery_type": "service",
        "delivery_content": {
            "type": "project",
            "instructions": "Entraremos em contato para definir requisitos"
        }
    },
    "monthly_subscription": {
        "name": "Assinatura Mensal - Acesso Premium",
        "description": "Acesso a todos os bots e ferramentas por 30 dias",
        "price": 50.00,
        "category": "subscription",
        "delivery_type": "access",
        "delivery_content": {
            "type": "credentials",
            "duration": "30 days",
            "instructions": "Credenciais de acesso enviadas por email"
        }
    }
}

# Salvar vendas realizadas
SALES_FILE = "sales_history.json"

def save_sale(sale_data):
    """Salvar venda no histórico"""
    try:
        if os.path.exists(SALES_FILE):
            with open(SALES_FILE, 'r', encoding='utf-8') as f:
                sales = json.load(f)
        else:
            sales = []
        
        sales.append(sale_data)
        
        with open(SALES_FILE, 'w', encoding='utf-8') as f:
            json.dump(sales, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar venda: {e}")
        return False

@app.route('/')
def marketplace():
    """Página principal do marketplace"""
    return render_template('marketplace.html', products=PRODUCTS)

@app.route('/dashboard')
def dashboard():
    """Painel administrativo de vendas"""
    return render_template('dashboard.html')

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
        response = "Posso criar posts para você! 📝<br>Temos pacotes a partir de R$ 20,00.<br><a href='/buy/auto_posts_10' style='color:#00ff88'>Clique aqui para comprar o pacote de 10 posts.</a>"
    elif 'analise' in user_msg or 'dados' in user_msg:
        response = "Precisa de insights? 📊<br>Eu analiso seus dados e entrego um relatório completo.<br><a href='/buy/analytics_basic' style='color:#00ff88'>Ver Pacote de Análise (R$ 30)</a>"
    elif 'ajuda' in user_msg:
        response = "Comandos disponíveis:<br>- Criar posts<br>- Analisar dados<br>- Monitorar concorrentes<br>- Status do sistema"
    else:
        response = "Entendi. Para executar essa tarefa, preciso que você escolha um dos nossos <a href='/' style='color:#00ff88'>Serviços de Automação</a>.<br>Posso te ajudar a escolher o melhor pacote?"
        
    return jsonify({"response": response})

@app.route('/product/<product_id>')
def product_details(product_id):
    """Detalhes de um produto específico"""
    if product_id not in PRODUCTS:
        return "Produto não encontrado", 404
    
    product = PRODUCTS[product_id]
    return render_template('product_details.html', 
                         product_id=product_id, 
                         product=product)

@app.route('/buy/<product_id>', methods=['GET', 'POST'])
def buy_product(product_id):
    """Comprar um produto - gera QR Code PIX"""
    if product_id not in PRODUCTS:
        return jsonify({"error": "Produto não encontrado"}), 404
    
    product = PRODUCTS[product_id]
    
    # Dados do comprador (opcional)
    customer_name = request.args.get('customer', 'Cliente')
    customer_email = request.args.get('email', '')
    
    print(f"\n💰 Nova compra iniciada:")
    print(f"   Produto: {product['name']}")
    print(f"   Preço: R$ {product['price']:.2f}")
    print(f"   Cliente: {customer_name}")
    if customer_email:
        print(f"   Email: {customer_email}")
    
    # Criar cobrança PIX
    try:
        charge = efi.create_pix_charge(
            amount=product['price'],
            description=f"{product['name']} - {product['description'][:50]}",
            customer_name=customer_name
        )
        
        if charge.get("success"):
            # Salvar informações da venda
            sale_data = {
                "txid": charge["txid"],
                "product_id": product_id,
                "product_name": product["name"],
                "amount": product["price"],
                "customer_name": customer_name,
                "customer_email": customer_email,
                "created_at": datetime.now().isoformat(),
                "status": "pending",
                "delivery_content": product["delivery_content"]
            }
            
            save_sale(sale_data)
            
            print(f"✅ Cobrança criada com sucesso!")
            print(f"   TXID: {charge['txid']}")
            
            return jsonify({
                "success": True,
                "product": product["name"],
                "amount": product["price"],
                "qr_code": charge["qr_code"],
                "qr_code_image": charge["qr_code_image"],
                "txid": charge["txid"],
                "instructions": "Escaneie o QR Code para pagar"
            })
        else:
            print(f"❌ Erro ao criar cobrança: {charge}")
            return jsonify(charge), 400
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook/payment', methods=['POST'])
def payment_webhook():
    """Webhook para receber notificação de pagamento confirmado"""
    try:
        data = request.json
        txid = data.get('txid')
        
        print(f"\n🔔 Pagamento recebido!")
        print(f"   TXID: {txid}")
        
        # Verificar pagamento
        status = efi.check_payment_status(txid)
        
        if status.get('paid'):
            # Buscar venda no histórico
            with open(SALES_FILE, 'r', encoding='utf-8') as f:
                sales = json.load(f)
            
            for sale in sales:
                if sale['txid'] == txid and sale['status'] == 'pending':
                    # Atualizar status
                    sale['status'] = 'paid'
                    sale['paid_at'] = datetime.now().isoformat()
                    
                    # Salvar atualização
                    with open(SALES_FILE, 'w', encoding='utf-8') as f:
                        json.dump(sales, f, indent=2, ensure_ascii=False)
                    
                    # Entregar produto/serviço
                    deliver_product(sale)
                    
                    print(f"✅ Venda confirmada e produto entregue!")
                    print(f"   Produto: {sale['product_name']}")
                    print(f"   Cliente: {sale['customer_name']}")
                    
                    return jsonify({"status": "success"}), 200
        
        return jsonify({"status": "pending"}), 200
        
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return jsonify({"error": str(e)}), 500

def deliver_product(sale):
    """Entregar produto/serviço ao cliente"""
    print(f"\n📦 Entregando produto: {sale['product_name']}")
    
    delivery = sale['delivery_content']
    
    # Aqui você pode implementar diferentes tipos de entrega:
    # - Enviar email com link de download
    # - Criar acesso em sistema
    # - Enviar credenciais
    # - Agendar serviço
    
    # Exemplo: Salvar em arquivo de entregas pendentes
    delivery_data = {
        "customer_name": sale['customer_name'],
        "customer_email": sale['customer_email'],
        "product": sale['product_name'],
        "delivery_type": delivery.get('type'),
        "instructions": delivery.get('instructions'),
        "delivered_at": datetime.now().isoformat()
    }
    
    # Salvar para processamento manual ou automático
    with open('pending_deliveries.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(delivery_data, ensure_ascii=False) + '\n')
    
    print(f"✅ Entrega registrada!")
    
    # TODO: Implementar envio de email automático
    # send_delivery_email(sale['customer_email'], delivery_data)

@app.route('/sales', methods=['GET'])
def list_sales():
    """Listar todas as vendas"""
    try:
        if os.path.exists(SALES_FILE):
            with open(SALES_FILE, 'r', encoding='utf-8') as f:
                sales = json.load(f)
            return jsonify({"sales": sales})
        else:
            return jsonify({"sales": []})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check-payment/<txid>')
def check_payment(txid):
    """Verificar status de pagamento"""
    status = efi.check_payment_status(txid)
    return jsonify(status)

if __name__ == "__main__":
    print("🛍️ MARKETPLACE - SISTEMA DE VENDAS AUTOMÁTICAS")
    print("=" * 70)
    print("\n📦 Produtos Disponíveis:")
    for product_id, product in PRODUCTS.items():
        print(f"   • {product['name']:40} R$ {product['price']:.2f}")
    print()
    print("🌐 Endpoints:")
    print("   • GET  / - Marketplace (lista de produtos)")
    print("   • GET  /product/<id> - Detalhes do produto")
    print("   • GET  /buy/<id> - Comprar produto (gera QR Code)")
    print("   • POST /webhook/payment - Recebe confirmação de pagamento")
    print("   • GET  /sales - Lista todas as vendas")
    print()
    print("💡 Exemplo de uso:")
    print("   http://localhost:5000/buy/bot_automation?customer=João&email=joao@email.com")
    print()
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
