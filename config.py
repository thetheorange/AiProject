"""
Des 配置文件
@Author thetheOrange
Time 2024/6/12
"""

config_json: dict = {
    # 配置mysql
    "mysql": {
        "server": "192.168.188.128",
        "port": 3306,
        "database": "User",
        "username": "rust",
        "password": "..."
    },
    # 配置flask服务器
    "flask": {
        "server": "0.0.0.0",
        "port": 5120
    }
}
