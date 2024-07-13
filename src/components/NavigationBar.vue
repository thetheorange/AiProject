<template>
  <el-row type="flex" align="middle" justify="space-between">
    <el-col :md="20">
      <el-menu class="el-menu"
      mode="horizontal"
      default-active="1-1"
      active-text-color="#66b1ff"
      >
        
        <el-submenu index="1">
          <template slot="title">测试服务</template>
          <el-menu-item index="1-1"><router-link to="/SimpleTest" class="second-text">简单测试</router-link></el-menu-item>
          <el-menu-item index="1-2"><router-link to="/ModelConsole" class="second-text">控制台</router-link></el-menu-item>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">用户管理</template>
          <el-menu-item index="2-1"><router-link to="/NormalUserManager" class="second-text">普通用户</router-link></el-menu-item>
          <el-menu-item index="2-2"><router-link to="/AdminUserManager" class="second-text">管理员用户</router-link></el-menu-item>
        </el-submenu>
        <el-menu-item index="4">token兑换码</el-menu-item>
        <el-menu-item index="5"><router-link to="/AppInfo">应用信息</router-link></el-menu-item>
      </el-menu>
    </el-col>
    <el-col :md="4" class="theme-change">
      <i class="el-icon-sunrise-1"></i>
      <el-switch v-model="theme" active-color="#cdcdcd" inactive-color="#1b1b1b"></el-switch>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "NavigationBar",
  data() {
    return {
      theme: true,
    }
  },
}
</script>

<style scoped>
/* 路由跳转标签统一样式 */
a {
  text-decoration: none;
}
a:hover {
  color: #66b1ff;
}
/* 切换主题 */
.theme-change {
  display: flex;
  align-items: center;
  justify-content: center;
}
.theme-change i {
  margin-right: 10px;
}
</style>