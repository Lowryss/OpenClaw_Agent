# Test PIX Charge Creation
from efi_payment_system import EfiPaymentSystem

print("💰 TESTE DE CRIAÇÃO DE COBRANÇA PIX")
print("=" * 70)
print()

# Initialize
efi = EfiPaymentSystem()

# Authenticate
print("1️⃣ Autenticando...")
if not efi.authenticate():
    print("❌ Falha na autenticação")
    exit(1)

print()
print("2️⃣ Criando cobrança de teste...")
print("   Valor: R$ 0,01 (teste mínimo)")
print("   Descrição: Teste de integração Efí")
print()

# Create a minimal test charge
try:
    charge = efi.create_pix_charge(
        amount=0.01,  # Minimum test amount
        description="Teste de integração Efí - OpenClaw Agent",
        customer_name="Teste"
    )
    
    print("-" * 70)
    
    if charge.get("success"):
        print()
        print("✅ COBRANÇA CRIADA COM SUCESSO!")
        print()
        print(f"📋 Detalhes:")
        print(f"   • TXID: {charge['txid']}")
        print(f"   • Valor: R$ {charge['amount']:.2f}")
        print(f"   • Descrição: {charge['description']}")
        print()
        print(f"🔗 QR Code (Copia e Cola):")
        print(f"   {charge['qr_code'][:80]}...")
        print()
        print(f"🖼️ Imagem QR Code:")
        print(f"   {charge['qr_code_image'][:80]}...")
        print()
        print("=" * 70)
        print("✅ SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print()
        print("📋 Próximos passos:")
        print("   1. Configurar webhook para notificações automáticas")
        print("   2. Integrar com sistema de entrega de serviços")
        print("   3. Começar a aceitar pagamentos reais!")
    else:
        print()
        print("❌ FALHA ao criar cobrança")
        print()
        print(f"Erro: {charge.get('error')}")
        
except Exception as e:
    print()
    print(f"❌ EXCEÇÃO: {e}")
    import traceback
    traceback.print_exc()
