#!/usr/bin/env python

# Update all secrets having a `tls.crt` which is expired.
# Read and adapt the code before running.

import base64
import datetime

from kubernetes import client, config

from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pem
from cryptography.hazmat.primitives import serialization

new_secret_value='LS0tLS1CRUdJTiBDR...'

def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    for ns in client.CoreV1Api().list_namespace().items:
        secrets = v1.list_namespaced_secret(ns.metadata.name)
        for secret in secrets.items:
            if not secret.data:
                continue
            crt = secret.data.get('tls.crt')
            if not crt:
                continue
            expired = handle_cert(crt, ns.metadata.name, secret.metadata.name)
            if expired:
                pass
                #secret.data['tls.crt'] = new_secret_value
                #v1.patch_namespaced_secret(secret.metadata.name, ns.metadata.name, secret)

            
def handle_cert(crt, namespace, name):
    # Load PEM certificate from a string
    certs = pem.parse(base64.b64decode(crt))
    expired = False
    for cert_str in certs:
        cert = x509.load_pem_x509_certificate(str(cert_str).encode(), default_backend())
        if cert.not_valid_after > datetime.datetime.now():
            continue
        expired = True
        print()
        print(f'############## expired Secret {name} {namespace} ####################')
        print("Issuer:", cert.issuer)
        print("Subject:", cert.subject)
        print("Serial Number:", cert.serial_number)
        print("Not valid before:", cert.not_valid_before)
        print("Not valid after:", cert.not_valid_after)
    return expired

def cert_to_text(cert_pem):
    cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
    return cert.public_bytes(serialization.Encoding.PEM).decode()

def chain_to_text(chain):
    return "\n".join(cert_to_text(cert) for cert in chain)
  
if __name__ == "__main__":
    main()
