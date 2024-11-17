<template>
	<uni-nav-bar left-icon="left" right-icon="home" dark title="设置" />
	<view class="uni-wrap">
		<uni-section title="选择主题" type="line">
			<uni-combox :candidates="candidates" placeholder="请选择主题" v-model="selectedTheme"></uni-combox>
		</uni-section>
		<uni-section title="选择字体大小" subTitle="设置字体" type="line" padding>
					<uni-easyinput v-model="value" :styles="styles" :placeholderStyle="placeholderStyle" placeholder="请输入内容"@input="input"></uni-easyinput>
		</uni-section>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				selectedTheme: 'black', // 绑定选择的主题
				candidates: ['black', 'white'],
				styles: {
					color: '#2979FF',
					borderColor: '#2979FF'
				}
			}
		},
		onReady() {},
		methods: {
			input(e) {
				console.log('输入内容：', e);
			},
			iconClick(type) {
				uni.showToast({
					title: `点击了${type==='prefix'?'左侧':'右侧'}的图标`,
					icon: 'none'
				})
			}
		}
	}
</script>

<style lang="scss">
	$uni-success: #18bc37 !default;

	.uni-wrap {
		flex-direction: column;
		/* #ifdef H5 */
		height: calc(100vh - 44px);
		/* #endif */
		/* #ifndef H5 */
		height: 100vh;
		/* #endif */
		flex: 1;
	}

	.scroll {
		flex-direction: column;
		flex: 1;
	}

	.mb-10 {
		margin-bottom: 10px;
	}

	.decoration {
		width: 6px;
		height: 6px;
		margin-right: 4px;
		border-radius: 50%;
		background-color: $uni-success;
	}
</style>
