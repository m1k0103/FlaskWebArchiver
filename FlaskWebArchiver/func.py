import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import hashlib

def md5it(input):
    return hashlib.md5(input.encode()).hexdigest()

def get_links(url): # the scraper
    soup = BeautifulSoup(requests.get(url=url).text)
    print(soup)

def checkUserExists(username):
    con = sqlite3.connect("../user.db")
    cursor = con.cursor()    
    cursor.execute(f"select 1 from userdata where username ='{username}';")
    if cursor.rowcount():
        return True # user exists
    else:
        return False # user doesnt exist

def checkPassword(username, password):
    con = sqlite3.connect("../user.db")
    cursor = con.cursor()    
    cursor.execute(f"SELECT {username} FROM userdata WHERE username='{username}';")

checkUserExists("test")