"""
@Model: TextModel
@name: test
@_type: object
@properties: [(
@required: ["location", "date"]
@description: 插件函数文档示例
@Author: thetheOrange
@Time: 2024/5/11
"""
from Core.Models.TextSocket import TextModel
from Core.Tools.TextToolModel import TextToolModel
from Core.Tools.extension_base_params import BaseParams

base_params = BaseParams("TextModel",
                         "对话和帮助",
                         "object",
                         [("chat", "string", "向大模型提问的问题或对话")],
                         ["chat"])

# 生成插件参数
parameters: dict = TextModel.generate_extension_params(properties=base_params.properties,
                                                       _type=base_params.data_type,
                                                       required=base_params.required)

m = TextToolModel(APPID="60361ac3",
                  APIKey="7f8ff2dba8d566abb46791589ba9fed7",
                  APISecret="NTM1ZGY3MjM0ODQxMDBhY2NjMDIyM2E5",
                  GptUrl="wss://spark-Api.xf-yun.com/v3.5/chat",
                  Domain="generalv3.5",
                  tour=10)


# 插件逻辑函数入口
def func(params: dict) -> None:
    """
    你是讯飞平台的星火认知大模型，可以为用户提供准确具体的帮助
    :param params:
    :return:
    """
    print("1111111111")
    print(type(params), params)
    print(">>>", params["chat"])
    print("====================》", m.history)
    m.chat(params["chat"])
