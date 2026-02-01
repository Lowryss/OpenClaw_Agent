# Quick Authentication Test with Error Logging
import sys
from pathlib import Path

# Redirect output to file
log_file = open('auth_test_log.txt', 'w', encoding='utf-8')
sys.stdout = log_file
sys.stderr = log_file

try:
    print("Testing Efí Authentication...")
    print("=" * 70)
    
    from efi_payment_system import EfiPaymentSystem
    
    efi = EfiPaymentSystem()
    print(f"\nClient ID: {efi.client_id}")
    print(f"Sandbox: {efi.sandbox}")
    print(f"Base URL: {efi.base_url}")
    print(f"Certificate: {efi.certificate_path}")
    print(f"PIX Key: {efi.pix_key}")
    
    print("\n\nAttempting authentication...")
    success = efi.authenticate()
    
    print(f"\n\nResult: {'SUCCESS' if success else 'FAILED'}")
    
    if success:
        print(f"Access Token: {efi.access_token[:50]}...")
    
except Exception as e:
    print(f"\n\nEXCEPTION: {e}")
    import traceback
    traceback.print_exc()

finally:
    log_file.close()
    
# Print to console
with open('auth_test_log.txt', 'r', encoding='utf-8') as f:
    print(f.read(), file=sys.__stdout__)
