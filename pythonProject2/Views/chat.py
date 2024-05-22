import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QPainter, QPaintEvent, QColor, QFontMetrics, QPolygon
from PyQt5.QtCore import Qt, QSize, QObject
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, pyqtSignal, Qt, QThread
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPolygon, QFontMetrics,QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QVBoxLayout, QSpacerItem, \
    QScrollArea, QScrollBar, QLabel, QWidget, QVBoxLayout, QApplication


class Signals(QObject):
    send = pyqtSignal(bool)


signal = Signals()


class Notice(QLabel):
    def __init__(self, text, type_=3, parent=None):
        super().__init__(text, parent)
        self.type_ = type_
        self.setFont(QFont('微软雅黑', 12))
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setAlignment(Qt.AlignCenter)


class Avatar(QLabel):
    def __init__(self, avatar, parent=None):
        super().__init__(parent)
        if isinstance(avatar, str):
            self.setPixmap(QPixmap(avatar).scaled(45, 45))
            self.image_path = avatar
        elif isinstance(avatar, QPixmap):
            self.setPixmap(avatar.scaled(45, 45))
        self.setFixedSize(QSize(45, 45))


class MessageType:
    Text = 1
    Image = 2


class OpenImageThread(QThread):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self) -> None:
        image = Image.open(self.image_path)
        image.show()


class ImageMessage(QLabel):
    def __init__(self, avatar, parent=None):
        super().__init__(parent)
        self.image = QLabel(self)
        if isinstance(avatar, str):
            self.setPixmap(QPixmap(avatar))
            self.image_path = avatar
        elif isinstance(avatar, QPixmap):
            self.setPixmap(avatar)
        self.setMaximumWidth(480)
        self.setMaximumHeight(720)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 左键按下
            self.open_image_thread = OpenImageThread(self.image_path)
            self.open_image_thread.start()


class Triangle(QLabel):
    def __init__(self, Type, is_send=False, parent=None):
        super().__init__(parent)
        self.Type = Type
        self.is_send = is_send
        self.setFixedSize(6, 45)

    def paintEvent(self, a0: QPaintEvent) -> None:
        super(Triangle, self).paintEvent(a0)
        if self.Type == MessageType.Text:
            painter = QPainter(self)
            triangle = QPolygon()
            if self.is_send:
                painter.setPen(QColor('#b2e281'))
                painter.setBrush(QColor('#b2e281'))
                triangle.setPoints(0, 20, 0, 35, 6, 27)
            else:
                painter.setPen(QColor('white'))
                painter.setBrush(QColor('white'))
                triangle.setPoints(0, 27, 6, 20, 6, 35)
            painter.drawPolygon(triangle)


class ScrollAreaContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.adjustSize()


class ScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet(
            '''
            border:none;
            '''
        )


class ScrollBar(QScrollBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            '''
          QScrollBar:vertical {
              border-width: 0px;
              border: none;
              background:rgba(64, 65, 79, 0);
              width:5px;
              margin: 0px 0px 0px 0px;
          }
          QScrollBar::handle:vertical {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0 #DDDDDD, stop: 0.5 #DDDDDD, stop:1 #aaaaff);
              min-height: 20px;
              max-height: 20px;
              margin: 0 0px 0 0px;
              border-radius: 2px;
          }
          QScrollBar::add-line:vertical {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
              height: 0px;
              border: none;
              subcontrol-position: bottom;
              subcontrol-origin: margin;
          }
          QScrollBar::sub-line:vertical {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
              height: 0 px;
              border: none;
              subcontrol-position: top;
              subcontrol-origin: margin;
          }
          QScrollBar::sub-page:vertical {
              background: rgba(64, 65, 79, 0);
          }

          QScrollBar::add-page:vertical {
              background: rgba(64, 65, 79, 0);
          }
            '''
        )


