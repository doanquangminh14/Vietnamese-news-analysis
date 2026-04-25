from sqlalchemy import create_engine, Table, Column, Integer, Text, MetaData, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

# ================= DB CONFIG =================
DB_USER = "postgres"
DB_PASSWORD = "14102005"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "news_db"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

metadata = MetaData()

# ================= RAW TABLE =================
table_raw_articles = Table(
    "raw_articles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", Text),
    Column("content", Text),
    Column("category", Text),
    Column("url", Text, unique=True),
    Column("publish_date", Text),
)

# ================= PROCESSED TABLE =================
table_processed_articles = Table(
    "processed_articles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("article_id", Integer, ForeignKey("raw_articles.id"), unique=True),
    Column("sentiment", Text),
    Column("intent", Text),
    Column("processed_at", TIMESTAMP, server_default=func.now())
)

#  tạo bảng
metadata.create_all(engine)

# ================= INSERT RAW =================
def insert_raw_articles(df):
    with engine.begin() as conn:
        for _, row in df.iterrows():
            stmt = insert(table_raw_articles).values(
                title=row.get("Title"),
                content=row.get("Content"),
                category=row.get("Category"),
                url=row.get("Link"),
                publish_date=row.get("Publish_Date")
            ).on_conflict_do_nothing(index_elements=["url"])
            conn.execute(stmt)

# ================= GET UNPROCESSED =================
def get_unprocessed_articles(limit=20):
    query = """
    SELECT r.id, r.title, r.content, r.category
    FROM raw_articles r
    LEFT JOIN processed_articles p
    ON r.id = p.article_id
    WHERE p.article_id IS NULL
    LIMIT :limit
    """
    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        return result.fetchall()

# ================= INSERT PROCESSED =================
def insert_processed_article(article_id, sentiment, intent):
    with engine.begin() as conn:
        stmt = insert(table_processed_articles).values(
            article_id=article_id,
            sentiment=sentiment,
            intent=intent
        ).on_conflict_do_nothing(index_elements=["article_id"])
        conn.execute(stmt)