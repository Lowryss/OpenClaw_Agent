# Detailed Authentication Test
import sys
import traceback
from pathlib import Path

print("🔍 DIAGNÓSTICO DETALHADO - AUTENTICAÇÃO EFÍ")
print("=" * 70)
print()

# Check .env file
print("1️⃣ Verificando arquivo .env...")
env_path = Path(".env")
if env_path.exists():
    print(f"   ✅ Arquivo .env encontrado")
    with open(env_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"   📋 {len(lines)} variáveis configuradas")
else:
    print(f"   ❌ Arquivo .env NÃO encontrado!")
print()

# Check certificate
print("2️⃣ Verificando certificado...")
cert_path = Path("producao-872278-clawdbot.p12")
if cert_path.exists():
    size = cert_path.stat().st_size
    print(f"   ✅ Certificado encontrado: {cert_path.name}")
    print(f"   📦 Tamanho: {size:,} bytes")
else:
    print(f"   ❌ Certificado NÃO encontrado: {cert_path}")
print()

# Load config
print("3️⃣ Carregando configuração...")
try:
    from config import config
    print(f"   ✅ Módulo config.py carregado")
    print(f"   • Client ID: {config.client_id[:30] if config.client_id else 'NÃO CONFIGURADO'}...")
    print(f"   • Client Secret: {'***' + config.client_secret[-10:] if config.client_secret else 'NÃO CONFIGURADO'}")
    print(f"   • PIX Key: {config.pix_key if config.pix_key else 'NÃO CONFIGURADO'}")
    print(f"   • Sandbox: {config.sandbox}")
    print(f"   • Base URL: {config.base_url}")
except Exception as e:
    print(f"   ❌ Erro ao carregar config: {e}")
    traceback.print_exc()
    sys.exit(1)
print()

# Initialize EfiPaymentSystem
print("4️⃣ Inicializando EfiPaymentSystem...")
try:
    from efi_payment_system import EfiPaymentSystem
    efi = EfiPaymentSystem()
    print(f"   ✅ Sistema inicializado")
except Exception as e:
    print(f"   ❌ Erro ao inicializar: {e}")
    traceback.print_exc()
    sys.exit(1)
print()

# Test authentication
print("5️⃣ Testando autenticação com API Efí...")
print("-" * 70)
try:
    success = efi.authenticate()
    print("-" * 70)
    
    if success:
        print()
        print("🎉 SUCESSO! Autenticação funcionou!")
        print()
        print("✅ Próximos passos:")
        print("   1. Testar criação de cobrança PIX")
        print("   2. Configurar webhook")
        print("   3. Testar pagamento real")
    else:
        print()
        print("❌ Autenticação falhou")
        print()
        print("🔧 Verifique:")
        print("   1. Credenciais no painel Efí")
        print("   2. Certificado é de produção")
        print("   3. Conta Efí está ativa")
        
except Exception as e:
    print()
    print(f"❌ ERRO DURANTE AUTENTICAÇÃO: {e}")
    print()
    print("📋 Detalhes do erro:")
    traceback.print_exc()
