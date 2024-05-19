"""
Des 生成初始api接口地址 通用URL鉴权
@Author thetheOrange
Time 2024/5/5
"""
import base64
import datetime
import hashlib
import hmac
from time import mktime
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time


class OriginAPI:
    """
    生成初始的api接口地址
    """

    def __init__(self, *, APPID, APIKey, APISecret, GptUrl):
        self.APPID: str = APPID
        self.APIKey: str = APIKey
        self.APISecret: str = APISecret
        self.host: str = urlparse(GptUrl).netloc
        self.path: str = urlparse(GptUrl).path
        self.GptUrl: str = GptUrl

    def generate_url(self) -> str:
        """
        生成api接口
        :return str:
        """
        # 生成RFC1123格式的时间戳
        date: str = format_date_time(mktime(datetime.datetime.now().timetuple()))
        # 拼接字符串
        signature_origin: str = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha_base64: str = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin: str = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization: str = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 鉴权参数
        params: dict = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        return self.GptUrl + '?' + urlencode(params)
