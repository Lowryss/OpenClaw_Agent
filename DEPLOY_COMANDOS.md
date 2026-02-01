# 🚀 DEPLOY HEROKU - COMANDOS PRONTOS

## ✅ Arquivos Já Criados
- Procfile ✅
- requirements.txt ✅
- runtime.txt ✅
- Sistema atualizado ✅

## 📋 COMANDOS PARA EXECUTAR

### 1. Abrir PowerShell NOVO (Importante!)
Feche e abra um novo terminal para carregar o Heroku CLI.

### 2. Login no Heroku
```powershell
heroku login
```
Isso abrirá o navegador. Faça login.

### 3. Navegar para o diretório
```powershell
cd C:\Users\Amauri\.gemini\antigravity\scratch\OpenClaw_Agent
```

### 4. Inicializar Git (se necessário)
```powershell
git init
git add .
git commit -m "ClawTasks BR - Sistema completo de vendas automaticas"
```

### 5. Criar App no Heroku
```powershell
heroku create clawtasks-br
```

**Se o nome já existir, tente:**
```powershell
heroku create clawtasks-brasil
# OU
heroku create marketplace-tarefas-br
# OU
heroku create vendas-automaticas-br
```

### 6. Configurar Variáveis de Ambiente
```powershell
heroku config:set EFI_CLIENT_ID=Client_Id_bc7b525b1d251d931ca0330e0c908bc0b07bd723

heroku config:set EFI_CLIENT_SECRET=Client_Secret_0e43d64ca0290804471442f6d093783898c0a8e1

heroku config:set EFI_CERTIFICATE_PATH=producao-872278-clawdbot.pem

heroku config:set EFI_PIX_KEY=56bbb9d4-d884-4456-97bd-8c32ea5ce8d7

heroku config:set EFI_SANDBOX=false
```

### 7. Deploy!
```powershell
git push heroku main
```

**Se estiver em branch master:**
```powershell
git push heroku master
```

### 8. Abrir App
```powershell
heroku open
```

### 9. Ver Logs (se necessário)
```powershell
heroku logs --tail
```

---

## 🎯 APÓS DEPLOY

### Sua URL será:
```
https://clawtasks-br.herokuapp.com
```

### Configurar Webhook Efí:
1. Acesse: https://gerencianet.com.br/painel
2. Vá em: API → Webhooks
3. Configure:
   ```
   URL: https://clawtasks-br.herokuapp.com/webhook/task-payment
   Eventos: PIX recebido
   ```

### Testar:
```
https://clawtasks-br.herokuapp.com/services
```

---

## 🚨 SE DER ERRO

### "App crashed"
```powershell
heroku logs --tail
```
Veja o erro e me avise.

### "No web process running"
```powershell
heroku ps:scale web=1
```

### "Application error"
Verifique se todas as variáveis foram configuradas:
```powershell
heroku config
```

---

## ✅ CHECKLIST

- [ ] Abrir PowerShell NOVO
- [ ] `heroku login`
- [ ] `cd C:\Users\Amauri\.gemini\antigravity\scratch\OpenClaw_Agent`
- [ ] `git init` (se necessário)
- [ ] `git add .`
- [ ] `git commit -m "Deploy"`
- [ ] `heroku create clawtasks-br`
- [ ] Configurar variáveis (6 comandos)
- [ ] `git push heroku main`
- [ ] `heroku open`
- [ ] Configurar webhook Efí
- [ ] Testar compra

---

## 🎉 PRONTO!

Após executar esses comandos, seu sistema estará ONLINE 24/7!

**Copie e cole cada comando no PowerShell.**
