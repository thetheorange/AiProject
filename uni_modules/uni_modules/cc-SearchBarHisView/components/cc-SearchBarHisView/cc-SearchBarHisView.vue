<template>

	<view>
	
		<view style="display: flex; width: 100vw;">

			<uni-search-bar style="width: calc(100vw - 52px);" bgColor="#FFFFFF" :placeholder="searchPlaceHolder"
				ref="searchBar" :focus="true" radius="6" v-model="searchText" cancelButton="none" />
			<view style="width: 52px; line-height: 50px;" @click="goSearchClick()"> 搜索 </view>


		</view>

		<view style="display: flex; margin-top: -6px;" v-if="hisSeen">
			<view class="hotSearchTitV"> 历史记录 </view>
			<image @click="deleteHisClick()"
				style="margin-left: calc(100vw - 222px);width: 22px;height: 22px;margin-top: 6px;"
				src="./delete_icon.png"></image>
		</view>

		<view class="upView" v-if="hisSeen"
			style="overflow: hidden; flex: 1; flex-wrap: wrap;  width: calc(100vw - 20px);  margin-top:2px;">

			<!-- 自定义了一个data-id的属性,可以通过js获取到它的值!  hover-class 指定按下去的样式类-->
			<view class="cellView" v-for="(tagItem, index) in hisList" :key="index" @click="selHisClick(tagItem)">
				{{tagItem}}
			</view>

		</view>

	</view>

</template>

<script>
	import uniSearchBar from './uni-search-bar/uni-search-bar.vue';

	export default {
		components: {

			uniSearchBar
		},
		props: {

			searchPlaceHolder: {
				type: String,
				default: ""
			},
			keyStr: {
				type: String,
				default: ""
			}



		},
		data() {
			return {
				hisList: [],
				hisSeen: false,
				searchText: ''
			}
		},

		mounted() {

			let hisArrStr = uni.getStorageSync(this.keyStr);
			console.log('hisArrStr = ' + hisArrStr);

			this.hisSeen = (hisArrStr.length > 0);
			this.hisList = hisArrStr.split(',');
		},
		methods: {
			selHisClick(item) {

				this.$emit('hisClick', item)
			},
			deleteHisClick() {


				let myThis = this;
				uni.showModal({
					confirmText: '清空',
					cancelText: '忽略',
					content: '清空后将无法恢复',
					title: "确认清空所有历史记录",
					success: function(res) {
						if (res.confirm) {

							console.log('清理数据');
							uni.removeStorageSync(myThis.keyStr);
							myThis.hisSeen = false;
							myThis.hisList = [];

						} else if (res.cancel) {

							console.log('用户点击取消');
						}
					}
				});


			},
			goSearchClick(item) {

				console.log('搜索值 = ' + JSON.stringify(this.searchText));
				if (this.searchText == undefined || this.searchText == '') {

					return;
				}


				this.$emit('searchClick', this.searchText)


				//  存储历史记录
				let hisArrStr = uni.getStorageSync(this.keyStr);
				let hisArr = hisArrStr.split(',');

				let selIndex = hisArr.indexOf(this.searchText);
				if (selIndex < 0) {

					if ((hisArrStr).length > 0) {

						uni.setStorageSync(this.keyStr, this.searchText + ',' + hisArrStr);

					} else {

						uni.setStorageSync(this.keyStr, this.searchText);

					}

				} else {
					hisArr.splice(selIndex, 1);
					hisArrStr = hisArr.join(",");
					uni.setStorageSync(this.keyStr, this.searchText + ',' + hisArrStr);

				}

			},

		}
	}
</script>

<style scoped>
	.hotSearchTitV {
		margin-left: 14px;
		margin-top: 4px;
		width: 170px;
		height: 22px;
		font-size: 14px;
		font-family: PingFangSC-Medium, PingFang SC;
		font-weight: 500;
		color: #161616;
		line-height: 22px;
	}

	.upView {
		display: flex;
		flex-direction: row;
		height: auto;
		margin-left: 4px;
	}

	.cellView {

		height: 16px;
		line-height: 16px;
		text-align: center;

		padding: 6px 10px !important;
		margin-top: 10px;
		font-size: 12px;
		margin-left: 10px;
		border-radius: 2px;
		background-color: white;
	}
</style>