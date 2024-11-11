### liu-search-bar适用于uni-app项目的搜索框组件
### 本组件目前兼容微信小程序、H5
### 本组件是简单好用的搜索框组件，支持多种展示形式，可自定义输入框placeholder、搜索框高度、搜索框圆角弧度、搜索图标大小、搜索框背景色、搜索框边框颜色、搜索框字体大小、搜索框字颜色、placeholder字颜色、搜索按钮字大小、搜索按钮字颜色
# --- 扫码预览、关注我们 ---

## 扫码关注公众号，查看更多插件信息，预览插件效果！ 

![](https://uni.ckapi.pro/uniapp/publicize.png)

### 使用方式
``` html
<view class="title">无搜索按钮(默认)</view>
<liu-search-bar :mode="1" @confirm="confirm" @blur="blur" @input="input"></liu-search-bar>
<view class="title">搜索按钮外显</view>
<liu-search-bar :mode="2" @confirm="confirm" @blur="blur" @input="input"></liu-search-bar>
<view class="title">搜索按钮内显</view>
<liu-search-bar :mode="3" @confirm="confirm" @blur="blur" @input="input"></liu-search-bar>
<view class="title">自定义搜索框圆角弧度</view>
<liu-search-bar :mode="1" @confirm="confirm" @blur="blur" @input="input" borderRadius="12rpx"></liu-search-bar>
<view class="title">自定义背景色、边框色、文字颜色、placeholder颜色、搜索图标颜色</view>
<liu-search-bar :mode="1" @confirm="confirm" @blur="blur" @input="input" bgColor="#E2F3FF"
	borderColor="#28A0F8" color="#28A0F8" placeholderColor="#28A0F8"></liu-search-bar>
<view class="title">自定义各类颜色</view>
<liu-search-bar :mode="2" @confirm="confirm" @blur="blur" @input="input" bgColor="#E2F3FF"
	borderColor="#28A0F8" color="#28A0F8" placeholderColor="#28A0F8"
	searchColor="#28A0F8"></liu-search-bar>
```
``` javascript
export default {
	data() {
		return {
			
		};
	},
	methods: {
		//点击搜索或者确定
		confirm(e) {
			console.log('confirm搜索内容：' + e)
		},
		//blur事件
		blur(e) {
			console.log('blur搜索内容：' + e)
		},
		//inut事件
		input(e) {
			console.log('input搜索内容：' + e)
		}
	}
}
```

### 属性说明
| 名称                         | 类型           | 默认值                  | 描述             |
| ----------------------------|--------------- | ---------------------- | ---------------|
| mode                        | Number         | 1                      | 显示模式（1:无搜索按钮；2:搜索按钮外显；3:搜索按钮内显）
| placeholder                 | String         | 请输入                  | 输入框placeholder
| height                      | String         | 72rpx                  | 搜索框高度
| borderRadius                | String         | 36rpx                  | 搜索框圆角弧度
| iconSize                    | String         | 32rpx                  | 搜索图标大小
| bgColor                     | String         | #F2F3F5                | 搜索框背景色
| borderColor                 | String         | #e4e4e5                | 搜索框边框颜色
| fontSize                    | String         | 30rpx                  | 搜索框字体大小
| color                       | String         | #666666                | 搜索框字颜色
| placeholderColor            | String         | #999999                | placeholder字颜色
| searchFontSize              | String         | 30rpx                  | 搜索按钮字大小
| searchColor                 | String         | #666666                | 搜索按钮字颜色
| @confirm                    | Function       |                        | 点击搜索或者确认回调事件
| @blur                       | Function       |                        | blur回调事件
| @input                      | Function       |                        | input回调事件
 

