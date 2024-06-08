"""
Des 文生文对话模型封装Socket类
    聊天接口 instance.chat() 要求传入标准化的列表 包含历史消息 (非流式)
            instance.stream() 流式聊天接口
    插件开发步骤: 1. TextModel.generate_extension_params 生成对应的插件参数
                2. TextModel.register_extension 注册插件
@Author thetheOrange
Time 2024/5/5
"""
import _thread as thread
import json
import os
import ssl
import importlib.util
from queue import Queue
from typing import Callable
from urllib.parse import urlparse

import jsonpath
import requests
import websocket

from Core.Tools.generate_url import OriginAPI
from Logging import app_logger


class TextModel:
    """
    文生文对话模型封装Socket类
    """

    def __init__(self, *, APPID, APIKey, APISecret, GptUrl, Domain, isLoadExtension=False):
        """
        :param APPID: 应用ID
        :param APIKey: 应用Key
        :param APISecret: 应用秘钥
        :param GptUrl: 文生文聊天模型接口地址
        :param Domain: 所使用的大模型领域
        """
        self.APPID: str = APPID
        self.APIKey: str = APIKey
        self.APISecret: str = APISecret
        self.host: str = urlparse(GptUrl).netloc
        self.path: str = urlparse(GptUrl).path
        self.GptUrl: str = GptUrl
        self.Domain: str = Domain
        self.isLoadExtension = isLoadExtension

        # 大模型回复的消息
        self.response_text: str = ""
        # 提问大模型时传入的列表 包含json
        self.query_message: list[dict] = []

        # 文本大模型请求参数
        self.query_param: dict = {
            "header": {
                "app_id": "",
            },
            "parameter": {
                "chat": {
                    "domain": "",
                    "temperature": 0.5,
                    "max_tokens": 4096,
                    "auditing": "default",
                }
            },
            "payload": {
                "message": {
                    "text": []
                }
            }
        }

        # 每一次会话消耗的token数
        self.total_tokens: int = -1

        # 消息队列
        self.message_queue: Queue = Queue()

    def on_message(self, ws: any, message: str) -> None:
        """
        websocket 对收到消息的处理

        :param ws:
        :param message:
        :return:
        """
        # print(">>>>>\n", message)
        self.message_queue.put(message)
        message: dict = json.loads(message)

        code: int = jsonpath.jsonpath(message, "$.header.code")[0]
        status: int = jsonpath.jsonpath(message, "$.header.status")[0]
        if code != 0:
            app_logger.error("socket connect error")
        else:
            self.response_text += jsonpath.jsonpath(message, "$.payload..text..content")[0]
            # status = 2 意味回复完毕
            if status == 2:
                # 获取消耗的token数
                self.total_tokens = jsonpath.jsonpath(message, "$..usage.text.total_tokens")[0]
                ws.close()

    def on_error(self, ws: any, error: any) -> None:
        """
        websocket 错误时的处理

        :param ws:
        :param error:
        :return:
        """
        app_logger.error("socket connect error")

    def on_close(self, ws: any) -> None:
        """
        关闭websocket套接字时的处理 记录日志 清除资源

        :param ws:
        :return:
        """
        app_logger.info("socket close")

    def on_open(self, ws: any) -> None:
        """
        websocket连接建立的处理

        :param ws:
        :return:
        """
        thread.start_new_thread(self.send_msg, (ws,))

    def send_msg(self, ws: any, *args) -> None:
        """
        发送请求消息

        :param ws:
        :param args:
        :return:
        """
        self.query_param["header"]["app_id"] = self.APPID
        self.query_param["parameter"]["chat"]["domain"] = self.Domain
        self.query_param["payload"]["message"]["text"] = self.query_message
        ws.send(json.dumps(self.query_param))

    def chat(self, query_message: list[dict]) -> tuple[int, str]:
        """
        连接文生文模型api接口，进行对话

        :param query_message: 聊天记录
        :return:
        """
        self.response_text = ""
        self.query_message += query_message

        websocket.enableTrace(False)  # 关闭调试模式
        ws_param = OriginAPI(APPID=self.APPID,
                             APISecret=self.APISecret,
                             APIKey=self.APIKey,
                             GptUrl=self.GptUrl)
        ws_url: str = ws_param.generate_url()

        ws = websocket.WebSocketApp(url=ws_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    on_open=self.on_open)
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        return (self.total_tokens, self.response_text) if self.total_tokens >= 0 else ""

    def stream(self) -> str:
        """
        连接文生文模型api接口，流式传输数据

        :return:
        """
        while self.message_queue.qsize() > 0:
            yield self.message_queue.get()


if __name__ == "__main__":
    test_session = TextModel(APPID="60361ac3",
                             APIKey="7f8ff2dba8d566abb46791589ba9fed7",
                             APISecret="NTM1ZGY3MjM0ODQxMDBhY2NjMDIyM2E5",
                             GptUrl="wss://spark-api.xf-yun.com/v3.5/chat",
                             Domain="generalv3.5")

    a = test_session.chat([{"role": "user", "content": "模仿李白的风格写一首古诗"},
                           {"role": "assistant", "content": """
                       青天有梦醉流光。
                        白云深处藏仙踪，
                        玉液金杯舞翠梁。
                        风送轻香入瑶池，
                        星河倒影映花枝。
                        夜半琴声飘四海，
                        李白临风笑千诗。"""},
                           {"role": "user", "content": "改写这首诗"}])
    for i in test_session.stream():
        print("****", i)
    print(type(a), a)
