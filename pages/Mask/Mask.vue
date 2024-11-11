<template>
  <uni-nav-bar left-icon="left" right-icon="home" dark title="mask" />
  
  <!-- 搜索栏 -->  
  <uni-search-bar radius="5" v-model="searchValue" placeholder="请输入想要的面具" 
    clearButton="always" cancelButton="always" @confirm="search" @cancel="cancel" />
 <!-- 添加面具 -->
 <uni-easyinput class="uni-mt-5" suffixIcon="star" v-model="value" placeholder="请添加想要的面具" @iconClick="iconClick">
 </uni-easyinput>
  <!-- 面具列表 -->
  <uni-list :border="true" v-for="(item, index) in arr" :key="index">
    <uni-list-chat 
	 clickable=true
      :title="item.maskname" 
      :avatar="item.avatar" 
      :note="item.data" 
      @click="onClick(item)"  
    />
  </uni-list>
  
</template>

<script>
export default {
  data() {
    return {
      searchValue: '',  // 初始化搜索框的值
	  value: '',
	  //password: '',
	  placeholderStyle: "color:#2979FF;font-size:14px",
	  styles: {
	  	color: '#2979FF',
	  	borderColor: '#2979FF'
	  },
      arr: [],  // 用来保存筛选后的数据，初始化为空数组
      list: [
        {
          mask_id: 1,
          avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
          maskname: "英语老师",
          data: "你好，有什么可以帮助您的",
        },
        {
          mask_id: 2,
          avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
          maskname: "数学老师",
          data: "请发送数学问题",
        }
      ]
    };
  },
  onLoad() {},
  onReady() {},
  methods: {
    // 搜索函数
    search(res) {
      uni.showToast({
        title: '搜索：' + res.value,
        icon: 'none'
      });
      // 根据搜索框的值筛选 list
      this.arr = this.list.filter(item =>
        item.maskname.toLowerCase().includes(this.searchValue.toLowerCase())  // 不区分大小写搜索
      );
    },
    // 清除事件
    clear(res) {
      uni.showToast({
        title: 'clear事件，清除值为：' + res.value,
        icon: 'none'
      });
    },
    // 取消事件
    cancel(res) {
      uni.showToast({
        title: '点击取消，输入值为：' + res.value,
        icon: 'none'
      });
    },
    input(e) {
    	console.log('输入内容：', e);
    },
    iconClick(type) {
    	uni.showToast({
    		title: `点击了${type==='prefix'?'左侧':'右侧'}的图标`,
    		icon: 'none'
    	})
		if (this.value.trim() === '') {
		  uni.showToast({
			title: '请输入面具名称',
			icon: 'none'
		  });
		  return;
		}
		console.log('添加新面具')
		// 创建一个新的面具对象
		const newMask = {
		  mask_id: this.list.length + 1, // 假设mask_id是自增的
		  avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
		  maskname: this.value,
		  data: "新添加的面具"
		};
		// 将新面具添加到list数组中
		this.list.push(newMask);
		// 清空输入框
		this.value = '';
		// 更新arr数组，以便新添加的面具能够显示
		this.arr = [...this.list];
		uni.showToast({
		  title: '面具添加成功',
		  icon: 'success'
		}); 
    }
  },
  // 生命周期函数，确保初始数据正常显示
  created() {
    // 默认显示所有数据
    this.arr = [...this.list];
  },
};
</script>


<style lang="scss">
	.uni-mt-5 {
		margin-top: 5px;
	}
</style>