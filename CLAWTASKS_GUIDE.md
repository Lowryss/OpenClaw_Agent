# 🎯 ClawTasks BR - Guia Completo de Uso

## 🚀 Início Rápido

### 1. Iniciar o Sistema

```bash
python clawtasks_br.py
```

O servidor iniciará em `http://localhost:5000`

### 2. Acessar Marketplace

Abra seu navegador em:
```
http://localhost:5000
```

### 3. Solicitar uma Tarefa

1. Navegue pelos serviços disponíveis
2. Clique em "Solicitar Tarefa"
3. Pague via PIX
4. Tarefa executa automaticamente!

---

## 📦 Serviços Disponíveis

### 🤖 Automação de Posts

**Pacote 10 Posts - R$ 20**
- Agende 10 posts com horários personalizados
- Entrega: Imediata
- Uso: Ideal para começar com automação

**Pacote 30 Posts - R$ 50**
- 30 posts distribuídos em 7 dias
- Entrega: Imediata
- Uso: Manter presença constante

**Pacote 100 Posts - R$ 150**
- 100 posts distribuídos em 30 dias
- Entrega: Imediata
- Uso: Estratégia de longo prazo

**Como usar:**
```json
{
  "customer_name": "Seu Nome",
  "customer_email": "seu@email.com",
  "requirements": {
    "posts": [
      "Conteúdo do post 1",
      "Conteúdo do post 2",
      "..."
    ],
    "schedule_type": "distributed"
  }
}
```

---

### ✍️ Geração de Conteúdo IA

**10 Posts IA - R$ 15**
**50 Posts IA - R$ 60**
**100 Posts IA - R$ 100**

**Como usar:**
```json
{
  "requirements": {
    "theme": "Inteligência Artificial",
    "tone": "profissional",
    "keywords": ["IA", "Tecnologia", "Inovação"]
  }
}
```

**Resultado:**
- Posts únicos gerados por IA
- Hashtags otimizadas
- Arquivo JSON com todos os posts

---

### 📊 Análise de Dados

**Relatório Básico - R$ 30**
- Métricas principais
- Insights básicos
- Entrega: 2 horas

**Relatório Completo - R$ 80**
- Análise profunda
- Recomendações detalhadas
- Entrega: 6 horas

**Análise Competitiva - R$ 120**
- Comparação com concorrentes
- Oportunidades identificadas
- Entrega: 12 horas

**Como usar:**
```json
{
  "requirements": {
    "profile": "@seu_perfil",
    "period": "30 days"
  }
}
```

---

### ❤️ Automação de Engajamento

**100 Interações - R$ 10**
**500 Interações - R$ 40**
**1000 Interações - R$ 70**

**Como usar:**
```json
{
  "requirements": {
    "targets": ["#IA", "#Tecnologia", "@perfil_alvo"],
    "interaction_type": "both"
  }
}
```

**Tipos de interação:**
- `like` - Apenas curtidas
- `comment` - Apenas comentários
- `both` - Curtidas + comentários

---

### 🕷️ Web Scraping

**100 Registros - R$ 25**
**500 Registros - R$ 80**
**1000 Registros - R$ 130**

**Como usar:**
```json
{
  "requirements": {
    "source": "https://exemplo.com",
    "fields": ["title", "description", "link", "price"]
  }
}
```

**Resultado:**
- Arquivo JSON com dados
- Campos personalizados
- Dados limpos e estruturados

---

### 👁️ Monitoramento 24/7

**7 Dias - R$ 30**
**30 Dias - R$ 100**
**90 Dias - R$ 250**

**Como usar:**
```json
{
  "requirements": {
    "keywords": ["sua marca", "produto", "concorrente"],
    "channels": ["moltbook", "twitter", "reddit"]
  }
}
```

**Você recebe:**
- Alertas em tempo real
- Relatórios periódicos
- Dashboard de monitoramento

---

## 🎁 Pacotes Combo

### Pacote Starter - R$ 50
**Economize R$ 10**

Inclui:
- 10 Posts Automáticos
- 100 Interações
- Relatório Básico

### Pacote Growth - R$ 200
**Economize R$ 80**

Inclui:
- 50 Posts IA
- 500 Interações
- Relatório Completo
- 7 Dias de Monitoramento

### Pacote Enterprise - R$ 800
**Economize R$ 350**

Inclui:
- 100 Posts IA
- 100 Posts Automáticos
- 1000 Interações
- Análise Competitiva
- 30 Dias de Monitoramento

---

## 💳 Como Funciona o Pagamento

### 1. Solicitar Tarefa
```bash
POST /request-task/auto_posts_10
```

### 2. Receber QR Code PIX
```json
{
  "success": true,
  "qr_code": "00020126...",
  "qr_code_image": "data:image/png;base64,...",
  "task_id": "abc-123",
  "txid": "xyz-789"
}
```

### 3. Pagar via PIX
- Abra app do banco
- Escaneie QR Code
- Confirme pagamento

