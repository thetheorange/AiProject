<template>
	<view class="uv-chat-input">
		<view class="plugin">
			<view>
				<uni-icons type="image" size="40"></uni-icons>
			</view>
			<view>
				<button @click="onSend" class="send">发送</button>
			</view>
		</view>
		<view class="input">
			<textarea 
			v-model="val"
			:fixed="true"
			:adjust-position="true"
			:show-confirm-bar="false"
			cursor-spacing="20"
			:auto-height="true" placeholder="输入内容"></textarea>
		</view>
		
	</view>
</template>

<script setup>
	import { ref } from 'vue'
	let val = ref('')
	const emits = defineEmits(['send'])
	const onSend = ()=>{
		let _v = val.value;
		val.value = ''
		emits('send',_v)
	}
	
</script>

<style scoped lang="scss">
	.send {
		background-color: #002fa7;
		font-size: 25rpx;
		line-height: 60rpx;
		color: #fff;
	}
	.uv-chat-input {
		// background-color: #fff;
		// padding: 20rpx;
		.input {
			background-color: #fff;
			border-radius: 14rpx;
			overflow: hidden;
			margin-top: 15rpx;
			padding: 40rpx;
			textarea {
				// padding: 20rpx;
				width: 100%;
				// background-color: #f4f5f7;
				max-height: 326rpx;
			}
		}
		.plugin {
			display: flex;
			align-items: flex-end;
			justify-content: space-between;
			padding: 0px 20rpx;
		}
	}
</style>