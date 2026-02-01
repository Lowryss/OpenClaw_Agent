# Efí (Gerencianet) Payment Automation System
# Automated PIX payments for AI agent services

import requests
import json
import base64
from datetime import datetime
import hashlib
import hmac
from pathlib import Path
try:
    from config import config
    USE_CONFIG = True
except ImportError:
    USE_CONFIG = False
    print("⚠️ Aviso: config.py não encontrado, usando configuração manual")

class EfiPaymentSystem:
    def __init__(self, client_id=None, client_secret=None, sandbox=None, certificate_path=None, pix_key=None):
        """
        Initialize Efí payment system
        
        Args:
            client_id: Your Efí Client ID (optional if using config.py)
            client_secret: Your Efí Client Secret (optional if using config.py)
            sandbox: True for testing, False for production (optional if using config.py)
            certificate_path: Path to .p12 certificate (optional if using config.py)
            pix_key: Your PIX key (optional if using config.py)
        """
        # Use config.py if available, otherwise use parameters
        if USE_CONFIG:
            self.client_id = client_id or config.client_id
            self.client_secret = client_secret or config.client_secret
            self.sandbox = sandbox if sandbox is not None else config.sandbox
            self.certificate_path = certificate_path or config.get_certificate_path()
            self.pix_key = pix_key or config.pix_key
            self.base_url = config.base_url
        else:
            self.client_id = client_id
            self.client_secret = client_secret
            self.sandbox = sandbox if sandbox is not None else True
            self.certificate_path = certificate_path
            self.pix_key = pix_key
            
            if self.sandbox:
                self.base_url = "https://pix-h.api.efipay.com.br"
            else:
                self.base_url = "https://pix.api.efipay.com.br"
        
        self.access_token = None
        self.session = self._create_session()
    
    def _create_session(self):
        """Create requests session with certificate for mTLS"""
        session = requests.Session()
        
        # Add certificate if available
        if self.certificate_path and Path(self.certificate_path).exists():
            session.cert = self.certificate_path
            print(f"✅ Certificado carregado: {Path(self.certificate_path).name}")
        else:
            if not self.sandbox:
                print("⚠️ Aviso: Certificado não encontrado. Produção requer certificado!")
        
        return session
    
    def authenticate(self):
        """Get OAuth access token"""
        auth_url = f"{self.base_url}/oauth/token"
        
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "cob.write cob.read pix.read pix.write"  # PIX scopes
        }
        
        try:
            response = self.session.post(auth_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            self.access_token = result.get('access_token')
            
            if self.access_token:
                print("✅ Autenticação bem-sucedida!")
                return True
            else:
                print("❌ Token de acesso não recebido")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de autenticação: {e}")
            if hasattr(e.response, 'text'):
                print(f"   Resposta: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return False
    
    def create_pix_charge(self, amount, description, customer_name="Cliente"):
        """
        Create a PIX charge with QR Code
        
        Args:
            amount: Amount in BRL (e.g., 50.00)
            description: Service description
            customer_name: Customer name
        
        Returns:
            dict with qr_code, qr_code_image, txid
        """
        if not self.access_token:
            self.authenticate()
        
        # Generate unique transaction ID (26-35 alphanumeric characters)
        import secrets
        import string
        txid = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        
        url = f"{self.base_url}/v2/cob/{txid}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "calendario": {
                "expiracao": 3600  # 1 hour expiration
            },
            "valor": {
                "original": f"{amount:.2f}"
            },
            "chave": self.pix_key  # PIX key from config
        }
        
        try:
            response = self.session.put(url, headers=headers, json=payload)
            result = response.json()
            
            if response.status_code == 201:
                # Get QR Code
                loc_id = result.get('loc', {}).get('id')
                qr_code_data = self.get_qr_code(loc_id)
                
                return {
                    "success": True,
                    "txid": txid,
                    "qr_code": qr_code_data.get('qrcode'),
                    "qr_code_image": qr_code_data.get('imagemQrcode'),
                    "amount": amount,
                    "description": description
                }
            else:
                return {
                    "success": False,
                    "error": result
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_qr_code(self, loc_id):
        """Get QR Code for a charge"""
        url = f"{self.base_url}/v2/loc/{loc_id}/qrcode"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        response = self.session.get(url, headers=headers)
        return response.json()
    
    def check_payment_status(self, txid):
        """Check if payment was received"""
        url = f"{self.base_url}/v2/cob/{txid}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        response = self.session.get(url, headers=headers)
        result = response.json()
        
        status = result.get('status')
        
        return {
            "paid": status == "CONCLUIDA",
            "status": status,
            "details": result
        }
    
    def configure_webhook(self, webhook_url, pix_key):
        """
        Configure webhook to receive payment notifications
        
        Args:
            webhook_url: Your webhook URL (e.g., https://yourdomain.com/webhook/efi)
            pix_key: Your PIX key
        """
        url = f"{self.base_url}/v2/webhook/{pix_key}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "webhookUrl": webhook_url
        }
        
        response = self.session.put(url, headers=headers, json=payload)
        return response.json()


