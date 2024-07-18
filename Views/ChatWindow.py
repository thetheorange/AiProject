"""
Des 聊天相关界面
@Author thetheOrange
Time 2024/6/14
Misaka-xxw: 记得改打开文件的路径为Aiproject！
"""
import json
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QAction, QLabel, QHBoxLayout, QListWidgetItem, QFrame, QApplication
from PyQt5.uic import loadUi
from qfluentwidgets import ToolTipFilter, PushButton, Icon, FluentIcon, ToolTipPosition, CommandBar, MessageBoxBase, \
    SubtitleLabel, ListWidget, PlainTextEdit, SearchLineEdit, MessageBox, InfoBar, InfoBarPosition

from Core.Tools.AudioRecorder import AudioRecorder
from Core.Tools.AudiotoText import AudiotoText
from Core.Tools.ImageToText import ImageToText
from Sqlite.ChatSql import ChatSql
from Sqlite.ChatSql import SenderType, SendType
from Sqlite.Static import static
from Views.FileWindow import FileWindow
from Views.GlobalSignal import global_signal
from Views.MessageBubble import MessageBubble


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
    聊天会话搜索界面，会被加到主页面里
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
        # 原来的会话示例
        # self.ListWidget: ListWidget
        # datadict = [
        #     {'name': '你好，新用户', 'icon': FluentIcon.CHAT},
        #     {'name': '这题怎么做', 'icon': FluentIcon.CALENDAR},
        #     {'name': '以“星期天为题”写一篇作文', 'icon': FluentIcon.BOOK_SHELF},
        # ]
        # for data in datadict:
        #     self.add_chat_list(data)
        self.update_dialogues()

    def update_dialogues(self):
        """根据本地数据库加载对话"""
        # 接入本地数据库
        self.ListWidget: ListWidget
        sql = ChatSql()
        datadict = sql.get_dialogues()
        for data in datadict:
            self.add_chat_list({'name': data['name'], 'icon': eval(f"FluentIcon.{data['icon']}")})

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
        # self.dialog_and_icons.append((name,icon))
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
        self.dialog: list = []
        self.update_mask_and_data()
        # self.chat_input.returnPressed.connect(self.send_button_clicked)

        # =============================================发送按钮设置end=============================================

    def update_mask_and_data(self):
        """
        更新面具
        """
        self.dialog = [{"role": "system", "content": static.mark_describe}]

    def init_message(self):
        """
        对话刚开始时，从本地数据库调取信息
        """
        sql = ChatSql()
        messages = sql.get_messages()
        for msg in messages:
            self.show_bubble(msg['info'], is_sender=msg['sender'], variety=msg['type'])

    def show_bubble(self, text: str = "", avatar_path: str = "../Assets/image/logo.png", is_sender: bool = True,
                    variety: str = "text"):
        """
        气泡的发送
        :param text:发送文本
        :param avatar_path:发送者头像路径
        :param is_sender:发送者是用户/ai
        :param variety:text/image
        """
        bubble = MessageBubble(text, avatar_path, is_sender=is_sender, variety=variety)

        # 创建一个 QListWidgetItem 并设置其大小提示
        item = QListWidgetItem(self.ListWidget)
        item.setSizeHint(bubble.sizeHint())

        # 将 MessageBubble 设置为 QListWidgetItem 的 widget
        self.ListWidget.setItemWidget(item, bubble)

        # 滚动到底部以显示最新消息（可选）
        self.ListWidget.scrollToBottom()
        # return bubble

    def send_button_clicked(self):
        """
        获取 PlainTextEdit 控件中的文本并发送聊天气泡
        """
        text = self.chat_input.toPlainText()
        if not text:
            InfoBar.error(
                title="输入状态",
                content="输入不能为空",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=1000,
                parent=self
            )
            return
        self.show_bubble(text)
        sql = ChatSql()
        sql.add_message(SenderType.GPT, SendType.TEXT, text, True)
        # sleep(1)
        self.dialog += [{"role": "user", "content": text}]
        print(self.dialog)
        url = r'http://47.121.115.252:8193/textModel/stream'
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "uuid": static.uuid,
            "username": static.username,
            "dialog": [{"role": "system", "content": ""},
                       {"role": "user", "content": text}]
        })
        # ai_bubble = self.text_bubble("", is_sender=False)
        with requests.post(url, headers=headers, data=data, stream=True) as r:
            buffer = ""
            all_text = ""
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    buffer += chunk.decode('utf-8')
                    try:
                        # 尝试在缓冲区中找到完整的 JSON 对象
                        start_index = buffer.find('{')
                        end_index = buffer.rfind('}') + 1
                        if start_index != -1 and end_index != -1:
                            json_str = buffer[start_index:end_index]
                            json_data = json.loads(json_str)
                            for text_item in json_data["payload"]["choices"]["text"]:
                                all_text += text_item["content"]
                                print(text_item["content"])
                                # ai_bubble.update_text(text_item["content"],is_add=True)
                            if json_data["header"]["code"] != 0:
                                InfoBar.error(
                                    title="错误",
                                    content=json_data["header"]["message"],
                                    orient=Qt.Vertical,
                                    isClosable=True,
                                    position=InfoBarPosition.BOTTOM_RIGHT,
                                    duration=1000,
                                    parent=self
                                )
                            # 结束
                            if json_data["header"]["status"] == 2:
                                token_info = json_data["payload"]["usage"]["text"]
                                print(f"'question_tokens': {token_info['question_tokens']}")
                                print(f"prompt_tokens': {token_info['prompt_tokens']}")
                                print(f"completion_tokens: {token_info['completion_tokens']}")
                                print(f"total_tokens: {token_info['total_tokens']}")
                                static.tokens -= token_info['total_tokens']
                            # 更新缓冲区，去掉已处理的部分
                            buffer = buffer[end_index:]
                    except json.JSONDecodeError:
                        pass
                    except Exception as e:
                        print(str(e))
            self.show_bubble(all_text, is_sender=False)
            sql.add_message(SenderType.GPT, SendType.TEXT, all_text, True)

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
        file_window = FileWindow()
        img_path = file_window.open_file_dialog()
        if img_path is None or "":
            print("未选中图片")
        else:
            print("yes选中了", img_path)
            is_sender = True  # 假设总是发送者
            try:
                self.show_bubble(img_path, is_sender=is_sender, variety="image")
                self.img_text(img_path)
                # 滚动到底部以显示最新消息（可选）
                self.ListWidget.scrollToBottom()
            except Exception as e:
                print(str(e))

    def upload_audio(self) -> None:
        """
        语音输入，上传音频到服务器

        :return:
        """
        global_signal.audio_submitted.connect(self.send_audio_message)
        AudioChoiceWindow(self).exec()

    def send_audio_message(self, audio_path: str) -> None:
        # print("send_audio")
        self.show_bubble(audio_path, variety="audio")
        # 语音转文字函数
        self.audio_text(audio_path)

    def img_text(self, path: str):
        """
        图片转文字
        """
        image_to_text = ImageToText(self)
        text = image_to_text.img_text(path)
        # print('接口封装测试',text)
        self.show_bubble(text, is_sender=False)

    def audio_text(self, path: str):
        audio_to_text = AudiotoText()
        text = audio_to_text.audio_text(path)
        # print('接口封装测试', text)
        ai_avatar_path = '../Assets/image/logo.png'
        is_sender = False
        bubble = MessageBubble(text, ai_avatar_path, is_sender=is_sender, variety="text")
        # 创建一个 QListWidgetItem 并设置其大小提示
        item = QListWidgetItem(self.ListWidget)
        item.setSizeHint(bubble.sizeHint())
        # 将 MessageBubble 设置为 QListWidgetItem 的 widget
        self.ListWidget.setItemWidget(item, bubble)


