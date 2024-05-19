import urllib.parse

import sqlalchemy
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

server: str = "192.168.188.128"
port: str = "3306"
database: str = "ProjectData"
username: str = "rust"
password: str = "rust%admin123"

engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{username}:{password}@{server}:{port}/{database}",
                                  echo=True)
print(engine)
Base = declarative_base()


class User(Base):
    """
    用户信息表
    """
    __tablename__ = "user"

    Id = Column(String(50), nullable=False, primary_key=True)
    UserName = Column(String(50), nullable=False)
    PassWord = Column(String(50), nullable=False)
    Tokens = Column(BigInteger)  # 用户剩余的token数
    Email = Column(String(10), nullable=False)

