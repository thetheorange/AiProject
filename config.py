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
        "password": "rust%admin"
    },
    # 配置flask服务器
    "flask": {
        "server": "0.0.0.0",
        "port": 5000,
        "jwt_secret": "S34d.}8Tkj63}B@"
    },
    # 讯飞平台api相关秘钥和必须参数
    "api": {
        "APPID": "60361ac3",
        "APIKEY": "7f8ff2dba8d566abb46791589ba9fed7",
        "API_SECRET": "NTM1ZGY3MjM0ODQxMDBhY2NjMDIyM2E5",
        "GPT_URL": "wss://spark-api.xf-yun.com/v3.5/chat",
        "DOMAIN": "generalv3.5"
    }
}
