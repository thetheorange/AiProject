<div align="center">
<h1>流星智慧云平台 后端flask部分</h1>
<p>
<img alt="Static Badge" src="https://img.shields.io/badge/language-python_3.11-blue">
<img alt="Static Badge" src="https://img.shields.io/badge/flask-3.0.3-orange">
<img alt="Static Badge" src="https://img.shields.io/badge/SQLAlchemy-2.0.30-green">
</p>
</div>

## 项目架构 :blue_book:

```text

.
├── Api 后端Api
│ ├── auth 鉴权相关接口
│ │ ├── Authentication.py
│ │ └── __init__.py
│ ├── back_stage 后台管理相关接口
│ │ ├── BackStageApi.py
│ │ └── __init__.py
│ ├── __init__.py
│ └── model 大模型相关接口
│     ├── __init__.py
│     └── ModelAPI.py
├── app.py 主程序入口
├── config.py 配置文件
├── Core 核心文件
│ ├── __init__.py
│ ├── Models 大模型Socket类
│ │ ├── __init__.py
│ │ ├── PictureToTextSocket.py
│ │ ├── TextSocket.py
│ │ └── VoiceToTextSocket.py
│ ├── StatusCode.py 错误状态码
│ └── Tools 辅助函数
│     ├── extension_base_params.py
│     ├── generate_url.py
│     ├── generate_uuid.py
│     ├── __init__.py
│     └── md5_password.py
├── DockerFile
├── Logging.py
├── Model 数据库orm映射表
│ ├── __init__.py
│ └── model.py
├── README.md
└── requirements.txt


```

## 接口说明 :mag_right:

### 公共返回值

| 参数名  | 类型            | 描述          |
|------|---------------|-------------|
| code | string/number | 状态码         |
| msg  | string        | 接口状态的具体描述信息 |

### 请求参数一览

| 参数名      | 类型           | 描述      |
|----------|--------------|---------|
| username | string       | 用户名     |
| password | string       | 用户密码    |
| email    | string       | 用户邮箱    |
| academy  | string       | 用户所属学院  |
| admin    | string       | 管理员名称   |
| dialog   | List[object] | 发送的消息对话 |

### 返回参数一览

| 参数名           | 类型     | 描述             |
|---------------|--------|----------------|
| uuid          | string | 用户id           |
| content       | string | 大模型回复消息        |
| tokens        | number | 用户剩余token数     |
| picTimes      | number | 用户剩余文字识别模型使用次数 |
| access_token  | string | 管理员jwt令牌       |
| refresh_token | string | 管理员刷新jwt令牌     |
| api_id        | string | 实例id           |
| api_key       | string | 实例秘钥           |
| api_secret    | string | 实例秘钥           |

### 鉴权相关接口

#### 用户注册接口 /auth/register

请求方式 POST

请求头

> Content-type: application/json

请求体 json

```json

{
  "username": "xxx",
  "password": "xxx",
  "email": "xxx",
  "academy": "xxx"
}

```

响应体 json

```json

{
  "code": 0, 
  "msg": "用户注册成功"
}

```

#### 用户登录接口 /auth/login

---

请求方式 POST

请求头

> Content-type: application/json

请求体 json

```json

{
  "username": "xxx",
  "password": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "xxx",
  "uuid": "xxx",
  "username": "xxx",
  "tokens": 0, # any number
  "picTimes": 0 # any number
}

```

#### 管理员登录接口 /admin/login

---

请求方式 POST

请求头

> Content-type: application/json

请求体 json

```json

{
  "admin": "xxx",
  "password": "xxx"
}

```

响应体 json

```json

{
  "access_token": "xxx",
  "refresh_token": "xxx",
  "app_info": {
    "app_id": "xxx",
    "api_key": "xxx",
    "api_secret": "xxx"
  },
  "code": 0,
  "msg": "管理员登录成功"
}

```

#### 刷新令牌接口 /admin/refresh

---

请求方式 GET

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

响应体 json

```json

{
  "access_token": "xxx",
  "code": 0,
  "msg": "刷新令牌成功"
}

```

### 大模型相关接口

#### 文本大模型非流式接口 /textModel/chat

---

请求方式 POST

请求头

> Content-Type: application/json,

请求体 json

```json

{
  "uuid": "xxx",
  "username": "xxx",
  "dialog": [
    {"role": "system", "content": "query text"},
    {"role": "user", "content": "query text"},
    {"role": "assistant", "content": "response text"}
  ]
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "文本大模型回复成功",
  "content": "xxx",
  "consume_token": 0 # any number
}

```

#### 文本大模型流式接口 /textModel/stream

---

请求方式 POST

请求头 

> Content-Type: application/json,

请求体 json

