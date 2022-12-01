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
    keyword = keyword.upper()
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if plaintext[i].islower():
                ciphertext += chr(
                    ord("z")
                    - (ord("z") - ord(plaintext[i]) + ord("A") - ord(keyword[i % len(keyword)]))
                    % (ord("z") - (ord("a")) + 1)
                )
            else:
                ciphertext += chr(
                    ord("Z")
                    - (ord("Z") - ord(plaintext[i]) + ord("A") - ord(keyword[i % len(keyword)]))
                    % (ord("Z") - (ord("A")) + 1)
                )
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
    keyword = keyword.upper()
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if ciphertext[i].islower():
                plaintext += chr(
                    ord("z")
                    - (ord("z") - ord(ciphertext[i]) - ord("A") + ord(keyword[i % len(keyword)]))
                    % (ord("z") - (ord("a")) + 1)
                )
            else:
                plaintext += chr(
                    ord("Z")
                    - (ord("Z") - ord(ciphertext[i]) - ord("A") + ord(keyword[i % len(keyword)]))
                    % (ord("Z") - (ord("A")) + 1)
                )
        else:
            plaintext += ciphertext[i]
    return plaintext
