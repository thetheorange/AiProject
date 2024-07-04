from PyQt5.QtWidgets import QHBoxLayout, QFrame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QRegion
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QRegion
from PyQt5.QtCore import Qt
from qfluentwidgets import AvatarWidget
class AvatarContainer(QFrame):
    """
    聊天头像样式
    """

    def __init__(self, avatar_path: str, parent=None):
        super(AvatarContainer, self).__init__(parent, frameShape=QFrame.NoFrame)  # 无边框
        self.initUI(avatar_path)

    def initUI(self, avatar_path: str):
        self.avatar_label =AvatarWidget(avatar_path)
        self.avatar_label.setRadius(20)

        avatar_pixmap = QPixmap(avatar_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatar_label.setPixmap(avatar_pixmap)

        self.avatar_label.setStyleSheet("QLabel { background-color: transparent; border: none; }")
        # 设置头像容器布局
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.avatar_label)
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 30)


class MessageBubble(QWidget):
    """
    消息气泡
    """

    def __init__(self, text: str, avatar_path: str, is_sender: bool = True, parent=None):
        super(MessageBubble, self).__init__(parent)
        self.initUI(text, avatar_path, is_sender)

    def initUI(self, text:str, avatar_path:str, is_sender:bool):
        self.bubble_container = QWidget(self)  # 气泡容器
        bubble_layout = QHBoxLayout(self.bubble_container)  # 气泡内部水平布局
        # 文本容器QWidget
        self.text_container = QWidget(self.bubble_container)
        text_layout = QVBoxLayout(self.text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)  # 设置文本容器的边距
        text=self.text_line_break(text)
        print(text)
        self.text_label = QLabel(text, self.text_container)
        self.text_label.setWordWrap(True)
        text_layout.addWidget(self.text_label)
        # 设置高度
        self.text_container.setMinimumHeight(50)
        # self.text_container.setMaximumHeight(self.text_label.height())
        # self.setMaximumHeight(self.text_container.height() + 200)
        # 把字体设置成微雅软黑
        font = QFont('Microsoft YaHei', 12)  # 12是字体大小，可以根据需要调整
        self.text_label.setFont(font)
        # 为文本容器设置背景色
        #      背景色
        #    #ffe4e1粉色，#e5f9e7绿色，#e0f2ff蓝色,#dbc6e0

        self.text_container.setStyleSheet("""  
            QWidget {  
                background-color:#e6e6fa;             /* 背景色 */  
                border-radius: 10px;                   /* 圆角 */  
               box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影 */
            }  
            QLabel {                                  /* 假设文本容器中包含QLabel */  
                font-size: 14px;                       /* 字体大小 */  
                color: #333;                           /* 字体颜色 */
            }  
            QWidget:hover {                            /* 鼠标悬停效果 */  
                background-color: #dbc6e0;             /* 悬停时背景色变化 */  
            }  
        """)

        # 头像QLabel
        self.avatar_container = AvatarContainer(avatar_path)

        # 设置气泡容器的样式
        if is_sender:
            bubble_layout.addWidget(self.text_container, stretch=1)
            bubble_layout.addWidget(self.avatar_container)

            bubble_style = """  
                QWidget {  
                    background-color:rgba(255, 255, 255, 0);  
                    border-radius: 10px 10px 10px 0;  
                    padding: 10px;  
                }  
            """
        else:
            bubble_layout.addWidget(self.avatar_container)
            bubble_layout.addWidget(self.text_container, stretch=1)
            bubble_style = """  
                QWidget {  
                    background-color: rgba(255, 255, 255, 0);  
                    border-radius: 10px 10px 0 10px;  
                    padding: 10px;  
                }  
            """
        self.bubble_container.setStyleSheet(bubble_style)

        # 主布局（可以是垂直布局，用于堆叠多个气泡）
        main_layout = QVBoxLayout(self)

        # 根据发送者或接收者设置气泡容器的位置
        if is_sender:
            main_layout.addWidget(self.bubble_container, alignment=Qt.AlignRight)
        else:
            main_layout.addWidget(self.bubble_container, alignment=Qt.AlignLeft)

    @staticmethod
    def text_line_break(s: str, limit: int = 15) -> str:
        lines = []
        for i in range(0, len(s), limit):
            lines.append(s[i:i + limit])
        return '\n'.join(lines)

class MessageBubbleWindow(QListWidget):
    """测试用"""

    def __init__(self):
        super(MessageBubbleWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Message Bubble Example')
        self.setGeometry(300, 300, 400, 300)  # 设置窗口位置和大小
        text = "Hellohhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
        is_sender = True  # 假设总是发送者
        avatar_path = "../Assets/image/logo.png"  # 发送者头像路径
        bubble = MessageBubble(text, avatar_path, is_sender=is_sender)
        
        item = QListWidgetItem(self)
        item.setSizeHint(bubble.sizeHint())

        # 将 MessageBubble 设置为 QListWidgetItem 的 widget
        self.setItemWidget(item, bubble)

        self.show()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = MessageBubbleWindow()
    sys.exit(app.exec_())

