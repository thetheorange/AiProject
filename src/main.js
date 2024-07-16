import Vue from 'vue'
import {
  Container, Header, Footer, Main, Aside,
  Button, Select, 
  Row, Col,
  Menu, MenuItem, MenuItemGroup, Submenu,
  Switch,
  Table,
  TableColumn,
  Input,
  Tag,
  Form,
  FormItem,
  Empty,
  Slider,
  Option,
  Drawer,
  Divider,
  Pagination,
  Dialog
} from 'element-ui'

import App from './App.vue'
import router from './router'
import VueRouter from 'vue-router'
import store from './store'
import axios from 'axios'

// 引入axios
Vue.prototype.$axios = axios;

Vue.config.productionTip = false;

Vue.use(VueRouter);

// =============== 引入element-ui控件 START ===============
// 布局相关控件
Vue.use(Container); Vue.use(Header); Vue.use(Footer); Vue.use(Main); Vue.use(Aside);
Vue.use(Row); Vue.use(Col);

// 表单元素控件
Vue.use(Form);
Vue.use(FormItem);
Vue.use(Button);
Vue.use(Select);
Vue.use(Input);
Vue.use(Select);
Vue.use(Option);

// 表格相关控件
Vue.use(Table); Vue.use(TableColumn);

// 导航栏控件
Vue.use(Menu); Vue.use(MenuItem); Vue.use(MenuItemGroup); Vue.use(Submenu);

// 抽屉控件
Vue.use(Drawer);

// 开关控件
Vue.use(Switch);

// 标签tag
Vue.use(Tag);

// 空白占位
Vue.use(Empty);

// 分割线
Vue.use(Divider);

// 滑块
Vue.use(Slider);

// 分页
Vue.use(Pagination);

// 对话框
Vue.use(Dialog);
// =============== 引入element-ui控件 END ===============

// =============== 引入font awesome START ===============
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from '@fortawesome/vue-fontawesome'

library.add(fas, far, fab)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component('font-awesome-layers', FontAwesomeLayers)
Vue.component('font-awesome-layers-text', FontAwesomeLayersText)

// =============== 引入font awesome END ===============

new Vue({
  render: h => h(App),
  router,
  store,
  beforeCreate(){
    Vue.prototype.$bus = this;
  }
}).$mount('#app')
