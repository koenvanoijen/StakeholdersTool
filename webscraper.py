from bs4 import BeautifulSoup
import requests
import re
import Preprocess
import tf_idf
import csv
import os
def get_links_html(url):
    """
    parameter : link in string_format
    get all the links of a webpage
    returns only unique values in the list

    """
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data,features = 'lxml')
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

def similarity_check_query_with_linklist(query, link_list):
    """
    query is not yet preprocessed, it is given as a normal list
    input:
        query : the query to be compared with to get similarity score
        link_list: list of links that must explored
        origin_link:

    output:
        return: list of links with their respective similarity score to the query
    """

    weights = [1 for _ in query]
    results = list()

    for index, link in enumerate(link_list):
        preprocessed_text = fetch_important_text_in_link(link)

        if is_not_valid_html_text(preprocessed_text):
            continue #text skips vectorization to prevent error

        print(index, link, preprocessed_text)
        similarity_score = tf_idf.scoreAnalysis(tf_idf.cosine(preprocessed_text, query)[0], weights)
        print(index, link, similarity_score)
        results.append([similarity_score, link])


    return sorted(results, reverse= True)

def results_of_tf_idf_to_dict(results):
    data_dict = {
        "similarity_score": results[0],
        "url_link": results[1],
        "source_link": results[2],
        "outgoing_links_list": ["https://example.com/page2", "https://example.com/page3"],
        "webpage_vector": [0.1, 0.2, 0.3, 0.4]
    }
def create_csv_file(file_path):
    """
    Creates a CSV file with the specified columns.

    Args:
        file_path (str): File path of the CSV file.

    Returns:
        None
    """
    # Define the column names
    fieldnames = ["similarity_score", "url_link", "source_link", "outgoing_links_list", "webpage_vector"]

    # Create the CSV file with column names
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    print(f"CSV file '{file_path}' created successfully!")

def update_csv_file(file_path, data):
    """
    Updates the CSV file with new data. If CSV file does not exists, it will be created by invoking create_csv_file

    Args:
        file_path (str): File path of the CSV file.
        data (dict): Data to be written to the CSV file. Should be a dictionary with keys as column names and values
                     as data to be written. In form :["similarity_score", "url_link", "source_link", "outgoing_links_list", "webpage_vector"]

    Returns:
        None
    """
    # Check if the file path exists
    if not os.path.exists(file_path):
        create_csv_file(file_path)

    # Append new data to the CSV file
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        writer.writerow(data)
    print(f"Data updated in CSV file '{file_path}' successfully!")





if __name__ == "__main__":
    query_words = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation']

    origin_query = "https://en.wikipedia.org/wiki/Absorptive_capacity"
    outgoing_page_links = list(get_links_html(origin_query))
    #results_of_tf_idf_to_dict()
    print(similarity_check_query_with_linklist(query_words, outgoing_page_links ))
    #print(fetch_important_text_in_link('https://www.hellonewday.nl'))
    data_dict = {
        "similarity_score": 0.9,
        "url_link": "https://example.com/page1",
        "source_link": "https://example.com/",
        "outgoing_links_list": ["https://example.com/page2", "https://example.com/page3"],
        "webpage_vector": [0.1, 0.2, 0.3, 0.4]
    }
    #update_csv_file("data/similarity_data.csv",data_dict)