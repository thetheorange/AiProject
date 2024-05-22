import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QSpinBox,QDoubleSpinBox, QVBoxLayout,QPushButton
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class LoginWindow(QWidget):

    def __init__(self):
        Window_icon:str=r'../Asserts/icons/add.png'
        super().__init__()
        loadUi("../Templates/sign3.ui", self)
        #设置标题，图标
        # self.setWindowTitle("你好")
        # self.setWindowIcon(QIcon(Window_icon))
        #获取字体大小修改控件和窗口透明度修改控件
        self.font_size_edit=self.findChild(QSpinBox,"fontSizeEdit")
        self.opacity_edit=self.findChild(QDoubleSpinBox,"opacityEdit")
        #设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        #添加关闭按钮
        close_icon: str = r"../Asserts/icons/close.png"
        self.close_button.setIcon(QIcon(close_icon))
        self.close_button.clicked.connect(self.close)
        # 添加最小化按钮
        minimize_icon:str=r'../Asserts/icons/minimize.png'
        self.minimize_button.setIcon(QIcon(minimize_icon))
        self.minimize_button.clicked.connect(self.showMinimized)
        #设置user图标
        img_path2 = r'../Asserts/icons/book.png'
        pixmap2 = QPixmap(img_path2).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.user_photo_label.setPixmap( pixmap2 )
        #添加最大化按钮
        maxmize_icon:str=r'../Asserts/icons/maxmize.png'
        self.maxmize_button.setIcon(QIcon(maxmize_icon))
        self.maxmize_button.clicked.connect(self.showMaximized)
       # self.maxmize_button.clicked.connect(self.showMaximized)

        #绑定信号与槽
        self.LoginButton.clicked.connect(self.sayHi)
        self.EnrollButton.clicked.connect(self.sayHi)
        self.close_button.clicked.connect(self.sayHi)
        #按钮添加图标
        LoginButton_icon:str=r"../Asserts/icons/sign.png"
        EnrollButton_icon:str=r'../Asserts/icons/user.png'
        self.LoginButton.setIcon(QIcon(LoginButton_icon))
        self.EnrollButton.setIcon(QIcon(EnrollButton_icon))
        #添加左侧图片
        img_path= r'../Asserts/image/backgroundphoto.jpg'
        pixmap = QPixmap(img_path)
        self.label.setPixmap(pixmap)
    #背景图片设置
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("../BackgroundPhoto.jpg")
        # 缩放图片以填充窗口
        scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        painter.drawPixmap(0, 0, scaled_pixmap)
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

