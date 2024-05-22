import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QSpinBox,QDoubleSpinBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
class LoginWindow(QWidget):

    def __init__(self):
        Window_icon:str=r'../Asserts/icons/add.png'
        super().__init__()
        loadUi("../Templates/register.ui", self)

        self.setWindowTitle("注册界面")
        self.setWindowIcon(QIcon(Window_icon))
        img_path = r'../Asserts/icons/user.png'
        pixmap = QPixmap(img_path).scaled(20, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.icon_photo.setPixmap(pixmap)


        #信号与槽
        self.confirm_button.clicked.connect(self.sayHi)
        self.cancel_button.clicked.connect(self.sayHi)


    def sayHi(self):  # click对应的槽函数
        print("hi")


if __name__ == "__main__":
    #QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
   # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
   # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    LoginWindow = LoginWindow()
    LoginWindow.show()
    sys.exit(app.exec_())

