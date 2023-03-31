from bs4 import BeautifulSoup
import requests
import re
import Preprocess
import tf_idf
import csv
def get_links_html(url):
    """
    parameter : link in string_format
    get all the links of a webpage
    returns only unique values in the list

    """
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data,features = 'lxml') #features = xml was op basis van advies van de console om foutmelding weg te halen
    links = list()
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    return set(link for link in links if 'https' in link)

def retrieve_webpage(url):
    """
    input: url --> receive a url as string
    output: returns webpage which is a list of all data on webpage
    """
    webpage = requests.get(url)
    return webpage

def remove_html_tags(text):

    """
    input: string of html line
    return: strRemove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def filter_text_in_html(soup_text):
    """
    input: soup_variable of webpage
    output: returns only relevant text
            that is in between wanted_html_tags without the tags itself
    """
    wanted_html_tags = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'p']
    return [remove_html_tags(tag.text) for tag in soup_text.find_all() if tag.name in wanted_html_tags]

def fetch_important_text_in_link(link):
    """
    input: link = url string
    output: return preprocessed text in the html page of link
    """
    webpage = retrieve_webpage(link)
    webpage_soup = BeautifulSoup(webpage.text, "html.parser")
    text_in_website = filter_text_in_html(webpage_soup)
    text_preprocessed = Preprocess.preproccess(text_in_website)
    text_preprocessed_joined = " ".join(text_preprocessed)
    return text_preprocessed_joined

def is_not_valid_html_text(text):
    """input:
        preprocessed text that should only contain text
    output:
        boolean: True if the text is NOT valid for using in vectorization
    """
    if len(text) < 10:
        return True

def similarity_query_links(link_list):
    """
    input:
        link_list: list of links that must explored

    output:
        return: list of links with their respective similarity score to the query
    """
    query = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation']
    query_preprocessed = [" ".join(Preprocess.preproccess(word, False)) for word in query]
    weights = [1 for _ in query]
    results = list()
    for index, link in enumerate(link_list):
        preprocessed_text = fetch_important_text_in_link(link)

        if is_not_valid_html_text(preprocessed_text):
            continue #text skips vectorization

        print(index, link, preprocessed_text)
        similarity_score = tf_idf.scoreAnalysis(tf_idf.cosine(preprocessed_text, query), weights)
        print(index, link, similarity_score)
        results.append([similarity_score, link])


    return sorted(results, reverse= True)

def write_csv(similarity_link_results_list):
    """
    input:
        list of all similarity score and respective link
    saves results of the list in csv file
    """
    try:
        with open("results.csv", "w") as output_file:
            writer = csv.writer(output_file)
            header = ["similarity_score", "url_link"]
            writer.writerow(header)
            writer.writerow(similarity_link_results_list)
            for row in similarity_link_results_list:
                pass


    except:
        print('something went wrong with writing the file')





if __name__ == "__main__":
    page_links = list(get_links_html("https://en.wikipedia.org/wiki/Absorptive_capacity"))
    print(similarity_query_links(page_links))
    #print(fetch_important_text_in_link('https://www.hellonewday.nl'))
    write_csv(page_links)