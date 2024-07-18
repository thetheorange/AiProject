import requests
from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition
from Sqlite.Static import static


class AudiotoText(object):
    def __init__(self):
        super().__init__()

    def audio_text(self, path: str):
        """
        音频转文字
        """
        audio_api: str = r"http://47.121.115.252:8193/voiceModel/chat"
        uuid = static.uuid
        user_name = static.username
        # print(user_name, uuid)
        if uuid == 0 or user_name == '未登录':
            # print("!")
            InfoBar.error(
                title="音转文",
                content="请先登录",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=1000,
                parent=self
            )
        else:
            for i in range(2):
                try:
                    # print(path)
                    r = requests.post(url=audio_api,
                                      headers={
                                          "uuid": uuid,
                                          "username": user_name,
                                      },
                                      files={
                                          "file": open(path, "rb")
                                      })
                    # print("r.status_code", r.status_code)
                    # print(requests.json())
                    if r.status_code == 200:
                        response_data = r.json()
                        code = response_data.get("code", None)
                        text = response_data.get("content", None)
                        if code != 0:
                            InfoBar.error(
                                title="音转文",
                                content="识别失败",
                                orient=Qt.Vertical,
                                isClosable=True,
                                position=InfoBarPosition.BOTTOM_RIGHT,
                                duration=1000,
                                parent=self
                            )
                        else:

                            return text
                        break  # 如果成功，跳出循环
                    else:
                        InfoBar.error(
                            title="音转文",
                            content=f"网络异常 {r.status_code}",
                            orient=Qt.Vertical,
                            isClosable=True,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            duration=1000,
                            parent=self
                        )
                except requests.RequestException as e:
                    print(f"请求错误: {e}")
                    if i == 1:  # 如果第二次也失败了，可以考虑抛出异常或进行其他处理
                        raise
        return None
