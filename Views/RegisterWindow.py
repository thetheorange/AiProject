"""
注册界面
Des 用于用户登录
@Author dty thetheOrange
Time 2024/5/26
"""
import json
import os
import string
import random
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi
from qfluentwidgets import Dialog, InfoBar, InfoBarPosition

from Core.Tools.generate_captcha import Captcha
from Core.Tools.readQss import ReadQss


class RegisterWindow(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("../Templates/register.ui", self)

        # =============================================基础设置start=============================================

        Window_icon: str = r"../Assets/icons/add.png"
        self.setWindowTitle("注册")
        self.setWindowIcon(QIcon(Window_icon))
        # 加载qss样式
        self.setStyleSheet(ReadQss.read("../Assets/Qss/register.qss"))

        # =============================================基础设置end=============================================

        # =============================================验证码图片设置start=============================================

        self.captcha_img_path: str = r"../Temp"
        captcha: Captcha = Captcha(char_4=self.get_random_char(),
                                   captcha_path=self.captcha_img_path)

        self.captcha_current: str = captcha.char_4  # 当前的验证码

        pixmap = QPixmap(captcha.captcha_position).scaled(100, 100, Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)
        self.captcha_img.setPixmap(pixmap)
        self.captcha_img.setBorderRadius(10, 10, 10, 10)

        # =============================================验证码图片设置end=============================================

        self.__bind_sign()

    @staticmethod
    def get_random_char() -> str:
        """
        生成一个由4个随机字符（包括ascii字母和数字）组成的字符串。

        :return: 4个随机字符组成的字符串。
        """
        chr_all = string.ascii_letters + string.digits
        return ''.join(random.sample(chr_all, 4))

    def __bind_sign(self) -> None:
        """
        绑定信号与槽

        :return:
        """
        self.captcha_img.clicked.connect(self.change_captcha)
        self.register_button.clicked.connect(self.register)

    def change_captcha(self) -> None:
        """
        点击后切换验证码图片

        :return:
        """
        try:
            captcha: Captcha = Captcha(char_4=self.get_random_char(),
                                       captcha_path=self.captcha_img_path)
            self.captcha_current: str = captcha.char_4
            print(self.captcha_current)

            pixmap = QPixmap(captcha.captcha_position).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.captcha_img.setPixmap(pixmap)
            self.clear_captcha()
        except Exception as e:
            print(str(e))

    def clear_captcha(self) -> None:
        """
        到验证码图片数量过多时，清除目录下的部分图片

        :return:
        """
        for captcha_name in os.listdir(self.captcha_img_path):
            if captcha_name != self.captcha_current:
                os.remove(os.path.join(self.captcha_img_path, captcha_name))

    def register(self) -> None:
        """
        发送注册消息

        :return:
        """

        # 用户名
        user_name: str = self.user_name_input.text()
        # 邮箱
        user_email: str = self.email_input.text()
        # 密码
        user_pwd: str = self.password_input.text()
        # 学校
        user_academy: str= self.academy_input.text()
        # 验证码
        input_captcha: str = self.captcha_input.text()

        # 注册接口
        register_api: str = r"http://47.121.115.252:8193/auth/register"

        if not user_name and not user_email and not user_pwd and not input_captcha:
            InfoBar.error(
                title="注册状态",
                content="输入不能为空",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=1000,
                parent=self
            )
            return

        if input_captcha == self.captcha_current:
            r = requests.post(url=register_api,
                              headers={
                                  "Content-Type": "application/json"
                              },
                              data=json.dumps({
                                  "username": user_name,
                                  "password": user_pwd,
                                  "email": user_email,
                                  "academy":user_academy
                              }))
            print(r.request.body)
            print(r.content.decode())
            if r.status_code == 200:
                # 检查是否注册成功
                code: int | str = r.json()["code"]
                if code != 0:
                    InfoBar.error(
                        title="注册状态",
                        content="用户名已存在",
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=1000,
                        parent=self
                    )
                else:
                    InfoBar.success(
                        title="注册状态",
                        content="注册成功",
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=1000,
                        parent=self
                    )
            else:
                InfoBar.error(
                    title="注册状态",
                    content="注册失败，请检查网络",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=1000,
                    parent=self
                )
        else:
            InfoBar.error(
                title="验证码错误",
                content="请检查验证码输入是否正确",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=1000,
                parent=self
            )


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    RegisterW = RegisterWindow()
    RegisterW.show()
    sys.exit(app.exec_())
