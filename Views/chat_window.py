"""
Des 聊天主界面
@Author thetheOrange
Time 2024/5/25
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QPushButton
from qfluentwidgets import SplitFluentWindow, FluentIcon

# from sub_chat_window import SubChatWindow
from chat import ChatWidget
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, qrouter, FluentWindow, NavigationAvatarWidget)

class MainChatWindow(SplitFluentWindow):
    """
    聊天主界面
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("聊天主界面")




        #导航栏按钮
        self.photohpath='../Asserts/icons/user.png'
        self.navigationInterface.addWidget(
            routeKey='settings',
            widget=NavigationAvatarWidget('个人中心', self.photohpath),
            onClick=self.settingwidget, # 槽函数
            position=NavigationItemPosition.BOTTOM,
        )
        self.photohpath2='../Asserts/icons/user.png'
        self.navigationInterface.addWidget(
            routeKey='mask',
            widget=NavigationAvatarWidget('面具',  self.photohpath2),
            onClick=self.maskwidget,
            position=NavigationItemPosition.TOP,
        )
        self.navigationInterface.addWidget(
            routeKey='insertion',
            widget=NavigationAvatarWidget('插件', self.photohpath2),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.TOP,
        )
        self.navigationInterface.addWidget(
            routeKey='newchat',
            widget=NavigationAvatarWidget('新的聊天', self.photohpath2),
            onClick=self.newchat,
            position=NavigationItemPosition.BOTTOM,
        )

    def settingwidget(self):
        print('hi')

    def maskwidget(self):
        print('hi')
    def newchat(self):
        # 添加子界面
        self.sub_chat_window = ChatWidget()
        # 第一个参数 添加的子界面对象， 第二个参数 导航栏所呈现的icon(建议直接用fluent框架提供的icon) 第三个参数 导航栏的所呈现的标题
        self.addSubInterface(self.sub_chat_window, FluentIcon.ROBOT, "聊天")
    def showMessageBox(self):
        #切换设置页面
        print('hi')



if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MainChatWindow()
    w.show()
    sys.exit(app.exec_())
