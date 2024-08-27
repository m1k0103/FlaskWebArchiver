import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_links(url): # the scraper
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    href_el = soup.find_all(href=True)
    src_el = soup.find_all(src=True)
    all_href = [i.get("href") for i in href_el]
    all_src = [i.get("src") for i in src_el]
    
    print(all_href)
    print(all_src)
    print(type(all_href[0]))

get_links("https://google.com")