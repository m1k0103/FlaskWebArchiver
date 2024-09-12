import sqlite3
import os

def db_make():
    db = open('./test.db', 'w+')
    db.close()
    
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE stats(
               sid INT PRIMARY KEY NOT NULL,
               total_searches INT,
               total_saves INT
               )""")
    #cursor.commit()

    #creates main userdata table
    cursor.execute("""CREATE TABLE userdata(
                   uid INT PRIMARY KEY NOT NULL,
                   username TEXT,
                   phash TEXT,
                   email TEXT,
                   stat_id INT,
                   vercode INT,
                   FOREIGN KEY(stat_id) REFERENCES stats(sid)
                   )""")


    cursor.execute("""CREATE TABLE sites(
                   site_id INT PRIMARY KEY NOT NULL,
                   scraped_by INT,
                   FOREIGN KEY(scraped_by) REFERENCES userdata(uid)
                   )""")


    cursor.execute("""CREATE TABLE sites_data (
                   site_id INT,
                   url TEXT,
                   timestamp FLOAT,
                   local_path TEXT,
                   FOREIGN KEY(site_id) REFERENCES sites(site_id)
                   )""")
    
    #cursor.commit()


    con.commit()
    cursor.close()
    con.close()

db_make()