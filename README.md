
# Deterministic RSA (DRSA)

A DRSA module capable of generating deterministic keys and a PNBG (Pseudo-Random Byte Generator) done with Python.



## Documentation

Complete documentation in the HTML format built with [Sphinx](https://www.sphinx-doc.org/en/master/) can be found in `docs/build/html/index.html`. 

## Installation

Create a Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required requirements:
```bash
python3 -m pip install -r requirements.txt
```

These external libraries are used to:
- Draw charts and images for statistical purposes (Pillow and matplotlib).
- Export the RSA generated keys to the PEM format (rsa).
- Force Python int/long to be limited to 64bit (similar to Java long primitive type) (numpy).
- Optimization of the computations (numpy).

The implemented functionality and logic is not dependent on these libraries.
    
## Usage/Examples

### randgen

The randgen module can be used to:
- Perform benchmarking tests on the PRBG setup (may take a long time)
- Output a given ammount of pseudo-random bytes, according to the password, confusion string an iteration count parameters provided.

#### Benchmarking

The program will perform 21 setups of the PRBG for each combination of confusion string size [1-3] / iteration count [1, 5, 10, 20, 50, 100, 200].
The statistical outputs will be saved in the `statistics/` folder.

To perform benchmarking, run:

```bash
python3 randgen.py --benchmark
```

#### Output pseudo-random bytes

Run:

```bash
python3 randgen.py --pwd <your_password> --cs <your_confusion_string> --ic <your_iteration_count> --nob <number_of_bytes>
```

The generator will be setted up according to your parameters, which will influence the setup time. After the setup, the bytes will be outputed through the stdout.
To output an infinite sequence of pseudo-random bytes, choose `--nob -1`.

### rsagen

The rsagen module implements the DRSA module, giving it pseudo-random bytes as it's input through stdin and later exporting the resulting DRSA key parameters to the PEM format.

To use it, we can first generate some pseudo-random bytes using the randgen module and then feed it's output to rsagen.

For example, the following commands:
```bash
python3 randgen.py --pwd ola --cs o --ic 2 --nob 512 > 512_random_bytes
python3 rsagen.py python_512 < 512_random_bytes
```

Will save a 4096bit RSA key pair to the files `python_512_pub_key.pem` and `python_512_priv_key.pem`, as the ones below:

```bash
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
```

```bash
-----BEGIN RSA PUBLIC KEY-----
MIICCgKCAgEAuN4IBvRZvVxw3bj/0nzKUMMhganHabrolqLUSnwKhqtKyLGPEzaf
3W8sKWpclGgY1QRL9fd4BVQrMjc1YcG3rJzKg8K5n6GQrNgCxh7XmxTLk406sxgG
7lbH+9ARjS87aootL7abH2u6Or4fTRoXHuUl3DB2yitIwd2Ly0geISi+8jycOEh2
E2X1c3mnJ5W/7dt9eBWGmoLf2mXq0F1eLAWVsGxxiCPwPrRL/v0lU4MBNGsNcw1r
7DCjvTNV7jrampHN+CuOvr76/eKfXHmekt9AzBO9ml6fTmBlQXbvZS/58jt0ZcJk
x1Xerdbcejk2S3Q8RZ57r7Z2r7jp88CU/wi3p9qYEllxf+n4/lWfpVt9i9NAzESU
Ry6GJDqGjlCalistvOcrMJ+1gSYb4dCEO35dseRiKWzlOSGziO5I/hwIwsBP3Ahu
bqYGcUQrKPK1qfvA26T8j0PV52E6dRmC1ye4Hh7dJqWm596XS5XY9b7OFIFlraCx
1l8CN93T0KfUc3vIE+Dk9IT7okT6OhrgFnpw+NWSbsninytoJHFZPxHTLEMTrBwl
kNB/icfuGpeTlOm5y5CCWiN8A3+6w+5eZYsJwr76IC+mPrfFIk7heyGiqe0pLe7+
44tmD8y94UhSmsOy/laKtxi7kdgvQQlezID70Jk23U9b8RLrrnvNFKECAwEAAQ==
-----END RSA PUBLIC KEY-----
```

In this case the `rsagen.py` execution was feeded with the `randgen.py` outputed pseudo-bytes, but any source of randomness can be tested through the stdin.

The produced private RSA key can be checked with the following command:
```bash
openssl rsa -check -noout -in python_512_priv_key.pem -text
```
## Authors

- [Duarte Mortágua - 92963](mailto:duarte.ntm@ua.pt)

