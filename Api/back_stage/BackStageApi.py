from typing import List

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity
from sqlalchemy.orm import sessionmaker

from Core.Models.TextSocket import TextModel
from Core.StatusCode import StatusCode
from Core.Tools.generate_uuid import create_uuid
from Core.Tools.md5_password import get_md5
from Logging import app_logger
from Model.model import engine, User, Admin, Token, UserToken
from config import config_json
from . import back_stage_blu

APPID = config_json["api"]["APPID"]
APIKEY = config_json["api"]["APIKEY"]
API_SECRET = config_json["api"]["API_SECRET"]
GPT_URL = config_json["api"]["GPT_URL"]
DOMAIN = config_json["api"]["DOMAIN"]


@back_stage_blu.route("/admin/console_test", methods=["POST"])
@jwt_required()
def console_test() -> Response:
    """
    控制台测试接口

    :return: json
    """

    try:
        dialog: List[dict] = request.json.get("dialog")
        limit: int = request.json.get("limit")
        top_k: int = request.json.get("top_k")
        temperature: int = request.json.get("temperature")

        text_chat_session: TextModel = TextModel(APPID=APPID,
                                                 APIKey=APIKEY,
                                                 APISecret=API_SECRET,
                                                 GptUrl=GPT_URL,
                                                 Domain=DOMAIN,
                                                 config={
                                                     "temperature": temperature,
                                                     "max_tokens": limit,
                                                     "top_k": top_k
                                                 })
        text_chat_session.chat(dialog)
        consume_token, response_text = text_chat_session.chat(dialog)
        return jsonify({
            "content": response_text,
            "consume_token": consume_token,
            "code": 0,
            "msg": "文本模型回复成功"
        })
    except Exception as e:
        app_logger.error(f"[TEXT MODEL] {e}")
        return jsonify({
            "code": StatusCode.ModelError,
            "msg": "回复失败"
        })


@back_stage_blu.route("/admin/add_normal_user", methods=["POST"])
@jwt_required()
def add_normal_user() -> Response:
    """
    添加普通用户接口

    :return: json
    """

    try:
        username: str = request.json.get("username")
        password: str = request.json.get("password")
        tokens: int = request.json.get("tokens")
        email: str = request.json.get("email")
        pictimes: int = request.json.get("pictimes")
        academy: str = request.json.get("academy")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            is_same_name: User = session.query(User).filter(User.UserName == username).first()
            # 查询添加的用户是否重名
            if is_same_name:
                return jsonify({"code": StatusCode.UserNameRepeat,
                                "msg": "用户名已存在"})
            else:
                # 加密用户密码
                pass_word = get_md5(password)
                # 生成唯一的uuid
                user_uuid: str = create_uuid(username)

                # 存储注册的用户信息
                new_user: User = User(Id=user_uuid,
                                      UserName=username,
                                      PassWord=pass_word,
                                      Tokens=tokens,
                                      Email=email,
                                      PicTimes=pictimes,
                                      Academy=academy)
                session.add(new_user)
                session.commit()
                return jsonify({"code": 0, "msg": "添加用户成功"})
    except Exception as e:
        app_logger.error(f"[ADD NORMAL USER] {e}")
        return jsonify({
            "code": StatusCode.AddUserError,
            "msg": "添加用户失败"
        })


