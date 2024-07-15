"""
Des 对话，聊天记录和面具的本地数据库
@Author MisakaW
Time 2024/6/29
Details:
Dialogue和Message
Change:
2024/7/15 大改，将LoginSql和ChatSql合并，将混乱的外键、关系，全改成简单的键，防止报错
结构如下：
一账户 -> 多对话（名字不可重复）-> 多消息（消息id不可重复）
一账户-> 多面具（不可重复）
一对话 -> 0/1面具
1面具 ->多对话
功能如下：
    1. 账户
        增
        删
        改： 账号、密码、自动填充
        查： 根据账号查id
    2. 对话
        增：绑定账户id和消息id
        删
        改？
        查：根据账户id和对话名查对话id
    3. 面具
        增：绑定账户id
        删
        改？
        查： 根据面具id查面具名和描述，根据账户id和面具名查面具id
    4. 消息
        增：绑定对话id
        删
        改：改发送状态、发送内容
        查：按日期排序查询一个对话的多个信息
"""
from datetime import datetime
from enum import Enum as BaseEnum

from sqlalchemy import Column
from sqlalchemy import create_engine, DateTime, Integer, String, Boolean, Enum
from sqlalchemy.orm import declarative_base, sessionmaker

from Logging import app_logger
from Sqlite.Static import static

Base = declarative_base()


# =============================================表的定义=============================================

class SenderType(BaseEnum):
    """
    信息发送人枚举体
    """
    USER = 0
    GPT = 1


class SendType(BaseEnum):
    """
    信息发送类型枚举体
    """
    TEXT = 0
    IMAGE = 1
    AUDIO = 2


class Mask(Base):
    """
    面具
    """
    __tablename__ = 'mask'
    mask_id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    mask_name = Column(String(50))
    mask_describe = Column(String(500))
    account_id = Column(Integer)
    icon = Column(String(20))


class Dialogue(Base):
    """
    对话
    """
    __tablename__ = 'dialogue'
    dialogue_id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    dialogue_name = Column(String(50))
    mask_id = Column(Integer)
    account_id = Column(Integer)
    icon = Column(String(20))


class Message(Base):
    """
    聊天信息
    """
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(Enum(SenderType, name="sender_enum"))
    send_time = Column(DateTime)
    send_type = Column(Enum(SendType, name="send_type_enum"))
    send_info = Column(String(2000))
    send_succeed = Column(Boolean)
    dialogue_id = Column(Integer)


