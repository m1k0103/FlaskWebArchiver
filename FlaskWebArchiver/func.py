import requests
from bs4 import BeautifulSoup
import os

def get_links(url):
    soup = BeautifulSoup(requests.get(url=url).text)
    print(soup)

def hash():
    pass

def userDataInteract():
    pass

def websiteDataInteract():
    pass