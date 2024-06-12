"""
Des User orm对象关系映射
@Author thetheOrange
Time 2024/5/21
"""
import urllib

import sqlalchemy
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

from config import config_json

server: str = config_json["mysql"]["server"]
port: int = config_json["mysql"]["port"]
database: str = config_json["mysql"]["database"]
username: str = config_json["mysql"]["username"]
password: str = urllib.parse.quote(config_json["mysql"]["password"])


engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@{server}:{port}/{database}?charset=utf8mb4",
                                  echo=False)
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
