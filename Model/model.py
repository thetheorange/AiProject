"""
Des User orm对象关系映射
@Author thetheOrange
Time 2024/5/21
"""
import urllib

import sqlalchemy
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

server: str = "192.168.188.128"
port: int = 3306
database: str = "User"
username: str = "rust"
password: str = urllib.parse.quote("...")


engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@{server}:{port}/{database}?charset=utf8mb4",
                                  echo=False)
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
    PicTimes = Column(BigInteger)
