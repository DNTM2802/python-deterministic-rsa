import rsa
import sys
import argparse

# Argument parser
parser = argparse.ArgumentParser(description='Deterministic RSA key generation (D-RSA): RSA key pair checker')
parser.add_argument('pub_key', type=str, help='public key file')
parser.add_argument('priv_key', type=str, help='private key file')
args = parser.parse_args()

priv = args.priv_key
pub = args.pub_key

# Read keys from files
f_priv = open(priv, "r")
f_pub = open(pub, "r")
privateKeyPkcs1PEM = f_priv.read()
publicKeyPkcs1PEM = f_pub.read()

# Import public key in PKCS#1 format, PEM encoded 
publicKeyReloaded = rsa.PublicKey.load_pkcs1(publicKeyPkcs1PEM.encode('utf8')) 
# Import private key in PKCS#1 format, PEM encoded 
privateKeyReloaded = rsa.PrivateKey.load_pkcs1(privateKeyPkcs1PEM.encode('utf8')) 

plaintext = "Viva Criptografia Alpicada!".encode('utf8')
print("Plaintext: ", plaintext)

ciphertext = rsa.encrypt(plaintext, publicKeyReloaded)
print("Ciphertext: ", ciphertext)
 
decryptedMessage = rsa.decrypt(ciphertext, privateKeyReloaded)
print("Decrypted message: ", decryptedMessage)