import pandas as pd
import re
import unicodedata


def remove_html(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;|&amp;|&lt;|&gt;', ' ', text)
    return text


def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFC', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def remove_special_char(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r'[^a-zA-Z0-9à-ỹ\s]', ' ', text)


def data_pipeline(df):
    # tránh warning
    df = df.copy()

    # chuẩn hóa tên cột (rất nên làm)
    df.columns = df.columns.str.strip()

    # drop duplicate theo link
    df = df.drop_duplicates(subset=['Link'])

    # drop missing
    df = df.dropna(subset=['Title', 'Content'])

    # clean text
    df['Title'] = df['Title'].apply(remove_html)\
                             .apply(normalize_text)\
                             .apply(remove_special_char)

    df['Content'] = df['Content'].apply(remove_html)\
                                  .apply(normalize_text)\
                                  .apply(remove_special_char)

    # combine
    df['Text'] = df['Title'] + ' ' + df['Content']

    return df