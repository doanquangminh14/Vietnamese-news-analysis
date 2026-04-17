import pandas as pd
import re
import unicodedata



def remove_html(text):
    text = re.sub(r'<[^>]+>', ' ', str(text))
    text = re.sub(r'&nbsp;|&amp;|&lt;|&gt;', ' ', text)
    return text



def normalize_text(text):
    text = unicodedata.normalize('NFC', str(text))
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text



def remove_special_char(text):
    text = re.sub(r'[^a-zA-Z0-9à-ỹ\s]', ' ', text)
    return text



def data_pipeline(df):
    
    df = df.drop_duplicates(subset=['Link'])
    print(f'Sau dedup: {len(df)} bài')

    df = df.dropna(subset=['Title', 'Contents'])
    df['Description'] = df['Description'].fillna('')

    df['Title'] = df['Title'].apply(remove_html).apply(normalize_text).apply(remove_special_char)
    df['Description'] = df['Description'].apply(remove_html).apply(normalize_text).apply(remove_special_char)
    df['Contents'] = df['Contents'].apply(remove_html).apply(normalize_text).apply(remove_special_char)


    df['Text'] = df['Title'] + ' ' + df['Description'] + ' ' + df['Contents']


    df = df[df['Text'].str.len() > 200]
    print(f'Sau lọc content ngắn: {len(df)} bài')

    return df