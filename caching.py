import requests
from bs4 import BeautifulSoup
import os

def remove_https(url_link):
    return url_link.replace("https://", "")

def get_correct_file_path_to_save(url_link, file_path):
    file_name_to_save = remove_https(url_link)
    if isinstance(file_path, str):
        complete_path = f"{file_path}{file_name_to_save}.html"if file_path[-1] == '/' else f"{file_path}/{file_name_to_save}.html"
        return complete_path
    elif file_path is None:
        complete_path = f"{file_name_to_save}.html"
        return complete_path
    else:
        if file_path is not None:
            raise Exception("you specified a wrong type!")
            return

def get_cached_file(complete_path):
    try:
        with open(complete_path, "r") as cached_file:
            return cached_file.read()
    except typeerror:
        raise Exception("something went wrong")


def save_cached_file(complete_path, html_file):
    with open(complete_path, "w") as cached_file:
        cached_file.write(html_file)


def get_or_save_cached_file_in_soup_format(url_link, file_path = None):
    """
        input:  url_link: link to get the souphtml from
                file_path: the folder that you want to access to get/save the output_file
        output:
                output: beautiful_soup object in html.parser
    """
    complete_path = get_correct_file_path_to_save(url_link=url_link, file_path=file_path)
    print("complete_path = ", complete_path)

    if os.path.isfile(complete_path):
        return get_cached_file(complete_path)
    else:
        html_text = requests.get(url_link, allow_redirects=True)
        webpage_soup = BeautifulSoup(html_text.text, "html.parser")
        print(webpage_soup)
        save_cached_file(complete_path=complete_path, html_file=webpage_soup)
        return webpage_soup


get_or_save_cached_file_in_soup_format('https://www.blog.goenvy.io/10-best-ai-marketing-blogs-you-should-follow', "cached_files")