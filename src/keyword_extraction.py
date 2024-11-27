import requests
from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from konlpy.tag import Mecab
from collections import Counter

# 1. 불용어 리스트 가져오기
url = 'https://gist.githubusercontent.com/spikeekips/40d99e1ddc41b06412a6b913d9c9b5b8/raw/3ec2b98210903bd4c8f5b8481e0a8fd0de5e8fc3/stopwords-ko.txt'
response = requests.get(url)
stopwords = set(response.text.splitlines())

# 2. Mecab 초기화
mecab = Mecab(dicpath='/usr/lib/mecab/dic/mecab-ko-dic')

# 3. 텍스트 전처리 함수
def preprocess_texts(texts, stopwords):
    all_nouns = []
    for text in texts:
        # 텍스트 정규화
        normalized_text = normalize(text, english=True, number=True)
        # 명사 추출
        nouns = mecab.nouns(normalized_text)
        # 불용어 제거
        filtered_nouns = [noun for noun in nouns if noun not in stopwords]
        all_nouns.extend(filtered_nouns)
    return all_nouns

# 4. 키워드 추출 함수
def extract_keywords(texts, stopwords):
    # 전처리 실행
    nouns = preprocess_texts(texts, stopwords)
    
    # KRWordRank 설정
    min_count = 1  # 최소 등장 횟수
    max_length = 10  # 키워드 최대 길이
    beta = 0.85  # PageRank의 decay factor
    max_iter = 10  # PageRank 반복 횟수
    
    # KRWordRank로 키워드 추출
    wordrank = KRWordRank(min_count=min_count, max_length=max_length, verbose=False)
    keywords, rank, graph = wordrank.extract([' '.join(nouns)], beta, max_iter)
    
    # 키워드 정렬
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    
    # 빈도 기반 키워드 추출
    keyword_counts = Counter(nouns)
    
    return {
        "wordrank_keywords": sorted_keywords[:10],  # 상위 10개
        "frequency_keywords": keyword_counts.most_common(10)  # 상위 10개
    }

