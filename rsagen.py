import argparse
import sys
from drsa import DRSA
import rsa
import os

def main():
    '''
    This application implements the DRSA module.
    It receives the first N pseudo-random bytes from the stdin, which are used
    to generate deterministic private and public parameters for an RSA key.
    The parameters are then used to convert the key pair to the PEM format,
    using an external library (rsa). The keys are then exported to a file with the
    given name.
    '''

    # Argument parser
    parser = argparse.ArgumentParser(description='Deterministic RSA key generation (D-RSA): rsagen')
    parser.add_argument('kn', type=str, help='key name')
    args = parser.parse_args()

    # Read bytes from stdin
    seed = sys.stdin.buffer.read()

    # Retrieve key name from user args
    key_name = args.kn

    # DRSA instance and retrieve parameters
    my_rsa = DRSA(seed)

    # Create PublicKey object to export to PEM, from
    # params calculated by DRSA
    n, e = my_rsa.get_public_params()
    publicKey = rsa.PublicKey(n, e)

    # Create PrivateKey object to export to PEM, from
    # params calculated by DRSA
    n, e, d, p, q = my_rsa.get_private_params()
    privateKey = rsa.PrivateKey(n, e, d, p, q)

    # Export public key in PKCS#1 format, PEM encoded 
    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8') 

    # Export private key in PKCS#1 format, PEM encoded 
    privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8')

    # Save the PEM encoded keys
    f_pub = open(f"{key_name}_pub_key.pem", "w")
    f_pub.write(publicKeyPkcs1PEM)
    #os.chmod(f"{key_name}_pub_key.pem", 400) # Give appropriate permissions

    f_priv = open(f"{key_name}_priv_key.pem", "w")
    f_priv.write(privateKeyPkcs1PEM)
    f_priv.close()
    #os.chmod(f"{key_name}_priv_key.pem", 400) # Give appropriate permissions

if __name__ == "__main__":
    main()