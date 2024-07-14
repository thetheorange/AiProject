"""
Des 聊天相关界面
@Author thetheOrange
Time 2024/6/14
"""
from PyQt5.QtWidgets import QWidget, QAction, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QListWidgetItem, QFrame, QListWidget, QPushButton
from PyQt5.uic import loadUi
from qfluentwidgets import ToolTipFilter, PushButton, Icon, FluentIcon, ToolTipPosition, CommandBar, MessageBoxBase, \
    SubtitleLabel, ListWidget, PlainTextEdit, SearchLineEdit, MessageBox
from AiProject2.AiProject.Views.GlobalSignal import global_signal
from PyQt5.QtGui import QPixmap


class ChatLineWidget(QWidget):
    """
    每行聊天按钮样式
    """

    def __init__(self, text, icon, parent=None):
        super(ChatLineWidget, self).__init__(parent)
        # 创建一个水平布局
        layout = QHBoxLayout()
        # 创建一个标签和一个按钮
        # self.label = QLabel()
        print(text, icon)
        self.button = PushButton(icon, text)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.start_chat)
    def start_chat(self) -> None:
        """
        点击面具按钮直接开始会话
        """
        global_signal.ChatOperation_Mask.emit("start_chat")


class ChatSearchWindow(QWidget):
    """
    聊天会话搜索界面
    """

    def __init__(self):
        super().__init__()
        loadUi("../Templates/chat_search.ui", self)

        # =============================================基础设置start=============================================

        self.add_session_btn: PushButton
        self.add_session_btn.setIcon(Icon(FluentIcon.ADD_TO))
        self.add_session_btn.setToolTip("新建一个新的对话✨")
        self.add_session_btn.installEventFilter(
            ToolTipFilter(self.add_session_btn, showDelay=300, position=ToolTipPosition.TOP))
        self.add_session_btn.clicked.connect(lambda x: ChatChoiceWindow(self).exec())

        # =============================================基础设置end=============================================
        # =============================================搜索设置start=============================================
        self.SearchLineEdit: SearchLineEdit
        self.SearchLineEdit.searchSignal.connect(self.search)
        # =============================================搜索设置end=============================================

        # =============================================添加聊天按钮行start=============================================
        self.ListWidget: ListWidget
        datadict = [
            {'name': '你好，新用户', 'icon': FluentIcon.CHAT},
            {'name': '这题怎么做', 'icon': FluentIcon.CALENDAR},
            {'name': '以“星期天为题”写一篇作文', 'icon': FluentIcon.BOOK_SHELF},
        ]
        for data in datadict:
            self.add_chat_list(data)

        # =============================================添加聊天按钮行end=============================================

    def search(self):
        """
        点击搜索框触发函数
        """
        cur_text = self.SearchLineEdit.text()
        print(cur_text)
        self.show_dialog(True, cur_text)

    def show_dialog(self, flag: bool, name: str):
        """
        搜索时弹出消息框
        """
        if flag:
            title = '"' + name + '"' + '对话存在，开始对话？'
            content = """"""
            w = MessageBox(title, content, self)
            if w.exec():
                self.start_chat()
            else:
                print('Cancel button is pressed')
        else:
            title = '"' + name + '"' + '对话不存在，请重新搜索'
            content = """"""
            w2 = MessageBox(title, content, self)
            if w2.exec():
                print('Yes')
            else:
                print('Cancel button is pressed')

    def start_chat(self) -> None:
        """
        点击面具按钮直接开始会话
        """
        global_signal.ChatOperation_Mask.emit("start_chat")

    def add_chat_list(self, data):
        name = data.get('name')
        icon = data.get('icon')
        item = QListWidgetItem(self.ListWidget)
        # self.data_and_icons.append((name,icon))
        # 创建CustomWidget实例，这里我们传递文本和一个模拟的图标名（实际实现可能需要调整）
        custom_widget = ChatLineWidget(name, icon)

        # 设置item的大小提示为custom_widget的大小提示
        item.setSizeHint(custom_widget.sizeHint())

        # 将custom_widget设置为item的widget
        self.ListWidget.setItemWidget(item, custom_widget)


