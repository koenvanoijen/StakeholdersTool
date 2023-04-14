import url_determiner
import tf_idf
url_link = '/javascript:print();'
source_url = "https://www.wiki.com"

if url_link[0] == "\\" or url_link[0] == "/" or "https" in url_link:
    url_link_final_redirect = url_determiner.get_correct_url(source_url=source_url, target_url=url_link)
print(url_link_final_redirect)

link1="https://en.wikipedia.org/wiki/Absorptive_capacity"
link2="https://en.wikipedia.org/w/index.php?title=Absorptive_capacity&printable=yes"
link3="https://en.m.wikipedia.org/wiki/Absorptive_capacity"
link4 ="https://en.m.wikipedia.org/wiki/deceptive_capacity"
similarity_score = tf_idf.cosine(link1, [link4])
print(similarity_score)

origin_url = url_determiner.get_base_url(link4)
print(origin_url)

from urllib.parse import urlparse

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove subdomains and keep only the main domain (e.g., "wikipedia.org")
    domain_parts = domain.split('.')
    main_domain = '.'.join(domain_parts[-2:])
    return main_domain

def extract_page_extension(url):
    parsed_url = urlparse(url)
    return parsed_url.path

def is_same_url(url1, url2):
    standardized_url1 = extract_domain(url1) + extract_page_extension(url1)
    standardized_url2 = extract_domain(url2) + extract_page_extension(url2)
    print(standardized_url1, standardized_url2)
    if standardized_url1 == standardized_url2:
        print(True)

def get_only_unique_links(url_link_list):
    unique_url_link_set = set()
    for url in url_link_list:
        standardized_url = extract_domain(url) + extract_page_extension(url)
        if standardized_url not in {t[1] for t in unique_url_link_set}:
            unique_url_link_set.add((url, standardized_url))
    return set(unique_url[0] for unique_url in unique_url_link_set)

is_same_url(link1, link3)