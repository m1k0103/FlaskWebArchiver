import sqlite3
import os
import random
import string

# ----- TO DO -----
#   > maybe make a config file to store the database names, admin password for the website, etc 
#     (this could be done in docker maybe??)
#   > research if previous idea is possible
#   > work on the theory too

def start():
    MAIN_DB_NAME = "database.db"

    if MAIN_DB_NAME not in os.listdir():
        # creates table for user data
        db = open(f'./{MAIN_DB_NAME}', 'w+')
        db.close()

        con = sqlite3.connect(MAIN_DB_NAME)
        cursor = con.cursor()

        cursor.execute("""CREATE TABLE stats(
                   stat_id INTEGER PRIMARY KEY ,
                   total_searches INT,
                   total_saves INT
                   )""")

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


        con.commit()
        cursor.close()
        con.close()

    
    #creates secret_key used for auth
    if "secret_key.py" not in os.listdir("./FlaskWebArchiver"):
        with open("./FlaskWebArchiver/secret_key.py", "w") as f:
            f.write(f"SECRET_KEY = b\"\"\"{''.join(random.choices(string.printable, k=16))}\"\"\"\nMAIL_ACCOUNT=\nMAIL_PASS=\n")
    else:
        pass

    # creates folder for website save data
    try:
        os.mkdir("FlaskWebArchiver/website_saves")
    except:
        print("[!] website_saves folder already exists")
    
    
    print("[!] starting program")
    from FlaskWebArchiver.routes import app
    app.run(host="0.0.0.0", port="5000",debug=True)