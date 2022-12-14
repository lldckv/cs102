"I'm a little string doc!"


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if plaintext[i].islower():
                ciphertext += chr(ord("z") - (ord("z") - ord(plaintext[i]) - shift) % (ord("z") - (ord("a")) + 1))
            else:
                ciphertext += chr(ord("Z") - (ord("Z") - ord(plaintext[i]) - shift) % (ord("Z") - (ord("A")) + 1))
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if ciphertext[i].islower():
                plaintext += chr(ord("z") - (ord("z") - ord(ciphertext[i]) + shift) % (ord("z") - (ord("a")) + 1))
            else:
                plaintext += chr(ord("Z") - (ord("Z") - ord(ciphertext[i]) + shift) % (ord("Z") - (ord("A")) + 1))
        else:
            plaintext += ciphertext[i]
    return plaintext
