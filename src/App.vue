<template>
  <div id="app">
    <el-container>
      <el-header>
        <NavigationBar/>
      </el-header>
      <el-main class="container">
          <transition name="el-zoom-in-top" mode="out-in">
            <router-view></router-view>
          </transition>
      </el-main>
      <el-footer>
        <FooterPart/>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue"
import FooterPart from "./components/FooterPart.vue"

export default {
  name: 'App',
  components: {
    NavigationBar,
    FooterPart
  }
}
</script>

<style>
/* 基础设置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}
@font-face {
  font-family: "Helvetica Neue";
  src: url("./assets/font/Helvetica-Neue-2.ttf") format('truetype');
}
body {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}
/* 容器设置 */
.el-container {
  height: 100vh;
}
.container {
  display: flex;
  justify-content: center;
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
</style>
