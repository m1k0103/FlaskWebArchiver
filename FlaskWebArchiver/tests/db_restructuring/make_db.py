import sqlite3
import os
import hashlib
def md5hash(input):
    return hashlib.md5(str(input).encode()).hexdigest()

def db_make():
    db = open('./test.db', 'w+')
    db.close()
    
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE stats(
               stat_id INTEGER PRIMARY KEY ,
               total_searches INT,
               total_saves INT
               )""")
    #cursor.commit()

    #creates main userdata table
    cursor.execute("""CREATE TABLE userdata(
                   uid INTEGER PRIMARY KEY,
                   username TEXT NOT NULL,
                   phash TEXT NOT NULL,
                   email TEXT NOT NULL,
                   stat_id INT NOT NULL,
                   vercode INT,
                   FOREIGN KEY(stat_id) REFERENCES stats(stat_id)
                   )""")


    cursor.execute("""CREATE TABLE sites(
                   site_id INTEGER PRIMARY KEY,
                   scraped_by INT NOT NULL,
                   FOREIGN KEY(scraped_by) REFERENCES userdata(uid)
                   )""")


    cursor.execute("""CREATE TABLE sites_data (
                   site_id INTEGER PRIMARY KEY,
                   url TEXT NOT NULL,
                   timestamp RFLOATEAL NOT NULL,
                   local_path TEXT NOT NULL,
                   FOREIGN KEY(site_id) REFERENCES sites(site_id)
                   )""")
    
    #cursor.commit()

    con.commit()
    cursor.close()
    con.close()

def insert_mock_data():
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    cursor.execute("INSERT INTO stats(total_searches, total_saves) VALUES (0,0)")
    cursor.execute(f"INSERT INTO userdata(username,phash,email,vercode, stat_id) VALUES ('larry','{md5hash(1)}','larry@mail.com',098776, {cursor.lastrowid})")

    cursor.execute("INSERT INTO stats(total_searches, total_saves) VALUES (0,0)")
    cursor.execute(f"INSERT INTO userdata(username,phash,email,vercode, stat_id) VALUES ('john','{md5hash(2)}','john@mail.com',123456, {cursor.lastrowid})")
    
    cursor.execute("INSERT INTO stats(total_searches, total_saves) VALUES (0,0)")
    cursor.execute(f"INSERT INTO userdata(username,phash,email,vercode, stat_id) VALUES ('bob','{md5hash(3)}','bob@mail.com',202020, {cursor.lastrowid})")
    
    
    con.commit()
    con.close()

def get_stats_by_username(username):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    # selects something im not too sure lol
    result = cursor.execute("SELECT userdata.stat_id, stats.total_searches, stats.total_saves FROM userdata JOIN stats ON (userdata.stat_id=stats.site_id) WHERE userdata.username=?", [username]).fetchall()[0]
    total_searches = result[1]
    total_saves = result[2]

    con.close()

    print(total_searches, total_saves)
    return total_searches, total_saves

def check_password(username,password):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    phash = md5hash(password)
    if str(phash) == cursor.execute("SELECT phash FROM userdata WHERE username=?", [username]).fetchall()[0][0]:
        con.close()
        return True
    else:
        con.close()
        return False 



#db_make()
#insert_mock_data()
#get_stats_by_username("bob")
print(check_password("bob",3))