"""
Des 文本纠错模型封装Socket类
    转换接口 instance.correct_text()
    主要针对语音和图片转换错误多的问题
@Author Misaka-xxw
Time 2024/5/26
"""
import hashlib
import base64
import json
import requests
from Core.Tools.generate_url import OriginAPI


class TextCorrectionSocket:
    """
    文本纠错模型封装Socket类
    :param APPID: 应用ID
    :param APIKey: 应用Key
    :param APISecret: 应用秘钥
    """

    def __init__(self, APPID, APISecret, APIKey):
        self.APPID = APPID
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.text = Text
        self.GptUrl = 'https://api.xf-yun.com/v1/private/s9a87e3ec'
        self.res: str = ""

    @staticmethod
    def sha256base64(data):
        """
        calculate sha256 and encode to base64
        """
        sha256 = hashlib.sha256()
        sha256.update(data)
        digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
        return digest

    def get_body(self):
        text = base64.b64encode(self.text.encode("utf-8")).decode('utf-8')
        body = {
            "header": {
                "app_id": self.APPID,
                "status": 3,
                # "uid":"your_uid"
            },
            "parameter": {
                "s9a87e3ec": {
                    # "res_id":"your_res_id",
                    "result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "input": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "status": 3,
                    "text": text
                }
            }
        }
        return body

    def correct_text(self, text: str = ""):
        """
        文本纠错
        """
        if text != "":
            self.text = text
        ws_param = OriginAPI(APPID=self.APPID,
                             APISecret=self.APISecret,
                             APIKey=self.APIKey,
                             GptUrl=self.GptUrl)
        request_url = ws_param.generate_url(method="POST ")
        headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': self.APPID}
        body = self.get_body()
        response = requests.post(request_url, data=json.dumps(body), headers=headers)
        print('onMessage：\n' + response.content.decode())
        tempResult = json.loads(response.content.decode())
        print(tempResult)
        advise = base64.b64decode(tempResult['payload']['result']['text']).decode()
        print('text字段解析：\n' + advise)
        advise = json.loads(advise)
        print(advise)
        self.res = self.text

        for words in advise["idm"]:
            if words[3] == '半角标点误用':
                self.res = self.res.replace(words[1], words[2])
        for words in advise["idm"]:
            self.res = self.res.replace(words[1], words[2])
        for words in advise["redund"]:
            self.res = self.res.replace(words[1], words[2])
        print(self.res)


if __name__ == '__main__':
    ...
# onMessage：
# {"message":"HMAC signature cannot be verified: fail to retrieve credential"}
