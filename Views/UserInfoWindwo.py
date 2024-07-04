"""
Des 用户信息展示页
@Author thetheOrange
Time 2024/6/12
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from qfluentwidgets import AvatarWidget


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

        # =============================================基础设置end=============================================
