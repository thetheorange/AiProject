"""
Des 语音转文字模型封装Socket类
    转换接口 instance.transform_voice()
@Author Misaka-xxw
Time 2024/5/18
"""
import os
import websocket
import base64
import json
from Core.Tools.generate_url import OriginAPI
import time
import ssl
import _thread as thread

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class VideoToTextModel(object):
    def __init__(self, APPID: str, APIKey: str, APISecret: str):
        """
        语音转文字模型封装Socket类
        :param APPID: 应用ID
        :param APIKey: 应用Key
        :param APISecret: 应用秘钥
        """
        self.APPID: str = APPID
        self.APIKey: str = APIKey
        self.APISecret: str = APISecret
        self.AudioFile: str = ""
        self.translate_text: str = ""
        # 公共参数(common)
        self.CommonArgs: dict = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs: dict = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo": 1,
                                   "vad_eos": 10000}
        self.GptUrl: str = 'wss://ws-Api.xfyun.cn/v2/iat'
        websocket.enableTrace(False)

    def transform_voice(self, audio_path: str = "") -> None:
        """
        语音转文字
        :param audio_path:音频路径。最好是pcm文件
        :return:
        """
        try:
            self.translate_text = ""
            if audio_path != "":
                self.AudioFile = audio_path
            if not os.path.exists(self.AudioFile):
                print("The audio file does not exist")
                return
            ws_param = OriginAPI(APPID=self.APPID,
                                 APISecret=self.APISecret,
                                 APIKey=self.APIKey,
                                 GptUrl=self.GptUrl)
            ws_url: str = ws_param.generate_url()
            ws = websocket.WebSocketApp(ws_url,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
            ws.on_open = self.on_open
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except Exception as e:
            print(str(e))

    def on_message(self, ws, message):
        """
        收到websocket消息的处理
        :param ws:
        :param message: 消息
        :return:
        """
        result = ""
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                data = json.loads(message)["data"]["result"]["ws"]
                # print(json.loads(message))
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                        print(result)
                print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
                self.translate_text += result
        except Exception as e:
            print("receive msg,but parse exception:", e)

    @staticmethod
    def on_error(ws, error):
        """
        收到websocket错误的处理，这是一个静态方法
        :param ws:
        :param error: 错误信息
        :return:
        """
        print("### error:", error)

    @staticmethod
    def on_close(ws, a, b):
        """
        收到websocket关闭的处理，这也是静态方法
        :param ws:
        :param a:
        :param b:
        :return:
        """
        print("### closed ###")

    def on_open(self, ws):
        """
        收到websocket连接建立的处理
        :param ws:
        :return:
        """

        def run(*args):
            frame_size = 8000  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(self.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frame_size)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    # 发送第一帧音频，带business 参数
                    # appid 必须带上，只需第一帧发送
                    if status == STATUS_FIRST_FRAME:
                        d = {"common": self.CommonArgs,
                             "business": self.BusinessArgs,
                             "data": {"status": 0, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(intervel)
            ws.close()

        thread.start_new_thread(run, ())


# # debug:
# wsParam = VideoToTextModel(APPID='c2102d12', APISecret='M2FjNGEzMzI3ZDhmOTliNjc2NzVlNWY2',
#                            APIKey='a1dbd44505bae49287c7f7421f9be66e')
# wsParam.transform_voice(r"D:\录音\录音 (2).wav")
# print(wsParam.translate_text)
"""
返回类型：
[{"bg": 24, "cw": [{"sc": 0, "w": "那么"}]}, {"bg": 80, "cw": [{"sc": 0, "w": "耳机"}]}, {"bg": 136, "cw": [{"sc": 0, "w": "是否"}]}, {"bg": 196, "cw": [{"sc": 0, "w": "能"}]}, {"bg": 220, "cw": [{"sc": 0, "w": "入"}]}, {"bg": 248, "cw": [{"sc": 0, "w": "的"}]}, {"cw": [{"sc": 0, "w": "了"}], "bg": 276}]
sid:iat000d4bba@dx18f8ba713aaa12b802 call success!,data is:[{"bg": 307, "cw": [{"sc": 0, "w": "？"}]}]
"""