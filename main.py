import requests
from bs4 import BeautifulSoup

#import NER
import Preprocess
import tf_idf


def retrieveURL(url):
    webpage = requests.get(url)
    return webpage

#TO DO make this automaticaly find relevant URL's
def getURL():
    # return "https://en.wikipedia.org/wiki/Absorptive_capacity"
    return "https://www.hellonewday.nl/wat-is-absorptive-capacity/"
    # return "https://www.hellonewday.nl/wieishellonewday/"
    # return "https://nos.nl/artikel/2466423-fc-den-bosch-ontslaat-trainer-de-gier-na-recordnederlaag-van-13-0"
    # return "https://www.infratech.nl/over-infratech/nieuws/exposanten/-groot-variabel-onderhoud-hoofdwegennet-wnz-2019-voor-vermeulen-groep"

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
    # retrieve the relevant urls and clean them with beautifulSoup
    page = retrieveURL(getURL())
    soup = BeautifulSoup(page.content, "html.parser")

    #Find all text that is between relevant html tags and then remove the tags
    website = [remove_html_tags(tag.text) for tag in soup.find_all() if tag.name in ['title', 'h1', 'h2', 'p']]

    # Recognize the language of the text
    language = Preprocess.languageRecognizeProcess(website)
    print("Dutch = ", language)
    website = " ".join(website)
    text = Preprocess.preproccess(website, language)
    text = " ".join(text)
    query = 'absorptive capacity, assimilatie'
    query = Preprocess.preproccess(query, True)
    print(query)
    query = ['absorptiv capacity', 'transformatie']
    tf_idf.cosine(text, query)
    #NER.predictPerson(website)



