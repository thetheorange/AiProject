from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from qfluentwidgets import FlowLayout
from PyQt5.QtCore import QEasingCurve


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = FlowLayout(self, needAni=True)  # 启用动画

        # 自定义动画参数
        layout.setAnimation(250, QEasingCurve.OutQuad)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        layout.addWidget(QPushButton('aiko'))
        layout.addWidget(QPushButton('刘静爱'))
        layout.addWidget(QPushButton('柳井爱子'))
        layout.addWidget(QPushButton('aiko 赛高'))
        layout.addWidget(QPushButton('aiko 太爱啦😘'))

        self.resize(250, 300)


if __name__ == '__main__':
    app = QApplication([])
    window = Demo()
    window.show()
    app.exec_()