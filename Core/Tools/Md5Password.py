"""
Des 未确定的数据加密
@Author MisakaW
Time 2024/6/29
"""
from hashlib import md5


class Md5Password:
    @staticmethod
    def encrypt(password: str) -> str:
        """
       MD5 加密密码
       :param password: 原始密码
       :return: 加密后的密码
       """
        return md5(password.encode()).hexdigest()

    @staticmethod
    def verify(password: str, encrypted_password: str) -> bool:
        """
        验证密码
        :param password: 输入的密码
        :param encrypted_password: 存储的加密密码
        :return: 密码是否匹配
        """
        return Md5Password.encrypt(password) == encrypted_password
