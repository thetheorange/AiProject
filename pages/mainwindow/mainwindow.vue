<template>
	<uni-nav-bar   title="用户主页" />
	<uni-swiper-dot :info="info" :current="current" field="content" :mode="mode">
		<swiper class="swiper-box" @change="change">
			<swiper-item v-for="(item ,index) in info" :key="index">
				<view class="swiper-item">
					<!-- {{item.content}} -->
					<image v-if="item.image" :src="item.image" mode="aspectFill" class="swiper-image"></image>
				</view>
			</swiper-item>
		</swiper>
	</uni-swiper-dot>
	<uni-section title="用户卡片" type="line">
		<uni-card title="orange" :isFull="true"  thumbnail="https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png">
			<!-- 显示 token 值 -->
			<text>token: {{ token }}</text>
			
		</uni-card>
	</uni-section>
	
</template>

<script>
	export default {
		data() {
			return {
				token:30,
				info: [{
						content: '内容 A',
						image:'../../static/girl.png'
					}, {
						content: '广告位招租',
						image:'../../static/cat.png'
					}, {
						content: '广告位招租',
						image:'../../static/girl.png'
					}],
					current: 0,
					mode: 'round',
				
			}
		},
		methods: {
			change(e) {
						this.current = e.detail.current;
					}
				
		}
	}
</script>

<style>

</style>