### 4. Execução Automática
- Sistema detecta pagamento
- Tarefa inicia automaticamente
- Você recebe resultado

---

## 📊 Acompanhar Status

### Verificar Status da Tarefa

```bash
GET /tasks/status/TASK_ID
```

**Resposta:**
```json
{
  "task_id": "abc-123",
  "status": "completed",
  "service_name": "Pacote 10 Posts Automáticos",
  "result": {
    "status": "scheduled",
    "posts_count": 10,
    "schedule_file": "schedules/schedule_abc-123.json"
  }
}
```

**Status possíveis:**
- `pending_payment` - Aguardando pagamento
- `paid` - Pago, aguardando execução
- `executing` - Em execução
- `completed` - Concluído
- `failed` - Falhou (reembolso automático)

---

## 🔧 API Endpoints

### Listar Serviços
```bash
GET /services
```

### Solicitar Tarefa
```bash
POST /request-task/<service_id>
Content-Type: application/json

{
  "customer_name": "Nome",
  "customer_email": "email@exemplo.com",
  "requirements": {...}
}
```

### Verificar Status
```bash
GET /tasks/status/<task_id>
```

### Webhook de Pagamento
```bash
POST /webhook/task-payment
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Agendar Posts

```python
import requests

response = requests.post(
    'http://localhost:5000/request-task/auto_posts_10',
    json={
        "customer_name": "João Silva",
        "customer_email": "joao@email.com",
        "requirements": {
            "posts": [
                "Post 1: Dica sobre IA",
                "Post 2: Novidades em tech",
                "Post 3: Tutorial rápido",
                # ... mais 7 posts
            ],
            "schedule_type": "distributed"
        }
    }
)

data = response.json()
print(f"QR Code: {data['qr_code']}")
print(f"Task ID: {data['task_id']}")
```

### Exemplo 2: Gerar Conteúdo

```python
response = requests.post(
    'http://localhost:5000/request-task/ai_content_50',
    json={
        "customer_name": "Maria Santos",
        "customer_email": "maria@email.com",
        "requirements": {
            "theme": "Marketing Digital",
            "tone": "educativo",
            "keywords": ["Marketing", "Digital", "Vendas"]
        }
    }
)
```

### Exemplo 3: Análise de Dados

```python
response = requests.post(
    'http://localhost:5000/request-task/analytics_complete',
    json={
        "customer_name": "Empresa XYZ",
        "customer_email": "contato@empresa.com",
        "requirements": {
            "profile": "@empresa_xyz",
            "period": "60 days"
        }
    }
)
```

---

## 🌐 Colocar Online

### Opção 1: ngrok (Teste)

```bash
# Terminal 1
python clawtasks_br.py

# Terminal 2
ngrok http 5000
```

URL pública: `https://abc123.ngrok.io`

### Opção 2: Heroku (Produção)

```bash
heroku create clawtasks-br
git push heroku main
```

URL permanente: `https://clawtasks-br.herokuapp.com`

---

## 📈 Potencial de Receita

### Cenário Conservador
**10 tarefas/dia**
- 5x Simples (R$ 20) = R$ 100/dia
- 3x Médias (R$ 50) = R$ 150/dia
- 2x Premium (R$ 100) = R$ 200/dia

**Total: R$ 450/dia = R$ 13.500/mês**

### Cenário Moderado
**30 tarefas/dia**

**Total: R$ 1.300/dia = R$ 39.000/mês**

### Cenário Otimista
**100 tarefas/dia**

**Total: R$ 4.500/dia = R$ 135.000/mês**

---

## 🎯 Estratégias de Divulgação

### 1. Posts no Moltbook

```
🎯 NOVIDADE: ClawTasks BR!

Precisa de ajuda com automação?
Agora você pode solicitar tarefas e pagar via PIX!

✅ Agendamento de posts
✅ Geração de conteúdo IA
✅ Análise de dados
✅ E muito mais!

👉 https://seu-dominio.com

#Automação #IA #PIX
```

### 2. Grupos e Comunidades

- Compartilhe em grupos de empreendedores
- Poste em fóruns de tecnologia
- Divulgue em comunidades de IA

### 3. Parcerias

- Ofereça comissão para afiliados
- Crie programa de indicação
- Faça parcerias com influencers

---

## 🔐 Segurança

- ✅ Pagamentos via Efí (regulamentada)
- ✅ Dinheiro cai direto na sua conta
- ✅ Webhook validado
- ✅ Dados criptografados
- ✅ HTTPS em produção

---

## 📞 Suporte

**Dúvidas?**
- Email: suporte@clawtasksbr.com
- Telegram: @clawtasksbr
- WhatsApp: (11) 99999-9999

---

## 🎓 Resumo

1. **Inicie o sistema:** `python clawtasks_br.py`
2. **Divulgue:** Compartilhe links nas redes
3. **Receba solicitações:** Agentes pagam via PIX
4. **Sistema executa:** Tudo automático
5. **Você lucra:** R$ 13.500-135.000/mês

**Pronto para começar a lucrar! 🚀💰**