class AudioChoiceWindow(MessageBoxBase):
    """
    录音按钮弹出选择界面
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.AudioWindow = AudioRecorder()
        # 标题
        self.sub_title = SubtitleLabel("请录音")
        self.sub_title.setAlignment(Qt.AlignCenter)
        # ’录音开始‘和’录音结束‘按钮
        self.start_recording_btn = PushButton()
        self.start_recording_btn.setText("开始录音")
        self.start_recording_btn.setIcon(Icon(FluentIcon.MICROPHONE))
        self.start_recording_btn.clicked.connect(self.AudioWindow.start_recording)

        self.stop_recording_btn = PushButton()
        self.stop_recording_btn.setText("结束录音")
        self.stop_recording_btn.setIcon(Icon(FluentIcon.MUTE))
        self.stop_recording_btn.clicked.connect(self.AudioWindow.stop_recording)

        self.hbox_layout_top = QHBoxLayout()
        self.hbox_layout_top.addWidget(self.sub_title)

        self.hbox_layout_bottom = QHBoxLayout()
        self.hbox_layout_bottom.addWidget(self.start_recording_btn)
        self.hbox_layout_bottom.addWidget(self.stop_recording_btn)

        # 将控件添加到布局中
        self.viewLayout.addLayout(self.hbox_layout_top)
        self.viewLayout.addLayout(self.hbox_layout_bottom)

        self.yesButton.setText("确认")
        self.yesButton.clicked.connect(self.send_message)
        self.cancelButton.setText("取消")

    def send_message(self):
        if self.AudioWindow.path is not None:
            # print("yes选中了")
            global_signal.audio_submitted.emit(self.AudioWindow.path)


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = ChatSessionWindow()
    w.show()
    sys.exit(app.exec_())
