import requests
from bs4 import BeautifulSoup
import os

def remove_invalid_characters(url_link):
    """
    removes all invalid characters of the invalid_char_list in the url_link and returns it
    """
    invalid_char_list = ["www.", 'https://', '#', '%', '&', '{', '}', '\\', '*', '?', '/', ' ', '$',
                         "\'", '\"', ':', '@', '+', "`", '|', '=']
    cleaned_string = url_link
    for char in invalid_char_list:
        # replace() "returns" an altered string

        cleaned_string = cleaned_string.replace(char, "#")

    return cleaned_string
def sanitize_url(url):
    """
    makes an url ready to be saved by removing invalid characters
    """
    sanitized_url = remove_invalid_characters(url)
    sanitized_url = url.replace("https://", "").replace("/", "_").replace("www.", "")
    return sanitized_url

def get_correct_file_path_to_save(url_link, file_path):
    """
        input:
            url_link = link that is going to be accessed
            file_path = location to be saved on

        output:
            complete_path = a combination of url_ink and file_path, for the cached file to be saved on

    """
    sanitized_file_name_to_save = sanitize_url(url_link)
    if isinstance(file_path, str):
        complete_path = f"{file_path}{sanitized_file_name_to_save}.html" if file_path[-1] == '\\' else f"{file_path}/{sanitized_file_name_to_save}.html"
        return complete_path
    elif file_path is None:
        complete_path = f"{sanitized_file_name_to_save}.html"
        return complete_path
    else:
        if file_path is not None:
            raise Exception("you specified a wrong type!")



def get_cached_file(complete_path):
    try:
        with open(complete_path, "r") as cached_file:
            original_url = cached_file.readline().strip()  # Read the first line to get the original url
            html = cached_file.read()  # Read the rest of the file to get the HTML
            return original_url, html
    except Exception as e:
        raise Exception(f"something went wrong: {str(e)}")

def save_cached_file(complete_path, original_url, html_file):
    with open(complete_path, "w") as cached_file:
        cached_file.write(original_url + "\n")  # Write the original url on the first line
        cached_file.write(str(html_file))  # Write the HTML after the url
def get_or_save_cached_file_in_soup_format(url_link, file_path=None):
    """
        input:  url_link: link to get access
                file_path: the folder that you want to access to get/save the output_file
        output:
                output: beautiful_soup object in html.parser
    """
    complete_path = get_correct_file_path_to_save(url_link=url_link, file_path=file_path)
    print("complete_path = ", complete_path)

    if os.path.isfile(complete_path):
        original_url, html = get_cached_file(complete_path)
        webpage_soup = BeautifulSoup(html, "html.parser")
        return original_url, webpage_soup
    else:
        response = requests.get(url_link, allow_redirects=True)
        response.raise_for_status()  # Check if the request was successful
        html_text = response.text
        webpage_soup = BeautifulSoup(html_text, "html.parser")
        print(webpage_soup)
        save_cached_file(complete_path=complete_path, original_url=url_link, html_file=webpage_soup)
        return url_link, webpage_soup


url_link = "https://www.artificialintelligence-news.com/2023/06/14/european-parliament-adopts-ai-act-position/"
#url_link = "https://www.google.nl"
url_link = "https://www.unidis.nl"
link, webpage = get_or_save_cached_file_in_soup_format(url_link, "cached_files")

print(link)
print('hi')