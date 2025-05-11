from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, Aiwi, AiwiLog
from schemas import UserCreate, ChatRequest
from naver_api import search_naver_shopping
from gemini_api import call_gemini_api

# DB 모델 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="상품 추천 AI 백엔드", description="Naver + Gemini 기반 FastAPI 서비스")

# 의존성 주입용 DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ 1. 회원가입 API
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "회원가입 완료", "user_id": new_user.user_id}


# ✅ 2. 네이버 쇼핑 검색 API
@app.post("/search")
def search_item(chat: ChatRequest):
    result = search_naver_shopping(chat.user_input)
    if not result:
        raise HTTPException(status_code=500, detail="네이버 API 호출 실패")
    return result


# ✅ 3. Gemini 기반 요약 생성 + 로그 저장
@app.post("/generate")
def generate_summary(chat: ChatRequest, db: Session = Depends(get_db)):
    # Gemini 호출
    ai_output = call_gemini_api(chat.user_input)

    # log 저장 (chat_id는 예시로 1로 지정. 실제로는 동적 처리 필요)
    log = AiwiLog(
        user_input=chat.user_input,
        ai_output1=ai_output["ai_output1"],
        ai_output2=ai_output["ai_output2"],
        ai_output3=ai_output["ai_output3"],
        chat_id=1
    )
    db.add(log)
    db.commit()

    return {
        "message": "Gemini 요약 생성 완료",
        "data": ai_output
    }
