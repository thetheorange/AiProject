"""
Des 变量
@Author Misaka-xxw
Time 2024/7/14
"""


class Static:
    uuid: str = "0"
    username: str = "未登录"
    tokens: int = 0
    picTimes: int = 0
    logining: bool = False
    sql_account_id: int = -1
    sql_dialogue_id: int = -1
    mark_describe: str = ""
    avatar_path:str = "../Assets/image/logo.png"

static = Static()
