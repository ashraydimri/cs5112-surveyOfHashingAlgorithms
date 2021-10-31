prime_a_const = 1627
prime_b_const = 28921
prime_c_const = 2473
prime_d_const = 47653

def hash1(word):
    hash = 0

    for c in word:
        hash = (hash * prime_a_const) + (ord(c) * prime_b_const)

    return hash

def hash2(word):
    hash = 0

    for c in word:
        hash = (hash * prime_b_const) + (ord(c) * prime_d_const)

    return hash
