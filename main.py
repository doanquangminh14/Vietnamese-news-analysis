import crawler
import cleaning
import nlp_processing

if __name__ == "__main__":
    df = crawler.scraper(crawler.categories)
    
    df = crawler.scraper_news_detail(df)
    
    df = cleaning.data_pipeline(df)
    
    df['Text_Segmented'] = df['Text'].apply(nlp_processing.tokenize_vi)
    
    df.to_csv("vnexpress_data_clean.csv", index=False, encoding='utf-8-sig')
    
    print(len(df))
    print(df[['Text']].head(2))