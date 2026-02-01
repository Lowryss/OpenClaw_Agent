# 🔄 GERAR NOVAS CREDENCIAIS COM ESCOPOS PIX

## ⚠️ Problema Identificado

O token atual **NÃO possui os escopos PIX** necessários. Isso acontece porque:

1. Você alterou os escopos da aplicação ✅
2. **MAS** as credenciais antigas (Client ID e Secret) foram geradas **ANTES** dessa alteração
3. É necessário **gerar novas credenciais** para incluir os novos escopos

## ✅ Solução: Gerar Novas Credenciais

### Passo 1: Acessar Painel Efí

1. Acesse: https://gerencianet.com.br/login
2. Vá em: **API** → **Minhas Aplicações**

### Passo 2: Gerar Novas Credenciais

1. Encontre sua aplicação (a mesma que você acabou de configurar os escopos)
2. Clique em **"Gerar Novas Credenciais"** ou **"Renovar Credenciais"**
3. **IMPORTANTE:** Isso irá gerar:
   - Novo **Client ID**
   - Novo **Client Secret**
   - Novo **Certificado .p12**

### Passo 3: Baixar Novo Certificado

1. Faça download do novo certificado `.p12`
2. Salve como: `producao-872278-clawdbot-v2.p12` (ou substitua o antigo)
3. **ATENÇÃO:** Você só pode baixar o certificado UMA VEZ!

### Passo 4: Atualizar Credenciais no .env

Abra o arquivo `.env` e atualize com as novas credenciais:

```env
# Credenciais de Produção (NOVAS - com escopos PIX)
EFI_CLIENT_ID=Client_Id_XXXXXXXXXXXXXXXX  # ← Cole o NOVO Client ID
EFI_CLIENT_SECRET=Client_Secret_XXXXXXXX  # ← Cole o NOVO Client Secret

# Certificado
EFI_CERTIFICATE_PATH=producao-872278-clawdbot-v2.p12  # ← Novo certificado
EFI_CERTIFICATE_PASSWORD=

# Chave PIX (não muda)
EFI_PIX_KEY=56bbb9d4-d884-4456-97bd-8c32ea5ce8d7

# Ambiente
EFI_SANDBOX=false
```

### Passo 5: Converter Novo Certificado

```bash
python convert_certificate.py
```

Isso irá converter o novo `.p12` para `.pem`

### Passo 6: Testar Novamente

```bash
python test_pix_charge.py
```

Agora deve funcionar! 🎉

## 🤔 Por que isso é necessário?

A Efí vincula os **escopos** às **credenciais** no momento da geração. Quando você:

1. Cria credenciais → Elas têm os escopos **daquele momento**
2. Altera escopos → As credenciais **antigas** continuam com os escopos antigos
3. Gera novas credenciais → As **novas** incluem os escopos atualizados

## 📋 Checklist

- [ ] Acessei o painel Efí
- [ ] Gerei novas credenciais
- [ ] Baixei o novo certificado .p12
- [ ] Atualizei o arquivo .env com novo Client ID e Secret
- [ ] Converti o novo certificado: `python convert_certificate.py`
- [ ] Testei: `python test_pix_charge.py`

---

**💡 Dica:** Guarde as credenciais antigas em um local seguro antes de substituí-las, caso precise reverter.
