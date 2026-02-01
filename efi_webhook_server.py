# Efí Webhook Server - Receives payment notifications
# Run this to automatically deliver services when payments are received

from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime
from efi_payment_system import EfiPaymentSystem, AgentServiceDelivery

app = Flask(__name__)

# Initialize systems using config.py
efi = EfiPaymentSystem()
delivery = AgentServiceDelivery(efi)

@app.route('/')
def index():
    """Main page with payment interface"""
    return render_template('index.html', services=delivery.services)

@app.route('/webhook/efi', methods=['POST'])
def efi_webhook():
    """
    Efí webhook endpoint
    This receives notifications when payments are completed
    """
    try:
        # Get webhook data
        webhook_data = request.json
        
        print(f"\n🔔 Webhook received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data: {json.dumps(webhook_data, indent=2)}")
        
        # Process payment and deliver service
        result = delivery.process_payment_webhook(webhook_data)
        
        if result.get("success"):
            print(f"✅ Service delivered successfully!")
            print(f"   Service: {result.get('result', {}).get('type')}")
            return jsonify({"status": "success"}), 200
        else:
            print(f"⚠️ Payment not confirmed yet")
            return jsonify({"status": "pending"}), 200
            
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/create-payment/<service_id>', methods=['GET', 'POST'])
def create_payment(service_id):
    """
    Create a payment link for a service
    Usage: http://localhost:5000/create-payment/automation_setup
    """
    customer_name = request.args.get('customer', 'Cliente')
    
    print(f"\n💰 Creating payment for service: {service_id}")
    print(f"   Customer: {customer_name}")
    
    result = delivery.create_payment_link(service_id, customer_name)
    
    if result.get("success"):
        print(f"✅ Payment created successfully")
        print(f"   TXID: {result['txid']}")
        print(f"   Amount: R$ {result['amount']:.2f}")
        
        return jsonify({
            "success": True,
            "service": result["service"],
            "amount": result["amount"],
            "qr_code": result["qr_code"],
            "qr_code_image": result["qr_code_image"],
            "txid": result["txid"],
            "instructions": "Scan the QR Code with your bank app to pay"
        })
    else:
        print(f"❌ Failed to create payment: {result}")
        return jsonify(result), 400

@app.route('/check-payment/<txid>', methods=['GET'])
def check_payment(txid):
    """Check payment status"""
    print(f"\n🔍 Checking payment status for TXID: {txid}")
    status = efi.check_payment_status(txid)
    
    if status.get('paid'):
        print(f"✅ Payment confirmed!")
    else:
        print(f"⏳ Payment status: {status.get('status')}")
    
    return jsonify(status)

@app.route('/services', methods=['GET'])
def list_services():
    """List available services"""
    services_list = []
    for service_id, service_data in delivery.services.items():
        services_list.append({
            "id": service_id,
            "description": service_data["description"],
            "price": service_data["price"]
        })
    
    return jsonify({"services": services_list})

if __name__ == "__main__":
    print("🚀 Efí Webhook Server Starting...")
    print("=" * 70)
    print("\n📋 Configuration:")
    print(f"   Environment: {'Production' if not efi.sandbox else 'Sandbox'}")
    print(f"   PIX Key: {efi.pix_key}")
    print(f"   Certificate: {efi.certificate_path}")
    print("\n🌐 Endpoints:")
    print("   • GET  / - Payment interface")
    print("   • POST /webhook/efi - Receives payment notifications")
    print("   • GET  /create-payment/<service_id> - Generate payment")
    print("   • GET  /check-payment/<txid> - Check payment status")
    print("   • GET  /services - List available services")
    print()
    print("Server running on: http://localhost:5000")
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
