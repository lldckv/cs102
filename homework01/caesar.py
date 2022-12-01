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
        if plaintext[i].islower() and plaintext[i].isalpha():
            if (ord(plaintext[i]) + shift) > ord("z"):
                ciphertext += chr(((ord(plaintext[i]) + shift) % ord("z")) + (ord("a")) - 1)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift)
        elif plaintext[i].isupper() and plaintext[i].isalpha():
            if (ord(plaintext[i]) + shift) > ord("Z"):
                ciphertext += chr(((ord(plaintext[i]) + shift) % ord("Z")) + (ord("A")) - 1)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift)
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
        if ciphertext[i].islower() and ciphertext[i].isalpha():
            if (ord(ciphertext[i]) - shift) < ord("a"):
                plaintext += chr(ord("z") + 1 - (ord("a") - (ord(ciphertext[i]) - shift)))
            else:
                plaintext += chr(ord(ciphertext[i]) - shift)
        elif ciphertext[i].isupper() and ciphertext[i].isalpha():
            if (ord(ciphertext[i]) - shift) < ord("A"):
                plaintext += chr(ord("Z") + 1 - (ord("A") - (ord(ciphertext[i]) - shift)))
            else:
                plaintext += chr(ord(ciphertext[i]) - shift)
        else:
            plaintext += ciphertext[i]
    return plaintext