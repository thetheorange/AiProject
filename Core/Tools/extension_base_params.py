from dataclasses import dataclass


@dataclass
class BaseParams:
    # 模型类型
    model: str
    # 插件名称
    name: str
    # 返回的数据类型
    data_type: str
    # 向大模型传入的参数 (name, type, description)
    properties: list[tuple]
    # 需要返回的参数 返回的参数会被封装成字典
    required: list[str]
