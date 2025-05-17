from db.database import session_local

#하나의 DB세션을 생성한다.
def get_db():
    db = session_local()
    try:
        yield db #FastAPI에서 의존성 주입에 사용됨.
    finally:
        db.close()
