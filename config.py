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
        "jwt_secret": "xxxx"
    },
    # 讯飞平台api相关秘钥和必须参数
    "api": {
        "APPID": "xxxx",
        "APIKEY": "xxxx",
        "API_SECRET": "xxxx",
        "GPT_URL": "wss://spark-api.xf-yun.com/v3.5/chat",
        "DOMAIN": "generalv3.5"
    }
}