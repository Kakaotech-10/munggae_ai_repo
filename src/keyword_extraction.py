import os
from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from konlpy.tag import Mecab
from collections import Counter

current_dir = os.path.dirname(os.path.abspath(__file__))
stopwords_path = os.path.join(current_dir, 'stopwords.txt')

# 1. 불용어 리스트 가져오기
try:
    with open(stopwords_path, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    print("불용어 리스트 불러오기 성공")
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {stopwords_path}")
except Exception as e:
    print(f"오류 발생: {e}")

# 2. Mecab 초기화
mecab = Mecab(dicpath='/usr/lib/mecab/dic/mecab-ko-dic')
#lucy환경에서 실행
#mecab = Mecab(dicpath='/opt/homebrew/lib/mecab/dic/mecab-ko-dic')

# 3. 텍스트 전처리 함수
def preprocess_texts(texts, stopwords, min_lenght = 2):
    all_nouns = []
    for text in texts:
        print(f"원본 텍스트: {text}")  # 원본 텍스트 확인
        normalized_text = normalize(text, english=True, number=True)
        print(f"정규화된 텍스트: {normalized_text}")  # 정규화 결과 확인
        nouns = mecab.nouns(normalized_text)
        print(f"추출된 명사: {nouns}")  # 명사 추출 결과 확인
        filtered_nouns = [noun for noun in nouns if len(noun) >= min_lenght and noun not in stopwords]
        print(f"불용어 및 최소 길이({min_lenght}) 필터링 후 명사: {filtered_nouns}")  # 불용어 필터링 결과 확인
        all_nouns.extend(filtered_nouns)
    return all_nouns


# 4. 키워드 추출 함수
def extract_keywords(texts, stopwords, min_lenght = 2):
    # 전처리 실행
    nouns = preprocess_texts(texts, stopwords, min_lenght = min_lenght)
    
    # 명사 리스트가 비어 있는지 확인
    if not nouns:
        print("추출된 명사가 없습니다. 입력 텍스트를 확인하세요.")
        return {
            "wordrank_keywords": [],
            "frequency_keywords": []
        }
        
    # KRWordRank 설정
    min_count = 1  # 최소 등장 횟수
    max_length = 10  # 키워드 최대 길이
    beta = 0.85  # PageRank의 decay factor
    max_iter = 10  # PageRank 반복 횟수
    
   # KRWordRank로 키워드 추출
    try:
        wordrank = KRWordRank(min_count=min_count, max_length=max_length, verbose=False)
        keywords, rank, graph = wordrank.extract([' '.join(nouns)], beta, max_iter)
        
    except ValueError as e:
        print(f"KRWordRank에서 오류 발생: {e}")
        return {
            "wordrank_keywords": [],
            "frequency_keywords": []
        }
        
    # 키워드 정렬
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    
    # 빈도 기반 키워드 추출
    keyword_counts = Counter(nouns)
    frequency_keywords = [word for word, count in keyword_counts.most_common(5)]

    
    return {
        "wordrank_keywords": sorted_keywords[:5],  # 상위 5개
        "frequency_keywords": keyword_counts  # 상위 5개
    }

