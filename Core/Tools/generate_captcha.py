"""
Des 生成四位数的随机验证码图片
@Author thetheOrange
Time 2024/5/25
"""
import os.path
import random
import string
import time

from PIL import Image, ImageDraw, ImageFont


class Captcha:
    """
    生成四位数的随机验证码图片
    """

    def __init__(self, *, char_4: str, captcha_path: str):
        """
        :param char_4: 长度为4的字符串
        :param captcha_path: 生成出的验证码图片路径 为jpg格式
        :return:
        """
        self.char_4: str = char_4
        self.captcha_path: str = captcha_path

        # 图片的具体位置
        self.captcha_position: str = os.path.join(self.captcha_path, self.char_4 + ".jpg")

        # 生成验证码图片
        self.get_picture()

    def __format__(self, format_spec) -> str:
        match format_spec:
            case "path":
                return self.captcha_path
            case "content":
                return self.char_4
            case _:
                raise ValueError("Unknown format specifier")

    def __repr__(self) -> str:
        return self.captcha_position

    @staticmethod
    def get_random_color(low: int, high: int) -> tuple:
        """
        生成一个随机颜色。

        :param low: 颜色值的下限。
        :param high: 颜色值的上限。
        :return: 以RGB格式表示的颜色元组。
        """
        return random.randint(low, high), random.randint(low, high), random.randint(low, high)

    def get_picture(self) -> None:
        """
        生成一个带有随机字符、线条和曲线的验证码图片。

        :return:
        """
        width, height = 180, 60
        image = Image.new('RGB', (width, height), self.get_random_color(20, 100))
        draw = ImageDraw.Draw(image)

        # 以变化的字体大小和旋转角度绘制字符。
        for i in range(4):
            font = ImageFont.truetype('C:/Windows/fonts/stxinwei.ttf', random.randint(30, 40))
            rotate = random.randint(-30, 30)
            char_image = Image.new('RGBA', (40, 40), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_image)
            char_draw.text((0, 0), self.char_4[i], font=font, fill=self.get_random_color(100, 200))
            char_image = char_image.rotate(rotate, expand=1)
            image.paste(char_image, (40 * i + 10, 5), char_image)

        # 绘制随机线条和曲线以产生干扰。
        for i in range(random.randint(3, 5)):
            draw.line([random.randint(0, width), random.randint(0, height)], fill=self.get_random_color(50, 150),
                      width=3)
        for i in range(random.randint(2, 5)):
            points = [(random.randint(i * width // 5, (i + 1) * width // 5), random.randint(0, height)) for i in
                      range(5)]
            draw.line(points, fill=self.get_random_color(50, 150), width=3)

        image.save(self.captcha_position)


if __name__ == "__main__":
    c = Captcha(char_4="aaaa", captcha_path="./")
