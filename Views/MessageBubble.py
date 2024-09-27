"""
备注：最好是打开名为Aiproject的项目，不是Aiproject2！！！
"""
import textwrap

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QGuiApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem
from qfluentwidgets import AvatarWidget, ImageLabel, PushButton, FluentIcon

from Core.Tools.Play_Audio import AudioPlayer
from Views.GlobalSignal import global_signal

class AvatarContainer(QFrame):
    """
    聊天头像样式
    """

    def __init__(self, avatar_path: str, parent=None):
        super(AvatarContainer, self).__init__(parent, frameShape=QFrame.NoFrame)  # 无边框
        self.initUI(avatar_path)

    def initUI(self, avatar_path: str):
        self.avatar_label = AvatarWidget(avatar_path)
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

    def __init__(self, text: str, avatar_path: str, is_sender: bool = True, parent=None, variety: str = "text"):
        """
        :param text:聊天文本
        :param avatar_path:头像路径
        :param is_sender:是否是发送者
        :param variety:种类，分text、image、audio三种吧
        """
        super(MessageBubble, self).__init__(parent)
        self.text = text
        self.initUI(text, avatar_path, is_sender, variety)

    def initUI(self, text, avatar_path: str, is_sender: bool, variety):
        self.bubble_container = QWidget(self)  # 气泡容器
        bubble_layout = QHBoxLayout(self.bubble_container)  # 气泡内部水平布局

        self.info_container = QWidget(self.bubble_container)
        # 设置高度
        self.info_container.setMinimumHeight(50)
        # self.info_container.setMaximumHeight(self.text_label.height())
        # self.setMaximumHeight(self.info_container.height() + 200)
        self.info_container.setStyleSheet("""  
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

        text_layout = QVBoxLayout(self.info_container)
        text_layout.setContentsMargins(0, 0, 0, 0)  # 设置文本容器的边距
        # 文本容器QWidget
        if variety == "text":
            self.installEventFilter(self)  # 安装事件过滤器
            text = self.text_line_break(text)
            print(text)
            self.text_label = QLabel(text, self.info_container)
            self.text_label.setWordWrap(True)
            text_layout.addWidget(self.text_label)
            # 把字体设置成微雅软黑
            font = QFont('Microsoft YaHei', 12)  # 12是字体大小，可以根据需要调整
            self.text_label.setFont(font)
            # 为文本容器设置背景色
            #      背景色
            #    #ffe4e1粉色，#e5f9e7绿色，#e0f2ff蓝色,#dbc6e0
        elif variety == "image":
            image = ImageLabel(text)
            image.scaledToHeight(200)
            image.setBorderRadius(8, 8, 8, 8)
            text_layout.addWidget(image)
        elif variety == "audio":
            # audio_button播放按钮
            audio_button = PushButton(FluentIcon.VOLUME, "播放")
            audio_button.clicked.connect(lambda: self.play_audio(text))
            text_layout.addWidget(audio_button)  # 使用stretch参数来分配多余的空间给时长标签
            # 转文字按钮
            play_button = PushButton(FluentIcon.LANGUAGE, "转文字")
            play_button.clicked.connect(lambda: self.audio_to_text(text))
            text_layout.addWidget(play_button)
            # 一个耳机的图标:FluentIcon.HEADPHONE

        # 头像QLabel
        self.avatar_container = AvatarContainer(avatar_path)

        # 设置气泡容器的样式
        if is_sender:
            bubble_layout.addWidget(self.info_container, stretch=1)
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
            bubble_layout.addWidget(self.info_container, stretch=1)
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

    def update_text(self, text, is_add: bool = False):
        if is_add:
            self.text += text
        else:
            self.text = text
        self.text_label.setText(self.text_line_break(self.text))

    @staticmethod
    def text_line_break(s: str, limit: int = 30) -> str:
        """
        手动自动换行，保留原始字符串中的换行符
        """
        paragraphs = s.split('\n')
        wrapped_paragraphs = []
        for paragraph in paragraphs:
            wrapped_paragraph = textwrap.wrap(paragraph, width=limit)
            wrapped_paragraphs.extend(wrapped_paragraph)
        return '\n'.join(wrapped_paragraphs)

    def audio_to_text(self, audio_path: str):
        """
        语音转文字
        """
        ...

    def play_audio(self, audio_path: str):
        """"
        播放按钮
        """
        # print(audio_path)
        audio_path = audio_path[:-4]
        audio_path = audio_path + '.wav'
        print(audio_path)

        try:
            # AudioPlayer(self).exe()
            self.player = AudioPlayer(audio_path)
            print("音频播放成功")

        except Exception as e:
            print(f"播放音频时发生错误: {e}")

    def eventFilter(self, obj, event):
        """
        点击复制到剪贴板
        """
        try:
            if (obj == self or obj == self.text_label) and event.type() == QEvent.MouseButtonPress:  # 判断是否是特定的 QLabel 并且是鼠标点击事件
                clipboard = QGuiApplication.clipboard()  # 获取系统剪贴板
                clipboard.setText(self.text)  # 设置要复制的内容
                global_signal.correct_msg.emit(["复制成功", "复制到剪贴板"])
                return True
            return super().eventFilter(obj, event)  # 传递给父类的事件过滤器
        except Exception as e:
            print(str(e))


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
        avatar_path = "./Assets/image/logo.png"  # 发送者头像路径
        bubble = MessageBubble(avatar_path, avatar_path, is_sender=is_sender, variety="audio")

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
