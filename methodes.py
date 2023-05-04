from bs4 import BeautifulSoup
import requests
import re
import Preprocess
import tf_idf
import csv_writer
import urllib
import url_determiner
import webscraper
import tf_idf
class Webscraper:
    """
    Class that starts the webscraper, it has default values for the link to start but it can be overwritten

    """
    def __init__(self, write_to_csv= True):

        self.starting_url = "https://en.wikipedia.org/wiki/Absorptive_capacity"
        self.starting_query = ['absorptive capacity', 'assimilation', 'acquisition', 'transformation']
        self.loops_to_execute = 3
        self.file_path_save = "similarity_data.csv"
        self.webpage = None
        self.write_to_csv = write_to_csv
        self.scanned_pages = list()
        self.evaluated_links = set()
        self.links_to_visit = list()

        self.starting_data = input("Do you want to give your own data? Answer with True or False: ").lower()

        if self.starting_data == "true":
            self.starting_url = Webscraper.get_starting_url()
            self.starting_query = input("Enter the starting queries separated by commas: ").split(',')
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

    def update_webscraper(self, webpage_object):
        self.scanned_pages.append(webpage_object.link_to_check)
        self.evaluated_links.add(webpage_object.unique_links_on_webpage)


    def scan_first_webpage(self):
        self.webpage = Webpage(query=self.starting_query, link_to_check=self.starting_url)
        self.webpage.scan_webpage()

        if self.write_to_csv:
            self.webpage.write_page_to_csv(self.file_path_save)

class Webpage:
    """
    Class that creates a webpage object that checks the whole text on a webpage and evaluates all links on that
    webpage
    """
    def __init__(self, query, link_to_check, parent_url=None, weights = 1):
        self.preprocessed_text = None
        self.valid_html_text = None
        self.cosine_similarity_text_and_query = None
        self.text_vector = None
        self.similarity_score_text_query = None
        self.links_on_webpage = None
        self.unique_links_on_webpage = None
        self.similarity_score_unique_links_on_webpage = None
        self.parent_url = parent_url
        self.weights = [weights for i in query]
        self.link_to_check = link_to_check
        self.query = query

    def scan_webpage(self):
        self.preprocessed_text = webscraper.fetch_important_text_in_webpage(self.link_to_check)
        self.valid_html_text = webscraper.is_not_valid_html_text(self.preprocessed_text)
        if self.valid_html_text:
            return "link_unvalid" #continue  # text skips vectorization to prevent error
        else:
            self.cosine_similarity_text_and_query, self.text_vector = tf_idf.cosine(self.preprocessed_text, self.query)
            self.similarity_score_text_query = tf_idf.scoreAnalysis(self.cosine_similarity_text_and_query, self.weights)
            self.links_on_webpage = webscraper.get_all_links_on_html_page(self.link_to_check)

            # Create a filter that groups the link_list so that it only has the links that are unique
            self.unique_links_on_webpage = url_determiner.get_only_unique_links(set(self.links_on_webpage))

            print("links_on_webpage=", self.links_on_webpage)
            print("unique_link_set=", self.unique_links_on_webpage)
            self.similarity_score_unique_links_on_webpage = webscraper.similarity_check_query_with_linklist(self.query, self.unique_links_on_webpage)

    def write_page_to_csv(self,file_path):
        results_dict = webscraper.results_of_tf_idf_to_dict(similarity_score=self.similarity_score_text_query,
                                                 page_url=self.link_to_check, parent_url=self.parent_url,
                                                 out_going_links_set=self.links_on_webpage,
                                                 out_going_links_list_with_similarity=self.similarity_score_unique_links_on_webpage,
                                                 webpage_vector=self.text_vector,
                                                 query_list=self.query)

        csv_writer.update_csv_file(file_path=file_path, data=results_dict)




if __name__ == "__main__":
    print("hi")
    start_page = Webscraper()
    start_page.scan_first_webpage()


