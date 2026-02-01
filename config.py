# Configuration Module for Efí Payment System
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EfiConfig:
    """Centralized configuration for Efí payment system"""
    
    def __init__(self):
        # Credentials
        self.client_id = os.getenv('EFI_CLIENT_ID')
        self.client_secret = os.getenv('EFI_CLIENT_SECRET')
        
        # Certificate
        self.certificate_path = os.getenv('EFI_CERTIFICATE_PATH', 'producao-872278-clawdbot.p12')
        self.certificate_password = os.getenv('EFI_CERTIFICATE_PASSWORD', '')
        
        # PIX Key
        self.pix_key = os.getenv('EFI_PIX_KEY')
        
        # Environment
        self.sandbox = os.getenv('EFI_SANDBOX', 'false').lower() == 'true'
        
        # Webhook
        self.webhook_url = os.getenv('EFI_WEBHOOK_URL', 'http://localhost:5000/webhook/efi')
        
        # API URLs
        if self.sandbox:
            self.base_url = "https://api-pix-h.gerencianet.com.br"
        else:
            self.base_url = "https://api-pix.gerencianet.com.br"
    
    def validate(self):
        """Validate that all required configuration is present"""
        errors = []
        
        if not self.client_id:
            errors.append("❌ EFI_CLIENT_ID não configurado")
        
        if not self.client_secret:
            errors.append("❌ EFI_CLIENT_SECRET não configurado")
        
        if not self.pix_key:
            errors.append("❌ EFI_PIX_KEY não configurado")
        
        # Check if certificate file exists
        cert_path = Path(self.certificate_path)
        if not cert_path.is_absolute():
            # If relative path, look in the same directory as this script
            cert_path = Path(__file__).parent / self.certificate_path
        
        if not cert_path.exists():
            errors.append(f"❌ Certificado não encontrado: {cert_path}")
        
        if errors:
            print("\n🚨 ERROS DE CONFIGURAÇÃO:")
            for error in errors:
                print(f"   {error}")
            return False
        
        print("\n✅ CONFIGURAÇÃO VALIDADA:")
        print(f"   • Client ID: {self.client_id[:20]}...")
        print(f"   • Ambiente: {'Sandbox (Testes)' if self.sandbox else 'Produção'}")
        print(f"   • Chave PIX: {self.pix_key}")
        print(f"   • Certificado: {cert_path.name}")
        print(f"   • Webhook: {self.webhook_url}")
        
        return True
    
    def get_certificate_path(self):
        """Get absolute path to certificate file"""
        cert_path = Path(self.certificate_path)
        if not cert_path.is_absolute():
            cert_path = Path(__file__).parent / self.certificate_path
        return str(cert_path)


# Global config instance
config = EfiConfig()


if __name__ == "__main__":
    print("🔧 EFÍ PAYMENT SYSTEM - CONFIGURAÇÃO")
    print("=" * 70)
    
    if config.validate():
        print("\n✅ Sistema pronto para uso!")
    else:
        print("\n❌ Corrija os erros acima antes de continuar.")
        print("\n💡 Dica: Verifique o arquivo .env")
