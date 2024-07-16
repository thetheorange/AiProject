"""
Des User orm对象关系映射
@Author thetheOrange
Time 2024/5/21
"""
import urllib

import sqlalchemy
from sqlalchemy import Column, String, BigInteger, INTEGER, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config import config_json

server: str = config_json["mysql"]["server"]
port: int = config_json["mysql"]["port"]
database: str = config_json["mysql"]["database"]
username: str = config_json["mysql"]["username"]
password: str = urllib.parse.quote(config_json["mysql"]["password"])

engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@{server}:{port}/{database}?charset=utf8mb4",
                                  echo=True)
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
    Academy = Column(String(100))


class Admin(Base):
    """
    管理员信息表
    """

    __tablename__ = "admin"

    Id = Column(String(50), nullable=False, primary_key=True)
    Auth = Column(INTEGER)
    Admin = Column(String(20), nullable=False)
    PassWord = Column(String(50), nullable=False)


class Token(Base):
    """
    令牌信息表
    """

    __tablename__ = "token"

    Id = Column(String(50), nullable=False, primary_key=True)
    Tokens = Column(BigInteger, nullable=False)
    PicTimes = Column(BigInteger, nullable=False)
    TokenRange = Column(String(100), nullable=False)
    Name = Column(String(100), nullable=False)
    Available = Column(INTEGER, nullable=False)


class UserToken(Base):
    """
    用户和令牌的关联表
    """

    __tablename__ = 'user_token'

    UserId = Column(String(50), ForeignKey('user.Id'), primary_key=True)
    TokenId = Column(String(50), ForeignKey('token.Id'), primary_key=True)

    user = relationship("User", backref="user_tokens")
    token = relationship("Token", backref="user_tokens")
