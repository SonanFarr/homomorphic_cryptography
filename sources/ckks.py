import tenseal as ts

# Auxiliar Functions ==============================================================================================================================================>

def ckks_context():
    # Parâmetros:
    poly_mod_degree = 8192                  # Grau do polinômio;
    coeff_mod_bit_sizes = [60, 40, 40, 60]  # Tamanho dos módulos dos coeficientes;

    # Escala usada para codificar números reais:
    scale = 2**40

    # Criação do contexto com esses parâmetros:
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=poly_mod_degree,
        coeff_mod_bit_sizes=coeff_mod_bit_sizes
    )
    context.generate_galois_keys()
    context.global_scale = scale

    return context

# Main Functions ==================================================================================================================================================>

def ckks_encrypt(context, clear_data):
    cipher_data = ts.ckks_vector(context, clear_data)
    return cipher_data

def ckks_decrypt(cipher_data, context):
    decrypted = cipher_data.decrypt()
    return decrypted[0]
    
def ckks_test(text_1, text_2):
    print("-> Criando contexto CKKS...")
    
    context = ckks_context()
    text_1 = [text_1]
    text_2 = [text_2]
    
    print("-> Encriptando mensagens...")
    
    cipher_1 = ckks_encrypt(context, text_1)
    cipher_2 = ckks_encrypt(context, text_2)
    
    print("Mensagens criptografadas")
    print("-> Inciando teste da propriedade aditiva...")
    
    cipher_sum = cipher_1 + cipher_2
    
    print("Textos claros: {} + {} = {}".format(text_1, text_2, text_1[0]+text_2[0]))
    print("Textos cifrados: {}".format(ckks_decrypt(cipher_sum, context)))
    
    print("-> Inciando teste da propriedade multiplicativa...")
    
    cipher_mult = cipher_1 * cipher_2
    
    print("Textos claros: {} * {} = {}".format(text_1, text_2, text_1[0]*text_2[0]))
    print("Textos cifrados: {}".format(ckks_decrypt(cipher_mult, context)))