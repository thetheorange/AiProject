"""
文件选择窗口
@Author Misaka-xxw
Time 2024/5/26
"""
import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication


class FileWindow(QWidget):
    """
    导入文件的窗口
    """

    def __init__(self, variety="image"):
        super().__init__()
        if variety == "image":
            self.name_filters: list = ["图片文件 (*.png *.jpg *.jpeg *.gif *.bmp)", "所有文件(*)"]
        else:
            self.name_filters: list = ["所有文件(*)"]
        # self.open_file_dialog()

    def open_file_dialog(self) -> str:
        """
        打开文件选择对话框
        :return: 文件路径
        """
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilters(["图片文件 (*.png *.jpg *.jpeg *.gif *.bmp)", "所有文件(*)"])
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                print(f'选择图片: {file_path}')
                return file_path
            else:
                return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_window = FileWindow()
    a = file_window.open_file_dialog()
    print(a)
    sys.exit(app.exec_())
