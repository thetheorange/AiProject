"""
Des 登录窗口
@Author thetheOrange
Time 2024/6/4
"""
import json
import sys
import time
import requests
from PyQt5.QtCore import Qt, QSize, QEventLoop, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.uic import loadUi
from qfluentwidgets import FluentIcon, CommandBar, PushButton, LineEdit, PasswordLineEdit, InfoBar, InfoBarPosition, \
    SplashScreen
from qfluentwidgets.common.icon import Icon

from Views.BaseWindow import BaseWindow
from Views.GlobalSignal import global_signal
from Views.RegisterWindow import RegisterWindow
from Sqlite.Static import static
from Sqlite.ChatSql import ChatSql
from Sqlite.LoginSql import LoginSql


class LoginWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        loadUi("../Templates/login.ui", self)

        # =============================================基础设置start=============================================

        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon("../Assets/Icons/sign.png"))

        # 设置登录和注册按钮手势
        self.login_button: PushButton
        self.register_link: PushButton
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.register_link.setCursor(Qt.PointingHandCursor)

        # 注册窗口
        self.register_win: RegisterWindow = RegisterWindow()

        # =============================================基础设置end=============================================

        # =============================================图片设置start=============================================

        window_icon: str = "../Assets/Image/logo_orange.png"
        background_img: str = "../Assets/image/background.jpg"
        logo_img: str = "../Assets/image/logo.svg"
        self.window_icon.setImage(QPixmap(window_icon).scaled(25, 25, Qt.KeepAspectRatio,
                                                              Qt.SmoothTransformation))
        self.banner.setImage(QPixmap(background_img).scaled(400, 400, Qt.KeepAspectRatio,
                                                            Qt.SmoothTransformation))
        self.logo.setImage(logo_img)

        # =============================================图片设置end=============================================

        # =============================================启动界面start=============================================

        # 1. 创建启动页面
        self.splashScreen = SplashScreen(QIcon(window_icon), self)
        self.splashScreen.setIconSize(QSize(200, 200))
        # 2. 在创建其他子页面前先显示主界面
        self.show()
        # 3. 创建子界面
        self.create_sub_interface()
        # 4. 隐藏启动页面
        self.splashScreen.finish()

        # =============================================启动界面end=============================================

        # =============================================CommandBar设置start=============================================

        self.command_bar: CommandBar
        # 最小化按钮
        min_btn: QAction = QAction(triggered=lambda x: self.showMinimized())
        min_btn.setIcon(Icon(FluentIcon.MINIMIZE))
        # 退出按钮
        exit_btn: QAction = QAction(triggered=lambda x: self.close())
        exit_btn.setIcon(Icon(FluentIcon.CLOSE))
        self.command_bar.setCursor(Qt.PointingHandCursor)
        self.command_bar.addAction(min_btn)
        self.command_bar.addAction(exit_btn)

        # =============================================CommandBar设置end=============================================

        self.__bind_signal()

    def __bind_signal(self) -> None:
        """
        绑定信号与槽

        :return:
        """
        self.login_button.clicked.connect(self.login)
        self.register_link.clicked.connect(lambda x: self.register_win.show())

    def login(self) -> None:
        """
        登录事件

        :return:
        """
        self.user_name_input: LineEdit  # 用户名
        self.pwd_input: PasswordLineEdit  # 用户密码
        # 登录接口
        login_api: str = r'http://47.121.115.252:8193/auth/login'
        user_name: str = self.user_name_input.text()
        user_pwd: str = self.pwd_input.text()
        print(user_name, user_pwd)
        if not user_name or not user_pwd:
            InfoBar.error(
                title="登录状态",
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
            r = requests.post(url=login_api,
                              headers={
                                  "Content-Type": "application/json"
                              },
                              data=json.dumps({
                                  "username": user_name,
                                  "password": user_pwd
                              }))
            # print(r.request.body)
            # print(r.content.decode())
            if r.status_code == 200:
                # 检查是否登录成功
                code = r.json()["code"]
                if code != 0:
                    InfoBar.error(
                        title="登录状态",
                        content="登录错误",
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=1000,
                        parent=self
                    )
                else:
                    InfoBar.success(
                        title="登录状态",
                        content="登录成功",
                        orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=1000,
                        parent=self
                    )
                    print("json是这样的", r.json())
                    static.uuid = r.json()['uuid']
                    static.username = r.json()['username']
                    static.tokens = r.json()['tokens']
                    static.picTimes = r.json()['picTimes']
                    global_signal.ChatOperation.emit("close_login_success")
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

    def create_sub_interface(self) -> None:
        """
        启动界面

        :return:
        """

        loop = QEventLoop(self)
        QTimer.singleShot(1000, loop.quit)
        loop.exec()


if __name__ == "__main__":
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        app = QApplication(sys.argv)
        w = LoginWindow()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
