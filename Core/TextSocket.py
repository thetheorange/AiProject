"""
Des 文生文对话模型封装Socket类
@Author thetheOrange
Time 2024/5/5
"""
import _thread as thread
import json
import ssl
from urllib.parse import urlparse

import jsonpath
import websocket

from Core.generate_url import OriginAPI
from Logging import app_logger


class TextModel:
    """
    文生文对话模型封装Socket类
    """

    def __init__(self, *, APPID, APIKey, APISecret, GptUrl, Domain):
        self.APPID: str = APPID
        self.APIKey: str = APIKey
        self.APISecret: str = APISecret
        self.host: str = urlparse(GptUrl).netloc
        self.path: str = urlparse(GptUrl).path
        self.GptUrl: str = GptUrl
        self.Domain: str = Domain

        # 存储消息的容器
        self.msg_container: list[str] = []
        # 单次消息的存储
        self.temp_msg: str = ""

    def on_message(self, ws: any, message: str) -> None:
        """
        websocket 对收到消息的处理
        :param ws:
        :param message:
        :return:
        """
        print(message)
        message: dict = json.loads(message)
        code: int = jsonpath.jsonpath(message, "$.header.code")[0]
        status: int = jsonpath.jsonpath(message, "$.header.status")[0]
        if code != 0:
            print("## error ##")
            app_logger.error("socket connect error")
        else:
            self.temp_msg += jsonpath.jsonpath(message, "$.payload..text..content")[0]
            if status == 2:
                self.msg_container.append(self.temp_msg)
                print(self.temp_msg)
                self.temp_msg = ""
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
        关闭websocket套接字
        :param ws:
        :return:
        """
        app_logger.info("socket close")

    def on_open(self, ws: any) -> None:
        """
        收到websocket连接建立的处理
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
        ws.send(json.dumps(self.generate_params(ws.query)))

    def generate_params(self, query) -> dict:
        """
        生成请求参数
        :return:
        """
        return {
            "header": {
                "app_id": self.APPID,
            },
            "parameter": {
                "chat": {
                    "domain": self.Domain,
                    "temperature": 0.5,
                    "max_tokens": 4096,
                    "auditing": "default",
                }
            },
            "payload": {
                "message": {
                    "text": [{"role": "user", "content": query}]
                }
            }
        }

    def chat(self, query) -> None:
        """
        连接文生文模型api接口，进行对话
        :return:
        """
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
        ws.query = query
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
