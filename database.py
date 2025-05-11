from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+pymysql://remote_user:your_password@3.36.97.66:3306/your_db_name"

engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



##### db 연결하고
각 data base에 연결하고 data전송하는 쿼리들 날리는 기능
예외처리는 data table 찾지 못할때는 loging처리
