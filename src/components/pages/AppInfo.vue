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
            <span class="highlight-text">{{ adminName }}</span>
          </h2>
        </div>
        <div>
          <h2>
            <i class="el-icon-s-management"></i>
            累计使用token量:&nbsp;
            <span class="highlight-text">{{ historyTokens }}</span>
          </h2>
        </div>
        <div>
          <h2>
            <i class="el-icon-position"></i>
            累计请求次数:&nbsp;
            <span class="highlight-text">{{ historyRequestTimes }}</span>
          </h2>
        </div>
      </div>
    </el-row>
    <div class="gap-vertical"></div>
    <!-- 修改密码弹出框 -->
    <el-dialog title="修改密码" :visible.sync="dialogStatus.modifyPasswordDialog" width="30%" :append-to-body="true">
      <el-input v-model="newPassword" placeholder="请输入新的密码" show-password></el-input>
      <span slot="footer">
        <el-button @click="dialogStatus.modifyPasswordDialog = false" type="primary">取消</el-button>
        <el-button @click="modifyPassword" type="primary">提交</el-button>
      </span>
    </el-dialog>
    <!-- 修改用户名弹出框 -->
    <el-dialog title="修改密码" :visible.sync="dialogStatus.modifyNameDialog" width="30%" :append-to-body="true">
      <el-input v-model="newName" placeholder="请输入新的用户名"></el-input>
      <span slot="footer">
        <el-button @click="dialogStatus.modifyNameDialog = false" type="primary">取消</el-button>
        <el-button @click="modifyName" type="primary">提交</el-button>
      </span>
    </el-dialog>
    <!-- 操作台 -->
    <div class="control-panner">
      <el-button @click="dialogStatus.modifyPasswordDialog = true" type="primary">修改密码</el-button>
      <el-button @click="dialogStatus.modifyNameDialog = true" type="primary">修改名称</el-button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import { Notification } from 'element-ui';

export default {
  data() {
    return {
      newPassword: "",
      newName: "",
      dialogStatus: {
        modifyPasswordDialog: false,
        modifyNameDialog: false
      }
    }
  },
  computed: {
    ...mapState("APPInfo", ["APPID", "APIKEY", "API_SECRET"]),
    ...mapState("AdminInfo", ["adminName", "historyTokens", "historyRequestTimes"])
  },
  methods: {
    modifyPassword() {
      this.$axios({
        method: "POST",
        url: "http://127.0.0.1:5000/admin/modify_admin",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`
        },
        data: {
          target_admin: this.$store.state.AdminInfo.adminName,
          new_password: this.newPassword
        }
      }).then(res => {
        let data = res.data;
        if (!data.code) {
          Notification({
            title: "修改密码成功",
            message: data.msg,
            type: "success"
          });
          console.log(data);
        }else {
          Notification.error({
            title: "修改密码失败",
            message: data.msg
          })
        }
      })
    },
    modifyName() {
      this.$axios({
        method: "POST",
        url: "http://127.0.0.1:5000/admin/modify_admin",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`
        },
        data: {
          target_admin: this.$store.state.AdminInfo.adminName,
          new_name: this.newName
        }
      }).then(res => {
        let data = res.data;
        if (!data.code) {
          Notification({
            title: "修改用户名成功",
            message: data.msg,
            type: "success"
          })
          // 更新用户名
          this.$store.commit("AdminInfo/ADMIN_NAME", this.newName);
        }else {
          Notification.error({
            title: "修改用户名失败",
            message: data.msg
          })
        }
      })
    }
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