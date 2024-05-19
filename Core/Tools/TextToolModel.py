"""
Des 基于文生文对话模型的工具模型，负责对话的压缩概括，实现插件与对话一体
@Author thetheOrange
Time 2024/5/11
"""
from urllib.parse import urlparse

from Core.Models.TextSocket import TextModel
from Logging import app_logger


class TextToolModel(TextModel):
    # 注册的插件基本信息 (function call的基本信息)
    extension_book: dict = {}
    # 插件执行的对应方法
    _extension_func: dict = {}

    def __init__(self, *, APPID, APIKey, APISecret, GptUrl, Domain, tour):

        super().__init__(APPID=APPID, APIKey=APIKey, APISecret=APISecret, GptUrl=GptUrl, Domain=Domain, tour=tour)

    # 重写重载插件方法的驱动 保证工具大模型类无任何插件
    def handle_load_extension(self, target_class, path: str) -> None:
        return


if __name__ == "__main__":
    test_session = TextToolModel(APPID="60361ac3",
                                 APIKey="7f8ff2dba8d566abb46791589ba9fed7",
                                 APISecret="NTM1ZGY3MjM0ODQxMDBhY2NjMDIyM2E5",
                                 GptUrl="wss://spark-Api.xf-yun.com/v3.5/chat",
                                 Domain="generalv3.5",
                                 tour=10)

    ctn: int = 10
    # test_session.on_mask()
    print(f"{test_session:extension_book}")
    while ctn > 0:
        print(test_session.history)
        test_session.chat(input(""))
        ctn -= 1
