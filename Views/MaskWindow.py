"""
Des 面具相关界面
@Author thetheOrange
Time 2024/6/14
"""
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtWidgets import QWidget, QAction, QApplication, QHBoxLayout, QLabel, QListWidgetItem
from PyQt5.uic import loadUi
from qfluentwidgets import PushButton, FluentIcon, ToolTipFilter, ToolTipPosition, CommandBar, Icon, MessageBoxBase, \
    SubtitleLabel, LineEdit, PlainTextEdit, ListWidget
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from GlobalSignal import  global_signal

class MaskSubSettingWindow(MessageBoxBase):
    """
    大模型面具设置子界面
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # 面具名输入框
        self.mask_name_input = LineEdit()
        self.mask_name_input.setPlaceholderText("输入新面具的名称")
        self.mask_name_input.setClearButtonEnabled(True)

        # 面具描述输入框
        self.mask_des_input = PlainTextEdit()
        self.mask_des_input.setPlaceholderText("这里填入您的面具描述，将作为system参数向模型发送请求，越细致越好")

        # 确认按钮
        self.yesButton.setText("提交")

        # 取消按钮
        self.cancelButton.setText("取消")

        # 将控件添加到布局中
        self.viewLayout.addWidget(self.mask_name_input)
        self.viewLayout.addWidget(self.mask_des_input)
        # 信号与槽
        self.yesButton.clicked.connect(self.on_yes_button_clicked)

    def on_yes_button_clicked(self):
        icon = FluentIcon.ROBOT
        mask_name = self.mask_name_input.text()
        mask_des = self.mask_des_input.toPlainText()
        data = {
            'name':  mask_name,
            'icon': icon
        }
        print(data)
        # 发射全局信号
        global_signal.mask_submitted.emit(data)


class MaskWidget(QWidget):
    '''
    每行面具样式
    '''

    def __init__(self, text, icon, parent=None):
        super(MaskWidget, self).__init__(parent)
        # 创建一个水平布局
        layout = QHBoxLayout()
        # 创建一个标签和一个按钮
        # self.label = QLabel()
        self.button = PushButton(icon, text)
        # 将标签和按钮添加到布局中
        # layout.addWidget(self.label)
        layout.addWidget(self.button)
        # 设置自定义小部件的布局
        self.setLayout(layout)

    def sizeHint(self):
        # 返回一个建议的大小，布局管理器可能会使用它
        # 但请注意，如果设置了最小/最大尺寸，则这些尺寸可能会覆盖它
        return QSize(100, 40)  # 示例值


class MaskSettingWindow(QWidget):
    """
    大模型面具设置界面
    """

    def __init__(self):
        super().__init__()
        loadUi("../Templates/mask_setting.ui", self)
        # =============================================基础设置start=============================================

        # 新建按钮
        self.add_mask: PushButton
        self.add_mask.setIcon(FluentIcon.ADD_TO)
        self.add_mask.setToolTip("新建一个新的面具✨")
        self.add_mask.installEventFilter(ToolTipFilter(self.add_mask, showDelay=300, position=ToolTipPosition.TOP))
        self.add_mask.clicked.connect(lambda x: MaskSubSettingWindow(self).exec())

        self.mask_info: ListWidget
        # =============================================基础设置end=============================================
        # 向列表中添加自定义小部件
        data_and_icons = [("机器学习", FluentIcon.ROBOT), ("机器学习", FluentIcon.CHAT),
                          ("小红书写手", FluentIcon.BOOK_SHELF)]

        for text, icon_name in data_and_icons:
            data={
                'name':text,
                'icon':icon_name
            }
            self.add_mask_list(data)
        global_signal.mask_submitted.connect(self.add_mask_list)
        #global_signal.ChatOperation.connect(self.test)
    def add_mask_list(self, data):
        item = QListWidgetItem(self.mask_info)
        name = data.get('name')
        icon = data.get('icon')
        # 创建CustomWidget实例，这里我们传递文本和一个模拟的图标名（实际实现可能需要调整）
        custom_widget = MaskWidget(name, icon)

        # 设置item的大小提示为custom_widget的大小提示
        item.setSizeHint(custom_widget.sizeHint())

        # 将custom_widget设置为item的widget
        self.mask_info.setItemWidget(item, custom_widget)



if __name__ == "__main__":
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        app = QApplication(sys.argv)
        w = MaskSettingWindow()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
