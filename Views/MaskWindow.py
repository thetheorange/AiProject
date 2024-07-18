"""
Des 面具相关界面
@Author thetheOrange
Time 2024/6/14
"""
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QHBoxLayout, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import PushButton, ToolTipFilter, ToolTipPosition, MessageBoxBase, \
    LineEdit, PlainTextEdit, ListWidget, SearchLineEdit, MessageBox, ToolButton
from qfluentwidgets import FluentIcon
from Views.GlobalSignal import global_signal
from Sqlite.ChatSql import ChatSql


class MaskSubSettingWindow(MessageBoxBase):
    """
    大模型面具设置子界面
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # 面具名输入框
        self.mask_name_input = LineEdit()
        self.mask_name_input.setPlaceholderText("输入新面具的名称")
        self.mask_name_input.setClearButtonEnabled(True)

        # 面具描述输入框
        self.mask_des_input = PlainTextEdit()
        self.mask_des_input.setPlaceholderText("这里填入您的面具描述，将作为system参数向模型发送请求，越细致越好")

        # 确认按钮
        self.yesButton.setText("提交")

        # 取消按钮
        self.cancelButton.setText("取消")

        # 将控件添加到布局中
        self.viewLayout.addWidget(self.mask_name_input)
        self.viewLayout.addWidget(self.mask_des_input)
        # 信号与槽
        self.yesButton.clicked.connect(self.on_yes_button_clicked)

    def on_yes_button_clicked(self):
        icon = FluentIcon.ROBOT
        mask_name = self.mask_name_input.text()
        mask_des = self.mask_des_input.toPlainText()
        data = {
            'name': mask_name,
            'icon': icon,
            'des': mask_des,
            'signal': 'add'
        }
        print(data)
        # 发射全局信号
        global_signal.mask_submitted.emit(data)


class MaskWidget(QWidget):
    """
    每行面具样式
    """

    def __init__(self, text, icon, parent=None):
        super(MaskWidget, self).__init__(parent)
        # 创建一个水平布局
        layout = QHBoxLayout()
        # 点击即开始聊天
        self.mask_name = text
        self.mask_icon = icon
        self.chat_button = PushButton(icon, self.mask_name)
        self.chat_button.clicked.connect(self.start_chat)
        global_signal.ChatOperation_Mask.connect(self.__handle_chat_signal2)
        # 创建一个删除按钮
        self.delete_button = ToolButton(FluentIcon.DELETE)
        self.delete_button.clicked.connect(self.delete_mask)
        # 将标签和按钮添加到布局中
        # layout.addWidget(self.label)
        layout.addWidget(self.chat_button)
        layout.addWidget(self.delete_button)

        # 设置自定义小部件的布局
        self.setLayout(layout)

    def delete_mask(self) -> None:
        data = {
            'name': self.mask_name,
            'icon': self.mask_icon,
            'des': '',
            'signal': 'delete'
        }
        global_signal.mask_submitted.emit(data)

    def start_chat(self) -> None:
        """
        点击面具按钮直接开始会话
        """
        global_signal.ChatOperation_Mask.emit("start_chat")

    def __handle_chat_signal2(self, signal: str) -> None:
        """
        处理窗口的信号
        """
        if signal == "start_chat":
            global_signal.ChatOperation.emit("start_chat")

    def sizeHint(self):
        # 返回一个建议的大小，布局管理器可能会使用它
        # 但请注意，如果设置了最小/最大尺寸，则这些尺寸可能会覆盖它
        return QSize(100, 45)  # 示例值


class MaskSettingWindow(QWidget):
    """
    大模型面具设置界面
    """

    def __init__(self):
        super().__init__()
        loadUi("../Templates/mask_setting.ui", self)
        # =============================================基础设置start=============================================

        # 新建按钮
        self.add_mask: PushButton
        self.add_mask.setIcon(FluentIcon.ADD_TO)
        self.add_mask.setToolTip("新建一个新的面具✨")
        self.add_mask.installEventFilter(ToolTipFilter(self.add_mask, showDelay=300, position=ToolTipPosition.TOP))
        self.add_mask.clicked.connect(lambda x: MaskSubSettingWindow(self).exec())

        self.mask_info: ListWidget
        # =============================================基础设置end=============================================
        # =============================================每行mask设置begin=============================================
        self.data_and_icons = [("机器学习", FluentIcon.ROBOT), ("英语写作", FluentIcon.CHAT),
                               ("小红书写手", FluentIcon.BOOK_SHELF), ("数学物理", FluentIcon.CALENDAR)]
        # 更新本地数据库
        self.sql = ChatSql()

        for text, icon_name in self.data_and_icons:
            data = {
                'name': text,
                'icon': icon_name,
                'des': '',
                'signal': 'add'
            }
            self.add_or_delete_mask_list(data)

        global_signal.mask_submitted.connect(self.add_or_delete_mask_list)

        # global_signal.ChatOperation.connect(self.test)
        # =============================================每行mask设置end=============================================
        # =============================================搜索设置begin=============================================
        self.search_mask: SearchLineEdit
        self.search_mask.searchSignal.connect(self.search)
        # =============================================搜索设置end=============================================

    def find_text_in_list(self, text):
        """
        在给定的数据列表中查找文本。

        :param text: 要查找的文本。
        :return: 如果找到文本，则返回1；否则返回0。
        """
        # print("?")
        for item_text, _ in self.data_and_icons:
            # print(item_text)
            if item_text == text:
                return True
        return False

    def search(self):
        """
        点击搜索框触发函数
        """

        cur_text = self.search_mask.text()
        print(cur_text)
        flag = self.sql.get_mask(cur_text)
        self.show_dialog(flag, cur_text)

    def show_dialog(self, flag: bool, name: str):
        if flag is not None:
            title = '"' + name + '"' + '面具存在，开始对话？'
            content = """"""
            w = MessageBox(title, content, self)
            if w.exec():
                self.start_chat()
            else:
                print('Cancel button is pressed')
        else:
            title = '"' + name + '"' + '面具不存在，请重新搜索'
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

    def add_or_delete_mask_list(self, data):
        signal = data.get('signal')
        name = data.get('name')
        icon = data.get('icon')
        des = data.get('des')
        if signal == 'add':
            # print(name, icon, des)
            # 更新本地数据库
            self.sql.add_mask(name, des, icon)
            # 发送全局信号
            global_signal.ChatOperation.emit("close_login_success")
            item = QListWidgetItem(self.mask_info)
            # self.data_and_icons.append((name,icon))
            # 创建CustomWidget实例，这里我们传递文本和一个模拟的图标名（实际实现可能需要调整）
            custom_widget = MaskWidget(name, icon)

            # 设置item的大小提示为custom_widget的大小提示
            item.setSizeHint(custom_widget.sizeHint())

            # 将custom_widget设置为item的widget
            self.mask_info.setItemWidget(item, custom_widget)
        else:
            print('delete')
            item = self.mask_info.currentItem()
            if item:
                # print(item)
                row = self.mask_info.row(item)
                # print(row)
                self.mask_info.takeItem(row)
            self.sql.delete_mask(name)


if __name__ == "__main__":
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        app = QApplication(sys.argv)
        w = MaskSettingWindow()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
