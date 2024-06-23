"""
Des 聊天相关界面
@Author thetheOrange
Time 2024/6/14
"""
from PyQt5.QtCore import QTimer, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QAction, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QListWidgetItem, QFrame,QListWidget
from PyQt5.uic import loadUi
from qfluentwidgets import ToolTipFilter, PushButton, Icon, FluentIcon, ToolTipPosition, CommandBar, MessageBoxBase, \
    SubtitleLabel, ListWidget, PlainTextEdit

from Views.GlobalSignal import global_signal
from MessageBubble import MessageBubble



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
        ChatChoiceMaskWindow(self).exec()
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
        #self.chat_input.returnPressed.connect(self.send_button_clicked)

        # =============================================发送按钮设置start=============================================



    def send_button_clicked(self):
        """
            获取 PlainTextEdit 控件中的文本并发送聊天气泡
        """
        text = self.chat_input.toPlainText()
        print(text)
        is_sender =True  # 假设总是发送者
        avatar_path = "../Assets/image/background.jpg"  # 发送者头像路径
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
        ...

    def change_model(self) -> None:
        """
        切换模型

        :return:
        """
        ...

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
