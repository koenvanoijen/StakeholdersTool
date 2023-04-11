from bs4 import BeautifulSoup
import requests
import re
import Preprocess
import tf_idf
import csv_writer
import urllib
import url_determiner

def get_links_html(url):
    """
    parameter : link in string_format --> this is the source url
    output:
        return all the links on the webpage in a set

    """
    page = requests.get(url, allow_redirects=True)
    source_url = page.url
    data = page.text
    soup = BeautifulSoup(data,features = 'lxml')
    links = set()


    for link in soup.find_all('a', href = True):

        url_link = link.get('href')
        url_link_final_redirect = url_determiner.get_correct_url(source_url=source_url, target_url=url_link )

        if "https" in url_link_final_redirect:
            links.add(url_link_final_redirect)
    print(str(links))
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

def fetch_important_text_in_webpage(link):
    """
    input: link = url string
    output: return preprocessed text in the html page of link
    """
    try:
        webpage = retrieve_webpage(link)
        webpage_soup = BeautifulSoup(webpage.text, "html.parser")
        text_in_website = filter_text_in_html(webpage_soup)
        text_preprocessed = Preprocess.preproccess(text_in_website)
        text_preprocessed_joined = " ".join(text_preprocessed)
        return text_preprocessed_joined
    except:
        return ""

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
        preprocessed_text = fetch_important_text_in_webpage(link)

        if is_not_valid_html_text(preprocessed_text):
            continue #text skips vectorization to prevent error

        similarity_score = tf_idf.scoreAnalysis(tf_idf.cosine(preprocessed_text, query)[0], weights)
        results.append((similarity_score, link))


    return sorted(results, reverse= True)

def results_of_tf_idf_to_dict(similarity_score, page_url, parent_url,out_going_links_set, out_going_links_list_with_similarity, webpage_vector, query_list):
    data_dict = {
        "similarity_score": similarity_score,
        "url_link": page_url,
        "parent_url": parent_url,
        "out_going_links_set": out_going_links_set,
        "out_going_links_list_with_similarity": out_going_links_list_with_similarity,
        "webpage_vector": webpage_vector,
        "query": query_list
    }
    return data_dict


def execution_web_page_one_loop_cycle(query, link_to_check,file_path, parent_url = 'None', write_to_csv = True):
    """
    task:
        perform the similarity test with the query and the text. It outputs the results in a dictionairy shape

        input:
            query = words to be vectorized and compared with text on url's html page
            link_to_check = link to be evaluated
            file_path = location and filename ot be saved e.g. similarity_data.csv or users/mehdi/data/similarity_data.csv
            parent_url = url where link_to_check came from, if not specified it gives as argument "None" as string
            write_to_csv = write to the csv file default is true

        output:
            return: results_dict containing of one webpage
                                        - similarity_score_text_query,
                                        - page_url=link_to_check
                                        - parent_url=parent_url,
                                        - out_going_links_set = only the link of similarity_link_list,
                                        - out_going_link_list_with_similarity= similarity_link_list,
                                        - webpage_vector= text_vector,
                                        - query_list= query)
                    return "link_unvalid" if the preproccesed_text is not valid with is_not_valid_html_text

    """
    # Create the possibility to give weights to certain search queries
    # for now set all the weights to 1
    weights = [1 for i in query]
    preprocessed_text = fetch_important_text_in_webpage(link_to_check)
    if is_not_valid_html_text(preprocessed_text):
        return "link_unvalid" #continue  # text skips vectorization to prevent error

    cosine_similarity_text_and_query, text_vector = tf_idf.cosine(preprocessed_text, query)
    similarity_score_text_query = tf_idf.scoreAnalysis(cosine_similarity_text_and_query, weights)
    link_list= list(get_links_html(link_to_check))
    similarity_link_list = similarity_check_query_with_linklist(query,link_list)
    results_dict = results_of_tf_idf_to_dict(similarity_score=similarity_score_text_query,
                                             page_url=link_to_check, parent_url=parent_url,
                                             out_going_links_set = set(link[1] for link in similarity_link_list),
                                             out_going_links_list_with_similarity= similarity_link_list,
                                             webpage_vector= text_vector,
                                             query_list= query)
    if write_to_csv:
        csv_writer.update_csv_file(file_path=file_path, data=results_dict)
    return results_dict


def filter_new_paths_threshold(link_list_similarity_score, threshold = 0.4):
    """
        input:
            link_list_similarity_score = which should be the similaritylinklist created by similarity_check_query_with_linklist
            threshold = the minimum similarity_score, default is set to 0.4

        output:
            link_list and similarity score that is at least the threshold
    """
    explorable_links_similarity = list()
    for similarity_score, url in link_list_similarity_score:
        if similarity_score > threshold:
            explorable_links_similarity.append((similarity_score, url))

    return explorable_links_similarity


def loop_through_webpages(query, file_path, url_link):
    """
    iterates over the links in the web_page then it does a similarity check with the query and the new webpages
    input:
        query = list of words to compare with html text in url_link
        file_path = location and filename ot be saved e.g. similarity_data.csv or users/mehdi/data/similarity_data.csv
        url_link = link of which text should be evaluated

    output:
        similarity_dict
    """
    similarity_dict_one_page = execution_web_page_one_loop_cycle(query, url_link, file_path)
    relevant_similarity_link_list = filter_new_paths_threshold(similarity_dict_one_page["out_going_links_list_with_similarity"])
    evaluated_links = set(url_link)

    similarity_dict_full = {url_link: similarity_dict_one_page}

    for score, link in similarity_dict_one_page["out_going_links_list_with_similarity"]:
        if (score, link) in relevant_similarity_link_list:
            similarity_dict_one_page = execution_web_page_one_loop_cycle(query=query, link_to_check=link,file_path=file_path, parent_url = url_link, write_to_csv = True)
            if similarity_dict_one_page == "link_unvalid":
                continue
            evaluated_links.update(link)
            evaluated_links.update(similarity_dict_one_page["out_going_links_set"])
            print(similarity_dict_one_page)
            similarity_dict_full[link] = similarity_dict_one_page
    return similarity_dict_full, evaluated_links

if __name__ == "__main__":
    query_words = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation']
    origin_query = "https://en.wikipedia.org/wiki/Absorptive_capacity"

    dictionairy_total = loop_through_webpages(query=query_words, url_link=origin_query, file_path="similarity_data.csv")
    print("all", dictionairy_total)
    #linkset = get_links_html("https://api.semanticscholar.org/CorpusID:153462623")



    """
    similarity_score = tf_idf.scoreAnalysis(tf_idf.cosine(text, query)[0], weights)
    results_of_tf_idf_to_dict()
    
    outgoing_page_links = list(get_links_html(origin_query))
    #results_of_tf_idf_to_dict()
    print(similarity_check_query_with_linklist(query_words, outgoing_page_links ))
    #print(fetch_important_text_in_webpage('https://www.hellonewday.nl'))
    data_dict = {
        "similarity_score": 0.9,
        "url_link": "https://example.com/page1",
        "source_link": "https://example.com/",
        "outgoing_links_list": ["https://example.com/page2", "https://example.com/page3"],
        "webpage_vector": [0.1, 0.2, 0.3, 0.4]
    }
    csv_writer.update_csv_file("data/similarity_data.csv",data_dict)
    """