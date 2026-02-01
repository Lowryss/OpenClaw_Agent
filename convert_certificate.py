# Certificate Converter - .p12 to .pem (Python version)
# Uses cryptography library to convert without OpenSSL

from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

def convert_p12_to_pem_python(p12_file, password="", output_pem=None):
    """
    Convert .p12 certificate to .pem format using Python cryptography library
    
    Args:
        p12_file: Path to .p12 certificate file
        password: Certificate password (empty string if no password)
        output_pem: Output .pem file path (optional)
    
    Returns:
        Path to generated .pem file or None if failed
    """
    p12_path = Path(p12_file)
    
    if not p12_path.exists():
        print(f"❌ Arquivo não encontrado: {p12_file}")
        return None
    
    if output_pem is None:
        output_pem = p12_path.with_suffix('.pem')
    else:
        output_pem = Path(output_pem)
    
    print(f"🔄 Convertendo certificado...")
    print(f"   Origem: {p12_path.name}")
    print(f"   Destino: {output_pem.name}")
    print()
    
    try:
        # Read .p12 file
        with open(p12_path, 'rb') as f:
            p12_data = f.read()
        
        # Convert password to bytes
        password_bytes = password.encode() if password else None
        
        # Load PKCS12
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            p12_data,
            password_bytes
        )
        
        # Write PEM file with both private key and certificate
        with open(output_pem, 'wb') as f:
            # Write private key
            if private_key:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            # Write certificate
            if certificate:
                f.write(certificate.public_bytes(
                    encoding=serialization.Encoding.PEM
                ))
            
            # Write additional certificates (certificate chain)
            if additional_certs:
                for cert in additional_certs:
                    f.write(cert.public_bytes(
                        encoding=serialization.Encoding.PEM
                    ))
        
        if output_pem.exists():
            size = output_pem.stat().st_size
            print(f"✅ Conversão bem-sucedida!")
            print(f"   📦 Arquivo gerado: {output_pem.name} ({size:,} bytes)")
            print()
            print(f"📋 Conteúdo:")
            if private_key:
                print(f"   ✅ Chave privada")
            if certificate:
                print(f"   ✅ Certificado")
            if additional_certs:
                print(f"   ✅ {len(additional_certs)} certificado(s) adicional(is)")
            
            return str(output_pem)
        else:
            print(f"❌ Arquivo PEM não foi criado")
            return None
            
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        print()
        print("💡 Possíveis causas:")
        print("   • Senha incorreta (certificado não tem senha)")
        print("   • Arquivo .p12 corrompido")
        print("   • Formato inválido")
        return None


if __name__ == "__main__":
    print("🔐 CONVERSOR DE CERTIFICADO EFÍ (Python)")
    print("=" * 70)
    print()
    
    # Certificate file
    p12_file = "producao-872278-clawdbot.p12"
    password = ""  # No password for this certificate
    
    # Convert
    pem_file = convert_p12_to_pem_python(p12_file, password)
    
    if pem_file:
        print()
        print("=" * 70)
        print("✅ PRONTO! Certificado convertido com sucesso.")
        print()
        print("📋 Próximos passos:")
        print("   1. O arquivo .pem será usado automaticamente")
        print("   2. Execute: python test_auth.py")
        print("   3. A autenticação deve funcionar agora!")
    else:
        print()
        print("=" * 70)
        print("❌ Conversão falhou. Verifique os erros acima.")
