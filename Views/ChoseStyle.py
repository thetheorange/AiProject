"""
Des 亚克力窗口选择
@Author dty Misaka-xxw
Time 2024/5/26
"""
import sys

from PyQt5.QtCore import QOperatingSystemVersion

# from PyQt5.QtWidgets import QWidget

is_win11: bool = sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

if is_win11:
    from qframelesswindow import AcrylicWindow as MyWindow
else:
    from qframelesswindow import FramelessWindow as MyWindow


class ChoseWindow(MyWindow):
    """
    亚克力window
    """

    def __init__(self, transparent:bool=True):
        """
        亚克力window
        :param transparent:是否为无边框界面。逻辑还不对但是先这样
        """
        super().__init__()
        if is_win11 and transparent:
            self.setAcrylicEffectEnabled(True)
        elif is_win11:
            self.setAcrylicEffectEnabled(False)

    def setAcrylicEffectEnabled(self, enable: bool):
        """ 设置亚克力效果 """
        if enable:
            self.setStyleSheet("background:transparent")
            if isinstance(self, MyWindow):
                self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F299")
                if QOperatingSystemVersion.current() != QOperatingSystemVersion.Windows10:
                    self.windowEffect.addShadowEffect(self.winId())
        else:
            self.setStyleSheet("background:#F2F2F2")
            if isinstance(self, MyWindow):
                self.windowEffect.removeBackgroundEffect(self.winId())
                self.windowEffect.removeShadowEffect(self.winId())
