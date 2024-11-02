"""
Des 设置
@Author Misaka-xxw
Time 2024/11/2
"""
from Sqlite.MyJson import MyJson


class Setting(MyJson):
    system_tray: bool = True  # 点击esc或者右上角关闭键，是缩到任务栏（True）还是退出程序（False）

    def __init__(self):
        super().__init__(json_path="./Sqlite/config.json")
        self.system_tray = self.data.get('system_tray', True)


setting = Setting()
