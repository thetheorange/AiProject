"""
Des 文生文对话模型封装Socket类
    聊天接口 instance.chat() 要求传入标准化的列表 包含历史消息
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
from typing import Callable
from urllib.parse import urlparse

import jsonpath
import websocket

from Core.Tools import TextToolModel
from Core.Tools.generate_url import OriginAPI
from Logging import app_logger


class TextModel:
    """
    文生文对话模型封装Socket类
    """

    # 注册的插件基本信息 (function call的基本信息)
    extension_book: dict = {}
    # 插件执行的对应方法
    _extension_func: dict = {}

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

        # 每隔几轮对话后对信息进行压缩
        self.tour: int = 5
        # 大模型回复的消息
        self.response_text: str = ""
        # 提问大模型时传入的列表 包含json
        self.query_message: list[dict] = []

        # 加载插件 从配置文件中读取插件目录
        if self.isLoadExtension:
            TextModel.load_extension(TextModel.__name__, "../../Extensions")

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

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            # 打印当前实例所绑定的插件函数和对应的插件文档
            case "extension_func":
                temp: dict = {k: (v, v.__doc__) for k, v in TextModel._extension_func.items()}
                return f"{temp}"
            # 打印当前实例所绑定的所有插件信息
            case "extension_book":
                return f"{TextModel.extension_book}"
            case _:
                raise ValueError("Unknown format specifier")

    @classmethod
    def register_extension(cls, name: str, description: str, parameters: dict, func: Callable) -> None:
        """
        注册插件
        :param name: 插件名称
        :param description: 插件描述
        :param parameters: 插件参数 字典对象
        :param func: 插件触发后执行的逻辑代码
        :return:
        """
        try:
            if name in cls.extension_book:
                app_logger.info("The antique extension has been supplanted.")
            cls.extension_book[name] = {"name": name,
                                        "description": description,
                                        "parameters": parameters}
            cls._extension_func[name] = func
        except Exception as e:
            app_logger.error(f"Erroneous registration of the extension. {e}")

    @classmethod
    def unregister_extension(cls, name: str) -> None:
        """
        解绑插件
        :param name: 插件名
        :return:
        """
        if name in cls.extension_book:
            del cls.extension_book[name]
            del cls._extension_func[name]
        else:
            app_logger.info(f"Not found extension to unregister {name}")

    @classmethod
    def generate_extension_params(cls, *, properties: list[tuple], _type: str = "object",
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

    @classmethod
    def load_extension(cls, target: str, path: str) -> None:
        """
        初始化或加载插件 每次新开一个对话或对插件做出修改时，都会调用一次该方法
        :return:
        """
        # 判断插件文件夹是否存在
        if not os.path.exists(path):
            app_logger.error(f"Extension dir not found {FileNotFoundError}")
            raise FileNotFoundError
        # 动态导入目标目录中的模块
        for file_name in os.listdir(path):
            if file_name.endswith(".py"):
                extension_name: str = file_name[:-3]
                extension_spec = importlib.util.spec_from_file_location(extension_name, os.path.join(path, file_name))
                extension = importlib.util.module_from_spec(extension_spec)
                extension_spec.loader.exec_module(extension)
                # 注册插件
                if extension.base_params.model == target:
                    cls.register_extension(name=extension.base_params.name,
                                           description=extension.func.__doc__,
                                           parameters=extension.parameters,
                                           func=extension.func)
                    app_logger.info(f"Extension {extension_name} loaded")

    def on_message(self, ws: any, message: str) -> None:
        """
        websocket 对收到消息的处理
        :param ws:
        :param message:
        :return:
        """
        # print(message)
        message: dict = json.loads(message)
        # 如果存在插件 则调用对应的函数
        if extension_info := jsonpath.jsonpath(message, "$.payload.choices.text..function_call"):
            # 函数参数
            params: str = extension_info[0].get("arguments")
            # 调用函数
            self._extension_func.get(extension_info[0].get("name"))(json.loads(params))

        code: int = jsonpath.jsonpath(message, "$.header.code")[0]
        status: int = jsonpath.jsonpath(message, "$.header.status")[0]
        if code != 0:
            app_logger.error("socket connect error")
        else:
            self.response_text += jsonpath.jsonpath(message, "$.payload..text..content")[0]
            # status = 2 意味回复完毕
            if status == 2:
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
        self.query_param["header"]["app_id"] = self.APPID
        self.query_param["parameter"]["chat"]["domain"] = self.Domain
        self.query_param["payload"]["message"]["text"] = self.query_message
        # 检测是否存在已注册的插件 如存在则加入插件
        if len(TextModel.extension_book.keys()) > 0 and self.isLoadExtension:
            self.query_param["payload"]["functions"] = {"text": [i for i in TextModel.extension_book.values()]}
        ws.send(json.dumps(self.query_param))

    def chat(self, query_message: list[dict]) -> str:
        """
        连接文生文模型api接口，进行对话
        :return:
        """
        self.response_text = ""
        self.query_message = query_message

        # 如果对话次数大于规定的最大轮次 则历史压缩消息
        if len(self.query_message) > self.tour:
            tool_model = TextToolModel.TextToolModel(APPID=self.APPID,
                                                     APIKey=self.APIKey,
                                                     APISecret=self.APISecret,
                                                     GptUrl=self.GptUrl,
                                                     Domain=self.Domain)
            self.query_message = tool_model.compress_msg(query_message)
            self.query_message.append(query_message[-1])
            del tool_model

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
        return self.response_text


# test
if __name__ == "__main__":
    ...
#     test_session.chat([{"role": "user", "content": "用两三句概括一下python的特性"},
#                        {"role": "assistant", "content": """1. **易于学习**：Python有着简洁的语法规则，使得它对于初学者来说是易于理解和学习的编程语言。
# 2. **面向对象**：作为一种面向对象的编程语言，Python支持封装、继承和多态等高级编程概念。
# 3. **可移植性**：Python代码可以在不同的操作系统上运行，如Windows、Linux和Mac OS等，这提供了极大的灵活性。
# 4. **解释性语言**：Python是一种解释型语言，这意味着开发过程中可以快速执行代码并获得结果，无需编译整个程序。
# 5. **开源性**：Python是开源的，拥有一个庞大的社区，不断有新的库和工具被开发出来，以支持各种应用。
# 6. **高级语言特性**：Python支持多种高级语言特性，如动态类型和自动内存管理，这使得编写Python代码更加高效。
# 7. **丰富的库支持**：Python有着强大的标准库以及第三方库，覆盖了网络、文件、图形用户界面等大量的应用领域。"""},
#                        {"role": "user", "content": "你是谁"},
#                        {"role": "assistant", "content": "您好，我是科大讯飞研发的认知智能大模型，我的名字叫讯飞星火认知大模型。我可以和人类进行自然交流，解答问题，高效完成各领域认知智能需求。"},
#                        {"role": "user", "content": "模仿李白的风格写一首古诗"},
#                        {"role": "assistant", "content": """
#                        青天有梦醉流光。
#                         白云深处藏仙踪，
#                         玉液金杯舞翠梁。
#                         风送轻香入瑶池，
#                         星河倒影映花枝。
#                         夜半琴声飘四海，
#                         李白临风笑千诗。"""},
#                        {"role": "user", "content": "把这首诗转化成英文"}])