class ChatWidget(QWidget):
    def sayHi(self):  # click对应的槽函数
        print("hi")

    def __init__(self):

        super().__init__()
        self.resize(500, 200)
        # 载入ui文件
        loadUi("../Templates/chat.ui", self)
        # 信号与槽
        # self.send_message_button.clicked.connect(self.sayHi)
        self.mask_button.clicked.connect(self.sayHi)
        self.my_button.clicked.connect(self.sayHi)
        self.insert_button.clicked.connect(self.sayHi)

        # 添加照片的按钮
        add_photo_button_icon: str = r'../Asserts/icons/add.png'
        self.add_photo_button.setIcon(QIcon(add_photo_button_icon))
        self.add_photo_button.clicked.connect(self.sayHi)

        layout = QVBoxLayout()
        self.groupBox_5.setLayout(layout)
        layout.setSpacing(0)
        self.adjustSize()
        # 生成滚动区域
        self.scrollArea = ScrollArea(self)
        scrollBar = ScrollBar()
        self.scrollArea.setVerticalScrollBar(scrollBar)
        # self.scrollArea.setGeometry(QRect(9, 9, 261, 211))
        # 生成滚动区域的内容部署层部件
        self.scrollAreaWidgetContents = ScrollAreaContent(self.scrollArea)
        self.scrollAreaWidgetContents.setMinimumSize(50, 100)
        # 设置滚动区域的内容部署部件为前面生成的内容部署层部件
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout.addWidget(self.scrollArea)
        self.layout0 = QVBoxLayout()
        self.layout0.setSpacing(0)
        self.scrollAreaWidgetContents.setLayout(self.layout0)
        self.setLayout(layout)

    def add_message_item(self, bubble_message, index=1):
        if index:
            self.layout0.addWidget(bubble_message)
        else:
            self.layout0.insertWidget(0, bubble_message)
        # self.set_scroll_bar_last()

    def set_scroll_bar_last(self):
        self.scrollArea.verticalScrollBar().setValue(
            self.scrollArea.verticalScrollBar().maximum()
        )

    def set_scroll_bar_value(self, val):
        self.verticalScrollBar().setValue(val)

    def verticalScrollBar(self):
        return self.scrollArea.verticalScrollBar()

    def update(self) -> None:
        super().update()
        self.scrollAreaWidgetContents.adjustSize()
        self.scrollArea.update()
        # self.scrollArea.repaint()
        # self.verticalScrollBar().setMaximum(self.scrollAreaWidgetContents.height())


class TextMessage(QLabel):
    heightSingal = pyqtSignal(int)

    def __init__(self, text, is_send=False, parent=None):
        super(TextMessage, self).__init__(text, parent)
        font = QFont('微软雅黑', 12)
        self.setFont(font)
        self.setWordWrap(True)
        self.setMaximumWidth(800)
        self.setMinimumWidth(100)
        self.setMinimumHeight(45)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        if is_send:
            self.setAlignment(Qt.AlignCenter | Qt.AlignRight)
            self.setStyleSheet(
                '''
                background-color:#b2e281;
                border-radius:10px;
                padding:10px;
                '''
            )
        else:
            self.setStyleSheet(
                '''
                background-color:white;
                border-radius:10px;
                padding:10px;
                '''
            )
        font_metrics = QFontMetrics(font)
        rect = font_metrics.boundingRect(text)
        self.setMaximumWidth(rect.width() + 30)


class BubbleMessage(QWidget):
    def __init__(self, str_content, avatar, Type, is_send=False, parent=None):
        super().__init__(parent)
        self.isSend = is_send
        # self.set
        self.setStyleSheet(
            '''
            border:none;
            '''
        )
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 5, 5, 5)
        # self.resize(QSize(200, 50))
        self.avatar = Avatar(avatar)
        triangle = Triangle(Type, is_send)
        if Type == MessageType.Text:
            self.message = TextMessage(str_content, is_send)
            # self.message.setMaximumWidth(int(self.width() * 0.6))
        elif Type == MessageType.Image:
            self.message = ImageMessage(str_content)
        else:
            raise ValueError("未知的消息类型")

        self.spacerItem = QSpacerItem(45 + 6, 45, QSizePolicy.Expanding, QSizePolicy.Minimum)
        if is_send:
            layout.addItem(self.spacerItem)
            layout.addWidget(self.message, 1)
            layout.addWidget(triangle, 0, Qt.AlignTop | Qt.AlignLeft)
            layout.addWidget(self.avatar, 0, Qt.AlignTop | Qt.AlignLeft)
        else:
            layout.addWidget(self.avatar, 0, Qt.AlignTop | Qt.AlignRight)
            layout.addWidget(triangle, 0, Qt.AlignTop | Qt.AlignRight)
            layout.addWidget(self.message, 1)
            layout.addItem(self.spacerItem)
        self.setLayout(layout)


