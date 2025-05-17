from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv() #.env  파일에서 DB 접속 정보를 불러온다.

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


database_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#실제로 DB와 연결하는 SQLAlchemy엔진 생성
engine = create_engine(
    database_url,
    pool_pre_ping=True
)

#DB에 쿼리할 수 있는 세션 객체 생성
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 엔티티 모델 클래스가 상속할 declarative_base 객체
base = declarative_base()
