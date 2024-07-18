"""
Des 设置界面
@Author thetheOrange
Time 2024/6/16
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from qfluentwidgets import ComboBox, SpinBox, DoubleSpinBox
from GlobalSignal import global_signal
from Views.LoginWindow import LoginWindow


class SettingWindow(QWidget):
    """
    设置界面
    """
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        loadUi("../Templates/setting.ui", self)
        # =============================================用户设置start=============================================
        self.login_button.clicked.connect(self.login)
        # =============================================用户设置start=============================================
        # =============================================视觉设置start=============================================

        # 主题选择下拉框
        self.choice_theme: ComboBox

        # 字体大小选择框
        self.font_size_setting: SpinBox
        self.font_size_setting.setRange(12, 20)

        # =============================================视觉设置end=============================================
        # =============================================大模型参数设置start=============================================

        # 回复长度限制
        self.limit_token_spin_box: SpinBox
        self.limit_token_spin_box.setRange(1, 8192)

        # top-k随机性
        self.top_k_spin_box: SpinBox
        self.top_k_spin_box.setRange(1, 6)

        # temperature灵活度
        self.temperature_spin_box: DoubleSpinBox
        self.temperature_spin_box.setRange(0.0, 1.0)

        # 历史消息长度压缩阈值
        self.history_compress_limit_spin_box: SpinBox
        self.history_compress_limit_spin_box.setRange(5, 20)

        # =============================================大模型参数设置end=============================================

    def login(self):
        """
        登录按钮
        """
        self.signal.emit("start_login")
        global_signal.ChatOperation.emit("start_login")
        print("print: start_login")
        # login_window=LoginWindow()
