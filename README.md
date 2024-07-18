<div align="center">   
<img  alt="logo" src="https://github.com/thetheorange/AiProject/blob/main/Assets/image/logo.jpg" />
</div>

<h1 align="center">AiProject</h1>

<h3 align="center">一键部署你的智慧系统应用</h3>
 <div align="center">   
    <img alt="Static Badge" src="https://img.shields.io/badge/language-python_3.11-blue" style="margin-right: 5px;">    
    <img alt="Static Badge" src="https://img.shields.io/badge/flask-3.0.3-orange" style="margin-right: 5px;">    
    <img alt="Static Badge" src="https://img.shields.io/badge/SQLAlchemy-2.0.30-green">    
	<img alt="Static Badge" src=https://img.shields.io/badge/Front%20End-PyQt_Fluent_Widgets-pink>
    <img alt="Static Badge" src=https://img.shields.io/badge/manage%20interface-vue2-purple>
</div>


![show_photo](https://github.com/thetheorange/AiProject/blob/main/Assets/image/show.jpg)

## 特别鸣谢

[![](https://github.com/joana123123/AiProject/blob/main/Assets/image/xunfei_logo.png?raw=true)](https://xinghuo.xfyun.cn/)


## 项目架构  :bookmark_tabs:
```text

├── Assets
│   ├── Qss
│      └──register.qss
│   ├── icons
│   ├── image
│   ├── Core/Tools
│       ├──AudioRecorder.py
│       ├──__init__.py
│       ├──config.py
│       ├──generate_captcha.py
│       └──readQss.py
│   ├── Templates
│       ├──chat_search.ui
│       ├──chat_session.ui
│       ├──login.ui
│       ├──register.ui
│       ├──setting.ui
│       └──user_info.ui
│   ├── Views
│       ├──BaseWindow.py
│       ├──ChatWindow.py
│       ├──GlobalSignal.py
│       ├──MainWindow.py
│       ├──MaskWindow.py
│       ├──MessageBubble.py
│       ├──RegisterWindow.py
│       ├──SettingWindow.py
│       └──UserInfoWindow.py
├── .gitignore
├── BackgroundPhoto.jpg
├── Logging.py
├── config.json
└── main.py

```
## 主要功能 :calling:
- 结合PyQt5和designer小工具，fluent控件设计的ui，界面清晰较为现代化
- 支持识别文字、图片和语音等多种信息
- 提供预制且可高度定制的角色模板，极大地简化了个性化对话的创建、分享与调试过程，让对话设计变得更加直观、高效且充满乐趣。
- 提供自定义的设置功能，设计个性化的智慧系统助手

## 开始使用 :arrow_forward:
- 准备好你的 OpenAIProject API Key;
- 下载并解压文件
- 添加新面具
- 选择直接开始对话或选择面具即可开始与Ai对话

## 开发计划 :calendar:
- [x] 设计主要的登录、注册页面和开启对话的主页面
- [x] 部署后端大模型接口，支持部署的大语言模型：讯飞星火
- [x] 部署本地数据库
- [ ] 前后端联调
- [ ] 后台管理界面



## 本地数据库 :computer:

<table>  
    <tr>    
        <th style="text-align: center;" colspan="1">表</th> 
        <th style="text-align: center;" colspan="2">dialogue</th>    
        <th style="text-align: center;" colspan="3">mask</th>    
        <th style="text-align: center;" colspan="6">message</th>    
        <th style="text-align: center;" colspan="2">user</th>     
    </tr>   
    <tr>    
        <td style="text-align: center;" colspan="1">表描述</td> 
        <td style="text-align: center;" colspan="2">对话</td>    
        <td style="text-align: center;" colspan="3">面具</td>    
        <td style="text-align: center;" colspan="6">信息</td>    
        <td style="text-align: center;" colspan="2">用户登录信息</td>     
    </tr>  
    <tr> 
        <td style="text-align: center;">字段</td >   
        <td  style="text-align: center;">dialogue_name</td>  
        <td  style="text-align: center;">mask_name</td>  
        <!-- 表头2下的3列 -->  
        <td  style="text-align: center;">mask_id</td>  
        <td  style="text-align: center;">mask_name</td>  
        <td  style="text-align: center;">mask_describe</td>  
        <!-- 表头3下的6列 -->  
        <td  style="text-align: center;">send_id</td>  
        <td  style="text-align: center;">sender</td>  
        <td  style="text-align: center;">send_time</td>  
        <td  style="text-align: center;">send_type</td>  
        <td  style="text-align: center;">send_info</td>  
        <td  style="text-align: center;">send_succeed</td>  
        <!-- 表头4下的2列 -->  
        <td style="text-align: center;">user_id</td>  
        <td style="text-align: center;">user_keyword</td>  
    </tr>   
    <tr> 
        <td>字段描述</td>   
        <td>对话名称</td>  
        <td>面具名称</td>  
        <!-- 表头2下的3列 -->  
        <td>面具编号</td>  
        <td>面具名称</td>  
        <td>面具描述</td>  
        <!-- 表头3下的6列 -->  
        <td>发送者编号</td>  
        <td>发送者</td>  
        <td>信息发送时间</td>  
        <td>信息发送类型</td>  
        <td>发送的信息</td>  
        <td>发生是否成功</td>  
        <!-- 表头4下的2列 -->  
        <td>账号</td>  
        <td>密码</td>  
    </tr>  
    <tr> 
        <td>字段类型</td>   
        <td>String(20)</td>  
        <td>String(20)</td>  
        <!-- 表头2下的3列 -->  
        <td>Integer</td>  
        <td>String(20)</td>  
        <td>String(500)</td>  
        <!-- 表头3下的6列 -->  
        <td> </td>  
        <td>Enum</td>  
        <td>DateTime</td>  
        <td>Enum</td>  
        <td>String(2000)</td>  
        <td>Boolean</td>  
        <!-- 表头4下的2列 -->  
        <td>String(50)</td>  
        <td>String(50)</td>  
    </tr>  
    <tr> 
        <td>说明</td>   
        <td>主键</td>  
        <td> </td>  
        <!-- 表头2下的3列 -->  
        <td>主键</td>  
        <td></td>  
        <td></td>  
        <!-- 表头3下的6列 -->  
        <td>主键 </td>  
        <td>USER/GPT</td>  
        <td></td>  
        <td>TEXT/IMAGE/AUDIO</td>  
        <td></td>  
        <td></td>  
        <!-- 表头4下的2列 -->  
        <td></td>  
        <td></td>  
    </tr>  
</table>


##  使用剪影 :sparkler: 
 <img alt="using_cut_photo" src="https://github.com/joana123123/AiProject/blob/main/Assets/image/using_cut_photo.jpg?raw=true">
<img alt="using_cut_photo" src="https://github.com/joana123123/AiProject/blob/main/Assets/image/using_cut_photo2.jpg?raw=true">

## Contributor :bow:
[@thetheorange](https://github.com/thetheorange)
[@Misaka-xxw](https://github.com/Misaka-xxw)
[@joana123123](https://github.com/joana123123)
