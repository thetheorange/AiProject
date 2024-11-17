"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      token: 30,
      info: [{
        content: "内容 A",
        image: "../../static/girl.png"
      }, {
        content: "广告位招租",
        image: "../../static/cat.png"
      }, {
        content: "广告位招租",
        image: "../../static/girl.png"
      }],
      current: 0,
      mode: "round"
    };
  },
  methods: {
    change(e) {
      this.current = e.detail.current;
    }
  }
};
if (!Array) {
  const _easycom_uni_nav_bar2 = common_vendor.resolveComponent("uni-nav-bar");
  const _easycom_uni_swiper_dot2 = common_vendor.resolveComponent("uni-swiper-dot");
  const _easycom_uni_card2 = common_vendor.resolveComponent("uni-card");
  const _easycom_uni_section2 = common_vendor.resolveComponent("uni-section");
  (_easycom_uni_nav_bar2 + _easycom_uni_swiper_dot2 + _easycom_uni_card2 + _easycom_uni_section2)();
}
const _easycom_uni_nav_bar = () => "../../uni_modules/uni-nav-bar/components/uni-nav-bar/uni-nav-bar.js";
const _easycom_uni_swiper_dot = () => "../../uni_modules/uni-swiper-dot/components/uni-swiper-dot/uni-swiper-dot.js";
const _easycom_uni_card = () => "../../uni_modules/uni-card/components/uni-card/uni-card.js";
const _easycom_uni_section = () => "../../uni_modules/uni-section/components/uni-section/uni-section.js";
if (!Math) {
  (_easycom_uni_nav_bar + _easycom_uni_swiper_dot + _easycom_uni_card + _easycom_uni_section)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.p({
      title: "用户主页"
    }),
    b: common_vendor.f($data.info, (item, index, i0) => {
      return common_vendor.e({
        a: item.image
      }, item.image ? {
        b: item.image
      } : {}, {
        c: index
      });
    }),
    c: common_vendor.o((...args) => $options.change && $options.change(...args)),
    d: common_vendor.p({
      info: $data.info,
      current: $data.current,
      field: "content",
      mode: $data.mode
    }),
    e: common_vendor.t($data.token),
    f: common_vendor.p({
      title: "orange",
      isFull: true,
      thumbnail: "https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png"
    }),
    g: common_vendor.p({
      title: "用户卡片",
      type: "line"
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
