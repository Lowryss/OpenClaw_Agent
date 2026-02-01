# Debug PIX Charge Error
import json
from efi_payment_system import EfiPaymentSystem

print("🐛 DEBUG - CRIAÇÃO DE COBRANÇA PIX")
print("=" * 70)
print()

efi = EfiPaymentSystem()

# Authenticate
print("Autenticando...")
if efi.authenticate():
    print(f"✅ Token recebido: {efi.access_token[:50]}...")
else:
    print("❌ Falha na autenticação")
    exit(1)

print()
print("Tentando criar cobrança...")
print()

# Try to create charge and capture full error
import requests

txid = "test123456789"
url = f"{efi.base_url}/v2/cob/{txid}"

headers = {
    "Authorization": f"Bearer {efi.access_token}",
    "Content-Type": "application/json"
}

payload = {
    "calendario": {
        "expiracao": 3600
    },
    "devedor": {
        "nome": "Teste"
    },
    "valor": {
        "original": "0.01"
    },
    "chave": efi.pix_key,
    "solicitacaoPagador": "Teste"
}

print(f"URL: {url}")
print(f"Headers: {json.dumps({k: v[:30] + '...' if len(v) > 30 else v for k, v in headers.items()}, indent=2)}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()

try:
    response = efi.session.put(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
