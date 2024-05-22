"""
Des 统一用户鉴权接口
@Author thetheOrange
Time 2024/5/19
"""
import hashlib
import time
import uuid

from flask import request, jsonify, Response
from sqlalchemy.orm import sessionmaker

from Core.StatusCode import StatusCode
from Model.model import engine, User
from . import auth_blu

# 特殊字符串 加盐
CODE: str = "#_#"


def get_md5(pwd: str) -> str:
    """
    md5加密用户密码

    :pwd: 用户密码
    :return: 返回MD5加密后的用户密码
    """
    pwd += CODE
    md5 = hashlib.md5()
    md5.update(pwd.encode("utf-8"))
    return md5.hexdigest()


def create_uuid(user_name: str) -> str:
    """
    根据时间戳和用户名创建唯一的uuid

    :return: 返回唯一的uuid
    """
    time_stamp: float = time.time()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{time_stamp}{user_name}").hex)


@auth_blu.route("/register", methods=["POST"])
def register() -> Response:
    """
    注册接口

    :return: 返回注册是否成功的json消息
    """
    # 新用户的数据
    user_name: str = request.json.get("username").strip()
    pass_word: str = request.json.get("password").strip()
    user_email: str = request.json.get("email").strip()

    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        same_name: User = session.query(User).filter(User.UserName == user_name).first()
        # 查询注册的用户名是否重名
        if same_name:
            return jsonify({"code": StatusCode.RegisterError, "msg": "用户名已存在"})
        else:
            # 加密用户密码
            pass_word = get_md5(pass_word)
            # 生成唯一的uuid
            user_uuid: str = create_uuid(user_name)

            # 存储注册的用户信息
            new_user: User = User(Id=user_uuid,
                                  UserName=user_name,
                                  PassWord=pass_word,
                                  Tokens=0,
                                  Email=user_email)
            session.add(new_user)
            session.commit()
            return jsonify({"code": 0, "msg": "用户注册成功"})


@auth_blu.route("/login", methods=["POST"])
def login() -> Response:
    """
    登录接口

    :return: 返回用户是否登录成功的json信息
    """
    # 用户的数据
    user_name: str = request.json.get("username").strip()
    pass_word: str = request.json.get("password").strip()

    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        is_login: User = session.query(User).filter(User.UserName == user_name,
                                                    User.PassWord == get_md5(pass_word))
        return jsonify({"code": 0, "msg": "用户登录成功"}) if is_login \
            else jsonify({"code": StatusCode.LoginError, "msg": "用户登录失败"})
