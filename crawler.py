import numpy as np
import pandas as pd
from selenium import webdriver
from time import sleep
import random
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

categories= {"Thể thao":"https://vnexpress.net/the-thao",
             # "Thế giới":"https://vnexpress.net/the-gioi",
             # "Sức khỏe":"https://vnexpress.net/suc-khoe", 
             # "Kinh doanh":"https://vnexpress.net/kinh-doanh"
              }

def scraper(categories,max_page = 2): 
    news_info = []  
    for catname, base_url in categories.items():
        for page in range(1,max_page+1):
            if page == 1:
                url = base_url
            else :
                url = f"{base_url}-p{page}"
            driver.get(url)
            sleep(2)
            html_content = driver.page_source
            data_html = BeautifulSoup(html_content,'html.parser')
            news = data_html.find_all('article',{'class':'item-news'})
            for i in news:
                news_details = {}
                title_elem = i.find(class_='title-news')
                if not title_elem or not title_elem.find('a'):
                    continue
                
                news_details['Title'] = title_elem.find('a').text.strip()
                news_details["Link"] = title_elem.find('a').get('href')
                
                news_details['Category'] = catname
                
                desc_elem = i.find('p', {'class': 'description'})
                if desc_elem:
                    news_details['Description'] = desc_elem.text.strip() 
                else:
                    news_details['Description'] = np.nan
                
                news_info.append(news_details)
            
    df = pd.DataFrame(news_info)
    return df

def scraper_news_detail(df):
    link_content = df['Link'].tolist()
    all_content = []
    
    for link in link_content:
        contents = np.nan
        try:
            driver.get(link)
            html_content = driver.page_source
            data_html = BeautifulSoup(html_content,'html.parser')
            
            article = data_html.find('article',{'class':"fck_detail"})
            if article:
                paragraphs = article.find_all('p', class_='Normal')
                if len(paragraphs) > 0:
                    contents = " ".join([p.text.strip() for p in paragraphs])
                    
            sleep(random.randint(3,6))
        except Exception as e:
            pass
        all_content.append(contents)
    df['Contents'] = all_content
    return df
        