@back_stage_blu.route("/admin/modify_normal_user", methods=["POST"])
@jwt_required()
def modify_normal_user() -> Response:
    """
    修改用户信息接口

    :return: json
    """

    try:
        target_user: str = request.json.get("target_user")
        new_user_info: dict = request.json.get("new_user_info")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            target_user_info: User = session.query(User).filter(User.UserName == target_user).first()
            if not target_user_info:
                return jsonify({
                    "code": StatusCode.UserNotFound,
                    "msg": "找不到目标用户"
                })
            else:
                # 查看新的用户名是否重名
                is_same_user: User = session.query(User).filter(
                    User.UserName == new_user_info.get("new_username")).first()
                if is_same_user:
                    return jsonify({
                        "code": StatusCode.UserNameRepeat,
                        "msg": "用户名已存在"
                    })
                else:
                    target_user_info.Id = create_uuid(new_user_info["new_username"])
                    target_user_info.UserName = new_user_info["new_username"]
                    target_user_info.PassWord = get_md5(new_user_info["new_password"])
                    target_user_info.Tokens = new_user_info["new_tokens"]
                    target_user_info.Email = new_user_info["new_email"]
                    target_user_info.PicTimes = new_user_info["new_pictimes"]
                    target_user_info.Academy = new_user_info["new_academy"]

                    session.commit()

                    return jsonify({
                        "code": 0,
                        "msg": "修改用户信息成功"
                    })
    except Exception as e:
        app_logger.error(f"[MODIFY NORMAL USER] {e}")
        return jsonify({
            "code": StatusCode.ModifyUserError,
            "msg": "修改用户消息错误"
        })


@back_stage_blu.route("/admin/delete_normal_user", methods=["POST"])
@jwt_required()
def delete_normal_user() -> Response:
    """
    删除用户接口

    :return: json
    """

    try:
        target_username: str = request.json.get("target_username")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            # 查看目标用户是否存在
            is_user_exit: User = session.query(User).filter(User.UserName == target_username).first()
            if is_user_exit:
                session.query(User).filter(User.UserName == target_username).delete()
                session.commit()

                return jsonify({
                    "code": 0,
                    "msg": f"{target_username} 删除成功"
                })
            else:
                return jsonify({
                    "code": StatusCode.UserNotFound,
                    "msg": "目标用户不存在"
                })
    except Exception as e:
        app_logger.error(f"[DELETE NORMAL USER] {e}")
        return jsonify({
            "code": StatusCode.DeleteUserError,
            "msg": "目标用户删除失败"
        })


@back_stage_blu.route("/admin/add_admin", methods=["POST"])
@jwt_required()
def add_admin() -> Response:
    """
    添加管理员用户接口

    :return: json
    """

    try:
        current_admin: str = get_jwt_identity()
        admin: str = request.json.get("admin")
        password: str = request.json.get("password")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            # 检查是否为超级管理员 0 为超级管理员 1 为普通管理员
            if not session.query(Admin).filter(Admin.Admin == current_admin).first().Auth:
                return jsonify({"code": StatusCode.PermissionNotAllow, "msg": "权限不足"})
            is_same_name: Admin = session.query(Admin).filter(Admin.Admin == admin).first()
            # 查询添加的用户是否重名
            if is_same_name:
                return jsonify({"code": StatusCode.UserNameRepeat,
                                "msg": "管理员用户名已存在"})
            else:
                # 加密用户密码
                pass_word = get_md5(password)
                # 生成唯一的uuid
                admin_uuid: str = create_uuid(admin)

                # 存储注册的用户信息
                new_admin: Admin = Admin(
                    Id=admin_uuid,
                    Auth=1,
                    Admin=admin,
                    PassWord=pass_word
                )
                session.add(new_admin)
                session.commit()
                return jsonify({"code": 0, "msg": "添加管理员成功"})
    except Exception as e:
        app_logger.error(f"[ADD ADMIN] {e}")
        return jsonify({"code": StatusCode.AddAdminError, "msg": "添加管理员失败"})


