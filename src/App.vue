<template>
  <div id="app">
    <el-container>
      <el-header>
        <NavigationBar />
      </el-header>
      <el-main class="container">
        <transition name="el-zoom-in-top" mode="out-in">
          <router-view></router-view>
        </transition>
      </el-main>
      <el-footer>
        <FooterPart />
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue"
import FooterPart from "./components/FooterPart.vue"

import { Notification } from 'element-ui';

export default {
  name: 'App',
  components: {
    NavigationBar,
    FooterPart
  },
  methods: {
    // 每隔10分钟刷新jwt令牌
    refreshJWT() {
      setInterval(() => {
        console.log("refresh...")
        this.$axios({
          method: "GET",
          url: "http://127.0.0.1:5000/admin/refresh",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("refresh_token")}`
          }
        }).then(res => {
          let data = res.data;
          if (!data.code) {
            // 存储新的jwt秘钥
            localStorage.setItem("access_token", data.access_token);
            Notification({
              title: "刷新登录状态成功",
              message: data.msg,
              type: "success"
            })
          }else {
            Notification.error({
              title: "刷新登录状态失败",
              message: data.msg
            })
          }
        }, error => {
          console.log(error);
          Notification.error({
              title: "刷新登录状态失败",
              message: "刷新登录状态失败"
            })
        })
      }, 10 * 60 * 1000)
    }
  },
  mounted() {
    this.refreshJWT();
  }
}
</script>

<style>
/* 基础设置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

@font-face {
  font-family: "Helvetica Neue";
  src: url("./assets/font/Helvetica-Neue-2.ttf") format('truetype');
}

body {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

/* 容器设置 */
.el-container {
  height: 100vh;
}

.container {
  display: flex;
  justify-content: center;
}

.table-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.el-menu a {
  text-decoration: none;
}

/* 次要信息文本 */
.second-text {
  color: #909399;
}

/* 强调文本 */
.highlight-text {
  font-weight: bold;
  font-size: large;
}

/* 卡片浮动特效 */
.card-float {
  transition: 0.2s ease all;
}

.card-float:hover {
  transform: translateY(-0.5em);
}

/* 间隔 */
.gap-horizontal {
  margin: 0 0.5em;
}

.gap-vertical {
  margin: 0.5em 0;
}

/* 基础表格设置 */
.table {
  width: 100%;
  overflow: auto;
}

/* 搜索框 */
.search {
  display: flex;
  justify-content: end;
  align-items: center;
}

.search i {
  margin-right: 10px;
}

/* 分页栏 */
</style>
