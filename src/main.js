import Vue from 'vue'
import {
  Container, Header, Footer, Main, Aside,
  Button, Select, 
  Row, Col,
  Menu, MenuItem, MenuItemGroup, Submenu,
  Switch
} from 'element-ui'
import App from './App.vue'
import router from './router'
import VueRouter from 'vue-router'

Vue.config.productionTip = false

Vue.use(VueRouter)

// =============== 引入第三方控件 START ===============
// 布局相关控件
Vue.use(Container); Vue.use(Header); Vue.use(Footer); Vue.use(Main); Vue.use(Aside);
Vue.use(Row); Vue.use(Col);

// 表单元素控件
Vue.use(Button);
Vue.use(Select);

// 导航栏控件
Vue.use(Menu); Vue.use(MenuItem); Vue.use(MenuItemGroup); Vue.use(Submenu)

// 开关控件
Vue.use(Switch)
// =============== 引入第三方控件 END ===============

new Vue({
  render: h => h(App),
  router,
  beforeCreate(){
    Vue.prototype.$bus = this;
  }
}).$mount('#app')
