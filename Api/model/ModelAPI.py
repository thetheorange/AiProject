"""
Des 各大模型调用接口
@Author thetheOrange
Time 2024/5/19
"""
import asyncio
import os.path
import queue
from typing import Optional

import anyio
from flask import request, Response, jsonify, stream_with_context, copy_current_request_context
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

from Core.Models.PictureToTextSocket import PictureToTextSocket
from Core.Models.TextSocket import TextModel
from Core.Models.VoiceToTextSocket import AudioToTextModel
from Core.StatusCode import StatusCode
from Logging import app_logger
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
async def text_model_stream() -> Response:
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

    try:
        # 请求的用户id
        query_user_uuid: str = request.json.get("uuid")
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
            if not user_info:
                return jsonify({
                    "code": StatusCode.UserNotFound,
                    "msg": "找不到指定用户"
                })
            if user_info.Tokens <= 0:
                return jsonify({
                    "code": StatusCode.TokenNotEnough,
                    "msg": "用户token额度不足"
                })

        # 2024.11.3 ============================================
        # thetheOrange 修改
        # 新建子线程，在子线程中执行异步操作，获取异步生成器里的内容，
        # 消息队列作为子主线程的桥梁，由此实现流式传输，代价是要多开一个子线程
        # 2024.11.3 ============================================
        text_model: TextModel = TextModel(APPID=APPID, APIKey=APIKEY, APISecret=API_SECRET, GptUrl=GPT_URL,
                                          Domain=DOMAIN)
        q = queue.Queue()

        # 异步获取消息 将其压入队列中
        async def fetch_data(q):
            try:
                async for chunk in text_model.chat(query_msg):
                    q.put(chunk)
            except Exception as e:
                q.put(f"{{'code': -1, 'msg': '{e}'}}")
                app_logger.error(f"[TEXT STREAM ERROR] {e}")
            finally:
                q.put(None)

        # 主线程中获取异步消息
        def handle(q):
            while True:
                chunk = q.get(True)
                print(chunk, type(chunk))
                if chunk is None:
                    with DBSession() as session:
                        user: User = session.query(User).filter(User.UserName == query_user_name,
                                                                User.Id == query_user_uuid).first()
                        user.Tokens -= text_model.total_tokens
                        session.commit()
                    break
                yield chunk

        # 在另一个线程中执行异步任务
        async def run_in_thread(q):
            await asyncio.to_thread(asyncio.run, fetch_data(q))

        asyncio.create_task(run_in_thread(q))

        return Response(handle(q))

    except Exception as e:
        app_logger.error(f"[TEXT MODEL STREAM] {e}")
        return jsonify({
            "code": StatusCode.ModelError,
            "msg": "文本大模型流式接口错误"
        })


# =============================== 文本模型接口end ================================

# ================================ 语音识别模型接口start ================================

@model_blu.route("/voiceModel/chat", methods=["POST"])
def voice_to_text_model() -> Response:
    """
    语音识别模型接口 需上传相应的pcm文件

    :return: 返回json字符串，包含语音识别的内容
    """
    try:
        # 存储音频文件的位置
        audio_stock: str = "Temp/Audio"
        # 获取用户上传的音频文件
        audio_file = request.files["file"]
        if not is_legal_file(audio_file.filename):
            return jsonify({
                "code": StatusCode.FileFormatIllegal,
                "msg": "文件格式不合法"
            })
        if not audio_file:
            return jsonify({
                "code": StatusCode.GetFileFail,
                "msg": "获取上传文件失败"
            })

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
            "msg": "请求成功",
            "content": ret
        })

    except Exception as e:
        app_logger.error(f"[VOICE MODEL] {e}")
        return jsonify({
            "code": StatusCode.AudioToTextError,
            "msg": "请求失败"
        })


# ================================ 语音识别模型接口end ================================

# ================================ 图片识别文字接口start ================================

@model_blu.route("/PictureToTextModel/chat", methods=["POST"])
def character_recognition() -> Response:
    """
    文字识别接口 请求头需包含用户名和uuid

    :return: 返回json
    """

    try:
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
            if not user_info:
                return jsonify({
                    "code": StatusCode.UserNotFound,
                    "msg": "找不到指定用户"
                })

            if user_info.PicTimes <= 0:
                return jsonify({
                    "code": StatusCode.PicTimesNotEnough,
                    "msg": "用户文字识别可用额度不足"
                })

            if not is_legal_file(picture.filename):
                return jsonify({
                    "code": StatusCode.FileFormatIllegal,
                    "msg": "文件格式不合法"
                })

            if not picture:
                return jsonify({
                    "code": StatusCode.GetFileFail,
                    "msg": "获取上传文件失败"
                })

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
                "msg": "请求成功",
                "content": ret
            })

    except Exception as e:
        app_logger.error(f"[PICTURE MODEL] {e}")
        return jsonify({
            "code": StatusCode.PictureToTextError,
            "msg": "文字识别接口请求错误"
        })

# ================================ 图片识别文字接口end ================================
