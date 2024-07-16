"""
Des 统一用户鉴权接口
@Author thetheOrange
Time 2024/5/19
"""
import hashlib
import time
import uuid

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity
from sqlalchemy.orm import sessionmaker

from Core.StatusCode import StatusCode
from Core.Tools.generate_uuid import create_uuid
from Core.Tools.md5_password import get_md5
from Model.model import engine, User, Admin
from config import config_json
from . import auth_blu


@auth_blu.route("/auth/register", methods=["POST"])
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
        is_same_name: User = session.query(User).filter(User.UserName == user_name).first()
        # 查询注册的用户名是否重名
        if is_same_name:
            return jsonify({"code": StatusCode.UserNameRepeat, "msg": "用户名已存在"})
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
                                  Email=user_email,
                                  PicTimes=0)
            session.add(new_user)
            session.commit()
            return jsonify({"code": 0, "msg": "用户注册成功"})


@auth_blu.route("/auth/login", methods=["POST"])
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
        user_info: User = session.query(User).filter(User.UserName == user_name,
                                                     User.PassWord == get_md5(pass_word)).first()
        return jsonify({"code": 0,
                        "msg": "用户登录成功",
                        "uuid": user_info.Id,
                        "username": user_info.UserName,
                        "tokens": user_info.Tokens,
                        "picTimes": user_info.PicTimes}) if user_info \
            else jsonify({"code": StatusCode.LoginError, "msg": "用户登录失败"})


# ================================ 后台管理界面鉴权start ================================

@auth_blu.route("/admin/login", methods=["POST"])
def admin_login() -> Response:
    """
    后台登录接口

    :return: json
    """
    admin: str = request.json.get("admin")
    password: str = request.json.get("password")

    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        admin_info: Admin = session.query(Admin).filter(Admin.Admin == admin,
                                                        Admin.PassWord == password).first()
        return jsonify({
            "access_token": create_access_token(identity=admin),
            "refresh_token": create_refresh_token(identity=admin),
            "app_info": {
                "app_id": config_json["api"].get("APPID"),
                "api_key": config_json["api"].get("APIKEY"),
                "api_secret": config_json["api"].get("API_SECRET")
            },
            "code": 0,
            "msg": "管理员登录成功"
        }) if admin_info else jsonify({"code": StatusCode.LoginError, "msg": "登录失败"})


@auth_blu.route("/admin/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh_jwt() -> Response:
    """
    刷新管理员jwt令牌

    :return: json
    """

    admin: str = get_jwt_identity()
    return jsonify({
        "access_token": create_access_token(identity=admin),
        "code": 0,
        "msg": "刷新令牌成功"
    })

# ================================ 后台管理界面鉴权end ================================
