import requests
from bs4 import BeautifulSoup

import NER

import Preprocess
import tf_idf


def retrieve_webpage(url):
    """
    url --> receive a url as string
    request webpage with url
    returns webpage which is a list of all data on webpage
    """
    webpage = requests.get(url)
    return webpage

#TO DO make this automaticaly find relevant URL's
def getURL():
    """
    returns one of webpages to test
    """
    return "https://en.wikipedia.org/wiki/Absorptive_capacity"
    # return "https://www.hellonewday.nl/wat-is-absorptive-capacity/"
    # return "https://www.hellonewday.nl/wieishellonewday/"
    # return "https://nos.nl/artikel/2466423-fc-den-bosch-ontslaat-trainer-de-gier-na-recordnederlaag-van-13-0"
    # return "https://www.infratech.nl/over-infratech/nieuws/exposanten/-groot-variabel-onderhoud-hoofdwegennet-wnz-2019-voor-vermeulen-groep"
    #return "https://www.dispuutbrut.nl/"


def cleanSoupList(listHTML):
    """"

    """
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
    page = retrieve_webpage(getURL())
    soup = BeautifulSoup(page.text, "html.parser")

    html_tags = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'p']
    #Find all text that is between relevant html tags and then remove the tags
    website = [remove_html_tags(tag.text) for tag in soup.find_all() if tag.name in html_tags]
    print(website)

    # Recognize the language of the text
    is_language_dutch = Preprocess.languageRecognizeProcess(website)
    print("Dutch = ", is_language_dutch)
    website = " ".join(website)
    text = Preprocess.preproccess(website, is_language_dutch) #text is received as list of words


    query = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation'] ##relevant query
    # query = ['trein', 'brein', 'onderwerp, schakel, raden', 'jargon'] # bullshit query
    query = [" ".join(Preprocess.preproccess(i, True)) for i in query]
    # Create the possibility to give weights to certain search queries
    # for now set all the weights to 1
    weights = [1 for i in query]

    tf_idf.occurranceMatching(text, query)
    text = " ".join(text)  #text to single string

    #NER.predictPerson(website)
    similarity_score = tf_idf.scoreAnalysis(tf_idf.cosine(text, query), weights)
    print(similarity_score)



