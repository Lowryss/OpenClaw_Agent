# OpenClaw Agent Session

Este diretório contém a configuração persistente do seu agente OpenClaw.

## Agent: Marylowrys_Bot
- **Status da Sessão:** Persistente (Local)
- **Rede Social:** Moltbook (Registrado)

## Como usar

### 1. Conectar/Rodar o Agente
Abra esta pasta no terminal e execute:
```powershell
openclaw channels login
openclaw dashboard
```

### 2. Verificar Heartbeat (Moltbook)
Para verificar notificações, status e novos posts no Moltbook, rode o script de heartbeat:
```powershell
.\heartbeat.ps1
```

Este script usa suas credenciais salvas (`moltbook_credentials.json`) para conectar na API.

## Arquivos Importantes
- `heartbeat.ps1` - Script de verificação de status.
- `moltbook_credentials.json` - Suas chaves de acesso (NÃO COMPARTILHE).
- `.openclaw/` - Sessão local do OpenClaw.
- `skills/` - Documentação e arquivos de habilidades.
