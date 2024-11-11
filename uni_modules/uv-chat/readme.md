# uv-chat 聊天消息组件

> **组件名：uv-chat**

## 安装

在市场导入**[聊天消息组件](https://ext.dcloud.net.cn/plugin?name=uv-chat)uni_modules**版本的即可，无需`import`

### 基本使用

```html
<template>
    <view>

        <scroll-view :scroll-y="true" :enable-flex="true" class="chat">
            <template v-for="(item,i) in 50" :key="i">
                <uv-chat 
                    @avatarClickDb="dbc" 
                    :me="i % 2 == 1" 
                >
                    <template v-slot:content="{ other, content }">
                        <uv-chat-text :text="content"></uv-chat-text>
                    </template>
                </uv-chat>
            </template>
        </scroll-view>
    </view>
</template>

<script setup>
    import { ref } from 'vue'

    const dbc = (e)=>{
        console.log('双击',e);
    }
</script>

<style scoped>
.chat {
    display: flex;
    flex-direction: column;
    padding:  35rpx;
    box-sizing: border-box;
    background-color: #f4f5f7;
}
</style>
```

### props

| 参数        | 说明                    | 类型      | 默认值    | 可选值 |
| --------- | --------------------- | ------- | ------ | --- |
| me        | 是否为自己发出的消息            | Boolean | false  | -   |
| avatar    | 头像                    | String  |        | -   |
| nick      | 昵称                    | String  | 小辣椒    | -   |
| nickColor | 昵称颜色                  | String  | #aaa   | -   |
| content   | 消息内容                  | String  | 这是一条消息 |     |
| other     | 其他参数，会在头像单击，头像双击事件中返回 | Object  | {}     |     |

## emits 事件

| 事件名           | 说明   | 参数        |
| ------------- | ---- | --------- |
| avatarClick   | 头像单击 | { other } |
| avatarClickDb | 头像双击 | { other } |

## slot 插槽

| 插槽名     | 说明                                              | 参数                 |
| ------- | ----------------------------------------------- | ------------------ |
| content | 消息内容承载的插槽;方便扩展不同的消息类型，目前自带文本消息类型的组件uv-chat-text | { other, content } |

## 内置消息类型组件 1. uv-chat-text

#### props 文本消息

| 参数   | 说明   | 类型     |
| ---- | ---- | ------ |
| text | 消息内容 | String |

## 内置消息类型组件 2. uv-chat-image

#### props 图片消息

| 参数      | 说明   | 类型     |
| ------- | ---- | ------ |
| content | 图片地址 | String |

其他消息类型 如：红包，视频，地图等消息可自行通过slot:content去实现；有封装好的可联系我添加进内置组件～

#### 如使用过程中有任何问题，或者您对uv-有一些好的建议，欢迎加入 qq群：632100308
