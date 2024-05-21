"""
Des 基于文生文对话模型的工具模型，负责对话的压缩概括，实现插件与对话一体
@Author thetheOrange
Time 2024/5/11
"""
import json
import ssl
from urllib.parse import urlparse

import websocket

from Core.Models.TextSocket import TextModel
from Core.Tools.generate_url import OriginAPI
from Logging import app_logger


class TextToolModel(TextModel):

    def __init__(self, *, APPID, APIKey, APISecret, GptUrl, Domain):
        super().__init__(APPID=APPID, APIKey=APIKey, APISecret=APISecret, GptUrl=GptUrl, Domain=Domain)
        self.message_to_compress: str = ""

    def chat(self, query_message: list[dict]) -> str:
        """
        连接文生文模型api接口，进行对话
        :return:
        """
        self.response_text = ""
        self.query_message = query_message

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
        print(self.response_text)
        return self.response_text

    def compress_msg(self, query_message: list[dict]) -> list[dict]:
        """
        :param query_message: 要压缩的消息
        :return 压缩后的消息
        """
        self.message_to_compress = query_message[:]
        self.message_to_compress.insert(0, {"role": "system", "content": "我需要你为我概括我向你提供的内容，最好不超过100字，越简短越好"})
        self.message_to_compress[-1] = {"role": "user", "content": "概括以上所有的对话内容"}
        return [{"role": "assistant", "content": f"{self.chat(self.message_to_compress)}"}]


# test
if __name__ == "__main__":
    ...

