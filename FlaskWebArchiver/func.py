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

def checkUserExists(username): # unchanged
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

def check_password(username,password): # DONE
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    phash = md5hash(password)
    if str(phash) == cursor.execute("SELECT phash FROM userdata WHERE username=?", [username]).fetchall()[0][0]:
        con.close()
        return True
    else:
        con.close()
        return False 

def makeAccount(username,password,email): # DONE i think
    if checkUserExists(username=username) == True:
        return False
    else:
        phash = md5hash(password)
        con = sqlite3.connect("user.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO stats(total_searches, total_saves) VALUES (0,0)")
        cursor.execute(f"INSERT INTO userdata(username,phash,email,vercode, stat_id) VALUES (?,?,?,NULL,{cursor.lastrowid})", [username,phash,email])
        con.commit()
        cursor.close()
        con.close()
        return f"user {username} registered"

def create_website_save(url,index_path,timestamp, scraped_by_user): # DONE
    os.chdir("../../../")
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    
    
    #gets user ID from username provided
    try:
        uid  = cursor.execute("SELECT uid FROM userdata WHERE username=?", [scraped_by_user]).fetchall()[0][0]
    except:
        print("user doesnt exist")
        uid = None
    finally:
        cursor.execute(f"INSERT INTO sites(scraped_by) VALUES ({uid})")
        cursor.execute("INSERT INTO sites_data(url,timestamp,local_path) VALUES (?,?,?)", [url,timestamp,index_path])

        con.commit()
        con.close()
        return True

def get_stats_by_username(username): # ---------- STILL HAVE TO ADD THE STATS ON WHICH WEBSITES HAVE BEEN SCRAPED BY USER
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    # selects something im not too sure lol
    result = cursor.execute("SELECT userdata.stat_id, stats.total_searches, stats.total_saves FROM userdata JOIN stats ON (userdata.stat_id=stats.site_id) WHERE userdata.username=?", [username]).fetchall()[0]
    total_searches = result[1]
    total_saves = result[2]

    con.close()

    print(total_searches, total_saves)
    return total_searches, total_saves

def get_website_from_time(url,start_date,end_date): # rewrite

    #if no start_date provided, it will just show the first ever timestamp
    if start_date == "":
        start_timestamp = 0
    else:
        start_timestamp = time.mktime(datetime.datetime.strptime(start_date,"%Y-%m-%d").timetuple())
    
    # if no end_date is provided, it will assume you're searching from a date to the present day.
    if end_date == "": 
        end_timestamp = time.mktime(datetime.datetime.strptime(str(datetime.datetime.today()).split(" ")[0],'%Y-%m-%d').timetuple())
        print(end_timestamp)
    else:
        end_timestamp = time.mktime(datetime.datetime.strptime(end_date,"%Y-%m-%d").timetuple()) # start of the day
    end_timestamp = end_timestamp + 86399 # 1 second before the day ends
    con = sqlite3.connect("website_data.db")
    cursor = con.cursor()
    result = cursor.execute("SELECT table_name FROM all_sites WHERE url=? AND timestamp >= ? AND timestamp <= ?", [url, start_timestamp, end_timestamp]).fetchall()
    a = []
    for table in result:
        a.append(cursor.execute(f"SELECT url,index_path FROM {table[0]}").fetchall()[0])
    con.close()
    return list(a)

def update_stats(user,stat,amount): # rewrite
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

def generate_code(): # rewrite
    digits = random.choices(string.digits, k=6)
    code = "".join(digits)
    return code

def add_vercode_2db(vcode,email): # rewrite
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    try:
        result = cursor.execute("UPDATE userdata SET vercode=? WHERE email=?", [vcode,email])
    except:
        print(f"failed to add verification code to account with email {email}")
    con.commit()
    con.close()
    return True

def check_vercode_validity(input_code, email): # rewrite
    con = sqlite3.connect("user.db")
    cursor = con.cursor()
    stored_code = cursor.execute("SELECT vercode FROM userdata WHERE email=?", [email]).fetchall()[0][0]
    if int(input_code) == int(stored_code):
        return True
    else:
        return False

def change_user_password(newpass,email): # rewrite
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
#get_website_from_time("https://google.com", "2024-09-02", "")
#get_stats("test")