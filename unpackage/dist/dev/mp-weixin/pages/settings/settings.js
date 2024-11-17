"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      selectedTheme: "black",
      // 绑定选择的主题
      candidates: ["black", "white"],
      styles: {
        color: "#2979FF",
        borderColor: "#2979FF"
      }
    };
  },
  onReady() {
  },
  methods: {
    input(e) {
      console.log("输入内容：", e);
    },
    iconClick(type) {
      common_vendor.index.showToast({
        title: `点击了${type === "prefix" ? "左侧" : "右侧"}的图标`,
        icon: "none"
      });
    }
  }
};
if (!Array) {
  const _easycom_uni_nav_bar2 = common_vendor.resolveComponent("uni-nav-bar");
  const _easycom_uni_combox2 = common_vendor.resolveComponent("uni-combox");
  const _easycom_uni_section2 = common_vendor.resolveComponent("uni-section");
  const _easycom_uni_easyinput2 = common_vendor.resolveComponent("uni-easyinput");
  (_easycom_uni_nav_bar2 + _easycom_uni_combox2 + _easycom_uni_section2 + _easycom_uni_easyinput2)();
}
const _easycom_uni_nav_bar = () => "../../uni_modules/uni-nav-bar/components/uni-nav-bar/uni-nav-bar.js";
const _easycom_uni_combox = () => "../../uni_modules/uni-combox/components/uni-combox/uni-combox.js";
const _easycom_uni_section = () => "../../uni_modules/uni-section/components/uni-section/uni-section.js";
const _easycom_uni_easyinput = () => "../../uni_modules/uni-easyinput/components/uni-easyinput/uni-easyinput.js";
if (!Math) {
  (_easycom_uni_nav_bar + _easycom_uni_combox + _easycom_uni_section + _easycom_uni_easyinput)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.p({
      ["left-icon"]: "left",
      ["right-icon"]: "home",
      dark: true,
      title: "设置"
    }),
    b: common_vendor.o(($event) => $data.selectedTheme = $event),
    c: common_vendor.p({
      candidates: $data.candidates,
      placeholder: "请选择主题",
      modelValue: $data.selectedTheme
    }),
    d: common_vendor.p({
      title: "选择主题",
      type: "line"
    }),
    e: common_vendor.o($options.input),
    f: common_vendor.o(($event) => _ctx.value = $event),
    g: common_vendor.p({
      styles: $data.styles,
      placeholderStyle: _ctx.placeholderStyle,
      placeholder: "请输入内容",
      modelValue: _ctx.value
    }),
    h: common_vendor.p({
      title: "选择字体大小",
      subTitle: "设置字体",
      type: "line",
      padding: true
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
