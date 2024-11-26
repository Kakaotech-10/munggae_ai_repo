# main.py 파일 내용
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from src.bot import generate_response

app = FastAPI()


class PostContent(BaseModel):
    content: str


@app.post("/api/chatbot/v1")
async def reply(post_content: PostContent):
    if not post_content.content:
        raise HTTPException(status_code=400, detail="No content provided")

    response = generate_response(post_content.content)
    return {"response": response}


# uvicorn 명령어 예시
# uvicorn main:app --reload
# /opt/homebrew/bin/python3 -m uvicorn main:app --reload -> lucy환경실행