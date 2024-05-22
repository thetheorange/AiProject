"""
@Model: TextModel
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
from Core.Tools.extension_base_params import BaseParams

base_params = BaseParams("TextModel",
                         "x站热门视频",
                         "object",
                         [("date", "string", "日期")],
                         ["date"])

# 生成插件参数
parameters: dict = TextModel.generate_extension_params(properties=base_params.properties,
                                                       _type=base_params.data_type,
                                                       required=base_params.required)


# 插件逻辑函数入口
def func(params: dict) -> None:
    """
    x站热门视频插件可以为用户提供今天的x站热门视频top10，并给出对应的介绍
    :param params:
    :return:
    """
    print("================")
    print(f"{params}")
    print("x站热门视频插件被调用")
    print("================")
