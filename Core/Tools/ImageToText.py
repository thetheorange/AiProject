import requests
from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition

from Sqlite.Static import static


class ImageToText(object):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def img_text(self, path: str):
        """
        图片转文字
        """
        img_api: str = r"http://47.121.115.252:8193/PictureToTextModel/chat"
        uuid = static.uuid
        user_name = static.username
        # print(user_name, uuid)
        if uuid == 0 or user_name == '未登录':
            # print("!")
            InfoBar.error(
                title="图转文",
                content="请先登录",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=1000,
                parent=self.parent
            )
        else:
            for i in range(2):
                try:
                    # print(path)
                    r = requests.post(url=img_api,
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
                        print(r.json())
                        code = response_data.get("code", None)
                        text = response_data.get("content", None)
                        print(code, text)

                        if code != 0:
                            InfoBar.error(
                                title="识别失败",
                                content=r.json()['msg'],
                                orient=Qt.Vertical,
                                isClosable=True,
                                position=InfoBarPosition.BOTTOM_RIGHT,
                                duration=1000,
                                parent=self.parent
                            )
                        else:
                            print(text)
                            return text
                        break  # 如果成功，跳出循环
                    else:
                        InfoBar.error(
                            title="图转文",
                            content=f"网络异常 {r.status_code}",
                            orient=Qt.Vertical,
                            isClosable=True,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            duration=1000,
                            parent=self.parent
                        )
                except requests.RequestException as e:
                    print(f"请求错误: {e}")
                    if i == 1:  # 如果第二次也失败了，可以考虑抛出异常或进行其他处理
                        pass
                        # raise
        return None


convert2jpg(r"C:\Users\xwwy\Desktop\5b6635a4-7a2c-4dbc-a08e-58be8adf2b95.png")
