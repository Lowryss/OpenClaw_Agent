# Guia de Configuração do Certificado Efí (.p12)

## 📋 Visão Geral

Este guia explica como configurar o certificado de produção `producao-872278-clawdbot.p12` para processar pagamentos PIX reais através da API Efí (Gerencianet).

## ✅ Pré-requisitos

- [x] Conta Efí criada e verificada
- [x] Certificado de produção baixado: `producao-872278-clawdbot.p12`
- [x] Credenciais de API (Client ID e Client Secret)
- [x] Chave PIX registrada na conta Efí

## 🔧 Configuração Passo a Passo

### 1. Verificar Localização do Certificado

O certificado deve estar no diretório do projeto:

```
OpenClaw_Agent/
├── producao-872278-clawdbot.p12  ← Certificado aqui
├── efi_payment_system.py
├── config.py
└── .env
```

**Status atual:** ✅ Certificado encontrado em `OpenClaw_Agent/producao-872278-clawdbot.p12`

### 2. Configurar Variáveis de Ambiente

O arquivo `.env` já foi criado com suas credenciais:

```env
EFI_CLIENT_ID=Client_Id_f937609e1d9f3d9294e3f342ff65402c06e313b7
EFI_CLIENT_SECRET=Client_Secret_3f3f42bbd1154cfa53fbae58a6990ce72a833ba4
EFI_CERTIFICATE_PATH=producao-872278-clawdbot.p12
EFI_PIX_KEY=56bbb9d4-d884-4456-97bd-8c32ea5ce8d7
EFI_SANDBOX=false
```

> [!WARNING]
> **Segurança Crítica**
> - Nunca compartilhe o arquivo `.env`
> - Nunca faça commit do `.env` no Git
> - O `.gitignore` já está configurado para proteger esses arquivos

### 3. Instalar Dependências

```bash
pip install requests python-dotenv flask
```

### 4. Testar Configuração

Execute o módulo de configuração para validar:

```bash
python config.py
```

**Saída esperada:**
```
✅ CONFIGURAÇÃO VALIDADA:
   • Client ID: Client_Id_f937609e...
   • Ambiente: Produção
   • Chave PIX: 56bbb9d4-d884-4456-97bd-8c32ea5ce8d7
   • Certificado: producao-872278-clawdbot.p12
   • Webhook: http://localhost:5000/webhook/efi
```

### 5. Testar Autenticação

Teste a autenticação com o certificado:

```python
from efi_payment_system import EfiPaymentSystem

# Inicializar (usa config.py automaticamente)
efi = EfiPaymentSystem()

# Testar autenticação
if efi.authenticate():
    print("✅ Autenticação com certificado bem-sucedida!")
else:
    print("❌ Falha na autenticação")
```

## 🚀 Uso em Produção

### Criar Cobrança PIX

```python
from efi_payment_system import EfiPaymentSystem

efi = EfiPaymentSystem()
efi.authenticate()

# Criar cobrança de R$ 50,00
charge = efi.create_pix_charge(
    amount=50.00,
    description="Automação de Redes Sociais",
    customer_name="João Silva"
)

if charge["success"]:
    print(f"QR Code: {charge['qr_code']}")
    print(f"Imagem: {charge['qr_code_image']}")
    print(f"TXID: {charge['txid']}")
```

### Verificar Pagamento

```python
status = efi.check_payment_status(txid)

if status["paid"]:
    print("✅ Pagamento confirmado!")
else:
    print(f"Status: {status['status']}")
```

## 🔐 Autenticação mTLS (Mutual TLS)

O certificado `.p12` é usado para autenticação mTLS com a API Efí:

1. **O que é mTLS?**
   - Autenticação de duas vias entre cliente e servidor
   - Mais seguro que apenas Client ID/Secret
   - Obrigatório para ambiente de produção

2. **Como funciona:**
   ```
   Seu App → [Certificado .p12] → API Efí
            ← [Validação] ←
            → [Token OAuth] →
   ```

3. **Implementação:**
   - O código usa `requests.Session()` com certificado
   - Todas as requisições incluem o certificado automaticamente
   - Não é necessário configurar manualmente

