from cryptography.fernet import Fernet

_key = b'wt0UTaHS_qF92b5WYP5__zsrDoYdt8aU6rup6QOCOz8='
_instance = Fernet(_key)
def encrypt(s):
    encoded_s = str(s).encode()
    return _instance.encrypt(encoded_s).decode()

def decrypt(s):
    encoded_s = str(s).encode()
    return _instance.decrypt(encoded_s).decode()
