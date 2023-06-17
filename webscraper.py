from bs4 import BeautifulSoup
import requests
import re
import Preprocess
import tf_idf
import csv_writer
import urllib
import url_determiner

def get_all_links_on_html_page(url):
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
        if len(url_link) == 0:
            continue
        if url_link[0] == "/" or "https" in url_link:
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

def fetch_important_text_in_webpage(webpage_soup):
    """
    input: web_page_soup = format should be in a beautifulsoup html.parser format
    output: return preprocessed text in the html page of link
    """
    try:
        text_in_website = filter_text_in_html(webpage_soup)
        text_preprocessed = [Preprocess.preproccess([line]) for line in text_in_website]
        text_preprocessed_joined = " ".join(text_preprocessed)
        return text_preprocessed_joined

    except Exception as e:
        print(f"!@!@!@!@ Error fetching content from URL: {link}. Error: {e}")
        return ""

def fetch_important_text_in_webpage_original(link):
    """
    input: link = url_link in string format
    output: list of lines of preprocessed text in the html page of the link
                The preprocessing uses the Preprocess python package
                It lemmitizes the words and removes stopwords

    """
    try:
        print(link)
        webpage = retrieve_webpage(link)
        webpage_soup = BeautifulSoup(webpage.text, "html.parser")
        text_in_website = filter_text_in_html(webpage_soup)
        text_preprocessed = [Preprocess.preproccess([line]) for line in text_in_website]
        text_preprocessed_joined = " ".join(text_preprocessed)
        return text_preprocessed_joined

    except Exception as e:
        print(f"!@!@!@!@ Error fetching content from URL: {link}. Error: {e}")
        return ""

def fetch_important_text_in_webpage_original_backup(link):
    """
    input: link = url string
    output: return preprocessed text in the html page of link
    """
    try:
        print(link)
        webpage = retrieve_webpage(link)
        webpage_soup = BeautifulSoup(webpage.text, "html.parser")
        text_in_website = filter_text_in_html(webpage_soup)
        text_preprocessed = Preprocess.preproccess(text_in_website)
        text_preprocessed_joined = " ".join(text_preprocessed)
        return text_preprocessed_joined

    except Exception as e:
        print(f"!@!@!@!@ Error fetching content from URL: {link}. Error: {e}")
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
        preprocessed_text = fetch_important_text_in_webpage_original(link)

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
    preprocessed_text = fetch_important_text_in_webpage_original(link_to_check)
    if is_not_valid_html_text(preprocessed_text):
        return "link_unvalid" #continue  # text skips vectorization to prevent error

    cosine_similarity_text_and_query, text_vector = tf_idf.cosine(preprocessed_text, query)
    similarity_score_text_query = tf_idf.scoreAnalysis(cosine_similarity_text_and_query, weights)
    link_set= set(get_all_links_on_html_page(link_to_check))

    #Create a filter that groups the link_list so that it only has the links that are unique
    unique_link_set = url_determiner.get_only_unique_links(link_set)

    print("link_set=", link_set)
    print("unique_link_set=",unique_link_set)
    similarity_link_list = similarity_check_query_with_linklist(query,unique_link_set)
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


def loop_through_webpages(similarity_dict_one_page,similarity_dict_full, query, file_path, url_link):
    """
    iterates over the links in the web_page then it does a similarity check with the query and the new webpages
    input:
        query = list of words to compare with html text in url_link
        file_path = location and filename ot be saved e.g. similarity_data.csv or users/mehdi/data/similarity_data.csv
        url_link = link of which text should be evaluated

    output:
        similarity_dict
    """
    relevant_similarity_link_list = filter_new_paths_threshold(similarity_dict_one_page["out_going_links_list_with_similarity"])
    print(relevant_similarity_link_list)
    evaluated_links = set(url_link)

    similarity_dict_full = {url_link: similarity_dict_one_page}

    for score, link in similarity_dict_one_page["out_going_links_list_with_similarity"]:
        if (score, link) in relevant_similarity_link_list:
            if link in similarity_dict_full: #skips the link if it is already present in the similarity_dict_one_page
                continue
            similarity_dict_one_page = execution_web_page_one_loop_cycle(query=query, link_to_check=link,file_path=file_path, parent_url = url_link, write_to_csv = True)
            if similarity_dict_one_page == "link_unvalid":
                continue
            evaluated_links.update(link)
            evaluated_links.update(similarity_dict_one_page["out_going_links_set"])
            print(similarity_dict_one_page)
            similarity_dict_full[link] = similarity_dict_one_page
    return similarity_dict_full, evaluated_links

