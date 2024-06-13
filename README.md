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

.
├── Api
│   ├── auth
│   │   ├── Authentication.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── model
│       ├── __init__.py
│       └── ModelAPI.py
├── app.py
├── Core
│   ├── __init__.py
│   ├── Models
│   │   ├── __init__.py
│   │   ├── PictureToTextSocket.py
│   │   ├── TextSocket.py
│   │   └── VoiceToTextSocket.py
│   ├── StatusCode.py
│   └── Tools
│       ├── extension_base_params.py
│       ├── generate_url.py
│       └── __init__.py
├── Logging.py
├── Model
│   ├── __init__.py
│   └── model.py
├── config.py
├── README.md
└── requirements.txt


```

## 部署方式 :writing_hand:

### docker部署

1.将下列文本写入到requirements.txt文件中，同时放在代码主目录下

```text
blinker==1.8.2
certifi==2024.2.2
cffi==1.16.0
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
Flask==3.0.3
gevent==24.2.1
greenlet==3.0.3
idna==3.7
itsdangerous==2.2.0
Jinja2==3.1.4
jsonpath==0.82.2
MarkupSafe==2.1.5
mysql-connector-python==8.4.0
mysqlclient==2.2.4
pycparser==2.22
PyMySQL==1.1.0
requests==2.32.2
SQLAlchemy==2.0.30
typing_extensions==4.11.0
urllib3==2.2.1
websocket-client==1.8.0
Werkzeug==3.0.3
zope.event==5.0
zope.interface==6.4.post2
```

2.构建镜像，**请确保Dockerfile**在当前目录下，然后执行如下命令

```shell
docker build -t ai_project_flask:0.0.1 -f Dockerfile .
```

注意，请确保容器中的端口同DockerFile中暴露的端口一致，同时，**尤其检查Dockerfile中的`CMD`，查看其中的端口是否一致**

3.运行容器

可以使用`docker images`检查镜像是否成功构建。接着，执行如下命令，运行容器。

```shell
docker run -p 8080:8080 --name=ai_project_flask -d ai_project_flask:0.0.1
```

这里的`-p`为端口映射，参数左边宿主机端口，右边容器端口，容器端口**和用户构建镜像时设置的暴露端口一致**

4.运行数据库依赖

首先拉取mysql的镜像 版本latest即可

```shell
docker pull mysql
```

接着运行mysql容器

```shell
docker run -p 8081:3306 \
-e MYSQL_ROOT_PASSWORD=123456 \
--name=db \
--restart=always \
-d mysql:latest
```

5.配置数据库表

推荐使用`dbeaver`远程连接数据库，或者在交互模式中，创建数据库`User`，按照下面的`sql`语句在其中新建一个user表

```sql
CREATE TABLE user (
    Id VARCHAR(50) PRIMARY KEY NOT NULL ,
    UserName VARCHAR(50) NOT NULL ,
    PassWord VARCHAR(50) NOT NULL ,
    Tokens INTEGER ,
    Email VARCHAR(50) NOT NULL ,
    PicTimes INTEGER DEFAULT 0
);
```

## 接口说明 :mag_right:

### 用户鉴权相关

---

参数说明

| 参数名      | 类型          | 描述                |
|----------|-------------|-------------------|
| username | string      | 用户名               |
| password | string      | 用户密码              |
| email    | string      | 用户邮箱              |
| code     | int, string | 状态码               |
| msg      | string      | 描述状态的具体信息         |
| uuid     | string      | 用户唯一id标识          |
| tokens   | int         | 用户可用的token        |
| picTimes | int         | 用户可调用的图片识别文字模型的次数 |
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

登录成功会返回用户的所有信息(包括用户id和uuid等信息) **登录失败则不返回**

```json
{
  "code": 0,
  "msg": "xxx",
  "uuid": "xxx",
  "tokens": 0,
  "picTimes": 0
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

```text

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

```text

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