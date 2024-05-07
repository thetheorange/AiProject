"""
Des 文生文对话模型封装Socket类
    聊天接口 instance.chat()
    插件开发步骤: 1. instance.generate_extension_params 生成对应的插件参数
                2. instance.register_extension 注册插件
@Author thetheOrange
Time 2024/5/5
"""
import _thread as thread
import json
import ssl
from typing import Callable
from urllib.parse import urlparse

import jsonpath
import websocket

from Core.Tools.generate_url import OriginAPI
from Logging import app_logger


class TextModel:
    """
    文生文对话模型封装Socket类
    """

    def __init__(self, *, APPID, APIKey, APISecret, GptUrl, Domain, tour):
        """
        :param APPID: 应用ID
        :param APIKey: 应用Key
        :param APISecret: 应用秘钥
        :param GptUrl: 文生文聊天模型接口地址
        :param Domain: 所使用的大模型领域
        :param tour: 可支持的最大消息轮次
        """
        self.APPID: str = APPID
        self.APIKey: str = APIKey
        self.APISecret: str = APISecret
        self.host: str = urlparse(GptUrl).netloc
        self.path: str = urlparse(GptUrl).path
        self.GptUrl: str = GptUrl
        self.Domain: str = Domain

        # 可支持的最大消息轮次
        self.tour: int = tour
        # 存储历史消息的容器
        self.history: list[dict] = []
        # 单次消息的存储
        self.temp_msg: str = ""

        # 注册的插件基本信息 (function call的基本信息)
        self.extension_book: dict = {}
        # 插件执行的对应方法
        self._extension_func: dict = {}

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            # 打印当前实例所绑定的插件函数和对应的插件文档
            case "extension_func":
                temp: dict = {k: (v, v.__doc__) for k, v in self._extension_func.items()}
                return f"{temp}"
            # 打印当前实例所绑定的所有插件信息
            case "extension_book":
                return f"{self.extension_book}"
            case _:
                raise ValueError("Unknown format specifier")

    @staticmethod
    def generate_extension_params(*, properties: list[tuple], _type: str = "object",
                                  required: list[str] = None) -> dict:
        """
        快速生成插件参数
        :param _type: 参数类型
        :param properties: 参数变量 (name, type, description)
        :param required: 需要返回的参数 逻辑函数所需的参数
        :return:
        """
        if not required:
            required = []
        data: dict = {"type": _type, "required": required}
        temp: dict = {}
        for i in properties:
            temp[i[0]] = {"type": i[1], "description": i[2]}
        data["properties"] = temp
        return data

    def on_message(self, ws: any, message: str) -> None:
        """
        websocket 对收到消息的处理
        :param ws:
        :param message:
        :return:
        """
        print(message)
        message: dict = json.loads(message)
        # 如果存在插件 则调用对应的函数
        if extension_info := jsonpath.jsonpath(message, "$.payload.choices.text..function_call"):
            # 函数参数
            params: dict = extension_info[0].get("arguments")
            # 调用函数
            self._extension_func.get(extension_info[0].get("name"))(params)

        code: int = jsonpath.jsonpath(message, "$.header.code")[0]
        status: int = jsonpath.jsonpath(message, "$.header.status")[0]
        # 如果对话次数大于规定的最大轮次 则清除历史消息
        if len(self.history) > self.tour * 2:
            self.history.clear()
        if code != 0:
            print("## error ##")
            app_logger.error("socket connect error")
        else:
            self.temp_msg += jsonpath.jsonpath(message, "$.payload..text..content")[0]
            if status == 2:
                self.history.append({"role": "assistant", "content": fr"{self.temp_msg[:]}"})
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
        关闭websocket套接字时的处理 记录日志 清除资源
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
        ws.send(json.dumps(self.generate_base_params()))

    def generate_base_params(self) -> dict:
        """
        生成基本对话请求参数
        :return:
        """
        data: dict = {
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
                    "text": self.history[:]
                }
            }
        }
        # 检测是否存在已注册的插件 如存在则加入插件
        if len(self.extension_book.keys()) > 0:
            data["payload"]["functions"] = {"text": [i for i in self.extension_book.values()]}

        return data

    def chat(self, question: str) -> None:
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
        self.history.append({"role": "user", "content": fr"{question}"})
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def register_extension(self, name: str, description: str, parameters: dict, func: Callable) -> None:
        """
        注册插件
        :param name: 插件名称
        :param description: 插件描述
        :param parameters: 插件参数 字典对象
        :param func: 插件触发后执行的逻辑代码
        :return:
        """
        try:
            if name in self.extension_book:
                app_logger.info("The antique extension has been supplanted.")
            self.extension_book[name] = {"name": name,
                                         "description": description,
                                         "parameters": parameters}
            self._extension_func[name] = func
        except Exception as e:
            app_logger.error(f"Erroneous registration of the extension. {e}")

    def unregister_extension(self, name: str) -> None:
        """
        解绑插件
        :param name: 插件名
        :return:
        """
        if name in self.extension_book:
            del self.extension_book[name]
            del self._extension_func[name]
        else:
            app_logger.info(f"Not found extension to unregister {name}")


# test
if __name__ == "__main__":
    m = TextModel(APPID="60361ac3",
                  APISecret="NTM1ZGY3MjM0ODQxMDBhY2NjMDIyM2E5",
                  APIKey="7f8ff2dba8d566abb46791589ba9fed7",
                  GptUrl="wss://spark-api.xf-yun.com/v3.5/chat",
                  Domain="generalv3.5",
                  tour=5)
    ctn: int = 0
    extension_p: dict = m.generate_extension_params(properties=[("location", "string", "地点，默认北京"),
                                                                ("date", "string", "日期")],
                                                    required=["location", "date"])

    m.register_extension(name="天气状况",
                         description="天气插件可以提供天气相关信息。你可以提供指定的地点信息、指定的时间点或者时间段信息，来精准检索到天气信息。",
                         parameters=extension_p,
                         func=lambda x: print(f"传入的参数为 >>>{x} 天气状况插件执行"))
    print(m.extension_book)
    print(f"{m:extension_book}")
    print(f"{m:extension_func}")

    # while ctn < 10:
    #     ctn += 1
    #     query: str = input()
    #     m.chat(query)