class AgentServiceDelivery:
    """Automatic service delivery after payment"""
    
    def __init__(self, efi_system):
        self.efi = efi_system
        self.services = {
            "automation_setup": {
                "price": 50.00,
                "description": "Social Media Automation Setup",
                "delivery": self.deliver_automation_setup
            },
            "data_analysis": {
                "price": 30.00,
                "description": "Data Analysis & Report",
                "delivery": self.deliver_data_analysis
            },
            "content_creation": {
                "price": 20.00,
                "description": "AI Content Creation (1 post)",
                "delivery": self.deliver_content_creation
            },
            "consulting": {
                "price": 100.00,
                "description": "AI Consulting (1 hour)",
                "delivery": self.deliver_consulting
            }
        }
    
    def create_payment_link(self, service_id, customer_name="Cliente"):
        """Generate payment QR Code for a service"""
        if service_id not in self.services:
            return {"error": "Service not found"}
        
        service = self.services[service_id]
        
        charge = self.efi.create_pix_charge(
            amount=service["price"],
            description=service["description"],
            customer_name=customer_name
        )
        
        if charge.get("success"):
            # Save charge info for later delivery
            self.save_pending_delivery(charge["txid"], service_id, customer_name)
            
            return {
                "success": True,
                "service": service["description"],
                "amount": service["price"],
                "qr_code": charge["qr_code"],
                "qr_code_image": charge["qr_code_image"],
                "txid": charge["txid"],
                "message": f"Scan the QR Code to pay R$ {service['price']:.2f}"
            }
        else:
            return charge
    
    def save_pending_delivery(self, txid, service_id, customer_name):
        """Save pending delivery to database/file"""
        pending = {
            "txid": txid,
            "service_id": service_id,
            "customer_name": customer_name,
            "created_at": datetime.now().isoformat(),
            "delivered": False
        }
        
        # Save to JSON file (in production, use a database)
        try:
            with open('pending_deliveries.json', 'r') as f:
                deliveries = json.load(f)
        except:
            deliveries = []
        
        deliveries.append(pending)
        
        with open('pending_deliveries.json', 'w') as f:
            json.dump(deliveries, f, indent=2)
    
    def process_payment_webhook(self, webhook_data):
        """Process webhook notification from Efí"""
        txid = webhook_data.get('txid')
        
        # Check payment status
        status = self.efi.check_payment_status(txid)
        
        if status["paid"]:
            # Load pending delivery
            with open('pending_deliveries.json', 'r') as f:
                deliveries = json.load(f)
            
            for delivery in deliveries:
                if delivery["txid"] == txid and not delivery["delivered"]:
                    # Deliver service
                    service_id = delivery["service_id"]
                    service = self.services[service_id]
                    
                    result = service["delivery"](delivery["customer_name"])
                    
                    # Mark as delivered
                    delivery["delivered"] = True
                    delivery["delivered_at"] = datetime.now().isoformat()
                    
                    # Save updated deliveries
                    with open('pending_deliveries.json', 'w') as f:
                        json.dump(deliveries, f, indent=2)
                    
                    return {
                        "success": True,
                        "message": "Service delivered",
                        "result": result
                    }
        
        return {"success": False, "message": "Payment not confirmed"}
    
    # Service delivery methods
    def deliver_automation_setup(self, customer_name):
        """Deliver automation setup service"""
        print(f"🤖 Delivering Automation Setup to {customer_name}")
        # Send instructions, credentials, etc.
        return {
            "delivered": True,
            "type": "automation_setup",
            "instructions": "Check your email for setup instructions"
        }
    
    def deliver_data_analysis(self, customer_name):
        """Deliver data analysis service"""
        print(f"📊 Delivering Data Analysis to {customer_name}")
        return {
            "delivered": True,
            "type": "data_analysis",
            "report_url": "https://example.com/report/123"
        }
    
    def deliver_content_creation(self, customer_name):
        """Deliver content creation service"""
        print(f"✍️ Delivering Content Creation to {customer_name}")
        return {
            "delivered": True,
            "type": "content_creation",
            "content": "Your AI-generated content is ready!"
        }
    
    def deliver_consulting(self, customer_name):
        """Deliver consulting service"""
        print(f"💼 Delivering Consulting to {customer_name}")
        return {
            "delivered": True,
            "type": "consulting",
            "calendar_link": "https://calendly.com/marylowrys_bot"
        }


# ==================== DEMO / TESTING ====================
if __name__ == "__main__":
    print("🏦 EFÍ PAYMENT AUTOMATION SYSTEM")
    print("=" * 70)
    print()
    
    print("📋 SETUP INSTRUCTIONS:")
    print("-" * 70)
    print("1. Create account at: https://sejaefi.com.br")
    print("2. Get your credentials:")
    print("   • Client ID")
    print("   • Client Secret")
    print("   • Certificate (.p12 or .pem)")
    print("3. Register your PIX key in Efí dashboard")
    print("4. Update credentials in this file")
    print()
    
    print("💡 FEATURES:")
    print("-" * 70)
    print("✅ Automatic PIX QR Code generation")
    print("✅ Real-time payment notifications (webhook)")
    print("✅ Automatic service delivery")
    print("✅ Transaction tracking")
    print("✅ Multiple service tiers")
    print()
    
    print("🔧 AVAILABLE SERVICES:")
    print("-" * 70)
    
    # Demo service catalog
    demo_services = {
        "automation_setup": {"price": 50.00, "desc": "Social Media Automation"},
        "data_analysis": {"price": 30.00, "desc": "Data Analysis & Report"},
        "content_creation": {"price": 20.00, "desc": "AI Content Creation"},
        "consulting": {"price": 100.00, "desc": "AI Consulting (1 hour)"}
    }
    
    for service_id, info in demo_services.items():
        print(f"• {info['desc']:30} R$ {info['price']:.2f}")
    
    print()
    print("=" * 70)
    print("🚀 NEXT STEPS:")
    print("   1. Get Efí credentials")
    print("   2. Update CLIENT_ID and CLIENT_SECRET in code")
    print("   3. Run: python efi_payment_system.py")
    print("   4. Start accepting automated payments!")
    print()
    print("💰 Ready to automate your revenue!")
