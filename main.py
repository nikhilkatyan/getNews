import glob
import os.path
import sys
import time

import requests
from bs4 import BeautifulSoup

import nkk_tools as nkk
import send_email as email


class CreateSoup:
    def __init__(self, passed_url):
        self.url = passed_url
        self.response = requests.get(self.url)
        self.html = self.response.content
        self.soup = BeautifulSoup(self.html, "html.parser")

    def get_soup(self):
        return self.soup


def return_urls():
    urls = ["http://www.tricitytoday.com/greater-noida",
            "https://tricitytoday.com/greater-noida-west",
            "https://tricitytoday.com/noida",
            "https://tricitytoday.com/ghaziabad",
            "https://tricitytoday.com/delhi-ncr",
            "https://tricitytoday.com/uttar-pradesh"
            ]
    return urls


def get_headlines_from_main_page(received_url):
    soup_url = CreateSoup(received_url).get_soup()
    abc = soup_url.find_all("div", {"class": "list"})
    headings_tri = []

    for ab in abc:
        headings_tri.append(ab.p.a["href"])
        # print(ab.p.a["title"])
        # print(ab.img["data-src"])
        # print("\n")

    if len(headings_tri) > 0:
        return headings_tri
    else:
        return False


def news_from_headings_tri(heading_url, news_tag):
    content_from_heading_page = CreateSoup(heading_url).get_soup()
    title = content_from_heading_page.find("h1", {"class": "title"}).text
    img_src = content_from_heading_page.find("picture").img["data-src"]
    section = content_from_heading_page.find("section").text
    timestamp = content_from_heading_page.find("div", {"class": "timestamp"}).text
    # print(title)
    # print(img_src)
    # print(timestamp)
    # print(section.replace("/t/n", ""))
    main_content = title + "\n\n" + timestamp + "\n\n" + img_src + "\n\n" + section

    receiver_email = nkk.read_email_id()

    # NKK : Create file with image name inside date folder with content
    file_name_to_save = str(img_src.split("/")[-1].split(".")[0]) + ".txt"
    folder_name = nkk.check_make_folder()
    file_name_with_path = os.path.join(os.getcwd(), folder_name, file_name_to_save)

    # NKK : Check if file already exists in any of child folder
    print(title)
    file_found = glob.glob(os.getcwd() + "/**/" + file_name_to_save, recursive=True)
    # print(file_found)

    if len(file_found) == 0:
        nkk.write_to_file_and_save(file_name_with_path, main_content)
        print("File created.")
        email.send_attach_email(title[0:60], file_name_with_path, file_name_to_save, news_tag,
                                receiver_email)
        print("Email sent.\n")
    else:
        print("File already exists.\n")


def main():
    url_list = return_urls()
    tag = ''
    for url in url_list:
        # url_tri_g_noida = "http://www.tricitytoday.com/greater-noida"
        url_index = url_list.index(url)
        if url_index == 0:
            tag = "Greater Noida"
        elif url_index == 1:
            tag = "Greater Noida West"
        elif url_index == 2:
            tag = "Noida"
        elif url_index == 3:
            tag = "Ghaziabad"
        elif url_index == 4:
            tag = "Delhi NCR"
        elif url_index == 5:
            tag = "Uttar Pradesh"
        # Headings from TriCity online portal
        headings_tri_city = get_headlines_from_main_page(url)
        if headings_tri_city:
            for headings in headings_tri_city:
                # further news from Headings pulled earlier
                news_from_headings_tri(headings, tag)
    input("\nCheck mailbox.\nPress any key to exit...")


if __name__ == '__main__':
    # email id to send content
    nkk.check_email_exists()

    # confirm if ready to proceed
    confirmation = str(input('Do you want to fetch news. y/N : '))
    if confirmation == confirmation.lower() == "y":
        main()
    # c to change email id
    elif confirmation == confirmation.lower() == "change_email":
        ask_email_id = str(input("enter id : "))
        # Change email id only if valid
        if nkk.check_passcode():
            if nkk.validate_email_id(ask_email_id):
                nkk.write_email_id(ask_email_id)
                # Confirmation again after changing email id
                confirmation_again = str(input('Do you want to fetch news. y/N : '))
                if confirmation_again == confirmation_again.lower() == "y":
                    main()
    elif confirmation == confirmation.lower() == "check_email":
        print(nkk.read_email_id())
        # Confirmation again after changing email id
        confirmation_again = str(input('Do you want to fetch news. y/N : '))
        if confirmation_again == confirmation_again.lower() == "y":
            main()
    else:
        print("exiting...")
        time.sleep(1)
        sys.exit()
