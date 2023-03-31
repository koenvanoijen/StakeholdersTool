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
def get_URL():
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

def filter_text_in_html(soup_text):
    """
    returns only relevant text that is in between wanted_html_tags without the tags itself
    """
    wanted_html_tags = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'p']
    return [remove_html_tags(tag.text) for tag in soup_text.find_all() if tag.name in wanted_html_tags]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # retrieve the relevant urls and clean them with beautifulSoup
    page = retrieve_webpage(get_URL())
    soup = BeautifulSoup(page.text, "html.parser")


    website = filter_text_in_html(soup)
    print("website",website)

    text = Preprocess.preproccess(website)


    query = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation'] ##relevant query
    # query = ['trein', 'brein', 'onderwerp, schakel, raden', 'jargon'] # bullshit query
    query = [" ".join(Preprocess.preproccess(word, False)) for word in query]
    # Create the possibility to give weights to certain search queries
    # for now set all the weights to 1
    weights = [1 for i in query]

    tf_idf.occurrance_matching(text, query)
    text = " ".join(text)  #text to single string

    #NER.predictPerson(website)
    similarity_score = tf_idf.scoreAnalysis(tf_idf.cosine(text, query), weights)
    print(similarity_score)



