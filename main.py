import crawler
import cleaning
import nlp_processing
import os

if __name__ == "__main__":
    df = crawler.scraper(crawler.categories)
    df = crawler.scraper_news_detail(df)
    df = cleaning.data_pipeline(df)
    
    df['Text_Segmented'] = df['Text'].apply(nlp_processing.tokenize_vi)
    
    folder_name = "data_output"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    file_path = os.path.join(folder_name, "vnexpress_data_clean.csv")
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    
    print(len(df))
    print(df[['Text']].head(2))