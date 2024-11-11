<template>
	<uni-nav-bar left-icon="left" right-icon="home" dark title="chat" />
	<list-view  :scroll-y="true">
		  <list-item v-for="(item,index) in list" :key="index" class="" type=1>
			   <view v-if="item.user_id==2">
				<div class="avatar-left"><img :src="item.avatar "alt="" style="height: 80rpx; width: 80rpx;" /></div>
			      <div><text class="chat">{{item.data}}</text></div>
			   </view>
			   <view v-if="item.user_id==1" class="">
				<div  class="avatar-right"><img :src="item.avatar "alt="" style="height: 80rpx; width: 80rpx; "/></div>  
			   	<div><text class="chat">{{item.data}}</text></div>
				</view>
		  </list-item>		  
	</list-view>
	

	<view class="content">
		<uni-easyinput 
			type="textarea" 
			autoHeight 
			v-model="value" 
			placeholder="请输入内容" 
			suffixIcon="paperplane" 
			@iconClick="iconClick"
		/>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				value: "", // 输入框的内容
				avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png", // 头像
				cards: [] ,// 存储卡片的数组
				list:[{
									user_id:2,
									avatar:"https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
									username:"机器人",
									data:"你好，有什么可以帮助您的",
									type:"text", 
									create_time:1570783530
								},{
									user_id:1,
									avatar:"https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
									username:"orange",
									data:"我是orange",
									type:"text", 
									create_time:1570783530
								}]
			}
		},
		methods: {
			// 发送按钮点击事件
			iconClick() {
				// 如果输入框有内容
				if (this.value.trim() !== '') {
					// 获取当前时间戳
					const createTime = Math.floor(Date.now() / 1000);
					
					// 新的聊天项
					const newItem = {
						user_id: 1,  // 假设是用户发送的消息（user_id 1）
						avatar: this.avatar,
						username: "orange",  // 用户名
						data: this.value,    // 用户输入的内容
						type: "text", 
						create_time: createTime
					};
					this.list.push(newItem);

					// 清空输入框
					this.value = '';

					// 控制台打印发送的内容
					console.log("发送内容:", this.value);
				} else {
					// 如果没有输入内容
					console.log("请输入内容！");
				}
			},

			// 卡片点击事件
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
		padding-left: 20rpx;  /* 左侧间距 */
		 padding-right: 20rpx;  /* 右侧间距 */
		 border-radius:20rpx;
	    padding:  35rpx;
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
