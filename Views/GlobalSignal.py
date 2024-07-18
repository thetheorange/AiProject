"""
Des 全局信号
@Author thetheOrange
Time 2024/6/16
"""
from PyQt5.QtCore import QObject, pyqtSignal


class GlobalSignal(QObject):
    ChatOperation = pyqtSignal(str)
    # 从面具窗口跳转聊天窗口
    ChatOperation_Mask = pyqtSignal(str)
    # 从聊天窗口跳转面具窗口
    mask_chatOperation = pyqtSignal(str)
    # 传递面具名和描述
    mask_submitted = pyqtSignal(dict)
    # 提示错误信息的信号
    error_msg = pyqtSignal(list)
    # 录音成功信息传递
    audio_submitted = pyqtSignal(str)


# 全局信号
global_signal = GlobalSignal()

if __name__ == "__main__":
    ...
