"""
Des 变量
@Author Misaka-xxw
Time 2024/7/14
"""

from Sqlite.MyJson import MyJson


class Static(MyJson):
    uuid: str = "0"  # 在json里
    username: str = "未登录"  # 在json里
    tokens: int = 0  # 在json里
    picTimes: int = 0  # 在json里
    academy: str = ""
    logining: bool = False
    sql_account_id: int = -1
    sql_dialogue_id: int = -1
    mask_name: str = ""
    mark_describe: str = ""
    avatar_path: str = "./Assets/image/logo.png"
    dialogue_name: str = ""

    def __init__(self):
        super().__init__(json_path="./Sqlite/userinfo.json")
        self.uuid = self.data.get('uuid', "0")
        self.username = self.data.get('username', "未登录")
        self.tokens = self.data.get('tokens', 0)
        self.picTimes = self.data.get('picTimes', 0)
        self.sql_account_id = self.data.get('sql_account_id', -1)
        self.dialogue_lisi: list = []


static = Static()
