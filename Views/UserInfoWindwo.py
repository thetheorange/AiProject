"""
Des 用户信息展示页
@Author thetheOrange
Time 2024/6/12
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.uic import loadUi
from qfluentwidgets import AvatarWidget

from Sqlite.Static import static


class UserInfoWindow(QWidget):
    """
    用户信息展示页
    """

    def __init__(self):
        super().__init__()
        loadUi("../Templates/user_info.ui", self)

        # =============================================基础设置start=============================================
        # 设置用户默认头像
        avatar_img: str = "../Assets/image/background.jpg"
        self.avatar: AvatarWidget
        self.avatar.setImage(QPixmap(avatar_img).scaled(125, 125, Qt.KeepAspectRatio,
                                                        Qt.SmoothTransformation))
        self.avatar.setRadius(64)
        # 用户信息标签
        self.user_name_label: QLabel
        self.email_label: QLabel
        self.id_label: QLabel
        self.info_show()
        # =============================================基础设置end=============================================

    def info_show(self):
        """
        用户信息bar的展示
        """
        self.user_name_label.setText(f'Username: \t{static.username}')
        # self.email_label.setText(f'Email: ')
        # self.id_label.setText(f'Id: {static}')

