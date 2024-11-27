# Python 3.11 이미지 사용
FROM python:3.11-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    mecab \
    mecab-ipadic-utf8 \
    libmecab-dev \
    && apt-get clean



# AWS CLI 설치 (S3 파일 다운로드용)
RUN apt-get update && apt-get install -y awscli && apt-get clean

# 작업 디렉토리 설정
WORKDIR /app

RUN mkdir -p /usr/lib/mecab/dic/mecab-ko-dic \
    && curl -o mecab-ko-dic.tar.gz https://munggae-ai-mecab.s3.ap-northeast-2.amazonaws.com/mecab-ko-dic.tar.gz \
    && tar -xzf mecab-ko-dic.tar.gz -C /usr/lib/mecab/dic/mecab-ko-dic \
    && rm mecab-ko-dic.tar.gz

# Mecab 설정 파일 생성
RUN echo "dicdir = /usr/lib/mecab/dic" > /usr/local/etc/mecabrc

ENV MECABRC=/usr/local/etc/mecabrc

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir nltk networkx && pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir konlpy mecab-python3

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8001

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

