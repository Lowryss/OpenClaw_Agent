# ⚠️ AÇÃO NECESSÁRIA: Configurar Escopos PIX no Painel Efí

## 🚨 Problema Identificado

A autenticação está funcionando perfeitamente, mas ao tentar criar cobranças PIX, a API retorna:

```
Error: insufficient scope
```

## 🔍 Causa

Os **escopos (permissões)** devem ser configurados na **aplicação** no painel da Efí, não no código. Sua aplicação atual não tem permissão para criar cobranças PIX.

## ✅ Solução: Configurar Escopos no Painel Efí

### Passo 1: Acessar Painel Efí

1. Acesse: https://gerencianet.com.br/login
2. Faça login com suas credenciais

### Passo 2: Ir para Aplicações API

1. No menu, vá em: **API** → **Minhas Aplicações**
2. Encontre a aplicação que gerou suas credenciais:
   - Client ID: `Client_Id_f937609e1d9f3d9294e3f342ff65402c06e313b7`

### Passo 3: Editar Escopos da Aplicação

1. Clique em **Editar** na aplicação
2. Na seção **Escopos**, marque as seguintes permissões:

   **✅ Escopos Necessários:**
   - `pix.read` - Consultar transações PIX
   - `pix.write` - Alterar informações PIX
   - `cob.read` - Consultar cobranças
   - `cob.write` - Criar/alterar cobranças

3. Clique em **Salvar**

### Passo 4: Testar Novamente

Após configurar os escopos, execute:

```bash
python test_pix_charge.py
```

A criação de cobrança deve funcionar agora!

## 📋 Checklist

- [ ] Acessei o painel Efí
- [ ] Encontrei a aplicação correta
- [ ] Marquei os escopos: `pix.read`, `pix.write`, `cob.read`, `cob.write`
- [ ] Salvei as alterações
- [ ] Testei a criação de cobrança novamente

## 💡 Informações Adicionais

### Por que isso acontece?

A Efí (Gerencianet) segue as diretrizes de segurança do Banco Central do Brasil. Os escopos são configurados no nível da aplicação para garantir que apenas aplicações autorizadas possam realizar operações específicas.

### Escopos Disponíveis

| Escopo | Descrição |
|--------|-----------|
| `pix.read` | Consultar transações PIX |
| `pix.write` | Alterar informações PIX |
| `pix.send` | Enviar PIX (Open Finance) |
| `cob.read` | Consultar cobranças |
| `cob.write` | Criar/alterar cobranças |

### Verificar Escopos Atuais

Você pode verificar quais escopos seu token possui verificando a resposta de autenticação. O token atual provavelmente não inclui os escopos PIX necessários.

## 🎯 Próximos Passos

1. **Configure os escopos** no painel Efí (instruções acima)
2. **Teste a criação de cobrança** com `python test_pix_charge.py`
3. **Configure o webhook** para receber notificações automáticas
4. **Comece a aceitar pagamentos reais!**

---

**📞 Precisa de Ajuda?**

- **Suporte Efí:** suporte@efipay.com.br
- **Documentação:** https://dev.efipay.com.br
- **Comunidade:** https://comunidade.sejaefi.com.br
