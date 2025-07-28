import random
import math

# Auxiliar Functions ==============================================================================================================================================>

def mmc(a, b):
    """ Function used to calculate th mmc of two numbers;

    Args:
        a (int): Number a;
        b (int): Number b;
    """
    
    return abs(a * b) // math.gcd(a, b)

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

def L(u, n):
    return (u - 1) // n

def generate_keys(p, q, bits=8):
    """ Function used to generate the public and private keys;

    Args:
        bits (int): Number of bits of the keys;
    """
    
    n = p * q
    nsquare = n * n
    λ = mmc(p - 1, q - 1)
    g = n + 1
    
    x = pow(g, λ, nsquare)
    μ = inv_mod(L(x, n), n)
    
    keys = {'public': (n, g), 'private': (λ, μ), 'nsquare': nsquare}
    
    return keys

# Main Functions ==================================================================================================================================================>

def paillier_encrypt(clear_text, public_key, nsquare):
    n, g = public_key
    r = random.randint(1, n - 1)
    while math.gcd(r, n) != 1:
        r = random.randint(1, n - 1)
    
    cipher_text = (pow(g, clear_text, nsquare) * pow(r, n, nsquare)) % nsquare
    return cipher_text

def paillier_decrypt(cipher_text, private_keykey, public_key, nsquare):
    λ, μ = private_keykey
    n, g = public_key
    x = pow(cipher_text, λ, nsquare)
    l_val = L(x, n)
    
    clear_text = (l_val * μ) % n
    return clear_text

def paillier_test(text_1, text_2, p, q):
    print("-> Gerando chaves Paillier...")
    keys = generate_keys(p, q, 8)
    
    public_key = keys["public"]
    private_key = keys["private"]
    nsquare = keys["nsquare"]
    
    print("Chave pública: {}".format(public_key))
    print("Chave privada: {}".format(private_key))
    
    print("-> Encriptando mensagens...")
    
    cipher_1 = paillier_encrypt(text_1, public_key, nsquare)
    cipher_2 = paillier_encrypt(text_2, public_key, nsquare)
    
    print("Texto criptografado 1: {}".format(cipher_1))
    print("Texto criptografado 2: {}".format(cipher_2))
    
    print("-> Inciando teste da propriedade aditiva...")
    
    cipher_add = (cipher_1 * cipher_2) % nsquare
    
    print("Textos claros: {} + {} = {}".format(text_1, text_2, text_1+text_2))
    print("Textos cifrados: {} * {} % {} = {}".format(cipher_1, cipher_2, nsquare, cipher_add))
    print("-> Descriptografando resultado da multiplicação dos textos cifrados...")
    
    clear_mult = paillier_decrypt(cipher_add, private_key, public_key, nsquare)
    
    print("Adição descriptografada: {}".format(clear_mult))