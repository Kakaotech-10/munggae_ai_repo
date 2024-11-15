# main.py 파일 내용
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일 로드
load_dotenv()

app = FastAPI()


class PostContent(BaseModel):
    content: str


# 환경 변수에서 API 키 가져오기
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_response(post_content):
    try:
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[
                {"role": "system",
                 "content":
                     """너는 게시글에 알맞은 답변을 해주는 챗봇이야. 답변은 한국어로 해줘. 답변은 반말로 해줘.
                       만약 정보를 물어본다거나, 도움이 필요한 글이거나 진지한 주제의 글이면 답변을 최대한 자세히 해줘.
                       만약 글이 일상적인 글이고 일상 공유를 하고 진지하지 않은 성격이면 친구처럼 간단하고 친근하게 답해줘. 가끔씩 이모지도 사용하면서 답해줘.
                     """},
                {"role": "user", "content": post_content}
            ]
        )
        return response.choices[0].message
    except Exception as e:
        print(f"Error generating response: {e}")
        return "답변을 생성하는 중 오류가 발생했습니다. 나중에 다시 시도해 주세요."


@app.post("/reply")
async def reply(post_content: PostContent):
    if not post_content.content:
        raise HTTPException(status_code=400, detail="No content provided")

    response = generate_response(post_content.content)
    return {"response": response}
