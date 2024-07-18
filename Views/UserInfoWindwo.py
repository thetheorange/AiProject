"""
Des 用户信息展示页
@Author thetheOrange
Time 2024/6/12
"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.uic import loadUi
from qfluentwidgets import AvatarWidget, PushButton, FluentIcon, ToolButton,Icon

from Sqlite.Static import static
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication
from Views.FileWindow import FileWindow


class UserInfoWindow(QWidget):
    """
    用户信息展示页
    """

    def __init__(self):
        super().__init__()
        loadUi("../Templates/user_info.ui", self)

        # =============================================基础设置start=============================================
        # 设置用户默认头像
        self.avatar_img: str = "../Assets/image/background.jpg"
        self.avatar: AvatarWidget
        self.avatar.setImage(QPixmap(self.avatar_img).scaled(125, 125, Qt.KeepAspectRatio,
                                                             Qt.SmoothTransformation))
        self.avatar.setRadius(64)
        # self.change_avatar_button = PushButton(FluentIcon.ADD, '更换头像')
        # self.change_avatar_button .setIcon(Icon(FluentIcon.ADD))
        self.change_avatar_button.clicked.connect(self.change_avatar)
        # 用户信息标签
        self.user_name_label: QLabel
        self.email_label: QLabel
        self.id_label: QLabel
        self.info_show()
        # =============================================基础设置end=============================================

    def change_avatar(self):
        file_window = FileWindow()
        self.avatar_img = file_window.open_file_dialog()
        self.avatar.setImage(QPixmap(self.avatar_img).scaled(125, 125, Qt.KeepAspectRatio,
                                                             Qt.SmoothTransformation))

    def info_show(self):
        """
        用户信息bar的展示
        """
        self.user_name_label.setText(f'Username: \t{static.username}')
        # self.email_label.setText(f'Email: ')
        # self.id_label.setText(f'Id: {static}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    userinfowindow = UserInfoWindow()
    userinfowindow.show()
    sys.exit(app.exec_())
