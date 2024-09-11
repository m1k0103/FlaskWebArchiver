import sqlite3
import os

def db_make():
    db = open('test.db', 'w+')
    db.close()
    

    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    #creates sites_data table
    cursor.execute("""CREATE TABLE sites_data(
                   site_id INT FOREIGN KEY(site_id) REFERENCES sites(site_id) ON DELETE CASCASDE ON UPDATE CASCASDE,
                   url TEXT,
                   timestamp FLOAT,
                   local_path TEXT
                   )""")
    #cursor.commit()

    #creates sites table

    cursor.execute("""CREATE TABLE sites(
                   site_id INT PRIMARY KEY NOT NULL,
                   scraped_by INT FOREIGN KEY(uid) REFERENCES userdata(uid) ON DELETE CASCADE ON UPDATE CASCADE
                   )""")

    cursor.execute(""" CREATE TABLE stats(
               stat_id INT PRIMARY KEY NOT NULL,
               total_searches INT,
               total_saves INT
               )""")
    #cursor.commit()

    #creates main userdata table
    cursor.execute(""" CREATE TABLE userdata(
                   uid INT PRIMARY KEY NOT NULL,
                   username TEXT,
                   phash TEXT,
                   email TEXT,
                   stat_id INT FOREIGN KEY(stat_id) REFERENCES stats(stat_id) ON DELETE CASCASDE ON UPDATE CASCASDE,
                   vercode TEXT
                   )""")
    cursor.commit()
    cursor.close()
    con.close()

db_make()