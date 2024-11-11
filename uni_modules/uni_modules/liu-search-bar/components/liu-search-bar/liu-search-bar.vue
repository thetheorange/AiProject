<template>
	<view>
		<view class="search-header" v-if="mode == 1">
			<image :style="{width:iconSize,height:iconSize}" class="search-img" src="../../static/search.png"></image>
			<input class="search-input-default"
				:style="{height:height,fontSize:fontSize,color:color,backgroundColor:bgColor,border:'solid '+borderColor+' 1rpx',borderRadius:borderRadius}"
				:placeholder="placeholder" type="text" v-model.trim="searchText" @blur="blurInfo" @input="inputInfo"
				@confirm="confirmSearch" :placeholder-style="'font-size:'+fontSize+';color:'+placeholderColor" />
		</view>
		<view class="search-header" v-if="mode == 2">
			<image :style="{width:iconSize,height:iconSize}" class="search-img" src="../../static/search.png"></image>
			<input class="search-input"
				:style="{height:height,fontSize:fontSize,color:color,backgroundColor:bgColor,border:'solid '+borderColor+' 1rpx',borderRadius:borderRadius}"
				:placeholder="placeholder" type="text" v-model.trim="searchText" @blur="blurInfo" @input="inputInfo"
				@confirm="confirmSearch" :placeholder-style="'font-size:'+fontSize+';color:'+placeholderColor" />
			<view class="search-name" @click.stop="confirmSearch" :style="{fontSize:searchFontSize,color:searchColor}">
				搜索
			</view>
		</view>
		<view class="search-header" v-if="mode == 3">
			<image :style="{width:iconSize,height:iconSize}" class="search-img" src="../../static/search.png"></image>
			<input class="search-input-default"
				:style="{height:height,fontSize:fontSize,color:color,backgroundColor:bgColor,border:'solid '+borderColor+' 1rpx',borderRadius:borderRadius}"
				:placeholder="placeholder" type="text" v-model.trim="searchText" @blur="blurInfo" @input="inputInfo"
				@confirm="confirmSearch" :placeholder-style="'font-size:'+fontSize+';color:'+placeholderColor" />
			<view class="search-name-default" @click.stop="confirmSearch"
				:style="{fontSize:searchFontSize,color:searchColor}">搜索
			</view>
		</view>
	</view>
</template>
<script>
	export default {
		props: {
			//显示模式（1:无搜索按钮；2:搜索按钮外显；3:搜索按钮内显）
			mode: {
				type: Number,
				default: 1
			},
			//输入框placeholder
			placeholder: {
				type: String,
				default: '请输入',
			},
			//搜索框高度
			height: {
				type: String,
				default: '72rpx'
			},
			//搜索框圆角弧度
			borderRadius: {
				type: String,
				default: '36rpx'
			},
			//搜索图标大小
			iconSize: {
				type: String,
				default: '32rpx'
			},
			//搜索框背景色
			bgColor: {
				type: String,
				default: '#F2F3F5'
			},
			//搜索框边框颜色
			borderColor: {
				type: String,
				default: '#e4e4e5'
			},
			//搜索框字体大小
			fontSize: {
				type: String,
				default: '30rpx'
			},
			//搜索框字颜色
			color: {
				type: String,
				default: '#666666'
			},
			//placeholder字颜色
			placeholderColor: {
				type: String,
				default: '#999999'
			},
			//搜索按钮字大小
			searchFontSize: {
				type: String,
				default: '30rpx'
			},
			//搜索按钮字颜色
			searchColor: {
				type: String,
				default: '#666666'
			},
		},
		data() {
			return {
				searchText: '', //搜索内容
			}
		},
		methods: {
			//点击搜索或者确认
			confirmSearch() {
				this.$emit('confirm', this.searchText)
			},
			//blur事件
			blurInfo() {
				this.$emit('blur', this.searchText)
			},
			//input事件
			inputInfo() {
				this.$emit('input', this.searchText)
			}
		}
	}
</script>
<style scoped>
	.search-header {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		position: relative;
	}

	.search-img {
		position: absolute;
		left: 28rpx;
	}

	.search-input-default {
		padding: 0 32rpx 0 72rpx;
		width: calc(100% - 104rpx);
	}

	.search-input {
		padding: 0 32rpx 0 72rpx;
		width: calc(90% - 104rpx);
	}

	.search-name {
		width: 80rpx;
		text-align: right;
	}

	.search-name-default {
		position: absolute;
		right: 28rpx;
	}
</style>
