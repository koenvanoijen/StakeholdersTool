import webscraper

linklist = webscraper.get_links_html("https://en.m.wikipedia.org/wiki/Adaptive_capacity")
print(linklist)