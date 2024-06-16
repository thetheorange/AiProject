"""
Des 面具相关界面
@Author thetheOrange
Time 2024/6/14
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.uic import loadUi
from qfluentwidgets import PushButton, FluentIcon, ToolTipFilter, ToolTipPosition, CommandBar, Icon, MessageBoxBase, \
    SubtitleLabel, LineEdit, PlainTextEdit


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

        # =============================================基础设置end=============================================
