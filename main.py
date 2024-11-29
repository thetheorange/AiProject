import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from Views.MainWindow import MainWindow

# 程序入口
if __name__=="__main__":
    if not os.path.exists('./Temp'):
        # 目录不存在，创建目录
        os.makedirs('./Temp')
        print(f"目录 '{'./Temp'}' 已创建。")
    else:
        # 目录已存在
        print(f"目录 '{'./Temp'}' 已存在。")
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    try:
        w = MainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
    # sys.exit(app.exec_())