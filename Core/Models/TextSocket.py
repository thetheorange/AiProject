"""
Des 文生文对话模型封装Socket类
    聊天接口 instance.chat() 流式传输接口
@Author thetheOrange
Time 2024/5/5
"""

import asyncio
import json
from urllib.parse import urlparse

import jsonpath
import websockets

from Core.Tools.generate_url import OriginAPI
from Logging import app_logger


class TextModel:
    """
    文生文对话模型封装Socket类
    """

    def __init__(self, *, APPID, APIKey, APISecret, GptUrl, Domain, isLoadExtension=False, config=None):
        """
        :param APPID: 应用ID
        :param APIKey: 应用Key
        :param APISecret: 应用秘钥
        :param GptUrl: 文生文聊天模型接口地址
        :param Domain: 所使用的大模型领域
        """
        if config is None:
            config = {
                "temperature": 0.5,
                "max_tokens": 4096,
                "top_k": 4
            }
        self.APPID: str = APPID
        self.APIKey: str = APIKey
        self.APISecret: str = APISecret
        self.host: str = urlparse(GptUrl).netloc
        self.path: str = urlparse(GptUrl).path
        self.GptUrl: str = GptUrl
        self.Domain: str = Domain
        self.isLoadExtension = isLoadExtension

        # 提问大模型时传入的列表 包含json
        self.query_message: list[dict] = []
        # 每一次会话消耗的token数
        self.total_tokens: int = -1

        # 文本大模型请求参数
        self.query_param: dict = {
            "header": {
                "app_id": APPID,
            },
            "parameter": {
                "chat": {
                    "domain": "generalv3.5",
                    "temperature": config["temperature"],
                    "max_tokens": config["max_tokens"],
                    "top_k": config["top_k"],
                    "auditing": "default",
                }
            },
            "payload": {
                "message": {
                    "text": []
                }
            }
        }

    async def chat(self, query_message: list[dict]):
        """
        连接文生文模型api接口，进行对话

        :param query_message: 聊天记录
        :return:
        """
        try:
            self.query_param["payload"]["message"]["text"] = query_message
            async with websockets.connect(OriginAPI(
                    APPID=self.APPID,
                    APIKey=self.APIKey,
                    APISecret=self.APISecret,
                    GptUrl=self.GptUrl
            ).generate_url()) as ws:
                await ws.send(json.dumps(self.query_param))
                async for msg in ws:
                    tmp = json.loads(msg)
                    status: int = jsonpath.jsonpath(tmp, "$.header.status")[0]
                    # 表示消息结束
                    if status == 2:
                        self.total_tokens = jsonpath.jsonpath(tmp, "$..usage.text.total_tokens")[0]
                    yield msg
        except Exception as e:
            app_logger.error(f"[TEXT MODEL] {e}")


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
