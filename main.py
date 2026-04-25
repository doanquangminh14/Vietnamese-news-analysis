import os
import crawler
import etl
from data import insert_raw_articles

def main():
    print(" Bắt đầu pipeline...")
    print(" Đang crawl dữ liệu...")
    df = crawler.run_crawler()
    if df is None or df.empty:
        print(" Không có dữ liệu crawl được!")
        return
    print(f"Crawl được {len(df)} bài")


    print(" Đang xử lý dữ liệu (ETL)...")
    df_clean = etl.data_pipeline(df)
    if df_clean.empty:
        print(" Dữ liệu sau ETL rỗng!")
        return
    print(f" Sau ETL còn {len(df_clean)} bài")


    os.makedirs("data_output", exist_ok=True)
    output_path = os.path.join("data_output", "vnexpress_data_clean.csv")
    df_clean.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f" Đã lưu file: {output_path}")

    print(" Đang lưu vào PostgreSQL...")
    insert_raw_articles(df_clean)

    print(" Đã lưu vào database (raw_articles)")

    print(" Pipeline hoàn thành!")


if __name__ == "__main__":
    main()