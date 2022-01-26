import datetime
import os


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


if __name__ == "__main__":
    pass
