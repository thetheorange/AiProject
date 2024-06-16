"""
Des 全局信号
@Author thetheOrange
Time 2024/6/16
"""
from PyQt5.QtCore import QObject, pyqtSignal


class GlobalSignal(QObject):
    ChatOperation = pyqtSignal(str)


# 全局信号
global_signal = GlobalSignal()
