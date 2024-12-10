# keyword_es.py
import pymysql
from elasticsearch import Elasticsearch
from src.keyword_extraction import extract_keywords, stopwords  # 키워드 추출 함수 import
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# .env 파일 로드
load_dotenv()

# MySQL 설정
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

# Elasticsearch 설정
ES_HOST = os.getenv("ES_HOST")
ES_PORT = os.getenv("ES_PORT")

# MySQL 데이터 가져오기
def fetch_data_from_mysql():
    # 오늘 날짜 가져오기
    today = datetime.now().strftime('%Y-%m-%d')
    #tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset="utf8mb4"
    )
    try:
        with connection.cursor() as cursor:
            # 오늘 추가된 게시물만 가져오는 쿼리
            query = """
                SELECT post_id, post_title, post_content, created_at
                FROM post
                WHERE DATE(created_at) = %s
            """
            cursor.execute(query, (today,))
            data = cursor.fetchall()
        return data
    finally:
        connection.close()
# Elasticsearch에 데이터 저장
def save_to_elasticsearch(es_client, index_name, postid, keywords):
    """
    각 키워드를 개별 문서로 저장하는 함수.
    """
    for keyword in keywords:
        doc = {
            "post_id": postid,
            "keyword": keyword
        }
        # Elasticsearch에 저장 (키워드를 기준으로 개별 문서로 저장)
        es_client.index(index=index_name, document=doc)

# 메인 실행 함수
def main():
    # MySQL 데이터 가져오기
    print("시작")
    data = fetch_data_from_mysql()
    print(f"mysql데이터는 : {data}")
    
    es_port = int(ES_PORT)
    
    # Elasticsearch 클라이언트 설정
    es = Elasticsearch([{"host": ES_HOST, "port": es_port, "scheme": "http"}])
    print(f"엘라스틱 서치 시작")
    # Elasticsearch 인덱스 이름 설정
    index_name = "keywords"

    # 데이터 처리 및 저장
    for row in data:
        postid, post_title, post_comment, created_at = row
        # 키워드 추출
        text = f"{post_title} {post_comment}"
        keywords = extract_keywords([text], stopwords)  # keyword_extraction.py에서 호출
        print(f"키워드는 : {keywords}")
        # Elasticsearch에 저장
        frequency_keywords = keywords["frequency_keywords"]
        print(f"추출된 빈도 기반 키워드: {frequency_keywords}")
        save_to_elasticsearch(es, index_name, postid, frequency_keywords)

    print("데이터 처리가 완료되었습니다.")

if __name__ == "__main__":
    main()
