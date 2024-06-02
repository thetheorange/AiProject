"""
Des 各大模型调用接口
@Author thetheOrange
Time 2024/5/19
"""
import time

from flask import request, Response, jsonify, stream_with_context
from sqlalchemy.orm import sessionmaker

from Core.Models.TextSocket import TextModel
from Core.StatusCode import StatusCode
from Model.model import engine, User
from . import model_blu

APPID = "60361ac3"
APIKey = "7f8ff2dba8d566abb46791589ba9fed7"
APISecret = "NTM1ZGY3MjM0ODQxMDBhY2NjMDIyM2E5"
GptUrl = "wss://spark-api.xf-yun.com/v3.5/chat"
Domain = "generalv3.5"


@model_blu.route("/textModel/chat", methods=["POST"])
def text_model_chat() -> Response:
    """
    调用文本大模型接口 非流式传输

    :return: 返回json字符串 包含回复消息
    """

    # 请求的用户id
    query_user_uuid: int = request.json.get("uuid")
    # 用户名
    query_user_name: str = request.json.get("username")
    # 发送给大模型的对话消息
    query_msg: list[dict] = request.json.get("dialog")

    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        # 查询用户信息
        user_info: User = session.query(User).filter(User.Id == query_user_uuid,
                                                     User.UserName == query_user_name).first()
        # 如果存在则判断用户剩余token是否大于0
        if user_info:
            if user_info.Tokens > 0:
                text_chat_session: TextModel = TextModel(APPID=APPID,
                                                         APIKey=APIKey,
                                                         APISecret=APISecret,
                                                         GptUrl=GptUrl,
                                                         Domain=Domain)
                consume_token, response_text = text_chat_session.chat(query_msg)
                user_info.Tokens -= consume_token
                session.commit()
                return jsonify({
                    "code": 0,
                    "text": response_text,
                    "consume_token": consume_token
                })
            else:
                return jsonify({
                    "code": StatusCode.TokenNotEnough
                })
        else:
            return jsonify({
                "code": StatusCode.UserNotFound
            })


@model_blu.route("/textModel/stream", methods=["POST"])
def text_model_stream() -> Response:
    """
    调用文本大模型接口 流式传输

    :return: 返回json字符串 包含回复消息
    """

    # 请求的用户id
    query_user_uuid: int = request.json.get("uuid")
    # 用户名
    query_user_name: str = request.json.get("username")
    # 发送给大模型的对话消息
    query_msg: list[dict] = request.json.get("dialog")

    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        # 查询用户信息
        user_info: User = session.query(User).filter(User.Id == query_user_uuid,
                                                     User.UserName == query_user_name).first()
        # 如果存在则判断用户剩余token是否大于0
        if user_info:
            if user_info.Tokens > 0:
                text_chat_session: TextModel = TextModel(APPID=APPID,
                                                         APIKey=APIKey,
                                                         APISecret=APISecret,
                                                         GptUrl=GptUrl,
                                                         Domain=Domain)
                text_chat_session.chat(query_msg)
                consume_token: int = text_chat_session.total_tokens
                user_info.Tokens -= consume_token
                return Response(stream_with_context(text_chat_session.stream()))
            else:
                return jsonify({
                    "code": StatusCode.TokenNotEnough
                })
        else:
            return jsonify({
                "code": StatusCode.UserNotFound
            })


@model_blu.route("/voiceModel/chat", methods=["POST"])
def voice_model() -> str:
    return "this is gpt-voice-Model"
