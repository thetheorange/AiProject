"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      value: "",
      // 输入框的内容
      avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
      // 头像
      cards: [],
      // 存储卡片的数组
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
    };
  },
  methods: {
    // 发送按钮点击事件
    iconClick() {
      if (this.value.trim() !== "") {
        const createTime = Math.floor(Date.now() / 1e3);
        const newItem = {
          user_id: 1,
          // 假设是用户发送的消息（user_id 1）
          avatar: this.avatar,
          username: "orange",
          // 用户名
          data: this.value,
          // 用户输入的内容
          type: "text",
          create_time: createTime
        };
        this.list.push(newItem);
        this.value = "";
        console.log("发送内容:", this.value);
      } else {
        console.log("请输入内容！");
      }
    },
    // 卡片点击事件
    onClickCard(card) {
      console.log("点击了卡片", card);
    }
  }
};
if (!Array) {
  const _easycom_uni_nav_bar2 = common_vendor.resolveComponent("uni-nav-bar");
  const _easycom_uni_easyinput2 = common_vendor.resolveComponent("uni-easyinput");
  (_easycom_uni_nav_bar2 + _easycom_uni_easyinput2)();
}
const _easycom_uni_nav_bar = () => "../../uni_modules/uni-nav-bar/components/uni-nav-bar/uni-nav-bar.js";
const _easycom_uni_easyinput = () => "../../uni_modules/uni-easyinput/components/uni-easyinput/uni-easyinput.js";
if (!Math) {
  (_easycom_uni_nav_bar + _easycom_uni_easyinput)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.p({
      ["left-icon"]: "left",
      ["right-icon"]: "home",
      dark: true,
      title: "chat"
    }),
    b: common_vendor.f($data.list, (item, index, i0) => {
      return common_vendor.e({
        a: item.user_id == 2
      }, item.user_id == 2 ? {
        b: item.avatar,
        c: common_vendor.t(item.data)
      } : {}, {
        d: item.user_id == 1
      }, item.user_id == 1 ? {
        e: item.avatar,
        f: common_vendor.t(item.data)
      } : {}, {
        g: index
      });
    }),
    c: common_vendor.o($options.iconClick),
    d: common_vendor.o(($event) => $data.value = $event),
    e: common_vendor.p({
      type: "textarea",
      autoHeight: true,
      placeholder: "请输入内容",
      suffixIcon: "paperplane",
      modelValue: $data.value
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
