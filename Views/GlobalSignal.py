"""
Des 全局信号
@Author thetheOrange
Time 2024/6/16
"""
from PyQt5.QtCore import QObject, pyqtSignal


class GlobalSignal(QObject):
    ChatOperation = pyqtSignal(str)
    ChatOperation_Mask = pyqtSignal(str)
    mask_submitted = pyqtSignal(dict)  # 假设我们传递面具名和描述

# 全局信号
global_signal = GlobalSignal()

if __name__=="__main__":
    ...
