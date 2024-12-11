from dotenv import load_dotenv
import openai
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 정의되어 있지 않습니다.")

# OpenAI API 키 설정
openai.api_key = api_key


def generate_response(post_content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
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
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error generating response: {e}")
        return "답변을 생성하는 중 오류가 발생했습니다. 나중에 다시 시도해 주세요."




def code_review_bot(post_content):
    """
    게시글에 포함된 코드를 분석하여 개선할 부분을 알려주는 챗봇 함수.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content":
                     """
                     You are a best code reviewr.
                     You need to review the code and make comment of that input code.
                     In your response, Dont say anything else except what i tell you.
                     {
                     1. The line number of code that needs to be changed.
                     2. Changed, fixed code of that line.
                     3. The reason of the changement. Explain this as detail as you can.
                     }
                     If there are more than 1 line that needs to be fixed, fix all the line with this format.
                     
                     Make answer format like i said. Number them.
                     Answer in Korean.
                     """},
                {"role": "user", "content": post_content}
            ]
        )
        # GPT 모델의 응답 가져오기
        return response.choices[0].message['content']

    except Exception as e:
        print(f"Error generating response: {e}")
        return "코드 리뷰를 생성하는 중 오류가 발생했습니다. 나중에 다시 시도해 주세요."

