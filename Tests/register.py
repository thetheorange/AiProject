import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QSpinBox,QDoubleSpinBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
import random
import string

from PIL import Image, ImageDraw, ImageFont, ImageFilter
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

        #验证码窗口
        char_4=get_picture()
        Verificationcode_img_path = r'../Asserts/image/%s.jpg' % char_4
        pixmap = QPixmap(Verificationcode_img_path).scaled(70, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.veri_code.setPixmap(pixmap)
        self.veri_code.clicked.connect(self.change_code_button_clicked)
        self.veri_code.setBorderRadius(10,10,10,10)

        #信号与槽
        self.confirm_button.clicked.connect(self.sayHi)
        self.cancel_button.clicked.connect(self.sayHi)

    def change_code_button_clicked(self):
        char_4 = get_picture()  # 假设 get_picture 是在其他地方定义的函数
        Verificationcode_img_path = r'../Asserts/image/%s.jpg' % char_4
        pixmap = QPixmap(Verificationcode_img_path).scaled(70, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.veri_code.setPixmap(pixmap)


    def sayHi(self):  # click对应的槽函数
        print("hi")



def get_random_char() -> str:
    """
    生成一个由4个随机字符（包括ascii字母和数字）组成的字符串。

    :return: 4个随机字符组成的字符串。
    """
    chr_all = string.ascii_letters + string.digits
    return ''.join(random.sample(chr_all, 4))


def get_random_color(low, high) -> tuple:
    """
    生成一个随机颜色。

    :param low: 颜色值的下限。
    :param high: 颜色值的上限。
    :return: 以RGB格式表示的颜色元组。
    """
    return random.randint(low, high), random.randint(low, high), random.randint(low, high)


def get_picture() -> str:
    """
    生成一个带有随机字符、线条和曲线的验证码图片。

    :return:
    """
    width, height = 180, 60
    image = Image.new('RGB', (width, height), get_random_color(20, 100))
    draw = ImageDraw.Draw(image)
    char_4 = get_random_char()

    # 以变化的字体大小和旋转角度绘制字符。
    for i in range(4):
        font = ImageFont.truetype('C:/Windows/fonts/stxinwei.ttf', random.randint(30, 40))
        rotate = random.randint(-30, 30)
        char_image = Image.new('RGBA', (40, 40), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((0, 0), char_4[i], font=font, fill=get_random_color(100, 200))
        char_image = char_image.rotate(rotate, expand=1)
        image.paste(char_image, (40 * i + 10, 5), char_image)

    # 绘制随机线条和曲线以产生干扰。
    for i in range(random.randint(3, 5)):
        draw.line([random.randint(0, width), random.randint(0, height)], fill=get_random_color(50, 150), width=3)
    for i in range(random.randint(2, 5)):
        points = [(random.randint(i * width // 5, (i + 1) * width // 5), random.randint(0, height)) for i in range(5)]
        draw.line(points, fill=get_random_color(50, 150), width=3)

    image.save('../Asserts/image/%s.jpg' % char_4)
    return char_4


if __name__ == "__main__":
    #QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
   # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
   # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    LoginWindow = LoginWindow()
    LoginWindow.show()
    sys.exit(app.exec_())








