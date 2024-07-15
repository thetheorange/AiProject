"""
Des 登录信息：账号密码的本地数据库
@Author MisakaW
Time 2024/6/29
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from Core.Tools.Md5Password import Md5Password

Base = declarative_base()
md5password = Md5Password()


class LoginAccount(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(32))
    auto_fill = Column(Boolean)


class LoginSql:
    def __init__(self):
        engine = create_engine('sqlite:///login.db')
        Base.metadata.create_all(engine)
        DB_session = sessionmaker(bind=engine)
        self.session = DB_session()

    def add_account(self, username: str, password: str = "", auto_fill: bool = False):
        """
        添加账号
        :param username: 用户名
        :param password: 密码
        :param auto_fill: 是否自动填充密码
        """
        account = LoginAccount(username=username, password=md5password.encrypt(password), auto_fill=auto_fill)
        self.session.add(account)
        self.session.commit()

    def delete_account(self, username: str):
        """
        删除账号
        :param username: 用户名
        """
        account = self.session.query(LoginAccount).filter_by(username=username).first()
        if account:
            self.session.delete(account)
            self.session.commit()
        else:
            print(f"找不到用户：{username}")

    def get_all_accounts(self):
        """
        获取所有账号密码信息
        :return: 包含账号密码信息的列表
        """
        accounts = self.session.query(LoginAccount).all()
        result = []
        for account in accounts:
            result.append({
                'username': account.username,
                'password': account.password,
                'auto_fill': account.auto_fill
            })
        return result

if __name__ == '__main__':
    sql = LoginSql()
    sql.add_account("admin", "123456", True)
    print(sql.get_all_accounts())
