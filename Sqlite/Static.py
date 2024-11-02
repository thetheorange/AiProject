"""
Des 变量
@Author Misaka-xxw
Time 2024/7/14
"""

import json
import os

from Logging import app_logger


class Static:
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
    json_path: str = "./Sqlite/userinfo.json"

    def __init__(self):
        self.data: dict = {}
        self.ensure_dir_exists()
        try:
            with open(self.json_path, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.init_json_file()

        self.uuid = self.data.get('uuid', "0")
        self.username = self.data.get('username', "未登录")
        self.tokens = self.data.get('tokens', 0)
        self.picTimes = self.data.get('picTimes', 0)
        self.sql_account_id = self.data.get('sql_account_id', -1)
        self.dialogue_lisi: list = []

    def ensure_dir_exists(self):
        """确保目录存在"""
        if not os.path.exists(os.path.dirname(self.json_path)):
            try:
                os.makedirs(os.path.dirname(self.json_path))
            except OSError as e:
                app_logger.error(f"创建目录失败: {e}")

    def init_json_file(self):
        """初始化JSON文件"""
        with open(self.json_path, 'w') as f:
            json.dump({}, f)

    def rewrite(self, title_key: str, info):
        """重新写入某一个值"""
        self.data[title_key] = info
        try:
            with open(self.json_path, 'w') as f:
                json.dump(self.data, f)
        except (json.JSONDecodeError, OSError) as e:
            app_logger.error(f"写入JSON文件失败: {e}")
            self.init_json_file()


static = Static()
