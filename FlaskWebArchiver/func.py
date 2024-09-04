import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import hashlib
import random
import datetime
import time
import string

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
        cursor.execute("INSERT INTO userdata (username,phash,email,total_saves,total_searches) VALUES (?,?,?,?,?)", [username,phash,email,0,0])
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
        cursor.execute(f"INSERT INTO {table_name} (url,index_path) VALUES (?,?)", [url,index_path])
        con.commit()

    else:
        print("table doesnt exist. creating new table.")
        cursor.execute(f"CREATE TABLE {table_name} (id,url STRING, index_path STRING, FOREIGN KEY(id) REFERENCES all_sites(url_id))")
        con.commit()
        cursor.execute(f"INSERT INTO {table_name} (url,index_path) VALUES (?,?)", [url,index_path])
        print(f"inserted data into table {table_name}")
        con.commit()
    

    cursor.execute(f"INSERT INTO all_sites(url, table_name, timestamp) VALUES (?,?,?)", [url, table_name,timestamp])
    con.commit()
    con.close()
    return True # completed successfully

def get_stats(username):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    result = cursor.execute("SELECT total_searches,total_saves FROM userdata WHERE username=?", [username]).fetchall()[0]
    total_searches = result[0]
    total_saves = result[1]
    return total_searches,total_saves

def get_website_from_time(url,date):
    if date == "":
        from_timestamp = time.mktime(datetime.datetime.strptime(str(datetime.datetime.today()).split(" ")[0],'%Y-%m-%d').timetuple())
        print(from_timestamp)
    else:
        from_timestamp = time.mktime(datetime.datetime.strptime(date,"%Y-%m-%d").timetuple()) # start of the day
    to_timestamp = from_timestamp + 1693781999 # 1 second before the day ends
    con = sqlite3.connect("website_data.db")
    cursor = con.cursor()
    result = cursor.execute("SELECT table_name FROM all_sites WHERE url=? AND timestamp >= ? AND timestamp <= ?", [url, from_timestamp, to_timestamp]).fetchall()
    a = []
    for table in result:
        a.append(cursor.execute(f"SELECT url,index_path FROM {table[0]}").fetchall()[0])
    con.close()
    return list(a)

def update_stats(user,stat,amount):
    # test | total_searches | 1
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    if stat == "total_searches":
        current_count = cursor.execute("SELECT total_searches FROM userdata WHERE username=?",[user]).fetchall()[0][0]
        cursor.execute("UPDATE userdata SET total_searches=? WHERE username=?",[int(current_count)+int(amount),user])
    elif stat == "total_saves":
        current_count = cursor.execute("SELECT total_saves FROM userdata WHERE username=?",[user]).fetchall()[0][0]
        cursor.execute("UPDATE userdata SET total_saves=? WHERE username=?",[int(current_count)+int(amount), user])
    else:
        raise NameError
    con.commit()
    con.close()
    return True

def generate_code():
    digits = random.choices(string.digits, k=6)
    code = "".join(digits)
    return code

def add_vercode_2db(vcode,email):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    try:
        result = cursor.execute("UPDATE userdata SET vercode=? WHERE email=?", [vcode,email])
    except:
        print(f"failed to add verification code to account with email {email}")
    con.commit()
    con.close()
    return True

def check_vercode_validity(input_code, email):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    stored_code = cursor.execute("SELECT vercode FROM userdata WHERE email=?", [email]).fetchall()[0][0]
    if int(input_code) == int(stored_code):
        return True
    else:
        return False

def change_user_password(newpass,email):
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    cursor.execute("UPDATE userdata SET phash=? WHERE email=?", [md5hash(newpass),email])    
    con.commit()
    con.close()
    return True


#get_stats("test")
#print(makeAccount("admin1","secret_password","admin@website.com"))
#print(checkUserExists("admin1"))
#print(checkPassword("admin1", "secret_password"))
#get_website_from_time("https://google.com","2024-09-02")
#update_stats("test","total_searches","1")
#add_vercode_2db("013845","test@test.com")
#print(generate_code())