# aiwi_backend
[클라우드 컴퓨팅 8팀 과제] LLM 기반 쇼핑 리스트 서비스

your_project/
├── api/          # 🔹 FastAPI 라우터 (엔드포인트만 담당)
├── core/         # 🔹 앱 전역 설정: config, database, dependencies 등
├── crud/         # 🔹 실제 DB 쿼리 로직 (create, read, update, delete)
├── db/           # 🔹 (선택) DB 초기화 스크립트나 마이그레이션 등
├── models/       # 🔹 SQLAlchemy ORM 엔티티
├── schemas/      # 🔹 Pydantic 스키마 (요청/응답 정의)
├── main.py       # 🔹 FastAPI 앱 진입점
└── .env          # 🔹 환경변수

