"I'm a little string doc!"


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range(len(plaintext) - len(keyword)):
        keyword += keyword[i]
    keyword = keyword.upper()
    for i in range(len(plaintext)):
        if plaintext[i].islower() and plaintext[i].isalpha():
            if (ord(plaintext[i]) + (ord(keyword[i]) - ord("A"))) > ord("z"):
                ciphertext += chr(((ord(plaintext[i]) + (ord(keyword[i]) - ord("A"))) % ord("z")) + (ord("a")) - 1)
            else:
                ciphertext += chr(ord(plaintext[i]) + (ord(keyword[i]) - ord("A")))
        elif plaintext[i].isupper() and plaintext[i].isalpha():
            if (ord(plaintext[i]) + (ord(keyword[i]) - ord("A"))) > ord("Z"):
                ciphertext += chr(((ord(plaintext[i]) + (ord(keyword[i]) - ord("A"))) % ord("Z")) + (ord("A")) - 1)
            else:
                ciphertext += chr(ord(plaintext[i]) + (ord(keyword[i]) - ord("A")))
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range(len(ciphertext) - len(keyword)):
        keyword += keyword[i]
    keyword = keyword.upper()
    for i in range(len(ciphertext)):
        if ciphertext[i].islower() and ciphertext[i].isalpha():
            if (ord(ciphertext[i]) - (ord(keyword[i]) - ord("A"))) < ord("a"):
                plaintext += chr(ord("z") + 1 - (ord("a") - (ord(ciphertext[i]) - (ord(keyword[i]) - ord("A")))))
            else:
                plaintext += chr(ord(ciphertext[i]) - (ord(keyword[i]) - ord("A")))
        elif ciphertext[i].isupper() and ciphertext[i].isalpha():
            if (ord(ciphertext[i]) - (ord(keyword[i]) - ord("A"))) < ord("A"):
                plaintext += chr(ord("Z") + 1 - (ord("A") - (ord(ciphertext[i]) - (ord(keyword[i]) - ord("A")))))
            else:
                plaintext += chr(ord(ciphertext[i]) - (ord(keyword[i]) - ord("A")))
        else:
            plaintext += ciphertext[i]
    return plaintext
