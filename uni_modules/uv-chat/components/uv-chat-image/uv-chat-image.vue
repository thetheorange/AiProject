<template>
	<view @click="preview" class="uv-chat-image">
		<image :src="content" mode="widthFix"></image>
	</view>
</template>

<script setup>
	const props = defineProps({
		content: {
			type: String,
			default: () => ''
		}
	})
	const preview = ()=>{
			uni.previewImage({
				urls: [props.content]
			})
	}
</script>

<style scoped>
	.uv-chat-image {
		border-radius: 14rpx;
		overflow: hidden;
		font-size: 0px;
		max-height: 500rpx;
	}
	image {
		width: 60vw;
		
	}
</style>