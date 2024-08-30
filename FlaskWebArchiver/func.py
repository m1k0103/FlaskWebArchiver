import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import hashlib
import random


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

def create_website_save(url,index_path,timestamp):
    os.chdir("../../../")
    con = sqlite3.connect("website_data.db")
    cursor = con.cursor()
    
    #creates website index table
    table_name = f"table{random.randint(0,100000000)}"

    if len(cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'").fetchall()) > 0:
        print("table already exists. not creating new table. inserting data")
        cursor.execute(f"INSERT INTO {table_name} (url,index_path,timestamp) VALUES (?,?,?)", [url,index_path,timestamp])
        con.commit()

    else:
        print("table doesnt exist. creating new table.")
        cursor.execute(f"CREATE TABLE {table_name} (id,url STRING, index_path STRING, timestamp STRING, FOREIGN KEY(id) REFERENCES all_sites(url_id))")
        con.commit()
        cursor.execute(f"INSERT INTO {table_name} (url,index_path,timestamp) VALUES (?,?,?)", [url,index_path,timestamp])
        print(f"inserted data into table {table_name}")
        con.commit()
    
    #new connection because why not idk

    cursor.execute(f"INSERT INTO all_sites(url, table_name) VALUES (?,?)", [url, table_name])
    con.commit()
    con.close()
    return True # completed successfully

#print(makeAccount("admin1","secret_password","admin@website.com"))
#print(checkUserExists("admin1"))
#print(checkPassword("admin1", "secret_password"))