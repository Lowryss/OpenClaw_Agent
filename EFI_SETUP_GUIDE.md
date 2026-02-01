# Guia Completo de Integração Efí
# Como configurar pagamentos automáticos para o Marylowrys_Bot

## 📋 PASSO A PASSO

### 1. Criar Conta Efí
1. Acesse: https://sejaefi.com.br
2. Clique em "Criar Conta"
3. Complete o cadastro (pessoa física ou jurídica)
4. Ative sua conta PIX

### 2. Obter Credenciais da API

#### 2.1 Acessar Dashboard
- Login em: https://gerencianet.com.br/login
- Vá em: **API** → **Minhas Aplicações**

#### 2.2 Criar Nova Aplicação
- Clique em "Nova Aplicação"
- Nome: "Marylowrys_Bot"
- Tipo: "PIX"
- Ambiente: "Produção" (ou "Homologação" para testes)

#### 2.3 Baixar Credenciais
Você receberá:
- **Client ID**: `Client_Id_xxxxxxxxxxxxx`
- **Client Secret**: `Client_Secret_xxxxxxxxxxxxx`
- **Certificado**: `producao-xxxxx.p12` ou `.pem`

### 3. Configurar Sistema

#### 3.1 Instalar Dependências
```bash
pip install requests flask
```

#### 3.2 Atualizar Credenciais
Edite `efi_payment_system.py`:
```python
CLIENT_ID = "SEU_CLIENT_ID_AQUI"
CLIENT_SECRET = "SEU_CLIENT_SECRET_AQUI"
```

#### 3.3 Adicionar Chave PIX
No arquivo `efi_payment_system.py`, linha ~70:
```python
"chave": "45520622809",  # Sua chave PIX
```

### 4. Configurar Webhook (Notificações Automáticas)

#### 4.1 Expor Servidor Localmente
Para testes, use **ngrok**:
```bash
# Baixe: https://ngrok.com/download
ngrok http 5000
```

Você receberá uma URL tipo:
```
https://abc123.ngrok.io
```

#### 4.2 Registrar Webhook na Efí
```python
from efi_payment_system import EfiPaymentSystem

efi = EfiPaymentSystem(CLIENT_ID, CLIENT_SECRET)
efi.authenticate()
efi.configure_webhook(
    webhook_url="https://abc123.ngrok.io/webhook/efi",
    pix_key="45520622809"
)
```

### 5. Iniciar Sistema

#### 5.1 Rodar Webhook Server
```bash
python efi_webhook_server.py
```

Servidor rodando em: `http://localhost:5000`

#### 5.2 Testar Pagamento
Acesse no navegador:
```
http://localhost:5000/create-payment/automation_setup
```

Você receberá:
- QR Code PIX
- Código de pagamento
- ID da transação

### 6. Fluxo Completo

```
1. Cliente solicita serviço
   ↓
2. Sistema gera QR Code PIX (Efí API)
   ↓
3. Cliente escaneia e paga
   ↓
4. Efí envia webhook → Seu servidor
   ↓
5. Sistema verifica pagamento
   ↓
6. Entrega automática do serviço
   ↓
7. Cliente recebe acesso/conteúdo
```

## 🔧 SERVIÇOS DISPONÍVEIS

| Serviço | Preço | ID |
|---------|-------|-----|
| Automação de Redes Sociais | R$ 50 | `automation_setup` |
| Análise de Dados | R$ 30 | `data_analysis` |
| Criação de Conteúdo | R$ 20 | `content_creation` |
| Consultoria em IA | R$ 100 | `consulting` |

## 📊 ENDPOINTS DA API

### Criar Pagamento
```
GET /create-payment/<service_id>?customer=Nome
```

### Verificar Pagamento
```
GET /check-payment/<txid>
```

### Listar Serviços
```
GET /services
```

### Webhook (Efí)
```
POST /webhook/efi
```

## 🚀 INTEGRAÇÃO COM MOLTBOOK

Atualize seus posts com links de pagamento:

```python
# Exemplo de post com pagamento
post_content = f"""
🤖 Serviço: Automação de Redes Sociais
💰 Preço: R$ 50,00

Para contratar:
1. Acesse: http://seu-dominio.com/create-payment/automation_setup
2. Escaneie o QR Code PIX
3. Pagamento confirmado = Entrega automática!

#AIServices #Automation
"""
```

## 💡 DICAS

1. **Ambiente de Testes (Sandbox)**
   - Use `sandbox=True` para testar sem dinheiro real
   - Efí fornece PIX de teste

2. **Segurança**
   - Nunca compartilhe Client Secret
   - Use HTTPS em produção
   - Valide webhooks com assinatura

3. **Produção**
   - Use servidor cloud (Heroku, AWS, etc.)
   - Configure domínio próprio
   - Monitore logs de pagamento

## 📞 SUPORTE

- **Efí Docs**: https://dev.efipay.com.br
- **Suporte Efí**: suporte@efipay.com.br
- **Comunidade**: https://comunidade.sejaefi.com.br

## ✅ CHECKLIST

- [ ] Conta Efí criada
- [ ] Credenciais obtidas (Client ID + Secret)
- [ ] Certificado baixado
- [ ] Chave PIX registrada
- [ ] Dependências instaladas (`pip install requests flask`)
- [ ] Credenciais atualizadas no código
- [ ] Webhook configurado
- [ ] Servidor rodando
- [ ] Teste de pagamento realizado
- [ ] Integração com Moltbook feita

---

**Pronto! Seu agente agora aceita pagamentos automáticos via PIX!** 💰🤖
