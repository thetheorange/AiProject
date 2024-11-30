
<template>
	<uni-nav-bar left-icon="left" right-icon="home" dark title="chat" />
	<list-view :scroll-y="true">
		<list-item v-for="(item,index) in list" :key="index" class="" type=1>
			<view v-if="item.user_id==2">
				<div class="avatar-left"><img :src="item.avatar " alt="" style="height: 80rpx; width: 80rpx;" /></div>
				<div><text class="chat">{{item.data}}</text></div>
			</view>
			<view v-if="item.user_id==1" class="">
				<div class="avatar-right"><img :src="item.avatar " alt="" style="height: 80rpx; width: 80rpx; " /></div>
				<div><text class="chat">{{item.data}}</text></div>
			</view>
		</list-item>
	</list-view>


	<view class="content">
		<uni-easyinput type="textarea" autoHeight v-model="value" placeholder="请输入内容" suffixIcon="paperplane"
			@iconClick="iconClick" />
	</view>
</template>

<script>
export default {
    data() {
        return {
            value: "", // 输入框的内容
            avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png", // 头像
            list: [{
                user_id: 2,
                avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
                username: "机器人",
                data: "你好，有什么可以帮助您的",
                type: "text",
                create_time: 1570783530
            }, {
                user_id: 1,
                avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
                username: "orange",
                data: "我是orange",
                type: "text",
                create_time: 1570783530
            }]
        }
    },
    methods: {
        // 发送按钮点击事件
        iconClick() {
            if (this.value.trim() !== '') {
                const createTime = Math.floor(Date.now() / 1000);

                // 用户输入的消息
                const newItem = {
                    user_id: 1,
                    avatar: this.avatar,
                    username: "orange",
                    data: this.value,
                    type: "text",
                    create_time: createTime
                };
                this.list.push(newItem);

                // 准备请求数据
                const requestData = {
                    uuid: "769c7d3159125dc49ad55213d524af7e",
                    username: "test4",
                    dialog: [
                        {
                            role: "user",
                            content: this.value
                        }
                    ]
                };

                const responseItem = {
                    user_id: 2,
                    avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png", // 更新为实际头像URL
                    username: "机器人",
                    data: "",
                    type: "text",
                    create_time: Math.floor(Date.now() / 1000)
                };
                this.list.push(responseItem);

                // 使用 uni.request 替代 fetch
				
				uni.request({
				    url: "http://47.121.115.252:8193/textModel/chat",
				    method: 'POST',
				    header: {
				        'Content-Type': 'application/json'
				    },
				    data: requestData,
				    success: (res) => {
				        try {
				            // 将响应数据视为字符串
				            const responseText = res.data;
				            let buffer = '';
				            let combinedResponse = '';
				
				            // 使用正则表达式非贪婪匹配每个 JSON 对象
				            const jsonObjects = responseText.match(/{.*?}(?=({.*?})|$)/g) || [];
				            jsonObjects.forEach(jsonString => {
				                try {
				                    const jsonObject = JSON.parse(jsonString);
				
				                    // 检查并确保 payload 和 choices 存在，并提取数据
				                    if (jsonObject.payload && jsonObject.payload.choices) {
				                        jsonObject.payload.choices.text.forEach(msg => {
											console.log(msg.content)
				                            responseItem.data += msg.content;
				                        });
				                    }
				                } catch (e) {
				                    console.error('JSON 解析错误:', e);
				                }
				            });
				
				            this.$forceUpdate(); // 手动触发更新
				        } catch (error) {
				            console.error('响应处理时出错:', error);
				        }
				    },
				    fail: (err) => {
				        console.log('请求失败:', err);
				    }
				});

                this.value = '';
            } else {
                console.log("请输入内容！");
            }
        },
        onClickCard(card) {
            console.log("点击了卡片", card);
        }
    }
}
</script>

<style>
	.content {
		margin-top: 700rpx;
		margin-bottom: 10rpx;
	}

	.chat {
		display: flex;
		flex-direction: column;
		padding-left: 20rpx;
		/* 左侧间距 */
		padding-right: 20rpx;
		/* 右侧间距 */
		border-radius: 20rpx;
		padding: 35rpx;
		box-sizing: border-box;
		background-color: powderblue;
	}

	.avatar-left {
		height: 80rpx;
		width: 80rpx;
		margin-left: 10rpx;
	}

	.avatar-right {
		height: 80rpx;
		width: 80rpx;
		margin-left: 650rpx;
	}
</style>
