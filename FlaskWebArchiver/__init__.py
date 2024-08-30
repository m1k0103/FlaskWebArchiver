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
    USER_DB_NAME = "user.db"
    WEBSITE_DB_NAME = "website_data.db"

    if USER_DB_NAME not in os.listdir():
        os.system(f'echo > {USER_DB_NAME}')
        print("[+] user database created")
        c = sqlite3.connect(USER_DB_NAME)
        cursor = c.cursor()

        # creates table for user data
        cursor.execute("CREATE TABLE userdata(user_id INTEGER PRIMARY KEY,username STRING NOT NULL,phash STRING NOT NULL,email STRING NOT NULL, total_searches INTEGER, total_saves INTEGER, vercode STRING)")
        c.commit()
        c.close()
        print("[+] table 'userdata' created in user table")
        
        if WEBSITE_DB_NAME not in os.listdir():
            os.system(f'echo > {WEBSITE_DB_NAME}')
            print("[+] website database created")

            c = sqlite3.connect(WEBSITE_DB_NAME)
            cursor = c.cursor()

            #creates table for indexes table
            cursor.execute("CREATE TABLE all_sites(url_id INTEGER PRIMARY KEY NOT NULL, url STRING, table_name STRING)")
            c.commit()
            
        else:
            print(["[!] website database already exists"])

    else:
        print("[!] user database already exists\n")
    
    

    #creates secret_key used for auth
    if "secret_key.py" not in os.listdir("./FlaskWebArchiver"):
        with open("./FlaskWebArchiver/secret_key.py", "w") as f:
            f.write(f"SECRET_KEY = b\"\"\"{''.join(random.choices(string.printable, k=16))}\"\"\"")
    else:
        pass

    # creates folder for website save data
    try:
        os.mkdir("FlaskWebArchiver/website_saves")
    except:
        print("[!] website_saves already exists")
        
    print("[!] starting program")
    from FlaskWebArchiver.routes import app
    app.run(host="0.0.0.0", port="5000",debug=True)