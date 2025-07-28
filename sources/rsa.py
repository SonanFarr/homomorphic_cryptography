import random
from math import gcd

# Auxiliar Functions ==============================================================================================================================================>

def is_prime(n, k=5):
    """ Function used to test if a number is prime;

    Args:
        n (int): Number;
        k (int): Range;
    """
    
    if n <= 1:
        return False
    if n <= 3:
        return True
    
    d = n - 1
    r = 0
    
    while (d % 2 == 0):
        d //= 2
        r += 1
        
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        
        if (x == 1) or (x == (n - 1)):
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if (x == (n - 1)):
                break
        
        else:
            return False
        
    return True

def inv_mod(a, m):
    """ Funtion used to calculate de inv mod of a number;

    Args:
        a (int): Number;
        m (int): Module;
    """
    
    m0, x0, x1 = m, 0, 1
    
    while (a > 1):
        q = a // m
        a, m = m, a%m
        x0, x1 = x1 - (q * x0), x0
    
    return x1 % m0

def generate_keys(p, q, bits=8):
    """ Function used to generate the public and private keys;

    Args:
        bits (int): Number of bits of the keys;
    """
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2

    d = inv_mod(e, phi)
    
    keys = {'public': (n, e), 'private': (n, d), 'primes': (p, q)}
    
    return keys    
        
# Main Functions ==================================================================================================================================================>

def rsa_encrypt(clear_text, public_key):
    n, e = public_key
    cipher_text = pow(clear_text, e, n)
    return cipher_text

def rsa_decrypt(cipher_text, private_key):
    n, d = private_key
    clear_text = pow(cipher_text, d, n)
    return clear_text

def rsa_test(text_1, text_2, p, q):
    print("-> Gerando chaves RSA...")
    keys = generate_keys(p, q, 8)
    
    public_key = keys["public"]
    private_key = keys["private"]
    
    print("Chave pública: {}".format(public_key))
    print("Chave privada: {}".format(private_key))
    
    print("-> Encriptando mensagens...")
    
    cipher_1 = rsa_encrypt(text_1, public_key)
    cipher_2 = rsa_encrypt(text_2, public_key)
    
    print("Texto criptografado 1: {}".format(cipher_1))
    print("Texto criptografado 2: {}".format(cipher_2))
    
    print("-> Inciando teste da propriedade multiplicariva...")
    
    cipher_mult = (cipher_1 * cipher_2) % public_key[0]
    
    print("Textos claros: {} * {} = {}".format(text_1, text_2, text_1*text_2))
    print("Textos cifrados: {} * {} % {} = {}".format(cipher_1, cipher_2, public_key[0], cipher_mult))
    print("-> Descriptografando resultado da multiplicação dos textos cifrados...")
    
    clear_mult = rsa_decrypt(cipher_mult, private_key)
    
    print("Multiplicação descriptografada: {}".format(clear_mult))