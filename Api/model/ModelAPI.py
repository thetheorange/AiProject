"""
Des 各大模型调用接口
@Author thetheOrange
Time 2024/5/19
"""
import os.path
from typing import Optional

from flask import request, Response, jsonify, stream_with_context
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

from Core.Models.PictureToTextSocket import PictureToTextSocket
from Core.Models.TextSocket import TextModel
from Core.Models.VoiceToTextSocket import AudioToTextModel
from Core.StatusCode import StatusCode
from Model.model import engine, User
from config import config_json

from . import model_blu

APPID = config_json["api"]["APPID"]
APIKEY = config_json["api"]["APIKEY"]
API_SECRET = config_json["api"]["API_SECRET"]
GPT_URL = config_json["api"]["GPT_URL"]
DOMAIN = config_json["api"]["DOMAIN"]

# 允许上传的文件拓展名
ALLOWED_EXTENSIONS: set = {"pcm", "jpg", "jpeg"}


def is_legal_file(filename: Optional[str]) -> bool:
    """
    检查文件拓展名是否合法

    :return:
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ================================ 文本模型接口start ================================

@model_blu.route("/textModel/chat", methods=["POST"])
def text_model_chat() -> Response:
    """
    调用文本大模型接口 非流式传输
    请求body
    {
        "uuid": 0,
        "username": "xxx",
        "dialog": [{"role": "system", "content": "query text"},
                    {"role": "user", "content": "query text"},
                    {"role": "assistant", "content": "response text"},
                    ...]
    }

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
                                                         APIKey=APIKEY,
                                                         APISecret=API_SECRET,
                                                         GptUrl=GPT_URL,
                                                         Domain=DOMAIN)
                consume_token, response_text = text_chat_session.chat(query_msg)
                user_info.Tokens -= consume_token
                session.commit()
                return jsonify({
                    "code": 0,
                    "content": response_text,
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
    请求body
    {
        "uuid": 0,
        "username": "xxx",
        "dialog": [{"role": "system", "content": "query text"},
                    {"role": "user", "content": "query text"},
                    {"role": "assistant", "content": "response text"},
                    ...]
    }

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
                                                         APIKey=APIKEY,
                                                         APISecret=API_SECRET,
                                                         GptUrl=GPT_URL,
                                                         Domain=DOMAIN)
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


# =============================== 文本模型接口end ================================

# ================================ 语音识别模型接口start ================================

@model_blu.route("/voiceModel/chat", methods=["POST"])
def voice_to_text_model() -> Response:
    """
    语音识别模型接口 需上传相应的pcm文件

    :return: 返回json字符串，包含语音识别的内容
    """
    # 存储音频文件的位置
    audio_stock: str = "Temp/Audio"
    # 获取用户上传的音频文件
    audio_file = request.files["file"]
    if audio_file and is_legal_file(audio_file.filename):
        audio_file_name: str = secure_filename(audio_file.filename)
        # 音频文件的具体存储位置
        audio_file_position: str = os.path.join(audio_stock, audio_file_name)
        audio_file.save(audio_file_position)

        audio_to_text_session: AudioToTextModel = AudioToTextModel(APPID=APPID, APISecret=API_SECRET, APIKey=APIKEY)
        ret: str = audio_to_text_session.transform_voice(audio_file_position)
        # 释放音频文件
        os.remove(audio_file_position)
        return jsonify({
            "code": 0,
            "content": ret
        })
    else:
        return jsonify({
            "code": StatusCode.AudioToTextError
        })


# ================================ 语音识别模型接口end ================================

# ================================ 图片识别文字接口start ================================

@model_blu.route("/PictureToTextModel/chat", methods=["POST"])
def character_recognition() -> Response:
    """
    文字识别接口 请求头需包含用户名和uuid

    :return: 返回json
    """

    # 请求的用户id
    query_user_uuid: str = request.headers.get("uuid")
    # 用户名
    query_user_name: str = request.headers.get("username")
    # 获取用户上传的图片文件
    picture = request.files["file"]

    # 存储图片的位置
    picture_stock: str = "Temp/Picture"

    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        # 查询用户信息
        user_info: User = session.query(User).filter(User.Id == query_user_uuid,
                                                     User.UserName == query_user_name).first()

        # 如果存在则判断用户剩余使用次数是否大于0
        if user_info:
            if user_info.PicTimes > 0:
                if picture and is_legal_file(picture.filename):
                    picture_file_name: str = secure_filename(picture.filename)
                    # 图片文件的具体存放位置
                    picture_file_position: str = os.path.join(picture_stock, picture_file_name)
                    picture.save(picture_file_position)

                    picture_to_text_session: PictureToTextSocket = PictureToTextSocket(APPID=APPID,
                                                                                       APIKey=APIKEY,
                                                                                       APISecret=API_SECRET)
                    ret: str = picture_to_text_session.translate_picture(picture_file_position)
                    return jsonify({
                        "code": 0,
                        "content": ret
                    })
                else:
                    return jsonify({
                        "code": StatusCode.PictureToTextError
                    })
            else:
                return jsonify({
                    "code": StatusCode.PicTimesNotEnough
                })
        else:
            return jsonify({
                "code": StatusCode.UserNotFound
            })

# ================================ 图片识别文字接口end ================================
