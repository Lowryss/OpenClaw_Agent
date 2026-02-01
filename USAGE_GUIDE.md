# 🚀 Guia de Uso - Sistema de Pagamentos PIX

## Como Usar o Sistema

### 1. Iniciar o Servidor

```bash
cd C:\Users\Amauri\.gemini\antigravity\scratch\OpenClaw_Agent
python efi_webhook_server.py
```

O servidor iniciará em: **http://localhost:5000**

### 2. Acessar a Interface Web

Abra seu navegador e acesse:
```
http://localhost:5000
```

Você verá a interface com todos os serviços disponíveis.

### 3. Criar um Pagamento

1. **Clique** no botão "💳 Pagar com PIX" do serviço desejado
2. **Aguarde** a geração do QR Code
3. **Escaneie** o QR Code com o app do seu banco
4. **Ou copie** o código PIX e cole no app
5. **Confirme** o pagamento no app do banco

### 4. Entrega Automática

Após o pagamento ser confirmado:
- ✅ O sistema detecta automaticamente (via webhook)
- 🚀 O serviço é entregue instantaneamente
- 📧 Cliente recebe as instruções/acesso

## Serviços Disponíveis

| Serviço | Preço | Descrição |
|---------|-------|-----------|
| Automação de Redes Sociais | R$ 50,00 | Setup completo de automação |
| Análise de Dados | R$ 30,00 | Relatório de análise de dados |
| Criação de Conteúdo | R$ 20,00 | Post gerado por IA |
| Consultoria em IA | R$ 100,00 | 1 hora de consultoria |

## API Endpoints

### GET /
Interface web principal

### GET /services
Lista todos os serviços disponíveis

**Resposta:**
```json
{
  "services": [
    {
      "id": "automation_setup",
      "description": "Social Media Automation Setup",
      "price": 50.00
    }
  ]
}
```

### GET /create-payment/<service_id>
Cria uma cobrança PIX

**Parâmetros:**
- `service_id`: ID do serviço (automation_setup, data_analysis, etc.)
- `customer` (opcional): Nome do cliente

**Exemplo:**
```
http://localhost:5000/create-payment/automation_setup?customer=João Silva
```

**Resposta:**
```json
{
  "success": true,
  "service": "Social Media Automation Setup",
  "amount": 50.00,
  "qr_code": "00020126580014br.gov.bcb.pix...",
  "qr_code_image": "data:image/png;base64,...",
  "txid": "abc123...",
  "instructions": "Scan the QR Code with your bank app to pay"
}
```

### GET /check-payment/<txid>
Verifica status de um pagamento

**Resposta:**
```json
{
  "paid": true,
  "status": "CONCLUIDA",
  "details": {...}
}
```

### POST /webhook/efi
Recebe notificações de pagamento da Efí (uso interno)

## Configurar Webhook em Produção

### Opção 1: Usar ngrok (Testes)

```bash
# Em um terminal, rode o servidor
python efi_webhook_server.py

# Em outro terminal, exponha com ngrok
ngrok http 5000
```

Você receberá uma URL como: `https://abc123.ngrok.io`

### Opção 2: Deploy em Servidor Cloud

**Heroku:**
```bash
heroku create seu-app
git push heroku main
```

**Railway:**
1. Conecte seu repositório GitHub
2. Deploy automático

### Registrar Webhook na Efí

```python
from efi_payment_system import EfiPaymentSystem

efi = EfiPaymentSystem()
efi.authenticate()

result = efi.configure_webhook(
    webhook_url="https://seu-dominio.com/webhook/efi",
    pix_key="56bbb9d4-d884-4456-97bd-8c32ea5ce8d7"
)

print(result)
```

## Personalizar Serviços

Edite `efi_payment_system.py`, classe `AgentServiceDelivery`:

```python
self.services = {
    "meu_servico": {
        "price": 99.00,
        "description": "Meu Serviço Personalizado",
        "delivery": self.deliver_meu_servico
    }
}

def deliver_meu_servico(self, customer_name):
    """Entregar meu serviço"""
    print(f"🎁 Entregando serviço para {customer_name}")
    # Sua lógica de entrega aqui
    return {
        "delivered": True,
        "type": "meu_servico",
        "message": "Serviço entregue com sucesso!"
    }
```

## Logs

O servidor mostra logs detalhados:

```
💰 Creating payment for service: automation_setup
   Customer: João Silva
✅ Payment created successfully
   TXID: abc123xyz...
   Amount: R$ 50.00

🔔 Webhook received at 2026-02-01 02:30:15
✅ Service delivered successfully!
   Service: automation_setup
```

## Troubleshooting

### Servidor não inicia
- Verifique se a porta 5000 está livre
- Confirme que Flask está instalado: `pip install flask`

### QR Code não aparece
- Verifique se a autenticação está funcionando
- Teste: `python test_pix_charge.py`

### Webhook não recebe notificações
- Certifique-se que a URL é pública (não localhost)
- Verifique se registrou o webhook na Efí
- Teste com ngrok primeiro

## Próximos Passos

1. **Testar localmente** com pagamentos reais (valores mínimos)
2. **Configurar webhook** com ngrok ou servidor cloud
3. **Integrar com Moltbook** para postar links de pagamento
4. **Monitorar** logs e transações
5. **Escalar** conforme necessário

---

**🎉 Seu sistema de pagamentos PIX está pronto para uso!**