class ChatChoiceWindow(MessageBoxBase):
    """
    聊天会话选择界面
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # 标题
        self.sub_title = SubtitleLabel("欢迎使用星火大模型")
        self.sub_title.setAlignment(Qt.AlignCenter)
        # ’选择面具‘和’直接开始‘按钮
        self.choice_mask_btn = PushButton()
        self.choice_mask_btn.setText("选择面具")
        self.choice_mask_btn.setIcon(Icon(FluentIcon.ROBOT))
        self.choice_mask_btn.clicked.connect(self.choice_mask)

        self.start_btn = PushButton()
        self.start_btn.setText("直接开始")
        self.start_btn.setIcon(Icon(FluentIcon.MESSAGE))
        self.start_btn.clicked.connect(self.start_chat)

        self.hbox_layout_top = QHBoxLayout()
        self.hbox_layout_top.addWidget(self.sub_title)

        self.hbox_layout_bottom = QHBoxLayout()
        self.hbox_layout_bottom.addWidget(self.choice_mask_btn)
        self.hbox_layout_bottom.addWidget(self.start_btn)

        # 将控件添加到布局中
        self.viewLayout.addLayout(self.hbox_layout_top)
        self.viewLayout.addLayout(self.hbox_layout_bottom)

        self.yesButton.hide()
        self.cancelButton.setText("取消")

    def choice_mask(self) -> None:
        """
        选择面具

        :return:
        """
        # print("?")
        global_signal.mask_chatOperation.emit("choice_mask")
        # ChatChoiceMaskWindow(self).exec()
        self.close()

    def start_chat(self) -> None:
        """
        直接开始会话

        :return:
        """
        global_signal.ChatOperation.emit("start_chat")
        self.close()


class ChatChoiceMaskWindow(MessageBoxBase):
    """
    聊天会话选择面具界面
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # 面具列表视图
        self.mask_list = ListWidget()

        self.viewLayout.addWidget(self.mask_list)

        self.yesButton.setText("确认")
        self.cancelButton.setText("取消")


from PyQt5.QtCore import Qt, pyqtSlot


class AvatarContainer(QFrame):
    """
    聊天图像样式
    """

    def __init__(self, avatar_path, parent=None):
        super(AvatarContainer, self).__init__(parent, frameShape=QFrame.NoFrame)  # 无边框
        self.initUI(avatar_path)

    def initUI(self, avatar_path):
        self.avatar_label = QLabel(self)
        # 加载并缩放头像
        avatar_pixmap = QPixmap(avatar_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatar_label.setPixmap(avatar_pixmap)
        # 头像标签背景保持透明
        self.avatar_label.setStyleSheet("QLabel { background-color: transparent; border: none; }")
        # 设置头像容器布局
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.avatar_label)
        self.layout().setAlignment(Qt.AlignCenter)  # 设置头像在容器中居中
        self.layout().setContentsMargins(0, 0, 0, 30)  # 移除布局边距

        # 如果需要，可以设置头像容器的边框和背景
        # self.setStyleSheet("QFrame { border: 1px solid #ccc; background-color: #f0f0f0; }")


