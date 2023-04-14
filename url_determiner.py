import requests
import urllib
def get_complete_url(origin_url, target_url):
    """
    combines the orign url with the target_url in case it has a weired structure such as /ahtor/page/
    """
    if "https" in target_url:
        return target_url

    base_url = get_base_url(origin_url)
    return urllib.parse.urljoin(base_url, target_url)

def get_base_url(url):
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def return_final_url_destination(url):
    """
        input: url
        output: url --> the final url that the url redirects to
    """
    response = requests.get(url, allow_redirects=True)
    return response.url

def extract_domain(url):
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    # Remove subdomains and keep only the main domain (e.g., "wikipedia.org")
    domain_parts = domain.split('.')
    main_domain = '.'.join(domain_parts[-2:])
    return main_domain

def extract_page_extension(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.path

def is_same_url(url1, url2):
    standardized_url1 = extract_domain(url1) + extract_page_extension(url1)
    standardized_url2 = extract_domain(url2) + extract_page_extension(url2)
    print(standardized_url1, standardized_url2)
    if standardized_url1 == standardized_url2:
        print(True)

def get_only_unique_links(url_link_list):
    """
        input:
            all url on a webpage
        output:
            all url on webpage that are filtered and the pre_extensions are removed
    """
    unique_url_link_set = set()
    for url in url_link_list:
        standardized_url = extract_domain(url) + extract_page_extension(url)
        if standardized_url not in {t[1] for t in unique_url_link_set}:
            unique_url_link_set.add((url, standardized_url))
    return set(unique_url[0] for unique_url in unique_url_link_set)
def get_correct_url(source_url, target_url):
    """
    tries to go to the target url, if that is not possible, it will try to combine the origin url

    input:
        source_url --> the origin url of where the target_url is located at
        target_url --> the link that is to be evaluated

    output:
        returns a valid link that can be accessed

    """


    #skips the whole function if already https is in the url and therefore valid
    if "https" in target_url:
        return target_url
    origin_url = get_base_url(source_url)

    try:
        url_link_final_redirect = return_final_url_destination(target_url)
    except requests.exceptions.MissingSchema:
        combined_url = get_complete_url(origin_url, target_url)
        url_link_final_redirect = return_final_url_destination(combined_url)

    except requests.exceptions.InvalidSchema:
        combined_url = get_complete_url(origin_url, target_url)
        print("combined", combined_url,"target", target_url, "origin", origin_url)
        url_link_final_redirect = return_final_url_destination(combined_url)
    except:
        print("something went wrong that is currently unclassified with source_link =", source_url, "and target_url", target_url)
        url_link_final_redirect = target_url

    return url_link_final_redirect




