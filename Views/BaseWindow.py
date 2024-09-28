"""
Des 无边框、窗口透明化、可拉伸、可拖动的窗体
@Author thetheOrange
Time 2024/6/15
"""
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMouseEventTransition


class BaseWindow(QWidget):
    """
    无边框、窗口透明化、可拉伸、可拖动的窗体
    """

    def __init__(self):
        super().__init__()
        # 设置窗口无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口透明化
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置窗口鼠标追踪
        self.setMouseTracking(True)

        # 鼠标偏移量
        self.__change_pos:int = 0
        # 鼠标起始值
        self.__start_pos:int = 0
        # 鼠标移动标志
        self.__move_flag:bool = False

        # 判断鼠标在哪个边界处的标志
        self.__right_flag = False
        self.__bottom_flag = False
        self.__corner_flag = False
        # 设置边界宽度
        self.__pad = 20
        # 设置边界范围
        self.__right_edge:list = []
        self.__bottom_edge:list = []
        self.__corner_edge:list = []

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # 获取窗口的边界范围
        # 右侧边缘
        self.__right_edge = [QPoint(x, y) for x in range(self.width() - self.__pad, self.width() + 1)
                             for y in range(0, self.height() - self.__pad)]
        # 底部边缘
        self.__bottom_edge = [QPoint(x, y) for x in range(0, self.width() - self.__pad)
                              for y in range(self.height() - self.__pad, self.height() + 1)]
        # 右下角边缘
        self.__corner_edge = [QPoint(x, y) for x in range(self.width() - self.__pad, self.width() + 1)
                              for y in range(self.height() - self.__pad, self.height() + 1)]

        if self.__move_flag:
            # 计算鼠标偏移量
            self.__change_pos = event.pos() - self.__start_pos
            # 移动窗口
            self.move(self.pos() + self.__change_pos)

        # 检测鼠标在窗口的位置，改变鼠标手势
        if event.pos() in self.__right_edge:
            self.setCursor(Qt.SizeHorCursor)
        elif event.pos() in self.__bottom_edge:
            self.setCursor(Qt.SizeVerCursor)
        elif event.pos() in self.__corner_edge:
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        # 根据鼠标的方向改变窗口大小
        if self.__right_flag and Qt.LeftButton:
            self.resize(event.pos().x(), self.height())
            event.accept()
        elif self.__bottom_flag and Qt.LeftButton:
            self.resize(self.width(), event.pos().y())
            event.accept()
        elif self.__corner_flag and Qt.LeftButton:
            self.resize(event.pos().x(), event.pos().y())
            event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if Qt.LeftButton:
            # 获取鼠标当前位置
            self.__start_pos = QPoint(event.x(), event.y())
            # 设置鼠标移动状态为True
            self.__move_flag = True

            if event.pos() in self.__right_edge:
                self.__right_flag = True
                self.__move_flag = False
                event.accept()
            elif event.pos() in self.__bottom_edge:
                self.__bottom_flag = True
                self.__move_flag = False
                event.accept()
            elif event.pos() in self.__corner_edge:
                self.__corner_flag = True
                self.__move_flag = False
                event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            # 释放鼠标位置信息并将移动状态改为False
            self.__move_flag = False
            self.__start_pos = None
            self.__change_pos = None
            self.__right_flag = False
            self.__bottom_flag = False
            self.__corner_flag = False
