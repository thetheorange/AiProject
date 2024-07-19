"""
Des 设置界面
@Author thetheOrange
Time 2024/6/16
"""
import json

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from qfluentwidgets import ComboBox, SpinBox, DoubleSpinBox, PushButton, LineEdit, InfoBar, InfoBarPosition

from Views.GlobalSignal import global_signal
from Sqlite.Static import static


class SettingWindow(QWidget):
    """
    设置界面
    """
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        loadUi("Templates/setting.ui", self)
        # =============================================用户设置start=============================================
        self.login_button.clicked.connect(self.login)
        # =============================================用户设置start=============================================
        # =============================================视觉设置start=============================================

        # 主题选择下拉框
        self.choice_theme: ComboBox

        # 字体大小选择框
        self.font_size_setting: SpinBox
        self.font_size_setting.setRange(12, 20)

        # =============================================视觉设置end=============================================
        # =============================================大模型参数设置start=============================================

        # 回复长度限制
        self.limit_token_spin_box: SpinBox
        self.limit_token_spin_box.setRange(1, 8192)

        # top-k随机性
        self.top_k_spin_box: SpinBox
        self.top_k_spin_box.setRange(1, 6)

        # temperature灵活度
        self.temperature_spin_box: DoubleSpinBox
        self.temperature_spin_box.setRange(0.0, 1.0)

        # 历史消息长度压缩阈值
        self.history_compress_limit_spin_box: SpinBox
        self.history_compress_limit_spin_box.setRange(5, 20)

        # self.duihuan_PushButton: PushButton
        self.duihuan_PushButton.clicked.connect(self.get_tokens)
        self.LineEdit: LineEdit
        self.LineEdit2: LineEdit
        # =============================================大模型参数设置end=============================================

    def login(self):
        """
        登录按钮
        """
        self.signal.emit("start_login")
        global_signal.ChatOperation.emit("start_login")
        print("print: start_login")
        # login_window=LoginWindow()

    def get_tokens(self):
        """兑换"""
        print("push")
        try:
            text = self.LineEdit.text()
            if not text:
                InfoBar.error(
                    title="输入错误",
                    content="输入不能为空",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=1000,
                    parent=self
                )
                return
            r = None
            for i in range(2):
                print("here")
                r = requests.post(url=r"http://47.121.115.252:8193/user/get_token",
                                  headers={
                                      "Content-Type": "application/json"
                                  },
                                  data=json.dumps({
                                      "token_id": text,  # 令牌id
                                      "user_id": static.uuid,  # 用户id
                                      "user_academy": self.LineEdit2.text()  # 用户所属学院
                                  }))
                # print(r.request.body)
                # print(r.content.decode())
                if r.status_code == 200:
                    # 检查是否登录成功
                    code = r.json()["code"]
                    if code != 0:
                        InfoBar.error(
                            title="兑换状态",
                            content=r.json()['msg'],
                            orient=Qt.Vertical,
                            isClosable=True,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            duration=1000,
                            parent=self
                        )
                    else:
                        # 唯一登录成功状态
                        InfoBar.success(
                            title="登录状态",
                            content=r.json()['msg'],
                            orient=Qt.Vertical,
                            isClosable=True,
                            position=InfoBarPosition.BOTTOM_RIGHT,
                            duration=1000,
                            parent=self
                        )
                    break
                # time.sleep(0.1)
            if r.status_code != 200:
                InfoBar.error(
                    title="登录状态",
                    content=f"网络异常 {r.status_code}",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=1000,
                    parent=self
                )
        except Exception as e:
            print(str(e))
