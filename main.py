from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel, Field

from src.keyword_extraction import extract_keywords, stopwords

# FastAPI 인스턴스 생성
app = FastAPI()


#로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 요청 데이터 모델 정의
# class TextRequest(BaseModel):
#     texts: list[str] = Field(..., examples = ["키워드 추출입니다." ,"키워드를 어떻게 추출해야 할까?", "어떤것이 키워드일까?"])  # "texts"는 문자열 리스트여야 함

# 게시글 데이터 모델
class TextRequest(BaseModel):
    title: str = Field(..., example="게시글 제목")
    content: str = Field(..., example="게시글 본문")

# 댓글 데이터 모델
class CommentRequest(BaseModel):
    post_id: int = Field(..., example=1)  # 댓글이 달릴 게시글의 ID
    comment: str = Field(..., example="댓글 내용")
    
@app.post("/api/v2/text/keyword")
async def extract_keywords_api(request: TextRequest):
    try:
        # 제목과 본문을 리스트로 전달
        texts = [request.title, request.content]
        logger.info(f"request.title = {request.title}")
        logger.info(f"request.content = {request.content}")

        if not texts or not isinstance(texts, list):
            raise HTTPException(status_code=400, detail="Invalid input: 'texts' must be a non-empty list of strings.")

        # 키워드 추출 실행
        results = extract_keywords(texts, stopwords)
        
        # 결과 반환
        return {
            "wordrank_keywords": results["wordrank_keywords"],
            "frequency_keywords": results["frequency_keywords"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/v2/comment/keyword")
async def extract_comment_keywords(request: CommentRequest):
    """
    댓글 내용에서 키워드를 추출합니다.
    """
    try:
        # 댓글 내용을 리스트로 전달
        texts = [request.comment]
        
        logger.info(f"request.comment = {request.comment}")
        
        # 키워드 추출 실행
        results = extract_keywords(texts, stopwords)
        
        # 결과 반환
        return {
            "wordrank_keywords": results["wordrank_keywords"],
            "frequency_keywords": results["frequency_keywords"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# uvicorn 명령어 예시
# uvicorn main:app --reload
# /opt/homebrew/bin/python3 -m uvicorn main:app --reload -> lucy환경실행
