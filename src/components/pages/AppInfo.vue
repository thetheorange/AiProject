<template>
  <div style="width: 100%">
    <!-- 实例信息 -->
    <el-row>
      <el-divider content-position="left">实例信息</el-divider>
      <div class="app-info card-float">
        <div>
          <H2>
            <i class="el-icon-s-flag"></i>
            APPID:&nbsp;
            <span class="highlight-text">{{ APPID }}</span>
          </H2>
        </div>
        <div>
          <H2>
            <i class="el-icon-s-goods"></i>
            APIKEY:&nbsp;
            <span class="highlight-text">{{ APIKEY }}</span>
          </H2>
        </div>
        <div>
          <H2>
            <i class="el-icon-cpu"></i>
            API_SECRET:&nbsp;
            <span class="highlight-text">{{ API_SECRET }}</span>
          </H2>
        </div>
      </div>
    </el-row>
    <div class="gap-vertical"></div>
    <!-- 个人信息 -->
    <el-row>
      <el-divider content-position="left">个人信息</el-divider>
      <div class="personal-info card-float">
        <div>
          <h2>
            <i class="el-icon-user-solid"></i>
            用户名:&nbsp;
            <span class="highlight-text">{{adminName}}</span>
          </h2>
        </div>
        <div>
          <h2>
            <i class="el-icon-s-management"></i>
            累计使用token量:&nbsp;
            <span class="highlight-text">{{historyTokens}}</span>
          </h2>
        </div>
        <div>
          <h2>
            <i class="el-icon-position"></i>
            累计请求次数:&nbsp;
            <span class="highlight-text">{{historyRequestTimes}}</span>
          </h2>
        </div>
      </div>
    </el-row>
    <div class="gap-vertical"></div>
    <!-- 操作台 -->
    <div class="control-panner">
      <el-button type="primary">修改密码</el-button>
      <el-button type="primary">修改名称</el-button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState("APPInfo", ["APPID", "APIKEY", "API_SECRET"]),
    ...mapState("AdminInfo", ["adminName", "historyTokens", "historyRequestTimes"])
  },
  created() {
    this.$store.dispatch("APPInfo/app_id");
    this.$store.dispatch("APPInfo/api_key");
    this.$store.dispatch("APPInfo/api_secret");
  }
}
</script>

<style scoped>
/* 实例信息 */
.app-info {
  width: 100%;
  padding: 1em;
  background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  border-radius: 5px;
}

.app-info>div {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-info>div:not(div:last-child) {
  margin-bottom: 1em;
}

/* 个人信息 */
.personal-info {
  width: 100%;
  padding: 1em;
  background-image: linear-gradient(120deg, #d4fc79 0%, #96e6a1 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  border-radius: 5px;
}
.personal-info>div {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.personal-info>div:not(div:last-child) {
  margin-bottom: 1em;
}
/* 操作台 */
.control-panner {
  display: flex;
  justify-content: start;
}
</style>