"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      searchValue: "",
      // 初始化搜索框的值
      value: "",
      //password: '',
      placeholderStyle: "color:#2979FF;font-size:14px",
      styles: {
        color: "#2979FF",
        borderColor: "#2979FF"
      },
      arr: [],
      // 用来保存筛选后的数据，初始化为空数组
      list: [
        {
          mask_id: 1,
          avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
          maskname: "英语老师",
          data: "你好，有什么可以帮助您的"
        },
        {
          mask_id: 2,
          avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
          maskname: "数学老师",
          data: "请发送数学问题"
        }
      ]
    };
  },
  onLoad() {
  },
  onReady() {
  },
  methods: {
    // 搜索函数
    search(res) {
      common_vendor.index.showToast({
        title: "搜索：" + res.value,
        icon: "none"
      });
      this.arr = this.list.filter(
        (item) => item.maskname.toLowerCase().includes(this.searchValue.toLowerCase())
        // 不区分大小写搜索
      );
    },
    // 清除事件
    clear(res) {
      common_vendor.index.showToast({
        title: "clear事件，清除值为：" + res.value,
        icon: "none"
      });
    },
    // 取消事件
    cancel(res) {
      common_vendor.index.showToast({
        title: "点击取消，输入值为：" + res.value,
        icon: "none"
      });
    },
    input(e) {
      console.log("输入内容：", e);
    },
    iconClick(type) {
      common_vendor.index.showToast({
        title: `点击了${type === "prefix" ? "左侧" : "右侧"}的图标`,
        icon: "none"
      });
      if (this.value.trim() === "") {
        common_vendor.index.showToast({
          title: "请输入面具名称",
          icon: "none"
        });
        return;
      }
      console.log("添加新面具");
      const newMask = {
        mask_id: this.list.length + 1,
        // 假设mask_id是自增的
        avatar: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png",
        maskname: this.value,
        data: "新添加的面具"
      };
      this.list.push(newMask);
      this.value = "";
      this.arr = [...this.list];
      common_vendor.index.showToast({
        title: "面具添加成功",
        icon: "success"
      });
    }
  },
  // 生命周期函数，确保初始数据正常显示
  created() {
    this.arr = [...this.list];
  }
};
if (!Array) {
  const _easycom_uni_nav_bar2 = common_vendor.resolveComponent("uni-nav-bar");
  const _component_uni_search_bar = common_vendor.resolveComponent("uni-search-bar");
  const _easycom_uni_easyinput2 = common_vendor.resolveComponent("uni-easyinput");
  const _easycom_uni_list_chat2 = common_vendor.resolveComponent("uni-list-chat");
  const _easycom_uni_list2 = common_vendor.resolveComponent("uni-list");
  (_easycom_uni_nav_bar2 + _component_uni_search_bar + _easycom_uni_easyinput2 + _easycom_uni_list_chat2 + _easycom_uni_list2)();
}
const _easycom_uni_nav_bar = () => "../../uni_modules/uni-nav-bar/components/uni-nav-bar/uni-nav-bar.js";
const _easycom_uni_easyinput = () => "../../uni_modules/uni-easyinput/components/uni-easyinput/uni-easyinput.js";
const _easycom_uni_list_chat = () => "../../uni_modules/uni-list/components/uni-list-chat/uni-list-chat.js";
const _easycom_uni_list = () => "../../uni_modules/uni-list/components/uni-list/uni-list.js";
if (!Math) {
  (_easycom_uni_nav_bar + _easycom_uni_easyinput + _easycom_uni_list_chat + _easycom_uni_list)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.p({
      ["left-icon"]: "left",
      ["right-icon"]: "home",
      dark: true,
      title: "mask"
    }),
    b: common_vendor.o($options.search),
    c: common_vendor.o($options.cancel),
    d: common_vendor.o(($event) => $data.searchValue = $event),
    e: common_vendor.p({
      radius: "5",
      placeholder: "请输入想要的面具",
      clearButton: "always",
      cancelButton: "always",
      modelValue: $data.searchValue
    }),
    f: common_vendor.o($options.iconClick),
    g: common_vendor.o(($event) => $data.value = $event),
    h: common_vendor.p({
      suffixIcon: "star",
      placeholder: "请添加想要的面具",
      modelValue: $data.value
    }),
    i: common_vendor.f($data.arr, (item, index, i0) => {
      return {
        a: common_vendor.o(($event) => _ctx.onClick(item), index),
        b: "77da02ee-4-" + i0 + "," + ("77da02ee-3-" + i0),
        c: common_vendor.p({
          clickable: "true",
          title: item.maskname,
          avatar: item.avatar,
          note: item.data
        }),
        d: index,
        e: "77da02ee-3-" + i0
      };
    }),
    j: common_vendor.p({
      border: true
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
