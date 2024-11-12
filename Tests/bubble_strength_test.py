from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy
from time import sleep

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)  # 创建垂直布局并设置给主窗口

        self.info_container = QWidget(self)  # 创建QWidget作为容器
        self.info_layout = QVBoxLayout(self.info_container)  # 创建垂直布局
        self.info_container.setLayout(self.info_layout)  # 将布局设置给容器

        self.label = QLabel("这是为什么啊！这是为什么啊！这是为什么啊！", self)  # 创建QLabel
        self.label.setWordWrap(True)  # 设置自动换行
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置QLabel的sizePolicy
        self.info_layout.addWidget(self.label)  # 将QLabel添加到布局中

        self.info_container.setStyleSheet("""
            QWidget {  
                background-color:#e6e6fa;             /* 背景色 */  
                border-radius: 10px;                   /* 圆角 */  
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影 */
            }  
            QLabel {                                  /* 假设文本容器中包含QLabel */  
                font-size: 30px;                       /* 字体大小 */  
                color: #333;                           /* 字体颜色 */
            }  
            QWidget:hover {                            /* 鼠标悬停效果 */  
                background-color: #dbc6e0;             /* 悬停时背景色变化 */  
            }  
        """)

        self.layout.addWidget(self.info_container)  # 将info_container添加到主窗口的布局中
        self.info_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # 设置info_container的sizePolicy

        self.setGeometry(800, 800, 800, 800)  # 设置窗口大小
        self.setWindowTitle('QLabel自动调整大小示例')  # 设置窗口标题
        self.show()

    def updateText(self):
        self.label.setText(self.label.text() + '呵呵')

if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    for i in range(60):
        ex.updateText()
        QApplication.processEvents()  # 确保界面更新
        sleep(0.01)  # 稍微暂停一下，以便观察效果
    app.exec_()