## 🌐 Configurar Webhook para Produção

Para receber notificações automáticas de pagamento, você precisa de uma URL pública.

### Opção 1: Usar ngrok (Testes)

```bash
# Instalar ngrok
# https://ngrok.com/download

# Expor porta 5000
ngrok http 5000
```

Você receberá uma URL como: `https://abc123.ngrok.io`

### Opção 2: Servidor Cloud (Produção)

Deploy em:
- **Heroku**: https://heroku.com
- **Railway**: https://railway.app
- **Render**: https://render.com
- **AWS/Azure/GCP**

### Registrar Webhook

```python
from efi_payment_system import EfiPaymentSystem

efi = EfiPaymentSystem()
efi.authenticate()

# Registrar webhook
result = efi.configure_webhook(
    webhook_url="https://seu-dominio.com/webhook/efi",
    pix_key="56bbb9d4-d884-4456-97bd-8c32ea5ce8d7"
)

print(result)
```

## 🧪 Teste Completo

Execute o servidor de webhook:

```bash
python efi_webhook_server.py
```

Acesse no navegador:
```
http://localhost:5000/create-payment/automation_setup
```

Você verá:
- QR Code PIX
- Valor da cobrança
- ID da transação

Escaneie o QR Code e pague. O webhook receberá a notificação automaticamente!

## 🐛 Troubleshooting

### Erro: "Certificate verify failed"

**Causa:** Certificado não encontrado ou caminho incorreto

**Solução:**
```bash
# Verificar se certificado existe
ls producao-872278-clawdbot.p12

# Verificar caminho no .env
cat .env | grep CERTIFICATE_PATH
```

### Erro: "Authentication failed"

**Causa:** Client ID/Secret incorretos

**Solução:**
1. Verificar credenciais no painel Efí
2. Atualizar `.env` com credenciais corretas
3. Testar novamente: `python config.py`

### Erro: "PIX key not found"

**Causa:** Chave PIX não registrada na conta Efí

**Solução:**
1. Login em: https://gerencianet.com.br
2. Ir em: **PIX** → **Minhas Chaves**
3. Verificar se `56bbb9d4-d884-4456-97bd-8c32ea5ce8d7` está registrada
4. Se não, registrar nova chave ou atualizar `.env`

### Webhook não recebe notificações

**Causa:** URL não acessível publicamente

**Solução:**
1. Usar ngrok para testes: `ngrok http 5000`
2. Registrar webhook com URL ngrok
3. Para produção, fazer deploy em servidor cloud

## 📊 Diferenças: Sandbox vs Produção

| Aspecto | Sandbox | Produção |
|---------|---------|----------|
| **URL Base** | `api-pix-h.gerencianet.com.br` | `api-pix.gerencianet.com.br` |
| **Certificado** | Opcional | **Obrigatório** |
| **Dinheiro** | Simulado | **Real** |
| **Pagamentos** | Teste | Reais |
| **Webhook** | Opcional | Recomendado |

## ✅ Checklist de Produção

Antes de ir para produção, verifique:

- [x] Certificado `.p12` configurado
- [x] Credenciais de produção no `.env`
- [x] `EFI_SANDBOX=false` no `.env`
- [x] Chave PIX registrada e ativa
- [ ] Webhook configurado com URL pública
- [ ] Teste de pagamento real realizado (valor mínimo)
- [ ] Sistema de entrega de serviço funcionando
- [ ] Logs e monitoramento configurados
- [ ] Backup das credenciais em local seguro

## 🎯 Próximos Passos

1. **Testar autenticação:** `python config.py`
2. **Criar cobrança de teste:** Valor mínimo (R$ 0,01)
3. **Configurar webhook:** Usar ngrok ou servidor cloud
4. **Testar fluxo completo:** Pagamento → Webhook → Entrega
5. **Monitorar transações:** Painel Efí + Logs locais

---

**🎉 Parabéns! Seu sistema está configurado para aceitar pagamentos PIX reais!**

Para suporte adicional:
- **Docs Efí:** https://dev.efipay.com.br
- **Suporte:** suporte@efipay.com.br
