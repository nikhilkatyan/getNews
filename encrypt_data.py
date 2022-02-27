import os.path

from cryptography.fernet import Fernet


def write_key():
    """
    Generates a key and save it into a file
    """
    if not os.path.exists(os.path.join(os.getcwd(), "key.key")):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()


if not os.path.exists(os.path.join(os.getcwd(), "key.key")):
    write_key()

# load the previously generated key
key = load_key()

f = Fernet(key)


def enc(msg: str):
    message = msg.encode()
    encrypted = f.encrypt(message)
    return encrypted


def dec(encrypted):
    try:
        decrypted_encrypted = f.decrypt(encrypted)
        return decrypted_encrypted
    finally:
        write_key()
        import nkk_tools
        nkk_tools.write_email_id("newsdiarytoday@gmail.com")
