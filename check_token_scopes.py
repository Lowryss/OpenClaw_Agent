# Check Token Scopes
import jwt
from efi_payment_system import EfiPaymentSystem

print("🔍 VERIFICANDO ESCOPOS DO TOKEN")
print("=" * 70)
print()

efi = EfiPaymentSystem()

print("1️⃣ Autenticando...")
if not efi.authenticate():
    print("❌ Falha na autenticação")
    exit(1)

print()
print("2️⃣ Decodificando token JWT...")
print()

try:
    # Decode JWT token (without verification, just to see contents)
    token = efi.access_token
    
    # JWT tokens have 3 parts separated by dots
    parts = token.split('.')
    
    if len(parts) == 3:
        import base64
        import json
        
        # Decode header
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        
        # Decode payload
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        
        print("📋 HEADER:")
        print(json.dumps(header, indent=2))
        print()
        
        print("📋 PAYLOAD:")
        print(json.dumps(payload, indent=2))
        print()
        
        # Check for scope
        if 'scope' in payload:
            scopes = payload['scope'].split() if isinstance(payload['scope'], str) else payload['scope']
            print("✅ ESCOPOS ENCONTRADOS:")
            for scope in scopes:
                print(f"   • {scope}")
        else:
            print("⚠️ Nenhum escopo encontrado no token")
            print()
            print("💡 Isso pode significar:")
            print("   1. As alterações ainda não foram aplicadas")
            print("   2. É necessário gerar novas credenciais")
            print("   3. A aplicação não tem escopos configurados")
        
        print()
        print("=" * 70)
        print()
        print("🔧 SOLUÇÕES:")
        print("   1. Aguarde 2-3 minutos e tente novamente")
        print("   2. Ou gere novas credenciais no painel Efí:")
        print("      • API → Minhas Aplicações → Sua App → Gerar Novas Credenciais")
        print("   3. Atualize o .env com as novas credenciais")
        
except Exception as e:
    print(f"❌ Erro ao decodificar token: {e}")
    print()
    print("Token (primeiros 100 caracteres):")
    print(token[:100] + "...")
