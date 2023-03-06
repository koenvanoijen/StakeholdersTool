import requests
from bs4 import BeautifulSoup

import Preprocess


def retrieveURL(url):
    webpage = requests.get(url)
    return webpage

#TO DO make this automaticaly find relevant URL's
def getURL():
     return "https://en.wikipedia.org/wiki/Absorptive_capacity"
    # return "https://www.hellonewday.nl/wat-is-absorptive-capacity/"

def getTitle(soup):
    return remove_html_tags(soup.find('title').text)

def getSubtitle(soup):
    return soup.find_all('h1')

def getSubsubtitle(soup):
    return soup.find_all('h2')

def getParagraphs(soup):
    return soup.find_all('p')

def cleanSoupList(listHTML):
    cleanarray = []
    for html in listHTML:
        cleanarray.append(remove_html_tags(html.text))
    return cleanarray

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #retrieve the relevant urls and clean them with beautifulSopu
    page = retrieveURL(getURL())
    soup = BeautifulSoup(page.content, "html.parser")
    cleantext = remove_html_tags(page.text)

    #Find all the relevant layers of text on a webpage
    title = [getTitle(soup)]
    subtitle = cleanSoupList(getSubtitle(soup))
    subsubtitle = cleanSoupList(getSubsubtitle(soup))
    paragraphs = cleanSoupList(getParagraphs(soup))
    website = title + subtitle + subsubtitle + paragraphs
    language = Preprocess.languageRecognizeProcess(website)
    website = " ".join(website)
    Preprocess.preproccess(website, language)


