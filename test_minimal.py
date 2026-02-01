# Simple PIX Charge Test
from efi_payment_system import EfiPaymentSystem
import json

efi = EfiPaymentSystem()

if not efi.authenticate():
    print("Auth failed")
    exit(1)

# Try minimal charge
import secrets
import string
txid = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

url = f"{efi.base_url}/v2/cob/{txid}"
headers = {
    "Authorization": f"Bearer {efi.access_token}",
    "Content-Type": "application/json"
}

# Minimal payload according to Efí docs
payload = {
    "calendario": {
        "expiracao": 3600
    },
    "valor": {
        "original": "0.01"
    },
    "chave": efi.pix_key
}

print(f"TXID: {txid}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()

try:
    response = efi.session.put(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")
