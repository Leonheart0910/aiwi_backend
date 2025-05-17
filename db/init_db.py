from db.database import base, engine


# base에 등록된 모든 모델의 메타 정보를 기준으로 실제 DB에 테이블을 생성
def init():
    base.metadata.create_all(bind=engine)

# main파일을 실행시 init함수 실행됨.
if __name__ == "__main__":
    init()
