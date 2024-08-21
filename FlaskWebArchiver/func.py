import requests
from bs4 import BeautifulSoup
import os
import sqlite3

def get_links(url):
    soup = BeautifulSoup(requests.get(url=url).text)
    print(soup)

def checkDetails():
    pass

def cookieGen():
    pass