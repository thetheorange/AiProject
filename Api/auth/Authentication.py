"""
Des 统一用户鉴权接口
@Author thetheOrange
Time 2024/5/19
"""
from . import auth_blu


@auth_blu.route("/auth")
def test() -> str:
    return "check auth"