class Test(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.resize(500, 600)
        self.w1 = ChatWidget()
        self.w1.send_message_button.clicked.connect(self.send_message)
        send_avatar = '../Asserts/icons/user.png'
        receive_avatar = '../Asserts/icons/fish.png'
        TEXT = MessageType.Text
        IMAGE = MessageType.Image
        time_message = Notice('2023-11-18 17:43')
        self.w1.add_message_item(time_message)
        text_message = self.w1.message.text()
        print(f"输入的文本是: {text_message}")
        bubble_message = BubbleMessage(text_message, receive_avatar, Type=TEXT, is_send=False)
        self.w1.add_message_item(bubble_message)

        # bubble_message = BubbleMessage('你好啊💖', send_avatar, Type=TEXT, is_send=True)
        # self.w1.add_message_item(bubble_message)

        # bubble_message = BubbleMessage('./data/fg1.png', send_avatar, Type=IMAGE, is_send=True)
        # self.w1.add_message_item(bubble_message)

        # bubble_message = BubbleMessage('咱们来对个诗吧！', send_avatar, Type=TEXT, is_send=True)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('落霞与孤鹜齐飞', send_avatar, Type=TEXT, is_send=True)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('秋水共成天一色', receive_avatar, Type=TEXT, is_send=False)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('风急天高猿啸哀', send_avatar, Type=TEXT, is_send=True)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('渚清沙白鸟飞回', receive_avatar, Type=TEXT, is_send=False)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('无边落木萧萧下', send_avatar, Type=TEXT, is_send=True)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('不尽长江滚滚来', receive_avatar, Type=TEXT, is_send=False)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('万里悲秋常作客', send_avatar, Type=TEXT, is_send=True)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('百年多病独登台', receive_avatar, Type=TEXT, is_send=False)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('艰难苦恨繁霜鬓', send_avatar, Type=TEXT, is_send=True)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('潦倒新停浊酒杯', receive_avatar, Type=TEXT, is_send=False)
        # self.w1.add_message_item(bubble_message)
        #
        # bubble_message = BubbleMessage('这是一串很长的文字\n好长好长好长好长好长好长好长好长好长好长好长好长好长好长好长好长好长好长好长好长', receive_avatar, Type=TEXT, is_send=False)
        # self.w1.add_message_item(bubble_message)
        # w2 = QLabel("nihao")
        layout.addWidget(self.w1)
        # layout.addWidget(w2)
        self.setLayout(layout)

    def send_message(self):
        send_avatar = 'icons/user.png'
        receive_avatar = 'icons/fish.png'
        TEXT = MessageType.Text
        IMAGE = MessageType.Image
        send_text=self.w1.message.text()
        self.w1.message.setText("")
        print(send_text)
        bubble_message = BubbleMessage(send_text, send_avatar, Type=TEXT, is_send=True)
        self.w1.add_message_item(bubble_message)

    def value(self, val):
        print('pos:', val)
        print('滚动条最大值', self.w1.verticalScrollBar().maximum())


if __name__ == '__main__':
    app = QApplication([])
    widget = Test()
    widget.w1.update()
    # widget = MyWidget()
    widget.w1.verticalScrollBar().setValue(200)
    print('滚动条最大值002', widget.w1.verticalScrollBar().maximum())
    widget.show()
    # QThread.sleep(2)
    widget.w1.verticalScrollBar().setValue(200)
    # widget.w1.verticalScrollBar().setValue(200)
    # widget.w1.verticalScrollBar().setValue(200)

    app.exec_()