@back_stage_blu.route("/admin/modify_admin", methods=["POST"])
@jwt_required()
def modify_admin() -> Response:
    """
    修改管理员用户信息接口

    :return: json
    """

    try:
        current_admin: str = get_jwt_identity()
        target_admin: str = request.json.get("target_admin")
        new_name: str = request.json.get("new_name")
        new_password: str = request.json.get("new_password")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            # 检查是否为超级管理员
            if not session.query(Admin).filter(Admin.Admin == current_admin).first().Auth:
                return jsonify({"code": StatusCode.PermissionNotAllow, "msg": "权限不足"})
            target_admin_info: Admin = session.query(Admin).filter(Admin.Admin == target_admin).first()
            if not target_admin_info:
                return jsonify({
                    "code": StatusCode.UserNotFound,
                    "msg": "找不到目标用户"
                })
            # 查看新的用户名是否重名
            is_same_user: Admin = session.query(Admin).filter(Admin.Admin == new_name).first()
            if is_same_user:
                return jsonify({
                    "code": StatusCode.UserNameRepeat,
                    "msg": "用户名已存在"
                })
            else:
                if new_name:
                    target_admin_info.Admin = new_name
                    target_admin_info.Id = create_uuid(new_name)
                if new_password:
                    target_admin_info.PassWord = get_md5(new_password)

                session.commit()

                return jsonify({
                    "code": 0,
                    "msg": "修改用户信息成功"
                })
    except Exception as e:
        app_logger.error(f"[MODIFY ADMIN] {e}")
        return jsonify({"code": StatusCode.ModifyAdminError, "msg": "修改管理员信息错误"})


@back_stage_blu.route("/admin/delete_admin", methods=["POST"])
@jwt_required()
def delete_admin() -> Response:
    """
    删除管理员接口

    :return: json
    """
    try:
        current_admin: str = get_jwt_identity()
        target_admin: str = request.json.get("target_admin")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            # 检查是否为超级管理员
            if not session.query(Admin).filter(Admin.Admin == current_admin).first().Auth:
                return jsonify({"code": StatusCode.PermissionNotAllow, "msg": "权限不足"})
            # 查看目标用户是否存在
            is_user_exit: Admin = session.query(Admin).filter(Admin.Admin == target_admin).first()
            if is_user_exit:
                session.query(Admin).filter(Admin.Admin == target_admin).delete()
                session.commit()

                return jsonify({
                    "code": 0,
                    "msg": f"{target_admin} 删除成功"
                })
            else:
                return jsonify({
                    "code": StatusCode.UserNotFound,
                    "msg": "目标用户不存在"
                })
    except Exception as e:
        app_logger.error(f"[DELETE ADMIN] {e}")
        return jsonify({
            "code": StatusCode.DeleteAdminError,
            "msg": "目标用户删除失败"
        })


@back_stage_blu.route("/admin/add_token", methods=["POST"])
@jwt_required()
def add_token() -> Response:
    """
    添加令牌接口

    :return: json
    """

    try:
        token_name: str = request.json.get("token_name")
        # 令牌额度
        token_limit: dict = request.json.get("token_limit")
        # 令牌适用范围 学院名
        token_range: str = request.json.get("token_range")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            # 检查令牌名是否重复
            has_same_token: Token = session.query(Token).filter(Token.Name == token_name).first()
            if has_same_token:
                return jsonify({"code": StatusCode.TokenRepeat, "msg": "令牌重名"})
            else:
                new_token: Token = Token(
                    Id=create_uuid(token_name),
                    Tokens=token_limit.get("tokens") if token_limit.get("tokens") else 0,
                    PicTimes=token_limit.get("pictimes") if token_limit.get("pictimes") else 0,
                    TokenRange=token_range,
                    Name=token_name,
                    Available=1
                )
                session.add(new_token)
                session.commit()

                return jsonify({"code": 0, "msg": "创建令牌成功"})
    except Exception as e:
        app_logger.error(f"[ADD TOKEN] {e}")
        return jsonify({"code": StatusCode.AddTokenError, "msg": "添加令牌失败"})


