# Own modules
from prbg import PRBG
from drsa import DRSA
import os
import rsa
# 
from sys import argv

#import rsa
import numpy as np
from PIL import Image

def test_prbg():

    prgb = PRBG(argv[1], argv[2], argv[3])
    plot_randomness(prgb, 'prgb_randomness')

def plot_randomness(generator, name):
    im = Image.new("RGB", (300,300))
    im = np.array(im)

    buffer = []
    counter = 0
    for i in range(300):
        for k in range (300):
            buffer.append(generator.next_byte())
            buffer.append(generator.next_byte())
            buffer.append(generator.next_byte())

            im[i][k] = buffer
            buffer = []

            counter += 1

    img = Image.fromarray(im, 'RGB')
    img.save(f"{name}.png")
    img.show()

def test_cp():
    prgb = PRBG(argv[1], argv[2], argv[3])
    #prgb.setup()


# def test_rsa():
#     prgb = PRBG(argv[1], argv[2], argv[3])
#     prgb.setup()
#     print(prgb)
    
#     bytes = bytearray([prgb.next_byte() for _ in range(512)])
#     print(bytes)
#     print("TYPE BYTES -> ", type(bytes))
#     my_rsa = DRSA(bytes)

#     n, e = my_rsa.get_public_params()
#     publicKey = rsa.PublicKey(n, e)
#     print(n)
#     print(e)
#     n, e, d, p, q = my_rsa.get_private_params()
#     privateKey = rsa.PrivateKey(n, e, d, p, q)
#     print(n)
#     print(e)

#     # Export public key in PKCS#1 format, PEM encoded 
#     publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8') 
#     print(publicKeyPkcs1PEM)
#     # Export private key in PKCS#1 format, PEM encoded 
#     privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8') 
#     print(privateKeyPkcs1PEM)

#     # Save and load the PEM encoded keys as you like

#     # Import public key in PKCS#1 format, PEM encoded 
#     publicKeyReloaded = rsa.PublicKey.load_pkcs1(publicKeyPkcs1PEM.encode('utf8')) 
#     # Import private key in PKCS#1 format, PEM encoded 
#     privateKeyReloaded = rsa.PrivateKey.load_pkcs1(privateKeyPkcs1PEM.encode('utf8')) 

#     plaintext = "vinay kumar shukla".encode('utf8')
#     print("Plaintext: ", plaintext)

#     ciphertext = rsa.encrypt(plaintext, publicKeyReloaded)
#     print("Ciphertext: ", ciphertext)
    
#     decryptedMessage = rsa.decrypt(ciphertext, privateKeyReloaded)
#     print("Decrypted message: ", decryptedMessage)

def test_init():
    prbg = PRBG("abcdefg", "oi", 2)
    print(prbg.consufion_pattern)
    prbg.setup()
    
    bytes = bytearray([prbg.next_byte() for _ in range(512)])

    my_rsa = DRSA(bytes)

    n, e = my_rsa.get_public_params()
    print(f"Public params:\nn: {n}\ne: {e}")
    n, e, d, p, q = my_rsa.get_private_params()
    print(f"\n\nPrivate params:\nd: {d}\np: {p}\nq: {q}")

    publicKey = rsa.PublicKey(n, e)
    privateKey = rsa.PrivateKey(n, e, d, p, q)

    # Export public key in PKCS#1 format, PEM encoded 
    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8') 

    # Export private key in PKCS#1 format, PEM encoded 
    privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8')

    # Save the PEM encoded keys
    f_pub = open(f"test_pub_key.pem", "w")
    f_pub.write(publicKeyPkcs1PEM)
    os.chmod(f"test_pub_key.pem", 400)

    f_priv = open(f"test_priv_key.pem", "w")
    f_priv.write(privateKeyPkcs1PEM)
    f_priv.close()
    os.chmod(f"test_priv_key.pem", 400)

def test_stdout_java():
    import sys
    prbg = PRBG("ola", "o", 2)
    prbg.setup()
    for _ in range(512):
        sys.stdout.buffer.write(prbg.next_byte().item().to_bytes(1,byteorder='big'))

test_stdout_java() 
#test_init()
#test_rsa()
#test_rsa()
#test_cp()    
#test_prbg()