from sources.rsa import rsa_test
from sources.paillier import paillier_test

if __name__ == "__main__":
    text_1 = 5
    text_2 = 7
    
    p = 61
    q = 53
    
    rsa_test(text_1, text_2, p, q)
    print("------------------------------------------------------------")
    paillier_test(text_1, text_2, p, q)