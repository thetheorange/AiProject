<div align="center">
<h1>代号：AiProject 后端flask部分</h1>
<p>
<img alt="Static Badge" src="https://img.shields.io/badge/language-python_3.11-blue">
<img alt="Static Badge" src="https://img.shields.io/badge/flask-3.0.3-orange">
<img alt="Static Badge" src="https://img.shields.io/badge/SQLAlchemy-2.0.30-green">
</p>
</div>

## 项目架构 :blue_book:

```text

d Api  # api接口

    d auth  # 用户鉴权接口
    d model  # 大模型调用接口
    
d Core  # 核心目录

    d Models  # 各大模型封装接口 (基于讯飞平台)
    d Tools  # 工具类

d Model  # 数据库orm映射类

d Temp  # 临时文件目录

    d Audio  # 用户上传的音频 .pcm
    d Picture  # 用户上传的图片 .jpg | .jpeg

- app.py  # 程序启动入口

- Logging.py  # 日志文件记录器

# 注解：`d` 目录， `-` 文件， `#` 注释
```

## 接口说明 :mag_right:

### 用户鉴权相关

---

参数说明

| 参数名      | 类型          | 描述        |
|----------|-------------|-----------|
| username | string      | 用户名       |
| password | string      | 用户密码      |
| email    | string      | 用户邮箱      |
| code     | int, string | 状态码       |
| msg      | string      | 描述状态的具体信息 |
| uuid     | string      | 用户唯一id标识  |

---

#### 注册接口

*请求地址* 

    http://host:port/auth/register

*请求方式* 
        
    POST

*请求头* 

    无要求

*请求体* 格式为json
```json
{
  "username": "xxx",
  "password": "xxx",
  "email": "xxx"
}
```

*响应体* 格式为json
```json
{
  "code": 0,
  "msg": "xxx"
}
```

---

#### 登录接口

*请求地址* 

    http://host:port/auth/login

*请求方式* 

    POST

*请求头*

    无要求

*请求体* 格式为json
```json
{
  "username": "xxx",
  "password": "xxx"
}
```

*响应体* 格式为json

登录成功会返回用户唯一的uuid **登录失败则不返回uuid**

```json
{
  "code": 0,
  "msg": "xxx",
  "uuid": "xxx"
}
```

---

### 大模型调用相关

---

参数说明

| 参数名           | 类型     | 描述                       |
|---------------|--------|--------------------------|
| dialog        | array  | 文本大模型的历史对话消息，严格按示例中的格式发送 |
| content       | string | 接口识别成功时返回处理消息            |
| consume_token | int    | 单次会话所消耗的token数           |

---

#### 文本模型接口 (非流式)

*请求地址*

    http://host:port/textModel/chat

*请求方式*

    POST

*请求头*

    无要求

*请求体* 格式为json

```json

{
  "uuid": "xxx",
  "username": "xxx",
  "dialog": [{"role": "system", "content": "query text"},
    {"role": "user", "content": "query text"},
    {"role": "assistant", "content": "response text"},
    ...]
}

```

*响应体* 格式为json

```json

{
    "code": 0,
    "consume_token": 43,
    "content": "您好，我是科大讯飞研发的认知智能大模型，我的名字叫讯飞星火认知大模型。我可以和人类进行自然交流，解答问题，高效完成各领域认知智能需求。"
}

```
    
---

#### 文本模型接口 (流式 推荐)

*请求地址*

    http://host:port/textModel/stream

*请求头*

    无要求

*请求体* 格式为json

    内容同非流式接口一致

*响应体* 格式为json

内容同讯飞星火文本大模型流式接口一致 具体可看 [星火文本大模型流式返回数据示例](https://www.xfyun.cn/doc/spark/Web.html#_1-4-%E6%8E%A5%E5%8F%A3%E5%93%8D%E5%BA%94)

```json

# 接口为流式返回，此示例为最后一次返回结果，开发者需要将接口多次返回的结果进行拼接展示
{
    "header":{
        "code":0,
        "message":"Success",
        "sid":"cht000cb087@dx18793cd421fb894542",
        "status":2
    },
    "payload":{
        "choices":{
            "status":2,
            "seq":0,
            "text":[
                {
                    "content":"我可以帮助你的吗？",
                    "role":"assistant",
                    "index":0
                }
            ]
        },
        "usage":{
            "text":{
                "question_tokens":4,
                "prompt_tokens":5,
                "completion_tokens":9,
                "total_tokens":14
            }
        }
    }
}

```

---

#### 语音识别模型接口

*请求地址*

    http://host:port/voiceModel/chat

*请求方式*

    POST

*请求头*

    无要求

*请求体* 

    二进制pcm文件

*响应体* 格式为json 

识别成功返回content **失败则不返回content**

```json

{
  "code": 0,
  "content": "xxx"
}

```
    

#### 图片识别文字接口

*请求地址*

    http://host:port/PictureToTextModel/chat

*请求方式*

    POST

*请求头* 必须包含以下参数 否则**无法获取到接口返回的内容**

```text

"uuid": "xxx"
"username": "xxx"

```

*请求体*

    二进制jpg或者jpeg文件

*响应体* 格式为json

识别成功返回content **失败则不返回content**

```json
{
  "code": 0,
  "content": "xxx"
}
```