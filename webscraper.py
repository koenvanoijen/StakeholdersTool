from bs4 import BeautifulSoup
import requests

def get_links_html(url):
    """
    parameter : link in string_format
    get all the links of a webpage
    returns only unique values in the list

    """
    page = requests.get(url)
    data = page.text
    print(page.text)
    soup = BeautifulSoup(data,features = 'lxml') #features = xml was op basis van advies van de console om foutmelding weg te halen
    links = list()
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    return set(link for link in links if 'https' in link)

print(len(get_links_html("https://hellonewday.nl")))


