# 特殊字符串 加盐
import hashlib

CODE: str = "#_#"


def get_md5(pwd: str) -> str:
    """
    md5加密用户密码

    :pwd: 用户密码
    :return: 返回MD5加密后的用户密码
    """
    pwd += CODE
    md5 = hashlib.md5()
    md5.update(pwd.encode("utf-8"))
    return md5.hexdigest()
