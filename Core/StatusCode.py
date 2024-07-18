"""
Des api状态code类 描述各个接口的不同状态信息
@Author thetheOrange
Time 2024/5/22
"""


class StatusCode:

    # ================================ 一般错误状态码start ================================

    # 404错误
    AppNotFoundError: str = "APP_NOT_FOUND_ERROR"
    # 400错误
    AppQueryMethodError: str = "APP_QUERY_METHOD_ERROR"
    # 500错误
    AppInternalError: str = "APP_INTERNAL_ERROR"

    # ================================ 一般错误状态码end ================================

    # ================================ 鉴权相关状态start ================================

    # 注册错误
    RegisterError: str = "REGISTER_ERROR"
    # 用户名重复
    UserNameRepeat: str = "USER_NAME_REPEAT"
    # 登录错误
    LoginError: str = "LOGIN_ERROR"
    # 用户不存在
    UserNotFound: str = "USER_NOT_FOUND"
    # 权限不足
    PermissionNotAllow: str = "PERMISSION_NOT_ALLOW"

    # ================================ 鉴权相关状态end ================================

    # ================================ 文本大模型相关状态start ================================

    # 用户token不足
    TokenNotEnough: str = "TOKEN_NOT_ENOUGH"
    # 文本模型错误
    ModelError: str = "MODEL_ERROR"

    # ================================ 文本大模型相关状态end ================================

    # ================================ 语音大模型相关状态start ================================

    # 使用语音转文字模型时错误
    AudioToTextError: str = "AUDIO_TO_TEXT_ERROR"

    # ================================ 语音大模型相关状态end ================================

    # ================================ 图片识别文字大模型相关状态start ================================

    # 文件格式不合法
    FileFormatIllegal: str = "FILE_FORMAT_ILLEGAL"
    # 获取上传文件失败
    GetFileFail: str = "GET_FILE_FAIL"
    # 用户使用图片文字识别模型次数不足
    PicTimesNotEnough: str = "PIC_TIMES_NOT_ENOUGH"
    # 使用图片文字识别模型时错误
    PictureToTextError: str = "PICTURE_TO_TEXT_ERROR"

    # ================================ 图片识别文字大模型相关状态end ================================

    # ================================ 后台管理界面相关Api状态start ================================

    # 添加用户信息接口错误
    AddUserError: str = "ADD_USER_ERROR"
    # 修改用户信息接口错误
    ModifyUserError: str = "MODIFY_USER_ERROR"
    # 删除用户错误
    DeleteUserError: str = "DELETE_USER_ERROR"

    # 添加管理员用户接口错误
    AddAdminError: str = "ADD_ADMIN_ERROR"
    # 修改管理员用户信息接口错误
    ModifyAdminError: str = "MODIFY_ADMIN_ERROR"
    # 删除管理员错误
    DeleteAdminError: str = "DELETE_ADMIN_ERROR"

    # 添加令牌接口错误
    AddTokenError: str = "ADD_TOKEN_ERROR"
    # 令牌重名
    TokenRepeat: str = "TOKEN_REPEAT"
    # 找不到令牌
    TokenNotFound: str = "TOKEN_NOT_FOUND"
    # 修改令牌信息接口错误
    ModifyTokenError: str = "MODIFY_TOKEN_ERROR"
    # 删除令牌接口错误
    DeleteTokenError: str = "DELETE_TOKEN_ERROR"
    # 禁用/启用令牌接口错误
    ControlTokenError: str = "CONTROL_TOKEN_ERROR"
    # 兑换令牌失败
    UserGetTokenError: str = "USER_GET_TOKEN_ERROR"
    # 已兑换过令牌
    TokenAlreadyGet: str = "TOKEN_ALREADY_GET"
    # 令牌失效
    TokenNotAvailable: str = "TOKEN_NOT_AVAILABLE"

    # 没有目标查询表
    TableNotFound: str = "TABLE_NOT_FOUND"
    # 查询表时出现错误
    QueryTableError: str = "QUERY_TABLE_ERROR"
    # 查询表中数据出现错误
    QueryTableDataError: str = "QUERY_TABLE_DATA_ERROR"

    # ================================ 后台管理界面相关Api状态end ================================
