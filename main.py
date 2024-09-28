import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from Views.MainWindow import MainWindow

if __name__=="__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    try:
        w = MainWindow()
        # w.show()
    except Exception as e:
        print(str(e))
    sys.exit(app.exec_())