class MessageBubble(QWidget):
    """
    消息气泡
    """

    def __init__(self, text, avatar_path, is_sender=True, parent=None):
        super(MessageBubble, self).__init__(parent)
        self.bubble_container = None
        self.text_container = None
        self.text_label = None
        self.initUI(text, avatar_path, is_sender)

    def initUI(self, text, avatar_path, is_sender):
        self.bubble_container = QWidget(self)  # 气泡容器
        bubble_layout = QHBoxLayout(self.bubble_container)  # 气泡内部水平布局
        # 文本容器QWidget
        self.text_container = QWidget(self.bubble_container)
        text_layout = QVBoxLayout(self.text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)  # 设置文本容器的边距
        self.text_label = QLabel(text, self.text_container)
        self.text_label.setWordWrap(True)
        text_layout.addWidget(self.text_label)
        # 为文本容器设置背景色
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

            /* 背景色 */  
            #ffe4e1粉色，#e5f9e7绿色，#e0f2ff蓝色
            }  
        """)
        # 头像QLabel
        self.avatar_container = AvatarContainer(avatar_path, self)

        # self.avatar_label = QLabel(self.bubble_container)
        # avatar_pixmap = QPixmap(avatar_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.avatar_label.setPixmap(avatar_pixmap)
        # 设置头像背景（如果需要的话，通常是透明的，因为直接使用QPixmap）
        # self.avatar_label.setStyleSheet("QLabel { background-color: transparent; border: none; }")

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


class ChatSessionWindow(QWidget):
    """
    聊天会话界面
    """

    def __init__(self):
        super().__init__()
        loadUi("../Templates/chat_session.ui", self)

        # =============================================聊天选项bar设置start=============================================

        self.chat_option_bar: CommandBar
        # 清除聊天记录按钮
        self.clear_history_btn: QAction = QAction(triggered=self.clear_history)
        self.clear_history_btn.setIcon(Icon(FluentIcon.ERASE_TOOL))
        self.clear_history_btn.setToolTip("清除聊天记录🧤")
        self.clear_history_btn.installEventFilter(
            ToolTipFilter(self.clear_history_btn, showDelay=300, position=ToolTipPosition.TOP))
        # 切换模型按钮
        self.change_model_btn: QAction = QAction(triggered=self.change_model)
        self.change_model_btn.setIcon(Icon(FluentIcon.ROBOT))
        self.change_model_btn.setToolTip("切换模型🎷")
        self.change_model_btn.installEventFilter(
            ToolTipFilter(self.change_model_btn, showDelay=300, position=ToolTipPosition.TOP))
        # 上传图片按钮
        self.upload_img_btn: QAction = QAction(triggered=self.upload_img)
        self.upload_img_btn.setIcon(Icon(FluentIcon.IMAGE_EXPORT))
        self.upload_img_btn.setToolTip("上传你的图片🎬")
        self.upload_img_btn.installEventFilter(
            ToolTipFilter(self.upload_img_btn, showDelay=300, position=ToolTipPosition.TOP))
        # 语音输入按钮
        self.audio_input_btn: QAction = QAction(triggered=self.upload_audio)
        self.audio_input_btn.setIcon(Icon(FluentIcon.MICROPHONE))
        self.audio_input_btn.setToolTip("音频输入🔈")
        self.audio_input_btn.installEventFilter(
            ToolTipFilter(self.audio_input_btn, showDelay=300, position=ToolTipPosition.TOP))

        self.chat_option_bar.addAction(self.clear_history_btn)
        self.chat_option_bar.addAction(self.change_model_btn)
        self.chat_option_bar.addAction(self.upload_img_btn)
        self.chat_option_bar.addAction(self.audio_input_btn)

        # =============================================聊天选项bar设置end=============================================

        # =============================================聊天输入框设置end=============================================

        self.chat_frame: QFrame
        self.chat_frame.setFixedHeight(100)

        self.chat_input: PlainTextEdit
        self.chat_input.setFixedHeight(80)

        # =============================================聊天输入框设置end=============================================

        # =============================================发送按钮设置start=============================================

        self.send_btn: PushButton
        self.send_btn.setIcon(Icon(FluentIcon.SEND))
        self.send_btn.clicked.connect(self.send_button_clicked)
        # self.chat_input.returnPressed.connect(self.send_button_clicked)

        # =============================================发送按钮设置end=============================================

    def send_button_clicked(self):
        """
            获取 PlainTextEdit 控件中的文本并发送聊天气泡
        """
        text = self.chat_input.toPlainText()
        print(text)
        is_sender = True  # 假设总是发送者
        avatar_path = "../Assets/image/logo.png"  # 发送者头像路径
        bubble = MessageBubble(text, avatar_path, is_sender=is_sender)

        # 创建一个 QListWidgetItem 并设置其大小提示
        item = QListWidgetItem(self.ListWidget)
        item.setSizeHint(bubble.sizeHint())

        # 将 MessageBubble 设置为 QListWidgetItem 的 widget
        self.ListWidget.setItemWidget(item, bubble)

        # 滚动到底部以显示最新消息（可选）
        self.ListWidget.scrollToBottom()

    def clear_history(self) -> None:
        """
        清除所有的聊天记录

        :return:
        """
        self.ListWidget.clear()

    def change_model(self) -> None:
        """
        切换模型

        :return:
        """

    def upload_img(self) -> None:
        """
        上传图片

        :return:
        """
        ...

    def upload_audio(self) -> None:
        """
        语音输入，上传音频到服务器

        :return:
        """
        ...
