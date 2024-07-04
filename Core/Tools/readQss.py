"""
Des 读取qss
@Author thetheOrange
Time 2024/6/3
"""


class ReadQss:

    def __init__(self, ):
        ...

    @staticmethod
    def read(qss_path: str) -> any:
        """
        读取qss

        :return: 字符串
        """

        with open(qss_path, "r") as qss:
            return qss.read()