def return_similarity_dict_by_loop_through_links_on_webpage(similarity_dict_one_page,similarity_dict_full, query, file_path, parent_url = None):
    """
    iterates over the links in the web_page then it does a similarity check with the query and the new webpages
    input:
        query = list of words to compare with html text in url_link
        file_path = location and filename ot be saved e.g. similarity_data.csv or users/mehdi/data/similarity_data.csv
        url_link = link of which text should be evaluated

    output:
        similarity_dict
    """
    relevant_similarity_link_list = filter_new_paths_threshold(similarity_dict_one_page["out_going_links_list_with_similarity"])
    print(relevant_similarity_link_list)
    evaluated_links = set()
    for score, link in similarity_dict_one_page["out_going_links_list_with_similarity"]:
        if (score, link) in relevant_similarity_link_list:
            if link in similarity_dict_full: #skips the link if it is already present in the similarity_dict_one_page
                continue
            newest_similarity_dict_this_loop = execution_web_page_one_loop_cycle(query=query, link_to_check=link,file_path=file_path, parent_url = parent_url, write_to_csv = True)
            if newest_similarity_dict_this_loop == "link_unvalid":
                continue
            evaluated_links.update(link)
            #evaluated_links.update(similarity_dict_one_page["out_going_links_set"])
            print(newest_similarity_dict_this_loop)
            similarity_dict_full[link] = newest_similarity_dict_this_loop
    return similarity_dict_full

def get_starting_url():
    while True:
        starting_url = input("Please enter the URL to start scraping on: ")

        try:
            requests.get(starting_url, allow_redirects=True)
            break
        except:
            print('Give me a valid URL! Include the https://www.')

    return starting_url


def get_starting_queries():
    starting_queries = []

    while True:
        query = str(input('Give me a word for the query, if you are done: press enter'))
        if query == "":
            break
        else:
            starting_queries.append(query)
            print(starting_queries)

    return starting_queries


def get_loop_depth():
    while True:
        loops_to_execute_crawler = input('How deep should the crawler go? Give an integer: ')

        try:
            loops_to_execute_crawler = int(loops_to_execute_crawler)

            if loops_to_execute_crawler > 0:
                break
            else:
                print('Give me a positive non-zero integer')
        except:
            print('Give me a valid integer!')

    return loops_to_execute_crawler


def get_file_path():
    while True:
        file_path = input('To what path should I save the results? It can be an existing file, it must include .csv: ')

        if ".csv" in file_path:
            break
        else:
            continue

    return file_path


def start_webscraper():
    starting_url = "https://api.semanticscholar.org/CorpusID:153462623 "#get_starting_url()
    starting_queries = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation']#get_starting_queries()
    loops_to_execute_crawler = get_loop_depth()
    file_path = "similarity_data.csv"#get_file_path()

    similarity_dict_one_page = execution_web_page_one_loop_cycle(starting_queries, starting_url, file_path, parent_url='None', write_to_csv=True)

    similarity_dict_full = {starting_url: similarity_dict_one_page}
    print("similarity_dict_one_page", similarity_dict_one_page)
    for loop in range(loops_to_execute_crawler):
        print('We started looping through the webpages at loop:', loop)
        similarity_dict_full = return_similarity_dict_by_loop_through_links_on_webpage(
            similarity_dict_one_page=similarity_dict_one_page,
            similarity_dict_full=similarity_dict_full,
            query=starting_queries,
            file_path=file_path,
            parent_url=starting_url
        )


