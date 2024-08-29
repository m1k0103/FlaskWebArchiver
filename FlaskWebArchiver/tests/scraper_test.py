import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import os
import datetime


def save_page(url,netloc):
    try:
        os.listdir()
        with open(f"{netloc}-{datetime.datetime.now().timestamp()}", "wb") as f:
            f.write(requests.get(url).content) 
            print(f"saved url {url}")
    except:
        print("error")
        pass


# the database format will be a table called after domain, and then in the table there will be stored all the links in the following format:
# | Saved_url | Local_directory_path | date_archived | Local_resources_path | a 
# 

def get_links(url): 
    netloc = urlsplit(url)[1]
    scheme = urlsplit(url)[0]
    print(netloc)
    if netloc not in os.listdir("./FlaskWebArchiver/website_saves"):
        os.mkdir(f"./FlaskWebArchiver/website_saves/{netloc}")
        os.chdir(f"./FlaskWebArchiver/website_saves/{netloc}")
    else:
        print("domain saved before. entering folder...")
        os.chdir(f"./FlaskWebArchiver/website_saves/{netloc}")

    web_contents = requests.get(url).text

    soup = BeautifulSoup(web_contents, 'html.parser')
    href_el = soup.find_all(href=True)
    src_el = soup.find_all(src=True)
    #find all sources and replace each with local path individually
    all_href = [i.get("href") for i in href_el]
    all_src = [i.get("src") for i in src_el]

    for el in range(len(all_href)):
        if not all_href[el].startswith("http"):
            save_page(f"{scheme}://{netloc}{all_href[el]}", netloc)
        else:
            save_page(all_src[el], netloc)

    for el in range(len(all_src)):
        if not all_src[el].startswith("http"):
            save_page(f"{scheme}://{netloc}{all_src[el]}", netloc)
        else:
            save_page(all_src[el], netloc)

    src_local = []

    for i in range(len(src_el)):
        src_el[i]["src"] = src_local_paths[i]


get_links("https://google.com")