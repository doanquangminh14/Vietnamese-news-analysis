import numpy as np
import pandas as pd
from selenium import webdriver
from time import sleep
import random
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import data

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

categories= {"Thể thao":"https://vnexpress.net/the-thao",
             #"Thế giới":"https://vnexpress.net/the-gioi",
             #"Sức khỏe":"https://vnexpress.net/suc-khoe", 
             #"Kinh doanh":"https://vnexpress.net/kinh-doanh"
              }

def crawl_metadata(categories, max_page=1):
    news_info = []

    for catname, base_url in categories.items():
        for page in range(1, max_page + 1):
            url = base_url if page == 1 else f"{base_url}-p{page}"
            driver.get(url)
            sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            news = soup.find_all('article', {'class': 'item-news'})

            for i in news:
                title_elem = i.find(class_='title-news')
                if not title_elem or not title_elem.find('a'):
                    continue

                link = title_elem.find('a').get('href')
                if not link.startswith('http'):
                    link = "https://vnexpress.net" + link

                news_info.append({
                    "Title": title_elem.text.strip(),
                    "Link": link,
                    "Category": catname
                })

    return pd.DataFrame(news_info)

def crawl_content(df):
    contents = []

    for link in df['Link']:
        text = None
        publish_date = None

        try:
            driver.get(link)
            sleep(random.randint(2, 4))

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            article = soup.find('article', {'class': 'fck_detail'})
            if article:
                paragraphs = article.find_all('p', class_='Normal')
                text = " ".join([p.text.strip() for p in paragraphs])

            date_tag = soup.find('span', {'class': 'date'})
            if date_tag:
                publish_date = date_tag.text.strip()

        except Exception as e:
            print(f"Lỗi tại {link}: {e}")

        contents.append({
            "Link": link,
            "Content": text,
            "Publish_Date": publish_date
        })

    return pd.DataFrame(contents)

def merge_data(df_meta, df_content):
    df_final = pd.merge(df_meta, df_content, on="Link", how="left")
    return df_final
        
def run_crawler():
    df_meta = crawl_metadata(categories)
    df_content = crawl_content(df_meta)
    df_final = merge_data(df_meta, df_content)
    
    data.insert_raw_articles(df_final)

    return df_final