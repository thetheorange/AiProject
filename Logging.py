"""
Des 项目日志对象
@Author thetheOrange
Time 2024/5/5
"""

import logging


def create_logger() -> logging.Logger:
    """
    项目全局日志对象
    :return:
    """
    # 创建logger对象
    logger = logging.getLogger("applogger")
    # 定义logger等级
    logger.setLevel(logging.DEBUG)
    # 创建formatter
    formatter = logging.Formatter("%(asctime)s | %(levelname)s -> %(message)s")

    # 创建handler，用于存放logger的位置
    file_handler = logging.FileHandler("log.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 绑定logger对象
    logger.addHandler(file_handler)

    return logger


app_logger = create_logger()
