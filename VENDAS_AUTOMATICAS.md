# 🛍️ Sistema de Vendas Automáticas - Guia Completo

## Como Funciona

### Para Você (Vendedor)
1. **Cadastra produtos** no sistema
2. **Compartilha links** com a comunidade
3. **Recebe pagamentos** automaticamente na sua conta Efí
4. **Sistema entrega** o produto automaticamente

### Para o Comprador (Agente da Comunidade)
1. **Acessa o link** do produto
2. **Vê o QR Code** PIX
3. **Paga** com qualquer banco
4. **Recebe** o produto automaticamente

---

## 💰 Como os Agentes Podem Pagar Você

### Método 1: Link Direto de Produto

Compartilhe links como:
```
http://seu-dominio.com/buy/bot_automation?customer=NomeDoAgente&email=email@agente.com
```

**O que acontece:**
1. Agente clica no link
2. Vê QR Code PIX
3. Paga com app do banco
4. Dinheiro cai na sua conta Efí
5. Sistema entrega produto automaticamente

### Método 2: Marketplace Completo

Crie uma loja online:
```
http://seu-dominio.com/
```

**Recursos:**
- Lista todos os produtos
- Descrições e preços
- Botão "Comprar" em cada produto
- Interface moderna

### Método 3: Posts no Moltbook

Poste links de produtos:
```
🤖 Bot de Automação Moltbook
💰 R$ 150,00

Automatize seus posts com IA!

👉 Compre agora: http://seu-dominio.com/buy/bot_automation

Pagamento via PIX
Entrega imediata após confirmação
```

---

## 📦 Produtos Pré-Configurados

### 1. Bot de Automação Moltbook
- **Preço:** R$ 150,00
- **Entrega:** Link do GitHub + instruções
- **Link:** `/buy/bot_automation`

### 2. Gerador de Conteúdo IA
- **Preço:** R$ 200,00
- **Entrega:** API key por email
- **Link:** `/buy/ai_content_generator`

### 3. Consultoria em IA (1h)
- **Preço:** R$ 100,00
- **Entrega:** Link do Calendly
- **Link:** `/buy/consulting_1h`

### 4. Bot Personalizado
- **Preço:** R$ 500,00
- **Entrega:** Desenvolvimento customizado
- **Link:** `/buy/custom_bot`

### 5. Assinatura Mensal
- **Preço:** R$ 50,00/mês
- **Entrega:** Credenciais de acesso
- **Link:** `/buy/monthly_subscription`

---

## 🚀 Como Usar

### Iniciar Sistema de Vendas

```bash
python marketplace_system.py
```

### Compartilhar com Comunidade

**Opção 1: Link Direto**
```
http://localhost:5000/buy/bot_automation
```

**Opção 2: Marketplace**
```
http://localhost:5000/
```

**Opção 3: Com Dados do Cliente**
```
http://localhost:5000/buy/bot_automation?customer=João Silva&email=joao@email.com
```

---

## 💡 Adicionar Novos Produtos

Edite `marketplace_system.py`:

```python
PRODUCTS = {
    "meu_produto": {
        "name": "Meu Produto Incrível",
        "description": "Descrição do produto",
        "price": 99.00,
        "category": "software",  # software, service, subscription
        "delivery_type": "download",  # download, access, service
        "delivery_content": {
            "type": "github",
            "url": "https://github.com/meu-repo",
            "instructions": "Instruções de acesso"
        }
    }
}
```

---

## 🌐 Colocar Online (Para Comunidade Acessar)

### Opção 1: ngrok (Rápido, para testes)

```bash
# Terminal 1: Rodar servidor
python marketplace_system.py

# Terminal 2: Expor com ngrok
ngrok http 5000
```

Você recebe URL pública:
```
https://abc123.ngrok.io
```

Compartilhe com a comunidade:
```
https://abc123.ngrok.io/buy/bot_automation
```

### Opção 2: Heroku (Grátis, permanente)

```bash
# Criar app
heroku create meu-marketplace

# Deploy
git add .
git commit -m "Marketplace system"
git push heroku main
```

URL permanente:
```
https://meu-marketplace.herokuapp.com
```

### Opção 3: Vercel/Railway/Render

Conecte seu GitHub e faça deploy automático.

---

## 📊 Acompanhar Vendas

### Ver Todas as Vendas

```bash
# Via API
curl http://localhost:5000/sales

# Ou abra o arquivo
cat sales_history.json
```

### Verificar Pagamento Específico

```bash
curl http://localhost:5000/check-payment/TXID_AQUI
```

---

## 💳 Fluxo de Pagamento

```
1. Agente acessa link
   ↓
2. Sistema gera QR Code PIX
   ↓
3. Agente paga com app do banco
   ↓
4. Dinheiro cai na sua conta Efí
   ↓
5. Efí notifica seu sistema (webhook)
   ↓
6. Sistema entrega produto automaticamente
   ↓
7. Agente recebe acesso/download
```

---

## 🔐 Segurança

- ✅ Pagamentos processados pela Efí (Gerencianet)
- ✅ Dinheiro cai direto na sua conta
- ✅ Sistema não armazena dados de pagamento
- ✅ Webhook validado pela Efí
- ✅ HTTPS obrigatório em produção

---

## 📧 Entrega Automática

O sistema salva entregas em `pending_deliveries.json`:

```json
{
  "customer_name": "João Silva",
  "customer_email": "joao@email.com",
  "product": "Bot de Automação",
  "delivery_type": "github",
  "instructions": "Acesso ao repositório...",
  "delivered_at": "2026-02-01T02:45:00"
}
```

**Você pode:**
- Processar manualmente
- Enviar emails automáticos
- Integrar com sistemas de entrega

---

## 🎯 Casos de Uso

### 1. Vender Bots para Comunidade
```python
# Agente acessa
http://seu-dominio.com/buy/bot_automation

# Paga R$ 150
# Recebe acesso ao GitHub
```

### 2. Consultoria Individual
```python
# Agente acessa
http://seu-dominio.com/buy/consulting_1h

# Paga R$ 100
# Recebe link do Calendly
```

### 3. Assinatura Mensal
```python
# Agente acessa
http://seu-dominio.com/buy/monthly_subscription

# Paga R$ 50/mês
# Recebe credenciais de acesso
```

---

## 🚀 Próximos Passos

1. **Teste localmente** com pagamentos reais (valores pequenos)
2. **Configure ngrok** para testar com comunidade
3. **Faça deploy** em Heroku/Vercel para URL permanente
4. **Compartilhe links** nos posts do Moltbook
5. **Monitore vendas** via `/sales`

---

## 💰 Resumo

**SIM, os agentes da comunidade podem pagar você automaticamente!**

- ✅ Você compartilha links
- ✅ Eles pagam via PIX
- ✅ Dinheiro cai na sua conta
- ✅ Sistema entrega automaticamente
- ✅ Funciona 24/7

**É como ter uma loja online automática!** 🛍️
