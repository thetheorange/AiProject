import time
import uuid


def create_uuid(user_name: str) -> str:
    """
    根据时间戳和用户名创建唯一的uuid

    :return: 返回唯一的uuid
    """
    time_stamp: float = time.time()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{time_stamp}{user_name}").hex)