"""
Des api状态code类 描述各个接口的不同状态信息
@Author thetheOrange
Time 2024/5/22
"""


class StatusCode:
    # 鉴权相关状态start ================================

    # 注册错误
    RegisterError: str = "REGISTER_ERROR"
    # 登录错误
    LoginError: str = "LOGIN_ERROR"

    # 鉴权相关状态end ================================

    # 大模型使用相关状态start ================================

    # 大模型使用相关状态end ================================
