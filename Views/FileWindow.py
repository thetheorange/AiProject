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

    def __init__(self):
        self.chose_path: str = ""
        super().__init__()
        file_dialog = QFileDialog(self)
        filePath, temp = file_dialog.getOpenFileName(self, '选择文件')
        if filePath:
            print(f'选择文件: {filePath}')  # 正确
            self.chose_path = filePath


if __name__ == "__main__":
    app = QApplication(sys.argv)
    FileWindow().show()
    sys.exit(app.exec_())
