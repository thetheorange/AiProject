from PyQt5.QtWidgets import QWidget
from qfluentwidgets import (ListWidget,NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, qrouter, FluentWindow, NavigationAvatarWidget)
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QListWidget, QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys

class MaskWidget(QWidget):
    """
    子聊天框
    """
    def __init__(self):
        super().__init__()
        self.setObjectName("MaskWidget")

        self.listWidget = ListWidget()
        self.hBoxLayout = QHBoxLayout(self)
        stands = [
           '心理医生','职业顾问','英专选手','小红书写手'
        ]
        # 添加列表项
        for stand in stands:
            item = QListWidgetItem(stand)
            item.setIcon(QIcon('Assets/icons/eye.png'))
            self.listWidget.addItem(item)
        self.hBoxLayout.setContentsMargins(30, 50, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MaskWidget()
    w.show()
    sys.exit(app.exec_())

