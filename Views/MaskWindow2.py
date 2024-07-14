from qfluentwidgets import PushButton, ToolTipFilter, ToolTipPosition, MessageBoxBase, \
    LineEdit, PlainTextEdit, ListWidget, SearchLineEdit, MessageBox, FlowLayout
from qfluentwidgets import FluentIcon
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QHBoxLayout, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import PushButton, ToolTipFilter, ToolTipPosition, MessageBoxBase, \
    LineEdit, PlainTextEdit, ListWidget, SearchLineEdit, MessageBox
from qfluentwidgets import FluentIcon
from AiProject2.AiProject.Views.GlobalSignal import global_signal

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QPushButton


# 假设您已经有了 FlowLayout 的实现，或者您可以使用第三方库中的流式布局
# 这里我们使用一个简化的 FlowLayout 占位符

class MaskSettingWindow2(QWidget):
    def __init__(self):
        super().__init__()
        #loadUi("../Templates/mask_setting2.ui", self)

        # 设置主窗口的垂直布局
        self.mainLayout = QVBoxLayout(self)

        # 创建上半部分的水平布局
        self.topLayout = QHBoxLayout()

        # 向上半部分添加小部件
        self.topLayout.addWidget(SearchLineEdit())
        self.add_mask = PushButton("添加面具")
        self.add_mask.setIcon(FluentIcon.ADD_TO)
        self.add_mask.setToolTip("新建一个新的面具")
        self.topLayout.addWidget(self.add_mask)

        # 将水平布局添加到垂直布局中
        self.mainLayout.addLayout(self.topLayout)

        # 创建下半部分的流式布局
        self.bottomLayout = FlowLayout()

        self.data_and_icons = [("机器学习", FluentIcon.ROBOT), ("英语写作", FluentIcon.CHAT),
                               ("小红书写手", FluentIcon.BOOK_SHELF), ("数学物理", FluentIcon.CALENDAR)]
        for text, icon_name in self.data_and_icons:
            self.bottomLayout.addWidget(PushButton(icon_name, text))
        # 将流式布局添加到垂直布局中
        self.mainLayout.addLayout(self.bottomLayout)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MaskSettingWindow2()
    window.setWindowTitle('Mixed Layouts Example')
    window.show()
    sys.exit(app.exec_())
