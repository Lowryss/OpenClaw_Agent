# 🚀 Deploy no Heroku - Guia Passo a Passo

## ✅ Arquivos Criados

Já criamos todos os arquivos necessários:
- ✅ `Procfile` - Comando de inicialização
- ✅ `requirements.txt` - Dependências Python
- ✅ `runtime.txt` - Versão do Python
- ✅ `clawtasks_br.py` - Atualizado para Heroku

## 📋 Passo a Passo

### 1. Instalar Heroku CLI

**Windows:**
```bash
# Baixe e instale: https://devcenter.heroku.com/articles/heroku-cli
# Ou use winget:
winget install Heroku.HerokuCLI
```

### 2. Login no Heroku

```bash
heroku login
```

Isso abrirá o navegador para você fazer login.

### 3. Criar App no Heroku

```bash
cd C:\Users\Amauri\.gemini\antigravity\scratch\OpenClaw_Agent
heroku create clawtasks-br
```

**Nota:** Se o nome já existir, tente:
- `clawtasks-brasil`
- `clawtasks-pix`
- `marketplace-tarefas-br`

### 4. Inicializar Git (se necessário)

```bash
git init
git add .
git commit -m "ClawTasks BR - Sistema completo"
```

### 5. Configurar Variáveis de Ambiente

```bash
heroku config:set EFI_CLIENT_ID=Client_Id_bc7b525b1d251d931ca0330e0c908bc0b07bd723
heroku config:set EFI_CLIENT_SECRET=Client_Secret_0e43d64ca0290804471442f6d093783898c0a8e1
heroku config:set EFI_CERTIFICATE_PATH=producao-872278-clawdbot.pem
heroku config:set EFI_PIX_KEY=56bbb9d4-d884-4456-97bd-8c32ea5ce8d7
heroku config:set EFI_SANDBOX=false
```

### 6. Adicionar Certificado ao Heroku

O certificado `.pem` precisa estar no repositório:

```bash
# Já está no diretório, apenas commit
git add producao-872278-clawdbot.pem
git commit -m "Add production certificate"
```

### 7. Deploy!

```bash
git push heroku main
```

**Ou se estiver em branch master:**
```bash
git push heroku master
```

### 8. Abrir App

```bash
heroku open
```

Isso abrirá seu app em: `https://clawtasks-br.herokuapp.com`

### 9. Ver Logs (se necessário)

```bash
heroku logs --tail
```

---

## 🔧 Configurar Webhook Efí

Após deploy, configure o webhook:

1. Acesse: https://gerencianet.com.br/painel
2. Vá em: **API** → **Webhooks**
3. Configure:
   ```
   URL: https://clawtasks-br.herokuapp.com/webhook/task-payment
   Eventos: PIX recebido
   ```

---

## ✅ Verificar se Está Funcionando

```bash
# Testar endpoint
curl https://clawtasks-br.herokuapp.com/services

# Ou abra no navegador
https://clawtasks-br.herokuapp.com
```

---

## 🎯 Após Deploy

1. **Copie a URL:** `https://clawtasks-br.herokuapp.com`

2. **Atualize posts de marketing:**
   - Substitua `http://localhost:5000` pela URL do Heroku
   - Gere novos posts com URL correta

3. **Teste compra:**
   - Acesse o marketplace
   - Solicite uma tarefa
   - Pague via PIX
   - Verifique execução

4. **Divulgue:**
   - Poste no Moltbook
   - Compartilhe em grupos
   - Comece a receber vendas!

---

## 🚨 Troubleshooting

### Erro: "App crashed"
```bash
heroku logs --tail
# Verifique os logs para ver o erro
```

### Erro: "No web process running"
```bash
heroku ps:scale web=1
```

### Erro: "Application error"
- Verifique se todas as variáveis de ambiente estão configuradas
- Confirme que `Procfile` está correto
- Veja logs com `heroku logs --tail`

---

## 💡 Comandos Úteis

```bash
# Ver status do app
heroku ps

# Reiniciar app
heroku restart

# Ver variáveis configuradas
heroku config

# Abrir dashboard
heroku dashboard
```

---

## 🎉 Pronto!

Após seguir esses passos, seu ClawTasks BR estará online 24/7 no Heroku!

**URL pública:** `https://clawtasks-br.herokuapp.com`

**Próximo passo:** Divulgar e começar a receber vendas! 💰
