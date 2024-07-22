"""
Des 主界面
@Author thetheOrange
Time 2024/6/14
"""

import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import FluentIcon, SplitFluentWindow, \
    NavigationAvatarWidget, NavigationItemPosition

from Sqlite.ChatSql import ChatSql
from Sqlite.Static import static
from Views.ChatWindow import ChatSearchWindow, ChatSessionWindow
from Views.GlobalSignal import global_signal
from Views.LoginWindow import LoginWindow
from Views.MaskWindow import MaskSettingWindow
from Views.SettingWindow import SettingWindow
from Views.UserInfoWindwo import UserInfoWindow


class MainWindow(SplitFluentWindow):
    """
    主界面
    """

    def __init__(self):
        super().__init__()
        # =============================================基础设置start=============================================

        self.setWindowTitle("所见即所得")
        self.setWindowIcon(QIcon("../Assets/image/logo_orange.png"))

        self.setMinimumSize(600, 500)
        self.resize(800, 600)

        self.__init_navigation()
        self.login_window: QWidget | None = None

        if static.username == "未登录":
            # 应该隐藏主窗口，调出登录窗口
            global_signal.ChatOperation.emit("start_login")
        else:
            sql = ChatSql()
            id = sql.get_account_id(static.username)
            if id is None:
                global_signal.ChatOperation.emit("start_login")
            else:
                static.sql_account_id = id
                global_signal.ChatOperation.emit("close_login_success")

        # self.login_history()
        # =============================================基础设置end=============================================

    def login_history(self):
        """
        根据历史登录信息，直接登录。此处为测试占位
        """
        static.uuid = "xxx"
        static.username = "xxx"
        static.sql_account_id = 1
        global_signal.ChatOperation.emit("close_login_success")

    def __init_navigation(self) -> None:
        """
        初始化导航栏
        :return:
        """
        # 添加子界面
        # 用户信息展示页
        self.user_info_window = UserInfoWindow()
        self.addSubInterface(self.user_info_window, FluentIcon.HOME, "我的")
        # 面具设置页
        self.mask_info_window = MaskSettingWindow()
        self.addSubInterface(self.mask_info_window, FluentIcon.ROBOT, "面具设置")

        self.navigationInterface.addSeparator()

        # 聊天选择界面
        self.chat_search_window = ChatSearchWindow()
        self.addSubInterface(self.chat_search_window, FluentIcon.CHAT, "聊天")

        # 设置窗口
        self.setting_window = SettingWindow()
        self.addSubInterface(self.setting_window, FluentIcon.SETTING, "设置", position=NavigationItemPosition.BOTTOM)
        self.setting_window.signal.connect(self.setting_signal)
        # 向导航栏底部添加用户头像
        self.navigationInterface.addWidget(
            routeKey="avatar",
            widget=NavigationAvatarWidget("thetheorange", static.avatar_path),
            position=NavigationItemPosition.BOTTOM
        )

        # 处理聊天窗口的信号
        global_signal.ChatOperation.connect(self.__handle_chat_signal)
        # 从选择聊天窗口跳转到选择面具窗口的信号处理
        global_signal.mask_chatOperation.connect(self.mask_chatOperation_signal)

    def setting_signal(self, signal: str) -> None:
        """
        设置里的信号
        """
        print("设置信号: ", signal)
        match signal:
            case "start_login":
                # 打开登录界面
                self.hide()
                self.login_window = LoginWindow()

            case "close_login_success":
                # 成功登录后
                self.user_info_window.info_show()
            case _:
                pass

    def mask_chatOperation_signal(self, signal: str) -> None:
        """
            从选择聊天窗口跳转到选择面具窗口
        """
        if signal == "choice_mask":
            # 切换当前窗口到会话界面
            self.stackedWidget.setCurrentWidget(self.mask_info_window)

    def create_window(self, name: str,id:int=-1,top:bool=True):
        self.chat_session_window = ChatSessionWindow(name=name,id=id)
        self.chat_session_window.setObjectName(name)
        self.addSubInterface(self.chat_session_window, FluentIcon.CHAT, name,
                             parent=self.chat_search_window)
        # 切换当前窗口到会话界面
        if top:
            self.stackedWidget.setCurrentWidget(self.chat_session_window)

    def __handle_chat_signal(self, signal: str) -> None:
        """
        处理各窗口的信号
        """
        print("全局信号：", signal)
        match signal:
            case "new_chat":
                # 会话的默认名字应该根据数据库读取目前的会话id数 命名 这里先用时间戳占位
                # if static.sql_dialogue_id == -1:  # 没有创建
                try:
                    session_name: str = "对话" + str(time.time())
                    sql = ChatSql()
                    sql.create_dialogue(session_name)
                    sql.get_dialogue_id_by_account_and_name(session_name)
                    self.create_window(session_name)

                    # # 修改窗口标题 提示用户目前在哪个会话
                    # self.setWindowTitle(session_name)
                except Exception as e:
                    print(str(e))
            case "start_chat": # 已经打开的窗口置顶
                pass
            case "start_login":
                # 打开登录界面
                self.hide()
                self.login_window = LoginWindow()

            case "close_login_success":
                # 成功登录后
                self.user_info_window.info_show()
                if self.login_window:
                    self.login_window.close()
                if not self.isVisible():
                    self.show()
                self.chat_search_window.update_dialogues()
                self.mask_info_window.update_masks()
                for data in static.dialogue_lisi:
                    try:
                        self.create_window(data['name'], data['id'], top=True)
                    except Exception as e:
                        print(str(e))

            case _:
                pass


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    try:
        w = MainWindow()
        # w.show()
    except Exception as e:
        print(str(e))
    sys.exit(app.exec_())
