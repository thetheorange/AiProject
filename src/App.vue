<template>
  <div id="app">
    <el-container>
      <el-header >
        <el-row type="flex" align="middle" justify="space-between">
          <el-col :span="20">
            <el-menu class="el-menu-demo" mode="horizontal">
              <el-menu-item index="1">服务通道测试</el-menu-item>
              <el-menu-item index="2">用户管理</el-menu-item>
              <el-menu-item index="3">黑名单管理</el-menu-item>
              <el-menu-item index="4">token兑换码</el-menu-item>
            </el-menu>
          </el-col>
          <el-col :span="4">
            <el-switch active-color="#13ce66" inactive-color="#ff4949"></el-switch>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
      <el-footer></el-footer>
    </el-container>
  </div>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
