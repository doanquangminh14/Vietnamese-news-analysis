import crawler
import cleaning

if __name__ == "__main__":
    df_result = crawler.scraper(crawler.categories)
    df_result1 = crawler.scraper_news_detail(df_result)
    df_result1.to_csv("vnexpress_data_clean.csv", index=False, encoding='utf-8-sig')
    print(df_result1)
    print(df_result1.columns)