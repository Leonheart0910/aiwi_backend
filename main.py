# from sqlalchemy.orm import Session
#
# from gemini_api import call_gemini_api


from fastapi import FastAPI
from api.v1.routers import router as api_router  # 라우터 모듈 import
from fastapi.middleware.cors import CORSMiddleware

from exception.handler import set_error_handlers

app = FastAPI()

# # CORS 미들웨어 설정
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # 허용할 출처(클라이언트) 주소를 지정합니다.
#     allow_credentials=True,
#     allow_methods=["*"],  # 모든 HTTP 메소드 허용
#     allow_headers=["*"],  # 모든 헤더 허용
# )
app.include_router(api_router, prefix="/api/v1")

set_error_handlers(app)
#
# # DB 모델 생성
#
#
#

#
# app = FastAPI(title="상품 추천 AI 백엔드", description="Naver + Gemini 기반 FastAPI 서비스")
#
# # 의존성 주입용 DB 세션
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
#
# # ✅ 1. 회원가입 API
# @app.post("/signup")
# def signup(user: UserCreate, db: Session = Depends(get_db)):
#     # 이메일 중복 확인
#     existing = db.query(User).filter(User.email == user.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
#
#     new_user = User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#
#     return {"message": "회원가입 완료", "user_id": new_user.user_id}
#
# # ✅ 3. Gemini 기반 요약 생성 + 로그 저장
# @app.post("/generate")
# def generate_summary(chat: ChatRequest, db: Session = Depends(get_db)):
#     # Gemini 호출
#     ai_output = call_gemini_api(chat.user_input)
#
#     # log 저장 (chat_id는 예시로 1로 지정. 실제로는 동적 처리 필요)
#     log = AiwiLog(
#         user_input=chat.user_input,
#         ai_output1=ai_output["ai_output1"],
#         ai_output2=ai_output["ai_output2"],
#         ai_output3=ai_output["ai_output3"],
#         chat_id=1
#     )
#     db.add(log)
#     db.commit()
#
#     return {
#         "message": "Gemini 요약 생성 완료",
#         "data": ai_output
#     }
