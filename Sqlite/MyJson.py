"""
Des json类基类
@Author Misaka-xxw
Time 2024/11/2
"""
import json
import os

from Logging import app_logger


class MyJson:
    def __init__(self, json_path=""):
        self.data: dict = {}
        self.json_path: str = json_path
        self.ensure_dir_exists()
        try:
            with open(self.json_path, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.init_json_file()

    def init_json_file(self):
        """初始化JSON文件"""
        with open(self.json_path, 'w') as f:
            json.dump({}, f)

    def rewrite(self, title_key: str, info):
        """
        重新写入某一个值

        :param title_key: 键值
        :param info: 内容
        """
        self.data[title_key] = info
        try:
            with open(self.json_path, 'w') as f:
                json.dump(self.data, f)
        except (json.JSONDecodeError, OSError) as e:
            app_logger.error(f"写入JSON文件失败: {e}")
            self.init_json_file()

    def ensure_dir_exists(self):
        """确保目录存在"""
        if not os.path.exists(os.path.dirname(self.json_path)):
            try:
                os.makedirs(os.path.dirname(self.json_path))
            except OSError as e:
                app_logger.error(f"创建目录失败: {e}")