@back_stage_blu.route("/admin/modify_token", methods=["POST"])
@jwt_required()
def modify_token() -> Response:
    """
    修改令牌消息接口

    :return: json
    """

    try:
        target_token: str = request.json.get("target_token")
        new_token_limit: dict = request.json.get("new_token_limit")
        new_token_range: str = request.json.get("new_token_range")
        new_token_is_available: int = request.json.get("new_token_is_available")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            target_token_info: Token = session.query(Token).filter(Token.Name == target_token).first()
            if not target_token_info:
                return jsonify({
                    "code": StatusCode.TokenNotFound,
                    "msg": "找不到目标令牌"
                })
            else:
                target_token_info.Tokens = new_token_limit["tokens"]
                target_token_info.PicTimes = new_token_limit["pictimes"]
                target_token_info.TokenRange = new_token_range
                target_token_info.Available = new_token_is_available

                session.commit()

                return jsonify({"code": 0, "msg": "令牌修改成功"})
    except Exception as e:
        app_logger.error(f"[MODIFY TOKEN] {e}")
        return jsonify({"code": StatusCode.ModifyTokenError, "msg": "修改令牌错误"})


@back_stage_blu.route("/admip/control_token", methods=["GET"])
@jwt_required()
def control_token() -> Response:
    """
    禁用/启用令牌接口

    :return: json
    """

    try:
        is_available: int = int(request.args.get("is_available"))
        target_token: str = request.args.get("token_name")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            target_token_info: Token = session.query(Token).filter(Token.Name == target_token).first()
            if not target_token_info:
                return jsonify({
                    "code": StatusCode.TokenNotFound,
                    "msg": "找不到目标令牌"
                })
            else:
                target_token_info.Available = is_available

                session.commit()

                return jsonify({"code": 0, "msg": f"令牌{'启用' if target_token_info.Available else '禁用'}成功"})
    except Exception as e:
        app_logger.error(f"[CONTROL TOKEN] {e}")
        return jsonify({"code": StatusCode.ControlTokenError, "msg": "修改令牌状态信息失败"})


@back_stage_blu.route("/admin/query_table", methods=["GET"])
@jwt_required()
def query_user_table() -> Response:
    """
    根据指定范围查询表

    :return: json
    """

    try:
        table: str = request.args["table"].strip().lower()
        query_range: int = int(request.args["query_range"])
        start: int = int(request.args["start"])

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            if table == "user":
                query_ret = session.query(User).order_by(User.Id).limit(query_range).offset(start).all()
                return jsonify({
                    "code": 0,
                    "msg": f"查询{len(query_ret)}条信息成功",
                    "data": [
                        {
                            "Id": user.Id,
                            "UserName": user.UserName,
                            "PassWord": user.PassWord,
                            "Tokens": user.Tokens,
                            "Email": user.Email,
                            "PicTimes": user.PicTimes,
                            "Academy": user.Academy
                        } for user in query_ret
                    ]
                })
            elif table == "admin":
                query_ret = session.query(Admin).order_by(Admin.Id).limit(query_range).offset(start).all()
                return jsonify({
                    "code": 0,
                    "msg": f"查询{len(query_ret)}条信息成功",
                    "data": [
                        {
                            "Id": admin.Id,
                            "Auth": admin.Auth,
                            "Admin": admin.Admin,
                            "Password": admin.PassWord
                        } for admin in query_ret
                    ]
                })
            elif table == "token":
                query_ret = session.query(Token).order_by(Token.Id).limit(query_range).offset(start).all()
                return jsonify({
                    "code": 0,
                    "msg": f"查询{len(query_ret)}条信息成功",
                    "data": [
                        {
                            "Id": token.Id,
                            "Tokens": token.Tokens,
                            "PicTimes": token.PicTimes,
                            "TokenRange": token.TokenRange,
                            "Name": token.Name,
                            "Available": token.Available
                        } for token in query_ret
                    ]
                })
            else:
                return jsonify({
                    "code": StatusCode.TableNotFound,
                    "msg": "未查询到指定表"
                })
    except Exception as e:
        app_logger.error(f"[QUERY TABLE] {e}")
        return jsonify({
            "code": StatusCode.QueryTableError,
            "msg": "查询时遇到错误"
        })


