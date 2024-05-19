"""
Des 读写配置文件
@Author thetheOrange
Time 2024/5/5
"""
import json
import os.path

from Logging import app_logger


class Config:
    """
    读写配置文件
    """
    # 初始配置文件
    init_config = json.dumps({
        "a": 1
    })

    def __init__(self):
        # 配置文件的位置
        self.config_path: str = "./config.json"

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "init":
                return f"'{self.config_path}' -> {self.init_config}"
            case "path":
                return f"{self.config_path}"
            case "config":
                return f"{self.init_config}"
            case _:
                raise ValueError("Unknown format specifier")

    def __str__(self) -> str:
        return f"{self.read()}"

    def read(self) -> dict:
        """
        读取配置文件 返回字典对象
        :return:
        """
        try:
            if not os.path.exists(self.config_path):
                with open(self.config_path, "w") as f:
                    f.write(Config.init_config)
                    return {}
            else:
                with open(self.config_path, "r") as f:
                    content = json.loads(f.read())
                    return content
        except FileNotFoundError as e:
            app_logger.error(f"[READ CONFIG] ERROR {e}")

    def modify(self, *, key: any, value: any) -> bool:
        """
        修改配置文件 返回是否修改成功的bool值
        :return:
        """
        try:
            if not os.path.exists(self.config_path):
                with open(self.config_path, "w") as f:
                    f.write(Config.init_config)
                    return False
            else:
                # 读取旧数据
                content: dict = self.read()
                if key in content:
                    content[key] = value
                else:
                    app_logger.info("not found key to update")
                    return False
                # 写入新数据
                with open(self.config_path, "w") as f:
                    json.dump(content, f, indent=2)
                return True
        except Exception as e:
            app_logger.error(f"[MODIFY CONFIG] ERROR: {e}")
