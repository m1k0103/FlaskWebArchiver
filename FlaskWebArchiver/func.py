import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import hashlib


def md5hash(input):
    return hashlib.md5(input.encode()).hexdigest()

def get_links(url): # the scraper
    soup = BeautifulSoup(requests.get(url=url).text)
    print(soup)


def checkUserExists(username):
    #print(os.getcwd())
    con = sqlite3.connect("user.db")
    cursor = con.cursor()    
    result = cursor.execute("select * from userdata where username =?", (username,)).fetchall()
    try:
        if len(result) > 0:
            return True 
        else:
            return False
    finally:        
        cursor.close()
        con.close()

def checkPassword(username, password):
    phash = md5hash(password)
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    result = cursor.execute("select * from userdata where username=? and phash=?", (username,phash)).fetchall()
    try:
        if len(result) > 0:
            return True
        else:
            return False
    finally:
        cursor.close()
        con.close()

def makeAccount(username,password,email):
    if checkUserExists(username=username) == True:
        return False
    else:
        phash = md5hash(password)
        con = sqlite3.connect("user.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO userdata (username,phash,email) VALUES (?,?,?)", [username,phash,email])
        con.commit()
        cursor.close()
        con.close()
        return f"user {username} registered"


#print(makeAccount("admin1","secret_password","admin@website.com"))
#print(checkUserExists("admin1"))
#print(checkPassword("admin1", "secret_password"))