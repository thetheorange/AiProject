"""
Des 图片转文字模型封装Socket类
    转换接口 instance.translate_picture()
@Author Misaka-xxw
Time 2024/6/3
"""
import base64
import json
import requests
from Core.Tools.generate_url import OriginAPI


class PictureToTextSocket:
    """
    图片转文字封装Socket类
    :param APPID: 应用ID
    :param APIKey: 应用Key
    :param APISecret: 应用秘钥
    """

    def __init__(self, APPID, APISecret, APIKey):
        self.APPID = APPID
        self.APISecret = APISecret
        self.APIKey = APIKey
        self.GptUrl = 'http://api.xf-yun.com/v1/private/hh_ocr_recognize_doc'
        self.picture_path: str = ""
        self.res: str = ""

    def get_body(self, file_path):
        """
        :param file_path:图片的路径
        """
        file = open(file_path, 'rb')
        buf = file.read()
        body = {
            "header": {
                "app_id": self.APPID,
                "status": 3
            },
            "parameter": {
                "hh_ocr_recognize_doc": {
                    "recognizeDocumentRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "image": {
                    "encoding": "jpg",
                    "image": str(base64.b64encode(buf), 'utf-8'),
                    "status": 3
                }
            }
        }
        return body

    def translate_picture(self, picture_path: str = ""):
        """
        图片转文字
        :param picture_path:图片路径
        """
        if picture_path != "":
            self.picture_path = picture_path
        ws_param = OriginAPI(APPID=self.APPID,
                             APISecret=self.APISecret,
                             APIKey=self.APIKey,
                             GptUrl=self.GptUrl)
        request_url = ws_param.generate_url(method="POST")
        print(request_url)
        headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'appid': 'APPID'}
        body = self.get_body(file_path=picture_path)
        response = requests.post(request_url, data=json.dumps(body), headers=headers)
        print(response)
        re = response.content.decode('utf8')
        str_result = json.loads(re)
        print("\nresponse-content:", re)
        if str_result.__contains__('header') and str_result['header']['code'] == 0:
            renew_text = str_result['payload']['recognizeDocumentRes']['text']
            res = base64.b64decode(renew_text)
            self.res = json.loads(res)["whole_text"]
            print(self.res)


if __name__ == "__main__":
    ...