```json

{
    "uuid": 0,
    "username": "xxx",
    "dialog": [
      {"role": "system", "content": "query text"},
      {"role": "user", "content": "query text"},
      {"role": "assistant", "content": "response text"}
    ]
}

```

响应体 

> 参考 [讯飞大模型流式接口](https://www.xfyun.cn/doc/spark/Web.html#_1-接口说明)

#### 语言识别模型接口 /voiceModel/chat

---

请求方式 POST

请求体 二进制文件 格式为pcm

响应体 json

```json

{
    "code": 0,
    "msg": "请求成功",
    "content": "xxx"
}

```

#### 图片识别文字接口 /PictureToTextModel/chat

---

请求方式 POST

请求头 

> uuid: xxx,<br>
  username: xxx

响应体 json

```json

{
  "code": 0,
  "msg": "请求成功",
  "content": "xxx"
}

```

### 后台管理相关接口

#### 控制台测试接口 /admin/console_test

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体

```json

{
  "dialog": [
    {
      "role": "system",
      "content": "query text"
    },
    {
      "role": "user",
      "content": "query text"
    },
    {
      "role": "assistant",
      "content": "response text"
    }
  ],
  "limit": 100,
  "top_k": 2,
  "temperature": 1
}

```

响应体 json

```json

{
  "content": "xxx",
  "consume_token": 0,
  "code": 0,
  "msg": "文本模型回复成功"
}

```

#### 添加普通用户接口 /admin/add_normal_user

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "username": "xxx",
  "password": "xxx",
  "tokens": 0,
  "email": "xxx",
  "pictimes": 0,
  "academy": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "添加用户成功"
}

```

#### 修改用户信息接口 /admin/modify_normal_user

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "target_user": "xxx",
  "new_user_info": {
    "new_username": "xxx",
    "new_tokens": 1,
    "new_password": "xxx",
    "new_email": "xxx",
    "new_pictimes": 1,
    "new_academy": "xxx"
  }
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "修改用户信息成功"
}

```

#### 删除用户接口 /admin/delete_normal_user

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "target_username": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "xxx用户删除成功"
}

```

#### 添加管理员用户接口 /admin/add_admin

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "admin": "xxx",
  "password": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "添加管理员成功"
}

```

#### 修改管理员用户信息接口 /admin/modify_admin

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "target_admin": "xxx",
  "new_name": "xxx",
  "new_password": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "修改用户信息成功"
}

```

#### 修改管理员用户信息接口 /admin/modify_admin

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "target_admin": "xxx",
  "new_name": "xxx",
  "new_password": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "修改用户信息成功"
}

```

#### 删除管理员接口 /admin/delete_admin

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "target_admin": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "xxx 删除成功"
}

```

#### 添加令牌接口 /admin/add_token

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "token_name": "xxx",
  "token_limit": "xxx",
  "token_range": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "创建令牌成功"
}

```

#### 修改令牌消息接口 /admin/modify_token

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "target_token": "xxx",
  "new_token_limit": {
    "new_token_range": "xxx",
    "new_token_is_available": 1
  }
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "令牌修改成功"
}

```

#### 删除令牌接口 /admin/delete_token

---

请求方式 POST

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

请求体 json

```json

{
  "target_token": "xxx"
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "xxx 删除成功"
}

```

#### 禁用/启用令牌接口 /admin/control_token?is_available=1&token_name=xxx

---

请求方式 GET

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

响应体 json

```json

{
  "code": 0,
  "msg": "xxx 启用/禁用成功"
}

```

#### 根据指定范围查询表接口 /admin/query_table?table=xxx&query_range=1&start=0

---

请求方式 GET

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

响应体 json

```json

{
  "code": 0,
  "msg": "查询 xxx 条信息成功",
  "data": [] # List[object]
}

```

#### 根据指定范围查询表中数据的总数接口 /admin/query_table_count?table=xxx

---

请求方式 GET

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

响应体 json

```json

{
  "code": 0,
  "msg": "查询 xxx 条信息成功",
  "total_count": 0
}

```

#### 查询指定表中的指定数据接口 /admin/query_table_data?table=xxx&target_name=xxx

---

请求方式 GET

请求头

> Content-Type: application/json, <br>
  Authorization: Bearer your access_token

响应体 json

```json

{
  "code": 0,
  "msg": "查询 xxx 成功",
  "data": {...}
}

```

#### 删除令牌接口 /admin/delete_token

---

请求方式 POST

请求头

> Content-Type: application/json

请求体 json

```json

{
  "token_id": "xxx", # 令牌id
  "user_id": "xxx", # 用户id
  "user_academy": "xxx" # 用户所属学院
}

```

响应体 json

```json

{
  "code": 0,
  "msg": "兑换令牌成功"
}

```