@back_stage_blu.route("/admin/query_table_data", methods=["GET"])
@jwt_required()
def query_table_data() -> Response:
    """
    查询指定表中的指定数据

    :return: json
    """

    try:
        table: str = request.args["table"]
        target_name: str = request.args["target_name"]

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            if table == "user":
                query_ret: User = session.query(User).filter(User.UserName == target_name).first()
                return jsonify({
                    "code": 0,
                    "msg": f"查询{query_ret.UserName}成功",
                    "data": {
                            "Id": query_ret.Id,
                            "UserName": query_ret.UserName,
                            "PassWord": query_ret.PassWord,
                            "Tokens": query_ret.Tokens,
                            "Email": query_ret.Email,
                            "PicTimes": query_ret.PicTimes,
                            "Academy": query_ret.Academy
                        }
                })
            elif table == "admin":
                query_ret: Admin = session.query(Admin).filter(Admin.Admin == target_name).first()
                return jsonify({
                    "code": 0,
                    "msg": f"查询{query_ret.Admin}成功",
                    "data": {
                            "Id": query_ret.Id,
                            "Auth": query_ret.Auth,
                            "Admin": query_ret.Admin,
                            "PassWord": query_ret.PassWord
                        }
                })
            elif table == "token":
                query_ret: Token = session.query(Token).filter(Token.Name == target_name).first()
                return jsonify({
                    "code": 0,
                    "msg": f"查询{query_ret.Name}成功",
                    "data": {
                            "Id": query_ret.Id,
                            "Tokens": query_ret.Tokens,
                            "PicTimes": query_ret.PicTimes,
                            "TokenRange": query_ret.TokenRange,
                            "Name": query_ret.Name,
                            "Available": query_ret.Available
                        }
                })
            else:
                return jsonify({
                    "code": StatusCode.TableNotFound,
                    "msg": "未查询到指定表"
                })

    except Exception as e:
        app_logger.error(f"[QUERY TABLE SPECIFY DATA] {e}")
        return jsonify({
            "code": StatusCode.QueryTableDataError,
            "msg": "查询时遇到错误"
        })


@back_stage_blu.route("/user/get_token", methods=["POST"])
def get_token() -> Response:
    """
    用户兑换令牌接口

    :return: json
    """

    try:
        token_id: str = request.json.get("token_id")
        user_id: str = request.json.get("user_id")
        user_academy: str = request.json.get("user_academy")

        DBSession = sessionmaker(bind=engine)
        with DBSession() as session:
            # 检查令牌是否存在和有效
            token: Token = session.query(Token).filter(Token.Id == token_id,
                                                       Token.TokenRange == user_academy,
                                                       Token.Available == 1).first()
            # 检查用户是否存在
            target_user: User = session.query(User).filter(User.Id == user_id,
                                                           User.Academy == user_academy).first()
            if not token and target_user:
                return jsonify({"code": StatusCode.TokenNotFound + StatusCode.UserNotFound,
                                "msg": "找不到对应的令牌或找不到对应的用户"})
            else:
                # 检查用户是否已经兑换过该令牌
                has_get_token: UserToken = session.query(UserToken).filter(UserToken.TokenId == token_id,
                                                                           UserToken.UserId == user_id).first()
                if has_get_token:
                    return jsonify({"code": StatusCode.TokenAlreadyGet, "msg": "用户已兑换过该令牌"})
                else:
                    # 创建兑换记录
                    history_get_token: UserToken = UserToken(
                        UserId=user_id,
                        TokenId=token_id
                    )
                    session.add(history_get_token)
                    session.commit()

                    # 根据令牌信息分配额度
                    target_user.Tokens += token.Tokens
                    target_user.PicTimes += token.PicTimes
                    session.commit()

                    return jsonify({"code": 0, "msg": "兑换令牌成功"})
    except Exception as e:
        app_logger.error(f"[USER GET TOKEN] {e}")
        return jsonify({"code": StatusCode.UserGetTokenError, "msg": "用户兑换令牌错误"})