class Webscraper:
    def __init__(self):

        self.starting_url = "https://en.wikipedia.org/wiki/Absorptive_capacity"
        self.starting_queries = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation']
        self.loops_to_execute = 3
        self.file_path_save = "similarity_data.csv"

        self.starting_data = input("Do you want to give your own data? Answer with True or False: ").lower()

        if self.starting_data == "true":


            self.starting_url = Webscraper.get_starting_url()
            self.starting_queries = input("Enter the starting queries separated by commas: ").split(',')
            self.loops_to_execute = int(input("Enter the number of loops to execute: "))
            self.file_path_save = input("Enter the file path to save the output: ")

    def get_starting_url():
        while True:
            starting_url = input("please enter url to start scraping on")
            try:
                requests.get(starting_url, allow_redirects=True)
                print('hi')
                return starting_url
            except:
                print('give me a valid url! include the https://www.')


def start_webscrapers():
    """
    starts the webscraper
    asks the user for the starting url and query
    not yet updated the query to be bug proof

    """
    starting_url = ""
    starting_queries = []
    loops_to_execute_crawler = int
    file_path = str()
    while True:
        starting_url = input("please enter url to start scraping on")

        try:
            requests.get(starting_url, allow_redirects=True)
            print('hi')
            break
        except:
            print('give me a valid url! include the https://www.')

    while True:
        query = str(input('give me a word for in the query, if you are done: press enter'))
        if query == "":
            break
        else:
            try:
                starting_queries.append(query)
                print(starting_queries)
            except:
                print('please enter a valid query word')
    while True:
        loops_to_execute_crawler = input('how deep should the crawler go? give an integer')
        try:
            loops_to_execute_crawler = int(loops_to_execute_crawler)

            if loops_to_execute_crawler > 0:
                break
            else:
                print('give me a positive non zero integer')
        except:
            print('give me a valid integer!')

    while True:
        file_path = input('to what path should I save the results? It can be an existing file, it must include .csv')

        if ".csv" in file_path:
            break
        else:
            continue

    similarity_dict_one_page = execution_web_page_one_loop_cycle(starting_queries, starting_url, file_path, parent_url='None', write_to_csv=True)

    similarity_dict_full = {starting_url: similarity_dict_one_page}
    print("similarity_dict_one_page", similarity_dict_one_page)
    for loop in range(loops_to_execute_crawler):
        print('we started looping through the webapges at loop:', loop)
        similarity_dict_full = return_similarity_dict_by_loop_through_links_on_webpage(
            similarity_dict_one_page = similarity_dict_one_page,
            similarity_dict_full = similarity_dict_full,
            query= starting_queries,
            file_path = file_path,
            parent_url= starting_url
        )





if __name__ == "__main__":
    webpage = retrieve_webpage("https://wwww.hellonewday.nl")
    print(webpage)
    #webpage_soup = BeautifulSoup(webpage.text, "html.parser")
    #ext_in_website = filter_text_in_html(webpage_soup)




    #query_words = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation']
    #origin_query = "https://en.wikipedia.org/wiki/Absorptive_capacity"

    #dictionairy_total = loop_through_webpages(query=query_words, url_link=origin_query, file_path="similarity_data.csv")
    #print("all", dictionairy_total)
    #linkset = get_all_links_on_html_page("https://api.semanticscholar.org/CorpusID:153462623")
    #start_webscraper()

    #similarity_dict_one_page = execution_web_page_one_loop_cycle(query_words, origin_query, "similarity_data.csv", parent_url='None', write_to_csv=True)


    """
    similarity_score = tf_idf.scoreAnalysis(tf_idf.cosine(text, query)[0], weights)
    results_of_tf_idf_to_dict()
    
    outgoing_page_links = list(get_all_links_on_html_page(origin_query))
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