class LoginAccount(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    auto_fill = Column(Boolean)
    email = Column(String(50))
    academy = Column(String(50))


# =============================================数据库封装=============================================

class ChatSql:
    # =============================================基础设置start=============================================
    def __init__(self):
        """
        初始化数据库连接和会话
        """
        try:
            engine = create_engine('sqlite:///chat.db')
            Base.metadata.create_all(engine)
            self.DB_session = sessionmaker(bind=engine)
        except Exception as e:
            app_logger.info(str(e))

    # =============================================基础设置end=============================================

    # =============================================账户设置start=============================================
    def add_account(self, username: str, password: str = "", auto_fill: bool = False):
        """
        添加账号，没问题
        :param username: 用户名
        :param password: 密码
        :param auto_fill: 是否自动填充密码
        """
        try:
            with self.DB_session() as session:
                # 先查找
                existing_account = session.query(LoginAccount).filter_by(username=username).first()
                # 在本机登录过的
                if existing_account:
                    if auto_fill:
                        existing_account.password = password
                    else:
                        existing_account.password = ""
                    static.sql_account_id = existing_account.id
                    existing_account.auto_fill = auto_fill
                    session.commit()
                    return

                # 没在本机登录过的
                account = LoginAccount(username=username, password=password, auto_fill=auto_fill)
                session.add(account)
                session.commit()
                account = session.query(LoginAccount).filter_by(username=username).first()
                static.sql_account_id = account.id
                self.add_mask("默认对话")
                self.create_dialogue('你好，新用户', icon='CHAT')
                self.create_dialogue('这题怎么做', icon='CALENDAR')
                self.create_dialogue('以“星期天为题”写一篇作文', icon='BOOK_SHELF')
                session.commit()
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))

    def delete_account(self, username: str):
        """
        删除账号
        :param username: 用户名
        """
        try:
            with self.DB_session() as session:
                account = session.query(LoginAccount).filter_by(username=username).first()
                if account:
                    session.delete(account)
                    session.commit()
                else:
                    print(f"找不到用户：{username}")
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))

    def get_all_accounts(self) -> list:
        """
        获取所有账号密码信息，没问题
        :return: 包含账号密码信息的列表
        """
        try:
            result = []
            with self.DB_session() as session:
                accounts = session.query(LoginAccount).all()
                print(accounts)
                for account in accounts:
                    result.append({
                        'username': account.username,
                        'password': account.password,
                        'auto_fill': account.auto_fill
                    })
            print(result)
            return result
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))
            return []

    def change_username(self, old_username: str, new_username: str):
        """
        更改用户名
        :param old_username: 旧用户名
        :param new_username: 新用户名
        """
        try:
            with self.DB_session() as session:
                account = session.query(LoginAccount).filter_by(username=old_username).first()
                if account:
                    account.username = new_username
                    session.commit()
                else:
                    print(f"找不到用户：{old_username}")
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))

    def change_password(self, username: str, new_password: str):
        """
        更改密码
        :param username: 用户名
        :param new_password: 新密码
        """
        try:
            with self.DB_session() as session:
                account = session.query(LoginAccount).filter_by(username=username).first()
                if account:
                    account.password = new_password
                    session.commit()
                else:
                    print(f"找不到用户：{username}")
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))

    def change_auto_fill(self, username: str, new_auto_fill: bool):
        """
        更改自动填充设置
        :param username: 用户名
        :param new_auto_fill: 新的自动填充设置
        """
        try:
            with self.DB_session() as session:
                account = session.query(LoginAccount).filter_by(username=username).first()
                if account:
                    account.auto_fill = new_auto_fill
                    session.commit()
                else:
                    print(f"找不到用户：{username}")
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))

    def update_account_id(self, username: str):
        """
        根据用户名获取本地账户id
        :param username: 用户名
        """
        try:
            with self.DB_session() as session:
                account = session.query(LoginAccount).filter_by(username=username).first()
                if account:
                    static.sql_account_id = account.id
                else:
                    print(f"找不到用户：{username}")
                    static.sql_account_id = -1
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))

    # =============================================账户设置end=============================================
    # =============================================对话start=============================================
    def create_dialogue(self, name: str, mask_name: str = "默认对话", icon: str = "CHAT"):
        """
        创建对话
        绑定账户id和面具id
        :param name: 对话名称
        :param mask_name: 面具名称，可以没有，默认
        :param icon: fluent图标
        """
        try:
            with self.DB_session() as session:
                mask = session.query(Mask).filter_by(mask_name=mask_name).first()
                if mask_name == "" or not mask:
                    mask = session.query(Mask).filter_by(mask_name="默认对话").first()
                if session.query(Dialogue).filter_by(dialogue_name=name).first():  # 已经出现
                    print("对话重复")
                    return
                dialogue = Dialogue(dialogue_name=name, mask_id=mask.mask_id, account_id=static.sql_account_id,
                                    icon=icon)
                session.add(dialogue)
                session.flush()
                session.commit()
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))

    def get_dialogue_by_account_and_name(self, dialogue_name: str,
                                         account_id=-1) -> Dialogue | None:
        """
        根据账户 ID 和对话名称获取对话
        :param dialogue_name: 对话名称
        :param account_id: 账户 ID
        :return: 对话对象，如果未找到则返回 None
        """
        try:
            if account_id == -1:
                account_id = static.sql_account_id
            with self.DB_session() as session:
                return session.query(Dialogue).filter_by(account_id=account_id, dialogue_name=dialogue_name).first()
        except Exception as e:
            app_logger.info(str(e))
            return None

    def update_dialogue_by_account_and_name(self, dialogue_name: str, account_id: int) -> None:
        """
        根据账户 ID 和对话名称更新对话id
        :param dialogue_name: 对话名称
        :param account_id: 账户 ID
        """
        dialogue = self.get_dialogue_by_account_and_name(dialogue_name, account_id)
        if dialogue:
            static.sql_dialogue_id = dialogue.dialogue_id

    def get_dialogue(self, dialogue_name: str) -> list | None:
        """
        根据名称获取对话
        :param dialogue_name: 对话名称
        """
        try:
            with self.DB_session() as session:
                return session.query(Dialogue).filter_by(dialogue_name=dialogue_name).first()
        except Exception as e:
            app_logger.info(str(e))

    def get_dialogues(self, account_id=-1) -> list:
        """
        :param account_id: id
        :return: 列表
        """
        try:
            result = []
            if account_id == -1:
                account_id = static.sql_account_id
            with self.DB_session() as session:
                dialogues = session.query(Dialogue).filter_by(account_id=account_id).all()
                for dialogue in dialogues:
                    result.append({
                        'name': dialogue.dialogue_name,
                        'icon': dialogue.icon,
                        'id': dialogue.dialogue_id
                    })
            print("dialogue list", account_id, result)
            return result
        except Exception as e:
            app_logger.info(str(e))
            print(str(e))
            return []

    # =============================================对话end=============================================
    # =============================================消息start=============================================
    def add_message(self, sender: SenderType | int, send_type: SendType | int,
                    send_info: str, send_succeed: bool, send_time: DateTime = datetime.now()):
        """
        添加消息
        :param sender: 发送者类型
        :param send_time: 发送时间
        :param send_type: 发送类型
        :param send_info: 发送信息
        :param send_succeed: 发送是否成功
        """
        try:
            if static.sql_dialogue_id == -1 or static.sql_account_id == -1:
                print("未登录")
                return
            with self.DB_session() as session:
                dialogue = session.query(Dialogue).filter_by(dialogue_id=static.sql_dialogue_id).first()
                if not dialogue:
                    print(f"Dialogue with id {static.sql_dialogue_id} not found")
                message = Message(dialogue_id=static.sql_dialogue_id, sender=sender, send_time=send_time,
                                  send_type=send_type,
                                  send_info=send_info, send_succeed=send_succeed)
                session.add(message)
                session.commit()
        except Exception as e:
            app_logger.info(str(e))

    def update_message(self, message_id: int, new_send_info: str):
        """
        更新消息
        :param message_id: 消息ID
        :param new_send_info: 新的发送信息
        """
        try:
            with self.DB_session() as session:
                message = session.query(Message).get(message_id)
                if message:
                    message.send_info = new_send_info
                    session.commit()
                else:
                    print(f"Message with id {message_id} not found")
        except Exception as e:
            app_logger.info(str(e))

    def delete_message(self, message_id: int):
        """
        删除消息
        :param message_id: 消息ID
        """
        try:
            with self.DB_session() as session:
                message = session.query(Message).get(message_id)
                if message:
                    session.delete(message)
                    session.commit()
                else:
                    print(f"Message with id {message_id} not found")
        except Exception as e:
            app_logger.info(str(e))

    def get_messages(self) -> list:
        """
        根据对话id获取消息
        :return: 消息列表，如果未找到相关对话则返回空列表
        """
        try:
            with self.DB_session() as session:
                dialogue = session.query(Dialogue).filter_by(dialogue_id=static.sql_dialogue_id).first()
                if dialogue:
                    return dialogue.messages
                else:
                    return []
        except Exception as e:
            app_logger.info(str(e))

    # =============================================消息end=============================================
    def add_mask(self, mask_name: str, mask_describe: str = "", account_id=-1, icon: str = "CHAT"):
        """
        增加新的面具
        :param mask_name: 面具名称
        :param mask_describe: 面具描述
        """
        try:
            with self.DB_session() as session:
                new_mask = Mask(mask_name=mask_name, mask_describe=mask_describe, account_id=account_id, icon=icon)
                session.add(new_mask)
                session.commit()
        except Exception as e:
            app_logger.info(str(e))

    def get_mask(self, mask_name: str) -> Mask:
        """
        根据名称查找面具
        :param mask_name: 面具名称
        :return: 面具对象，如果未找到则返回 None
        """
        try:
            with self.DB_session() as session:
                return session.query(Mask).filter_by(mask_name=mask_name).first()
        except Exception as e:
            app_logger.info(str(e))

    def delete_mask(self, mask_name: str):
        """
        根据名称删除面具
        :param mask_name: 面具名称
        """
        try:
            with self.DB_session() as session:
                mask = self.get_mask(mask_name)
                if mask:
                    session.delete(mask)
                    session.commit()
                else:
                    print(f"Mask with name {mask_name} not found")
        except Exception as e:
            app_logger.info(str(e))

    # =============================================对话与面具end=============================================
    def __format__(self, format_spec: str) -> str:
        """
        格式化输出
        """
        try:
            with self.DB_session() as session:
                if format_spec == "dialogues":
                    dialogues = session.query(Dialogue).all()
                    return "\n".join(
                        [f"对话名: {dialogue.dialogue_name}, 面具id: {dialogue.mask_id}" for dialogue in dialogues])
                elif format_spec == "masks":
                    masks = session.query(Mask).all()
                    return "\n".join(
                        [f"面具id: {mask.mask_id}, 面具名: {mask.mask_name}, 面具描述: {mask.mask_describe}" for mask in
                         masks])
                elif "messages" in format_spec:  # e.g. "messages Dialogue1 5"
                    target_format = format_spec.split(' ')
                    if len(target_format) < 2:
                        return "Miss parameters"
                    update_num = int(target_format[-1]) if len(target_format) >= 2 else 5
                    dialogue_name = target_format[1]
                    dialogue = session.query(Dialogue).filter_by(dialogue_name=dialogue_name).first()
                    if dialogue:
                        messages = dialogue.messages
                        sorted_messages = sorted(messages, key=lambda x: x.id, reverse=True)
                        print_messages = sorted_messages[:update_num]
                        return "\n".join([
                            f"信息id: {message.id}, 发送者: {message.sender.name}, 发送时间: {message.send_time}, 发送类型: {message.send_type.name}, 发送内容: {message.send_info}, 发送是否成功: {message.send_succeed}"
                            for message in print_messages])
                    else:
                        return f"未找到 {dialogue_name} 这个对话"
                else:
                    app_logger.info("Unknown format specifier")
        except Exception as e:
            app_logger.info(str(e))
            return str(e)


if __name__ == '__main__':
    sql = ChatSql()
    sql.add_account("wly", "561")
    print(sql.get_all_accounts())
    exit(0)
    sql.add_mask("Mask1", mask_describe="test mask。测试测试")
    sql.create_dialogue("Dialogue1", "Mask1")
    for i in range(30):
        sql.add_message(SenderType.USER, SendType.TEXT, str(i), True)
    # dialogue = sql.get_dialogue("Dialogue1")
    # messages = sql.get_messages("Dialogue1")
    # print(format(sql, "dialogues"))
    # print(format(sql, "masks"))
    # print(format(sql, "messages Dialogue1 6"))
