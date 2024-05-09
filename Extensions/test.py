"""
@model: TextModel
@name: test
@_type: object
@properties: [("location", "string", "地点，默认北京"),
            ("date", "string", "日期")]
@required: ["location", "date"]
@description: 插件函数文档示例
@Author: thetheOrange
@Time: 2024/5/9
"""
from Core.Models.TextSocket import TextModel

# 模型类型
model: str = "TextModel"
# 插件名称
name: str = "天气"
# 返回的数据类型
_type: str = "object"
# 向大模型传入的参数 (name, type, description)
properties: list[tuple] = [("location", "string", "地点，默认北京"),
                           ("date", "string", "日期")]
# 需要返回的参数 返回的参数会被封装成字典
required: list[str] = ["location", "date"]

# 生成插件参数
parameters: dict = TextModel.generate_extension_params(properties=properties,
                                                       _type=_type,
                                                       required=required)


# 插件逻辑函数入口
def func(params: dict) -> None:
    """
    天气插件可以提供天气相关信息。你可以提供指定的地点信息、指定的时间点或者时间段信息，来精准检索到天气信息。
    :param params:
    :return:
    """
    print("================")
    print(f"{params}")
    print("查询天气函数被调用")
    print("================")



