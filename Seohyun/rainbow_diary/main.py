from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google import genai  # 👈 임포트 방식이 새로워졌어!

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ⭐️ 서현님의 API 키를 넣어줘!
GOOGLE_API_KEY = "AIzaSyBeIzUcljCbRQY5Z6G2hWV0pZHMPQknz4o"

# 새로운 방식으로 제미나이 클라이언트 생성!
client = genai.Client(api_key=GOOGLE_API_KEY)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
async def chat_with_gemini(req: ChatRequest):
    user_text = req.message

    try:
        prompt = f"너는 다정하고 공감 능력이 뛰어난 일기장 챗봇이야. 사용자가 다음 일기를 썼어: '{user_text}'. 이 일기 내용에 대해 친근하고 따뜻하게 1~2문장으로 반말을 써서 대답해줘."

        # 새로운 SDK의 깔끔한 호출 방식! (최신 모델 사용)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        return {"reply": response.text}

    except Exception as e:
        return {"reply": f"제미나이 연결에 문제 발생 😭 (오류: {e})"}