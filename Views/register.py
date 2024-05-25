"""
Des 生成四位数的随机验证码图片
@Author dty thetheOrange
Time 2024/5/25
"""

import os
import random
import string
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from Core.Tools.generate_captcha import Captcha


class LoginWindow(QWidget):
    """
    登录窗口
    """

    def __init__(self):
        super().__init__()

        loadUi("../Templates/register.ui", self)

        Window_icon: str = r"../Assets/icons/add.png"
        user_img_path: str = r"../Assets/Icons/user.png"

        self.setWindowTitle("注册界面")
        self.setWindowIcon(QIcon(Window_icon))
        pixmap = QPixmap(user_img_path).scaled(20, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_photo.setPixmap(pixmap)

        # 验证码图片设置
        self.captcha_img_path: str = r"../Temp"
        captcha: Captcha = Captcha(char_4=self.get_random_char(),
                                   captcha_path=self.captcha_img_path)

        self.captcha_current: str = captcha.char_4  # 当前的验证码

        pixmap = QPixmap(captcha.captcha_position).scaled(70, 80, Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)
        self.veri_code.setPixmap(pixmap)
        self.veri_code.setBorderRadius(10, 10, 10, 10)

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
        self.confirm_button.clicked.connect(self.sayHi)
        self.cancel_button.clicked.connect(self.sayHi)
        self.veri_code.clicked.connect(self.change_code_button_clicked)

    def change_code_button_clicked(self) -> None:
        """
        点击后切换验证码图片

        :return:
        """
        # 生成验证码图片
        captcha: Captcha = Captcha(char_4=self.get_random_char(),
                                   captcha_path=self.captcha_img_path)
        self.captcha_current: str = captcha.char_4

        pixmap = QPixmap(captcha.captcha_position).scaled(70, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.veri_code.setPixmap(pixmap)
        self.clear_captcha()

    def clear_captcha(self) -> None:
        """
        到验证码图片数量过多时，清除目录下的部分图片

        :return:
        """
        for captcha_name in os.listdir(self.captcha_img_path):
            if captcha_name != self.captcha_current:
                os.remove(os.path.join(self.captcha_img_path, captcha_name))

    def sayHi(self) -> None:
        """
        click对应的槽函数 测试

        :return:
        """
        print("hi")


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    LoginWindow = LoginWindow()
    LoginWindow.show()
    sys.exit(app.exec_())
