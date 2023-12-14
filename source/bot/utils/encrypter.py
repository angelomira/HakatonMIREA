import hashlib
import random


def generate_and_encrypt_code():
    code_len = 6
    code = ''.join(random.choices('0123456789', k=code_len))

    encrypted_code = hashlib.sha256(code.encode()).hexdigest()

    return code, encrypted_code
