import datetime
import os
import re

import cryptography
import pyautogui

import encrypt_data

# publicKey, privateKey = rsa.newkeys(512)
#
#
# def encrypt_email_id(message: str):
#     encrypt_message = rsa.encrypt(message.encode(), publicKey)
#     print(type(encrypt_message))
#     return encrypt_message
#
#
# def decrypt_email_id(encrypted_msg):
#     decrypted_message = rsa.decrypt(encrypted_msg, privateKey).decode()
#     return decrypted_message
master_email_id = "newsdiarytoday@gmail.com"


def check_make_folder():
    folder_name = (str(datetime.datetime.today()).split()[0])
    if not os.path.exists(os.path.join(os.getcwd(), folder_name)):
        os.makedirs(folder_name)
    return folder_name


def write_to_file_and_save(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    f.close()
    return True


def validate_email_id(email_id: str):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email_id):
        # print("Valid email")
        return True
    else:
        print("Invalid id")
        return False


def write_email_id(email_id: str):
    # remove space if provided with email id
    email_id.replace(" ", "")

    # validate if email id format is correct
    if validate_email_id(email_id):
        # encrypt email id to get it saved in file, encoding is must(only bytes can be encrypted not string).
        encrypted_content = encrypt_data.enc(email_id)
        file_name_to_save = "send.dat"
        file_name_with_path = os.path.join(os.getcwd(), file_name_to_save)
        with open(file_name_with_path, "wb") as file:
            file.write(encrypted_content)
        file.close()
        print("success.")


def check_email_exists():
    if not os.path.exists(os.path.join(os.getcwd(), "send.dat")):
        write_email_id("newsdiarytoday@gmail.com")


def read_email_id() -> str:
    check_email_exists()

    email_dat_file = open(os.path.join(os.getcwd(), "send.dat"), "r")
    # email id mentioned in file is encrypted, will decrypt while returning
    email_id_mentioned_in_dat_file = email_dat_file.readline()
    email_dat_file.close()

    # .encode() required as it needs to be converted to bytes before decrypting
    decrypted_email_id = (encrypt_data.dec(email_id_mentioned_in_dat_file.encode())).decode("utf-8")

    return decrypted_email_id


def check_passcode() -> bool:
    pass_code = pyautogui.password(text='Enter passcode to change id.', title='Enter passcode', default='', mask='*')
    if pass_code == "nikhil":
        return True
    else:
        input("Wrong passcode. Press any key to exit...")
        return False


if __name__ == "__main__":
    # write_email_id("nikhilkatyan@gmail.com")
    # print(read_email_id())
    pass
