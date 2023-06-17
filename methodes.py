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
import csv
import os
import caching

class Webscraper:
    """
    Class that starts the webscraper, it has default values for the link to start but it can be overwritten

    """
    def __init__(self, write_to_csv= True, threshold=0.3):

        self.starting_url = "https://blog.goenvy.io/10-best-ai-marketing-blogs-you-should-follow"
        self.starting_query = ['generative AI', 'general intelligence', 'improvements', 'smart machines', 'scary']
        self.loops_to_execute = 100
        self.file_path_save = "similarity_data_AI_to_check_test.csv"
        self.webpage = None
        self.write_to_csv = write_to_csv
        self.scanned_pages = list()
        self.evaluated_links = set()
        self.links_to_visit_with_parent = list()
        self.threshold = threshold
        self.webpage_object_list = [1 for num in range(self.loops_to_execute*2)]

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

    def start_from_csv(self):
        """
        asks user for a csv name, opens this file and updates the Webscraper class with previous data
        from executing the webscraper. It creates a None as parent to make it compatible with working code, this
        is not how it should be but it is for now.
        """
        while True:
            file_path = input("please enter file_path to continue on")

            try:
                with open(file_path, 'r') as csv_file:
                    csv_reader = list(csv.reader(csv_file, delimiter= ","))
                    index_column_url_link = [index for index, column_name in enumerate(csv_reader[0])
                                                if column_name == "url_link"][0]

                    self.scanned_pages =([row[index_column_url_link] for row in csv_reader[1:]])
                    index_out_going_links_list_with_similarity =[index for index, column_name in enumerate(csv_reader[0])
                                                if column_name == "out_going_links_list_with_similarity"][0]

                    links_to_visit_with_similarity = csv_reader[len(csv_reader)-1][index_out_going_links_list_with_similarity]
                    links_to_visit_with_similarity = self.convert_csv_text_to_python_data(links_to_visit_with_similarity)
                    self.links_to_visit_with_parent = [(link_sim, "no_parent") for link_sim in links_to_visit_with_similarity]

                    break
            except FileNotFoundError:
                print('that was the wrong file_name')
                continue

    def convert_csv_text_to_python_data(self, data):
        """
        asks for data in text format that is in the csv, then it converts is back into lists and tuples
        """
        data = data.strip("[]")
        data = data.split("), ")

        formatted_data = []

        for item in data:
            item = item.strip("()")
            number, url = item.split(", ", 1)
            number = float(number)
            url = url.strip("'")
            formatted_data.append((number, url))

        return formatted_data
    def update_webscraper(self, webpage_object):
        """
        adds the pages that are scanned
        add the links that have been tf_idf'ed
        removes the scanned_pages from the links to visit --> this can be improved by removing the links that are similar
        """
        print("links_to_visit_with_parent = ",self.links_to_visit_with_parent)
        self.scanned_pages.append(webpage_object.link_to_check)
        [self.evaluated_links.add(unique_link) for unique_link in webpage_object.unique_links_on_webpage]
        for link in self.links_to_visit_with_parent:
            print("link[0][1]", link[0][1])
            print("scanned_pages", self.scanned_pages)
            print(link[0][1] not in self.scanned_pages)
        self.links_to_visit_with_parent = [link for link in self.links_to_visit_with_parent if link[0][1] not in self.scanned_pages]

        print("scanned_pages = ", self.scanned_pages)
        print("evaluated_links = ", self.evaluated_links)
        print("links_to_visit_with_parent = ", self.links_to_visit_with_parent)


    def scan_first_webpage(self):
        """
        scans first webpage, then puts in links to visit with their
        similarity scores in self.links_to_visit with parent link
        """
        self.webpage = Webpage(query=self.starting_query, link_to_check=self.starting_url)
        self.webpage.scan_webpage()
        links_to_visit = webscraper.filter_new_paths_threshold(
            self.webpage.similarity_score_unique_links_on_webpage,
            threshold=self.threshold
        )
        self.links_to_visit_with_parent = [(link,self.starting_url) for link in links_to_visit]
        if self.write_to_csv:
            self.webpage.write_page_to_csv(self.file_path_save, self.links_to_visit_with_parent)
        self.update_webscraper(self.webpage)

    def scan_webpages_until_loops_to_execute(self):
        """
        loops through webpages until the amount of loos_to_execute has been met
        Creates a webpage object for each instance in a list
        writes to a csv file in the old format of a dictionairy through the write_page_to_csv

        """
        for loop_number in range(self.loops_to_execute):
            if len(self.links_to_visit_with_parent) <=0:
                break
            print(self.scanned_pages)
            print(self.links_to_visit_with_parent)
            print("I will visit ", self.links_to_visit_with_parent[0][0][1])
            self.webpage_object_list[loop_number] = Webpage(query=self.starting_query,
                                                            link_to_check=self.links_to_visit_with_parent[0][0][1],
                                                            parent_url=self.links_to_visit_with_parent[0][1])
            self.webpage_object_list[loop_number].scan_webpage()
            links_to_visit = []
            try:
                links_to_visit = webscraper.filter_new_paths_threshold(
                    self.webpage_object_list[loop_number].similarity_score_unique_links_on_webpage,
                    threshold=self.threshold
                )
            except TypeError:
                raise TypeError("a wrong type was given with the link =", self.links_to_visit_with_parent[0][0][1])
                print('error', self.webpage_object_list[loop_number].link_to_check)

            self.links_to_visit_with_parent.extend([(link, self.links_to_visit_with_parent[0][0][1]) for link in links_to_visit])
            self.links_to_visit_with_parent = self.remove_duplicates_from_list_and_sort()

            if self.write_to_csv:
                self.webpage_object_list[loop_number].write_page_to_csv(self.file_path_save, self.links_to_visit_with_parent)
            self.update_webscraper(self.webpage_object_list[loop_number])

    def remove_duplicates_from_list_and_sort(self):
        return sorted(list(dict.fromkeys(self.links_to_visit_with_parent)), reverse=True)

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
        #TODO the 2 lines of code are to make the webpage work with cashing of url_text to enhance process. however
        #TODO the code does not work in cashing, it needs a database system to work properly
        original_cached_in_file_link, soup_webpage = caching.get_or_save_cached_file_in_soup_format(self.link_to_check,
                                                                                            file_path="cached_files")
        self.preprocessed_text = webscraper.fetch_important_text_in_webpage(soup_webpage)

        temporary_text = webscraper.fetch_important_text_in_webpage_original(self.link_to_check)
        if temporary_text == self.preprocessed_text:
            print('it is the same')
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

    def write_page_to_csv_old(self,file_path):
        results_dict = webscraper.results_of_tf_idf_to_dict(similarity_score=self.similarity_score_text_query,
                                                 page_url=self.link_to_check, parent_url=self.parent_url,
                                                 out_going_links_set=self.links_on_webpage,
                                                 out_going_links_list_with_similarity=self.similarity_score_unique_links_on_webpage,
                                                 webpage_vector=self.text_vector,
                                                 query_list=self.query)

        csv_writer.update_csv_file(file_path=file_path, data=results_dict)

    def write_page_to_csv(self,file_path, out_going_list_with_similarity_with_parent_not_yet_visited):
        self.update_csv_file(file_path=file_path,
        out_going_list_with_similarity_with_parent_not_yet_visited= out_going_list_with_similarity_with_parent_not_yet_visited)


    def create_csv_file(self, file_path):
        """
        Creates a CSV file with the specified columns.

        Args:
            file_path (str): File path of the CSV file.

        Returns:
            None
        """
        # Define the column names
        fieldnames = ["similarity_score", "url_link", "parent_url", "outgoing_link_on_webpage_with_similarity",
                      "out_going_list_with_similarity_with_parent_not_yet_visited", "query_words"]

        # Create the CSV file with column names
        with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
        print(f"CSV file '{file_path}' created successfully!")

    def update_csv_file(self, file_path, out_going_list_with_similarity_with_parent_not_yet_visited):
        """
        Updates the CSV file with new data. If CSV file does not exists, it will be created by invoking create_csv_file

        Args:
            file_path (str): File path of the CSV file.
            data (dict): Data to be written to the CSV file. Should be a dictionary with keys as column names and values
                         as data to be written. In form :
                                                        "similarity_score",
                                                        "url_link",
                                                        "parent_url",
                                                        "outgoing_link_on_webpage_with_similarity",
                                                        "out_going_list_with_similarity_with_parent_not_yet_visited"
                                                        "query_words"
        Returns:
            None
        """
        # Check if the file path exists
        if not os.path.exists(file_path):
            self.create_csv_file(file_path)

        data_dict = dict()
        data_dict = {
            "similarity_score": self.similarity_score_text_query,
            "url_link": self.link_to_check,
            "parent_url": self.parent_url,
            "outgoing_link_on_webpage_with_similarity": self.similarity_score_unique_links_on_webpage,
            "out_going_list_with_similarity_with_parent_not_yet_visited": out_going_list_with_similarity_with_parent_not_yet_visited,
            "query_words": self.query
        }

        # Append new data to the CSV file
        with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data_dict.keys())
            writer.writerow(data_dict)
        print(f"Data updated in CSV file '{file_path}' successfully!")


if __name__ == "__main__":
    print("hi")
    start_page = Webscraper()
    #start_page.start_from_csv()
    start_page.scan_first_webpage()
    start_page.scan_webpages_until_loops_to_execute()


