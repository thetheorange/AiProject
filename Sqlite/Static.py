"""
Des 变量
@Author Misaka-xxw
Time 2024/7/14
"""
import json


class Static:
    uuid: str = "0"  # 在json里
    username: str = "未登录"  # 在json里
    tokens: int = 0  # 在json里
    picTimes: int = 0  # 在json里
    academy: str = ""
    logining: bool = False
    sql_account_id: int = -1
    sql_dialogue_id: int = -1
    mask_name:str = ""
    mark_describe: str = ""
    avatar_path: str = "./Assets/image/logo.png"
    dialogue_name:str=""

    def __init__(self):
        self.data: json
        with open("./Sqlite/userinfo.json", 'r') as f:
            self.data = json.load(f)
            data = self.data
            self.uuid = data.get('uuid', "0")
            self.username = data.get('username', "未登录")
            # self.academy = data.get('academy', "未填写")
            self.tokens = data.get('tokens', 0)
            self.picTimes = data.get('picTimes', 0)
            # self.logining = data.get('logining', False)
            self.sql_account_id = data.get('sql_account_id', -1)
            self.dialogue_lisi: list = []
            # self.sql_dialogue_id = data.get('sql_dialogue_id', -1)
            # self.mark_describe = data.get('mark_describe', "")

    def rewrite(self, title_key: str, info):
        """重新写入某一个值"""
        self.data[title_key] = info
        with open("./Sqlite/userinfo.json", 'w') as f:
            json.dump(self.data, f)


static = Static()
